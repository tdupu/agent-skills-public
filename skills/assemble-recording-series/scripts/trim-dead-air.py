#!/usr/bin/env python3
"""Remove dead air from a lecture recording, keeping pauses that carry picture.

    trim-dead-air.py --video IN.mp4 --out OUT.mp4 [--map OUT.map.json]

A silent stretch is only dead air if nothing is happening on screen either.
In a recording of someone writing, most silence is the pen moving, and cutting
it destroys the explanation: the board jumps and the audio no longer matches
what is being written. So a gap is cut only when it is BOTH quiet and visually
static.

Writes a timestamp map so annotations timed against the untrimmed video can be
moved onto the trimmed one. Without it every later cue silently drifts.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile


def duration(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=nw=1:nk=1", path], capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 0.0


def silences(video, noise, minlen):
    r = subprocess.run(["ffmpeg", "-nostdin", "-hide_banner", "-i", video,
                        "-af", f"silencedetect=noise={noise}dB:d={minlen}",
                        "-f", "null", "-"],
                       capture_output=True, text=True, stdin=subprocess.DEVNULL)
    starts = [float(m) for m in re.findall(r"silence_start: ([\d.]+)", r.stderr)]
    ends = [float(m) for m in re.findall(r"silence_end: ([\d.]+)", r.stderr)]
    return [(s, e) for s, e in zip(starts, ends) if e - s >= minlen]


def still(video, t0, t1, threshold, tmp):
    """Is the picture essentially unchanged across [t0, t1]?"""
    from PIL import Image, ImageChops, ImageStat
    paths = []
    for i, t in enumerate((t0 + 0.3, t1 - 0.3)):
        p = os.path.join(tmp, f"s{i}.png")
        subprocess.run(["ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error",
                        "-y", "-ss", f"{t:.2f}", "-i", video, "-frames:v", "1",
                        "-vf", "scale=320:-2", p],
                       capture_output=True, stdin=subprocess.DEVNULL)
        if not os.path.exists(p):
            return False
        paths.append(p)
    diff = ImageChops.difference(Image.open(paths[0]).convert("L"),
                                 Image.open(paths[1]).convert("L"))
    return ImageStat.Stat(diff).mean[0] < threshold


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--video", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--map")
    ap.add_argument("--noise", type=float, default=-32.0, help="dB floor")
    ap.add_argument("--min-silence", type=float, required=True,
                    help="shortest gap to remove. A lecturer pauses ~1-2s between phrases, so values near that remove the delivery, not dead air; 4s+ removes only genuine stops. Screencasts tolerate lower. No default: choose for the recording.")
    ap.add_argument("--keep", type=float, default=0.35,
                    help="seconds of each cut gap to leave, so speech does not "
                         "butt together")
    ap.add_argument("--still-threshold", type=float, default=1.2,
                    help="mean frame difference under which the picture counts "
                         "as static")
    ap.add_argument("--crf", default="18")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    for tool in ("ffmpeg", "ffprobe"):
        if shutil.which(tool) is None:
            sys.exit(f"{tool} is not on PATH")
    total = duration(a.video)
    if not total:
        sys.exit(f"{a.video}: cannot read a duration")

    gaps = silences(a.video, a.noise, a.min_silence)
    tmp = tempfile.mkdtemp(prefix="deadair-")
    cuts, kept_writing = [], 0.0
    for s, e in gaps:
        if still(a.video, s, e, a.still_threshold, tmp):
            # leave `keep` seconds, split either side of the cut
            c0, c1 = s + a.keep / 2, e - a.keep / 2
            if c1 - c0 > 0.2:
                cuts.append((c0, c1))
        else:
            kept_writing += e - s
    removed = sum(c1 - c0 for c0, c1 in cuts)
    print(f"{len(gaps)} silent gaps >= {a.min_silence}s")
    print(f"  cutting {len(cuts)} that are also visually static: "
          f"{removed / 60:.1f} min")
    print(f"  keeping {kept_writing / 60:.1f} min of silence where the picture "
          f"is changing (writing)")
    print(f"  {total / 60:.1f} min -> {(total - removed) / 60:.1f} min")
    # Minutes removed is the flattering number: it grows as the damage grows.
    # Cuts per minute is the one that predicts how the result sounds, so it is
    # printed last, where a reader stops.
    if cuts:
        # Per minute of SOURCE, so the figure does not inflate as more is removed,
        # and so it matches what the documentation quotes.
        density = len(cuts) / (total / 60.0)
        print(f"  {density:.1f} cuts per minute of source")
    if a.dry_run:
        print("\nDRY RUN - nothing written.")
        return 0
    if not cuts:
        print("nothing to cut")
        return 0

    keep = []
    at = 0.0
    for c0, c1 in cuts:
        if c0 > at:
            keep.append((at, c0))
        at = c1
    if at < total:
        keep.append((at, total))

    # The concat demuxer with per-entry inpoint/outpoint, not a select
    # expression: a few hundred `between(t,..)` terms joined by + overruns
    # ffmpeg's expression parser, and a lecture easily has that many gaps.
    listfile = os.path.join(tmp, "keep.txt")
    src = os.path.abspath(a.video)
    with open(listfile, "w", encoding="utf8") as fh:
        for s_, e_ in keep:
            fh.write(f"file '{src}'\ninpoint {s_:.3f}\noutpoint {e_:.3f}\n")
    staging = a.out + ".partial.mp4"
    cmd = ["ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error", "-y",
           "-f", "concat", "-safe", "0", "-i", listfile,
           "-c:v", "libx264", "-preset", "medium", "-crf", a.crf,
           "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
           "-movflags", "+faststart", staging]
    r = subprocess.run(cmd, capture_output=True, text=True, stdin=subprocess.DEVNULL)
    if r.returncode != 0 or not os.path.exists(staging):
        sys.exit(f"ffmpeg failed: {r.stderr.strip()[:200]}")
    got = duration(staging)
    want = total - removed
    if abs(got - want) > max(3.0, want * 0.02):
        os.remove(staging)
        sys.exit(f"TRIMMED LENGTH WRONG: {got / 60:.1f} min vs expected "
                 f"{want / 60:.1f} min; discarded")
    os.replace(staging, a.out)

    if a.map:
        with open(a.map, "w", encoding="utf8") as fh:
            json.dump({"source": a.video, "output": a.out,
                       "kept_intervals": [[round(s, 3), round(e, 3)] for s, e in keep]},
                      fh, indent=1)
        print(f"wrote {a.map}")
    shutil.rmtree(tmp, ignore_errors=True)
    print(f"wrote {a.out} ({got / 60:.1f} min)")
    if cuts:
        density = len(cuts) / (total / 60.0)
        if density >= 1.0:
            print(f"  NOTE: {density:.1f} cuts per minute of source. On speech that is "
                  f"dense enough to be removing pauses rather than dead air. Listen to "
                  f"a few minutes before using this; raising --min-silence cuts fewer.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
