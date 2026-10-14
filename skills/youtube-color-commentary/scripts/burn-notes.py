#!/usr/bin/env python3
"""Burn attributed commentary notes into a video.

    burn-notes.py --video IN.mp4 --notes notes.json --out OUT.mp4 \
                  --author NAME --model LABEL [options]

notes.json:  {"notes": [{"kind": "gloss"|"aside", "at": 33, "text": "..."}]}
             "at" is seconds. "kind" selects the panel style.

Options:
  --vf FILTER     filter applied before overlay, e.g. "transpose=2" for a
                  sideways recording. Rotation is detected so panel placement
                  uses the OUTPUT geometry.
  --rate N        words per second used to size display windows (default 2.6)
  --samples N     frames sampled per note when measuring free space (default 6)
  --crf N         x264 quality for the re-encode (default 18)
  --date D        date printed in the attribution (default today)
  --dry-run       print the ffmpeg command and exit

The output is a full re-encode (libx264, AAC 192k). Placement costs --samples
ffmpeg invocations per note plus an integral image per width attempt, so a long
note list is minutes of work before encoding starts.

Exit status is nonzero if any note is dropped, if the output is missing, or if
its duration does not match the input.
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import atexit
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import notes as N  # noqa: E402

WIDTH_STEPS = (0.42, 0.34, 0.28, 0.23)


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


def dimensions(path, vf):
    """Output dimensions, MEASURED through the filter chain.

    ALWAYS measured, including when there is no filter. ffprobe reports the
    CODED size, but ffmpeg applies a rotation display matrix on decode, so a
    phone recording tagged rotation:90 decodes transposed. Trusting the coded
    size there put a panel at 100% coverage over the writing and reported it
    placed. Inferring a swap from the substring "transpose" is wrong too, for
    "transpose=2,transpose=2" (180 degrees, no swap), for "rotate=", and for
    any scale filter.
    """
    with tempfile.TemporaryDirectory() as tmp:
        frame = os.path.join(tmp, "probe.png")
        subprocess.run(["ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error",
                        "-y", "-i", path, "-frames:v", "1",
                        "-vf", vf or "null", frame],
                       capture_output=True, stdin=subprocess.DEVNULL, check=False)
        if not os.path.exists(frame):
            return 0, 0
        from PIL import Image
        with Image.open(frame) as im:
            return im.width, im.height


# A panel is published with the video and cannot be edited afterwards, so a
# private identifier burned into one is permanent. These two shapes name nothing
# a viewer can reach and leak the source tree's structure; prose asking for
# public citations did not hold, so they are refused here instead.
# Prose asking for short notes did not hold either -- the same failure the
# private-identifier check records -- so the ceiling is refused here. The
# target is ten or fifteen; this is the point past which nobody finishes.
MAX_UNITS = 35
TYPESET_CHECK = bool(shutil.which("latex") and shutil.which("dvipng"))

PRIVATE = [
    (re.compile(r"\b[\w./-]+\.(?:tex|bib|sty|aux|md|json|py)\b"), "a source filename"),
    (re.compile(r"\b(?:prop|thm|theorem|lem|lemma|cor|defn?|eqn?|sec|rem|ex|fig|tab|conj|claim)"
                r"[:_][A-Za-z0-9][\w-]*"), "an internal label"),
]


def validate(items, video_seconds):
    """Reject a malformed note list with a message, not a traceback."""
    problems = []
    for i, note in enumerate(items):
        where = f"note {i}"
        if not isinstance(note, dict):
            problems.append(f"{where}: not an object"); continue
        if note.get("kind") not in N.STYLES:
            problems.append(f"{where}: kind={note.get('kind')!r}, expected one of "
                            f"{sorted(N.STYLES)}")
        if "at" not in note:
            problems.append(f"{where}: missing 'at' (seconds)")
        else:
            try:
                at = float(note["at"])
                if at < 0:
                    problems.append(f"{where}: at={at} is negative")
                elif video_seconds and at >= video_seconds:
                    problems.append(f"{where}: at={at:.0f}s is past the end of the "
                                    f"video ({video_seconds:.0f}s)")
            except (TypeError, ValueError):
                problems.append(f"{where}: at={note['at']!r} is not a number")
        text = note.get("text")
        if not isinstance(text, str) or not text.strip():
            problems.append(f"{where}: missing or empty 'text'")
        elif not text.isascii():
            bad = sorted({c for c in text if not c.isascii()})
            problems.append(f"{where}: non-ASCII {bad} would render as tofu")
        if isinstance(text, str):
            units = N.reading_units(text)
            if units > MAX_UNITS:
                problems.append(f"{where}: {units} word-equivalents; a panel is read at a "
                                f"glance over moving video and holds about {MAX_UNITS}. "
                                f"Shorten it, or move the detail to the description.")
            if TYPESET_CHECK and "$" in text:
                try:
                    from mathrender import latex_body
                    latex_body(text, 600)
                except ValueError as e:
                    problems.append(f"{where}: LaTeX does not compile: {str(e)[:120]}")
                except Exception:
                    pass
            for rx, what in PRIVATE:
                hit = rx.search(text)
                if hit:
                    problems.append(f"{where}: {hit.group(0)!r} is {what}; a viewer "
                                    f"cannot look it up. Cite a published source or "
                                    f"state the result plainly.")
    return problems


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--video", required=True)
    ap.add_argument("--notes", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--author", required=True,
                    help="whose request these notes were added at")
    ap.add_argument("--model", required=True, help="what added them")
    ap.add_argument("--vf", default="", help='pre-overlay filter, e.g. "transpose=2"')
    ap.add_argument("--rate", type=float, default=N.WORDS_PER_SEC,
                    help="words per second for display windows")
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    ap.add_argument("--samples", type=int, default=6)
    ap.add_argument("--crf", default="18")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    for tool in ("ffmpeg", "ffprobe"):
        if shutil.which(tool) is None:
            sys.exit(f"{tool} is not on PATH; both are required")

    spec = json.load(open(args.notes, encoding="utf8"))
    items = spec["notes"] if isinstance(spec, dict) else spec
    seconds = duration(args.video)
    if not seconds:
        sys.exit(f"{args.video}: ffprobe could not read a duration. Refusing to "
                 f"continue: the past-the-end check and the truncation guard "
                 f"both depend on it.")
    problems = validate(items, seconds)
    if problems:
        for p in problems:
            print(f"INVALID: {p}", file=sys.stderr)
        sys.exit(f"{len(problems)} problem(s) in {args.notes}")

    width, height = dimensions(args.video, args.vf)
    if not width:
        sys.exit(f"{args.video}: could not measure output geometry"
                 + (f" through --vf {args.vf!r}; check the filter"
                    if args.vf else "; is it a readable video?"))

    tmpdir = tempfile.mkdtemp(prefix="burn-notes-")
    atexit.register(shutil.rmtree, tmpdir, True)
    placed, dropped = [], []
    for i, note in enumerate(items):
        start = float(note["at"])
        want = N.reading_seconds(note["text"], args.rate)
        end = min(start + want, seconds)
        if end - start < N.MIN_SECS:
            dropped.append((note, f"only {end - start:.1f}s remain before the end "
                                  f"of the video; {N.MIN_SECS:.0f}s is the minimum "
                                  f"readable window"))
            continue
        try:
            mask, used = N.ink_mask(args.video, start, end, width, height,
                                    samples=args.samples, vf_pre=args.vf)
        except N.MaskError as exc:
            dropped.append((note, f"could not read the picture: {exc}"))
            continue
        # Panels already on screen during this window are not free space.
        blocked = [(x, y, x + w, y + h) for (_p, x, y, w, h, t0, t1) in placed
                   if t0 < end and start < t1]
        image = position = None
        tried = []
        for frac in WIDTH_STEPS:
            candidate = N.panel(note["kind"], note["text"], args.author,
                                args.model, args.date, int(width * frac))
            tried.append(f"{candidate.width}x{candidate.height}")
            found = N.place(mask, candidate.width, candidate.height,
                            blocked=blocked)
            if found is not None:
                image, position = candidate, found
                break
        if position is None:
            # Ask which constraint actually bit, rather than assuming that
            # because overlapping panels exist they must be the cause. A board
            # that is simply full fails identically with and without them, and
            # blaming the panels sends the reader to re-time notes when the
            # real fix is a different timestamp or more samples.
            why = "no clear space in the picture"
            if blocked:
                # Retry the WHOLE ladder with the panels ignored. Retrying one
                # rung under-detects: WIDTH_STEPS[-1] is the narrowest fraction
                # but not the shortest panel (at 1920 rung 3 is 175px tall and
                # rung 4 is 200px), so a slot that only rung 3 fits was being
                # reported as "no clear space" when a panel was the real cause.
                for frac_ in WIDTH_STEPS:
                    probe_panel = N.panel(note["kind"], note["text"], args.author,
                                          args.model, args.date, int(width * frac_))
                    if N.place(mask, probe_panel.width, probe_panel.height) is not None:
                        why = ("the only clear space was under a panel already "
                               "on screen")
                        break
            dropped.append((note, f"{why} (sampled {used} frames; tried "
                                  f"{', '.join(tried)})"))
            continue
        path = os.path.join(tmpdir, f"note{i}.png")
        image.save(path)
        placed.append((path, position[0], position[1], image.width, image.height,
                       start, end))
        print(f"placed {note['kind']} at {start:.0f}-{end:.0f}s "
              f"({image.width}x{image.height} at {position[0]},{position[1]})")

    for note, why in dropped:
        print(f"DROPPED {note['kind']} at {note['at']}s: {why}")
    print(f"{len(placed)} placed, {len(dropped)} dropped")
    if not placed:
        sys.exit("nothing could be placed; not rendering")

    chain, prev = [], "0:v"
    if args.vf:
        chain.append(f"[0:v]{args.vf}[base]")
        prev = "base"
    for j, (_p, x, y, _w, _h, t0, t1) in enumerate(placed):
        label = f"v{j}"
        chain.append(f"[{prev}][{j + 1}:v]overlay=x={x}:y={y}"
                     f":enable='between(t,{t0:.2f},{t1:.2f})'[{label}]")
        prev = label
    graph = ";".join(chain) + f";[{prev}]null[outv]"

    # Render beside the target and rename only after the duration check, so a
    # failed run cannot destroy a good earlier render.
    staging = args.out + ".partial.mp4"
    cmd = ["ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error", "-y",
           "-i", args.video]
    for path, *_ in placed:
        cmd += ["-i", path]
    cmd += ["-filter_complex", graph, "-map", "[outv]", "-map", "0:a?",
            "-c:v", "libx264", "-crf", args.crf, "-preset", "medium",
            "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
            "-movflags", "+faststart", staging]
    if args.dry_run:
        print(" ".join(cmd))
        return 1 if dropped else 0

    # -nostdin is load-bearing: ffmpeg reads stdin as keypresses, and a `q`
    # arriving from an inherited file quits it gracefully, leaving a valid,
    # playable, SHORT file with exit status 0.
    result = subprocess.run(cmd, capture_output=True, text=True,
                            stdin=subprocess.DEVNULL)
    if result.returncode != 0 or not os.path.exists(staging):
        sys.exit(f"ffmpeg failed: {result.stderr.strip()[:200]}")
    src, dst = seconds, duration(staging)
    if src and abs(dst - src) > max(2.0, src * 0.01):
        os.remove(staging)
        sys.exit(f"TRUNCATED: {dst / 60:.1f} min vs source {src / 60:.1f} min; "
                 f"discarded, {args.out} left untouched")
    os.replace(staging, args.out)
    print(f"wrote {args.out} ({dst / 60:.1f} min)")
    print("Now extract a frame at the MIDPOINT of each note's window and look "
          "at it, e.g.")
    for _p, _x, _y, _w, _h, t0, t1 in placed:
        print(f"  ffmpeg -nostdin -y -ss {(t0 + t1) / 2:.1f} -i {args.out} "
              f"-frames:v 1 check-{t0:.0f}s.png")
    return 1 if dropped else 0


if __name__ == "__main__":
    sys.exit(main())
