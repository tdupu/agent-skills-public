#!/usr/bin/env python3
"""List candidate takes under a recording folder, with durations.

    discover-takes.py --root DIR [--json]

Handles both layouts: flat capture files, and per-session folders holding a
video plus a separate mixed audio track. Lists only; choosing and ordering
takes is a human decision recorded in a manifest.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys

VIDEO = (".mov", ".mp4", ".mkv", ".webm", ".flv", ".m4v")
AUDIO = (".wav", ".aiff", ".flac", ".m4a")


def duration(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                        "format=duration", "-of", "default=nw=1:nk=1", path],
                       capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 0.0


def find(root):
    """(video, audio_or_None) pairs. A sibling audio file under the same
    session folder is offered as the better mix; it is not assumed."""
    takes = []
    for dirpath, _dirnames, filenames in os.walk(root):
        vids = sorted(f for f in filenames if f.lower().endswith(VIDEO))
        auds = sorted(os.path.join(dirpath, d, f)
                      for d in ([""] + [x for x in os.listdir(dirpath)
                                        if os.path.isdir(os.path.join(dirpath, x))])
                      for f in (os.listdir(os.path.join(dirpath, d))
                                if os.path.isdir(os.path.join(dirpath, d)) else [])
                      if f.lower().endswith(AUDIO))
        for v in vids:
            vp = os.path.join(dirpath, v)
            takes.append((vp, auds[0] if len(auds) == 1 else None))
    return sorted(takes)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", required=True)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if shutil.which("ffprobe") is None:
        sys.exit("ffprobe is not on PATH")
    if not os.path.isdir(a.root):
        sys.exit(f"{a.root}: not a directory")

    rows = []
    for video, audio in find(a.root):
        d = duration(video)
        rows.append({"video": video, "audio": audio, "seconds": round(d, 2)})
    if a.json:
        print(json.dumps({"takes": rows}, indent=1))
        return
    if not rows:
        print(f"no video files under {a.root}")
        return
    print(f"{len(rows)} candidate take(s) under {a.root}:\n")
    for r in rows:
        mins = r["seconds"] / 60
        print(f"  {mins:6.1f} min  {r['video']}")
        if r["audio"]:
            print(f"              + audio {r['audio']}")
    print("\nWatch these, then write a manifest. Short takes are often false "
          "starts and\nrepeated topics are often retakes, but neither is "
          "decidable from here.")


if __name__ == "__main__":
    main()
