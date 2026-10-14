#!/usr/bin/env python3
"""Join the takes named in a manifest into one video.

    assemble.py --manifest manifest.json [--dry-run] [--crf 18]

Every take is normalised to one encode before joining, because concatenating
mismatched streams yields a file that plays wrongly from the join onwards
instead of failing. The result is checked against the sum of the trimmed
inputs: a short concatenation is the characteristic failure and it looks
healthy until someone watches the end.

Writes <output>.manifest.md with each take's start offset in the finished
file. Those offsets are what a commentary pass needs.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile


def probe(path, entries, stream=False):
    cmd = ["ffprobe", "-v", "error"]
    if stream:
        cmd += ["-select_streams", "v:0"]
    cmd += ["-show_entries", entries, "-of", "default=nw=1:nk=1", path]
    return subprocess.run(cmd, capture_output=True, text=True).stdout.strip()


def duration(path):
    try:
        return float(probe(path, "format=duration"))
    except ValueError:
        return 0.0


def validate(spec, base):
    problems, takes = [], spec.get("takes") or []
    if not spec.get("output"):
        problems.append("manifest has no 'output'")
    if not takes:
        problems.append("manifest lists no takes")
    for i, t in enumerate(takes):
        if not isinstance(t, dict) or "video" not in t:
            problems.append(f"takes[{i}]: needs a 'video'")
            continue
        for key in ("video", "audio"):
            p = t.get(key)
            if p and not os.path.exists(os.path.join(base, p)):
                problems.append(f"takes[{i}].{key}: no such file: {p}")
        s, e = t.get("start"), t.get("end")
        for name, v in (("start", s), ("end", e)):
            if v is not None and (not isinstance(v, (int, float)) or v < 0):
                problems.append(f"takes[{i}].{name}: {v!r} is not a non-negative number")
        if s is not None and e is not None and e <= s:
            problems.append(f"takes[{i}]: end {e} is not after start {s}")
    return problems


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--crf", default="18")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    for tool in ("ffmpeg", "ffprobe"):
        if shutil.which(tool) is None:
            sys.exit(f"{tool} is not on PATH")

    with open(a.manifest, encoding="utf8") as fh:
        spec = json.load(fh)
    base = os.path.dirname(os.path.abspath(a.manifest))
    problems = validate(spec, base)
    if problems:
        for p in problems:
            print(f"INVALID: {p}", file=sys.stderr)
        sys.exit(f"{len(problems)} problem(s) in {a.manifest}")

    takes = spec["takes"]
    out = os.path.join(base, spec["output"])
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)

    plan, expected = [], 0.0
    for i, t in enumerate(takes):
        v = os.path.join(base, t["video"])
        full = duration(v)
        start = float(t.get("start") or 0.0)
        end = float(t["end"]) if t.get("end") is not None else full
        if end > full + 0.5:
            sys.exit(f"takes[{i}]: end {end:.1f}s is past the take's "
                     f"{full:.1f}s length")
        plan.append((i, t, v, start, end))
        expected += end - start
    print(f"{len(plan)} take(s), expected total {expected / 60:.1f} min")
    for i, t, v, start, end in plan:
        print(f"  [{i}] {(end - start) / 60:5.1f} min  {t.get('label', '')}"
              f"  <- {os.path.basename(v)}"
              + (f" trimmed {start:.1f}-{end:.1f}" if t.get("start") or t.get("end") else "")
              + (f" + {os.path.basename(t['audio'])}" if t.get("audio") else ""))
    for x in spec.get("excluded") or []:
        print(f"  excluded: {x.get('video')} - {x.get('why', 'no reason given')}")
    if a.dry_run:
        print("\nDRY RUN - nothing written.")
        return 0

    tmp = tempfile.mkdtemp(prefix="assemble-")
    parts = []
    for i, t, v, start, end in plan:
        part = os.path.join(tmp, f"{i:03d}.mp4")
        cmd = ["ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error", "-y"]
        if start:
            cmd += ["-ss", f"{start:.3f}"]
        cmd += ["-i", v]
        amap = "0:a:0"
        if t.get("audio"):
            if start:
                cmd += ["-ss", f"{start:.3f}"]
            cmd += ["-i", os.path.join(base, t["audio"])]
            amap = "1:a:0"
        cmd += ["-t", f"{end - start:.3f}", "-map", "0:v:0", "-map", amap,
                "-c:v", "libx264", "-preset", "medium", "-crf", a.crf,
                "-pix_fmt", "yuv420p", "-r", "30",
                "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
                part]
        r = subprocess.run(cmd, capture_output=True, text=True,
                           stdin=subprocess.DEVNULL)
        if r.returncode != 0 or not os.path.exists(part):
            sys.exit(f"take {i} failed: {r.stderr.strip()[:200]}")
        print(f"  normalised [{i}] {duration(part) / 60:.1f} min")
        parts.append(part)

    listfile = os.path.join(tmp, "concat.txt")
    with open(listfile, "w", encoding="utf8") as fh:
        for p in parts:
            fh.write(f"file '{p}'\n")
    staging = out + ".partial.mp4"
    r = subprocess.run(["ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error",
                        "-y", "-f", "concat", "-safe", "0", "-i", listfile,
                        "-c", "copy", "-movflags", "+faststart", staging],
                       capture_output=True, text=True, stdin=subprocess.DEVNULL)
    if r.returncode != 0 or not os.path.exists(staging):
        sys.exit(f"concat failed: {r.stderr.strip()[:200]}")
    got = duration(staging)
    if abs(got - expected) > max(2.0, expected * 0.01):
        os.remove(staging)
        sys.exit(f"ASSEMBLED SHORT: {got / 60:.1f} min vs expected "
                 f"{expected / 60:.1f} min; discarded, {out} untouched")
    os.replace(staging, out)

    lines = [f"# {os.path.basename(out)}", "",
             f"{len(plan)} takes, {got / 60:.1f} min total.", "",
             "| start | length | take | source |", "|---|---|---|---|"]
    at = 0.0
    for (i, t, v, start, end), part in zip(plan, parts):
        d = duration(part)
        lines.append(f"| {int(at // 60)}:{int(at % 60):02d} | {d / 60:.1f} min | "
                     f"{t.get('label', '')} | `{t['video']}`"
                     + (f" {start:.0f}-{end:.0f}s" if t.get('start') or t.get('end') else "")
                     + " |")
        at += d
    if spec.get("excluded"):
        lines += ["", "## Excluded", ""]
        lines += [f"- `{x.get('video')}` - {x.get('why', 'no reason given')}"
                  for x in spec["excluded"]]
    with open(out + ".manifest.md", "w", encoding="utf8") as fh:
        fh.write("\n".join(lines) + "\n")
    shutil.rmtree(tmp, ignore_errors=True)
    print(f"\nwrote {out} ({got / 60:.1f} min) and {out}.manifest.md")
    print("Offsets above are what youtube-color-commentary needs.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
