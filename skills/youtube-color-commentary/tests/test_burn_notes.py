#!/usr/bin/env python3
"""Tests for the CLI: geometry, validation, drop reasons, timing.

Run: python3 tests/test_burn_notes.py
Needs ffmpeg and ffprobe; synthesises its own clips, so no fixtures.

These exist because two blocking defects lived in burn-notes.py while
tests/test_notes.py was green: every assertion there covers notes.py.
"""
from __future__ import annotations

import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, os.pardir, "scripts", "burn-notes.py")
_spec = importlib.util.spec_from_file_location("bn", SCRIPT)
sys.argv = ["burn-notes.py"]
bn = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(bn)
FAILED = []


def check(name, ok, detail=""):
    print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f"  [{detail}]" if detail and not ok else ""))
    if not ok:
        FAILED.append(name)


def make(path, seconds=30, size="640x480", extra=None, rotate=None):
    cmd = ["ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error", "-y"]
    if rotate:
        cmd += ["-display_rotation", str(rotate)]
    cmd += ["-f", "lavfi", "-i", f"color=c=0xC8C5C2:s={size}:d={seconds}:r=10"]
    if extra:
        cmd += ["-vf", extra]
    cmd += ["-c:v", "libx264", "-crf", "30", "-pix_fmt", "yuv420p", path]
    subprocess.run(cmd, capture_output=True, check=False)


def run(video, notes, tmp, *extra):
    nf = os.path.join(tmp, "n.json")
    with open(nf, "w", encoding="utf8") as fh:
        json.dump({"notes": notes}, fh)
    proc = subprocess.run(
        [sys.executable, SCRIPT, "--video", video, "--notes", nf,
         "--out", os.path.join(tmp, "o.mp4"), "--author", "A. Person",
         "--model", "Test Model", "--dry-run", *extra],
        capture_output=True, text=True)
    return proc.returncode, proc.stdout + proc.stderr


def main():
    if not (shutil.which("ffmpeg") and shutil.which("ffprobe")):
        print("ffmpeg/ffprobe not on PATH; skipping")
        return 0

    with tempfile.TemporaryDirectory() as tmp:
        plain = os.path.join(tmp, "plain.mp4")
        make(plain, extra="drawbox=x=0:y=0:w=60:h=480:color=0x482A1A@1:t=fill")

        print("[1] geometry is measured, never inferred from the filter text")
        check("no filter", bn.dimensions(plain, "") == (640, 480))
        check("a single transpose swaps", bn.dimensions(plain, "transpose=2") == (480, 640))
        check("a DOUBLE transpose does not swap",
              bn.dimensions(plain, "transpose=2,transpose=2") == (640, 480),
              str(bn.dimensions(plain, "transpose=2,transpose=2")))
        check("scale is honoured", bn.dimensions(plain, "scale=320:240") == (320, 240))
        check("a broken filter yields no geometry",
              bn.dimensions(plain, "nosuchfilter=1") == (0, 0))

        rot = os.path.join(tmp, "rot.mp4")
        make(rot, rotate=90, extra="drawbox=x=0:y=0:w=60:h=480:color=0x482A1A@1:t=fill")
        coded = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
             "stream=width,height", "-of", "csv=p=0", rot],
            capture_output=True, text=True).stdout.strip().strip(",")
        measured = bn.dimensions(rot, "")
        check("rotation metadata is respected, not the coded size",
              measured == (480, 640), f"coded={coded} measured={measured}")

        print("\n[2] malformed notes are named, never a traceback")
        code, out = run(plain, [{"kind": "nope", "at": 1, "text": "x"}], tmp)
        check("unknown kind is named", code != 0 and "expected one of" in out)
        check("no traceback", "Traceback" not in out)
        code, out = run(plain, [{"kind": "gloss", "at": 9999, "text": "x"}], tmp)
        check("past the end is rejected up front", "past the end" in out)
        code, out = run(plain, [{"kind": "gloss", "at": 1, "text": "sub ₊"}], tmp)
        check("non-ASCII is named", "non-ASCII" in out)

        print("\n[3] a window squeezed by the end of the video is dropped")
        code, out = run(plain, [{"kind": "gloss", "at": 28, "text": "late note"}], tmp)
        check("dropped, not shown briefly",
              "minimum readable window" in out and "0 placed" in out)

        print("\n[4] drop reasons distinguish their causes")
        code, out = run(plain, [{"kind": "gloss", "at": 2, "text": "x"}], tmp,
                        "--vf", "nosuchfilter=1")
        check("a broken filter is reported as geometry, not as 'no space'",
              "geometry" in out and "no clear space" not in out, out[-160:])

        print("\n[5] two notes with overlapping windows do not stack")
        code, out = run(plain, [{"kind": "gloss", "at": 2, "text": "first note"},
                                {"kind": "aside", "at": 4, "text": "second note"}], tmp)
        coords = [l.split(" at ")[-1] for l in out.split("\n") if l.startswith("placed")]
        check("both placed", out.count("placed ") >= 2, out)
        check("at different positions", len(set(coords)) == len(coords), str(coords))

        print("\n[6] private identifiers are refused before any encode")
        for text, why in [("This is Proposition prop:key in notes.tex.", "label and filename"),
                          ("Conclusion (Corollary cor:conj-false).", "label"),
                          ("See Remark rem:index-blind.", "label"),
                          ("Defined in notes.tex.", "filename")]:
            code, out = run(plain, [{"kind": "gloss", "at": 2, "text": text}], tmp)
            check(f"refused: {why}", code != 0 and "cannot look it up" in out, out[-160:])
        good = ("Zariski-Nagata purity, Stacks Tag 0BMB (Lemma 58.21.4); "
                "SGA 1, Expose X, Theorem 3.1, p. 276; arXiv:1711.07034.")
        code, out = run(plain, [{"kind": "gloss", "at": 2, "text": good}], tmp)
        check("public citations are not refused", "cannot look it up" not in out, out[-200:])

    print(f"\n{'ALL PASS' if not FAILED else str(len(FAILED)) + ' FAILED'}")
    return 1 if FAILED else 0


if __name__ == "__main__":
    sys.exit(main())
