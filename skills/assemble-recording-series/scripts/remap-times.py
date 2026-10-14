#!/usr/bin/env python3
"""Move annotation timestamps from an untrimmed video onto the trimmed one.

    remap-times.py --map OUT.map.json --notes notes.json --out notes-trimmed.json

Cutting dead air shifts everything after each cut. Re-timing by hand is the
obvious way to put every later note in the wrong place.
"""
from __future__ import annotations

import argparse
import json
import sys


def mapper(kept):
    """Original seconds -> trimmed seconds, or None if inside a cut."""
    def f(t):
        out = 0.0
        for s, e in kept:
            if t < s:
                return None          # t fell in a removed gap
            if t <= e:
                return out + (t - s)
            out += e - s
        return None
    return f


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--map", required=True)
    ap.add_argument("--notes", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    kept = json.load(open(a.map, encoding="utf8"))["kept_intervals"]
    f = mapper(kept)
    spec = json.load(open(a.notes, encoding="utf8"))
    notes = spec["notes"] if isinstance(spec, dict) else spec
    moved, lost = [], []
    for n in notes:
        t = f(float(n["at"]))
        if t is None:
            # the cue landed in removed silence; nudge to the next kept moment
            nxt = next((s for s, _e in kept if s > float(n["at"])), None)
            t = f(nxt + 0.05) if nxt is not None else None
        if t is None:
            lost.append(n)
            continue
        m = dict(n); m["at"] = round(t, 2); moved.append(m)
    out = dict(spec) if isinstance(spec, dict) else {}
    out["notes"] = sorted(moved, key=lambda n: n["at"])
    with open(a.out, "w", encoding="utf8") as fh:
        json.dump(out, fh, indent=1)
    print(f"remapped {len(moved)} note(s); {len(lost)} could not be placed")
    for n in lost:
        print(f"  LOST at {n['at']}s: {n['text'][:60]}", file=sys.stderr)
    return 1 if lost else 0


if __name__ == "__main__":
    sys.exit(main())
