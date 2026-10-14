#!/usr/bin/env python3
"""Tests for series detection and playlist fault finding.

Run: python3 tests/test_plan_cards.py
Standard library only.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                os.pardir, "scripts"))
import importlib.util  # noqa: E402

spec = importlib.util.spec_from_file_location(
    "plan_cards", os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               os.pardir, "scripts", "plan-cards.py"))
pc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pc)

FAILED = []


def check(name, ok, detail=""):
    print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f"  [{detail}]" if detail and not ok else ""))
    if not ok:
        FAILED.append(name)


def main():
    print("[1] episode numbers are read from titles")
    for title, want in (("Course - 3 - Balls", ("course", (3,))),
                        ("Course - 12.1 - Fibrations", ("course", (12, 1))),
                        ("Widgets part 04 - Posets", ("widgets", (4,))),
                        ("Gadgets pt. 2", ("gadgets", (2,)))):
        got = pc.series_key_no(title)
        check(f"{title!r}", got == want, f"got {got}")
    check("a title with no number yields None",
          pc.series_key_no("Picture Frame Puzzle") is None)
    check("a bare number with no series name is not a series",
          pc.series_key_no("- 7 -") is None)

    print("\n[2] distinct runs in one playlist are kept apart")
    a = pc.series_key_no("Asymptotic Roch for Divisors - part 1")
    b = pc.series_key_no("Hilbert Polynomials for Divisors - part 01")
    check("different series get different keys", a and b and a[0] != b[0],
          f"{a} vs {b}")

    titles = {"v1": "Course - 1 - A", "v2": "Course - 2 - B",
              "w1": "Other - 1 - X", "w2": "Other - 2 - Y"}
    # interleaved but each run internally ordered: NOT a fault
    items = [(0, "v1"), (1, "w1"), (2, "v2"), (3, "w2")]
    dupes, unordered = pc.anomalies(items, titles)
    check("interleaved but individually ordered runs are not flagged",
          not dupes and not unordered, f"{unordered}")

    # one run genuinely out of order: IS a fault
    items = [(0, "v2"), (1, "w1"), (2, "v1"), (3, "w2")]
    dupes, unordered = pc.anomalies(items, titles)
    check("an out-of-order run is flagged", "course" in unordered, f"{unordered}")
    check("the well-ordered run beside it is not", "other" not in unordered)

    print("\n[3] duplicate entries")
    items = [(0, "v1"), (1, "v2"), (2, "v1")]
    dupes, _ = pc.anomalies(items, titles)
    check("a repeated video is reported once", dupes == ["v1"], f"{dupes}")
    items = [(0, "v1"), (1, "v2")]
    dupes, _ = pc.anomalies(items, titles)
    check("no false duplicate on a clean playlist", dupes == [])

    print("\n[4] a single-member run is never 'out of order'")
    solo = {"s1": "Solo - 1 - only"}
    _d, unordered = pc.anomalies([(0, "s1")], solo)
    check("one member cannot be unordered", unordered == {})

    print("\n[5] end-screen targets follow the SERIES, not playlist order")
    items = [(0, "c1"), (1, "o1"), (2, "c2"), (3, "o2")]
    t2 = {"c1": "Course - 1 - A", "o1": "Other - 1 - X",
          "c2": "Course - 2 - B", "o2": "Other - 2 - Y"}
    check("part 1 points at part 2 of its own run",
          pc.next_in_series(items, 0, t2) == "c2")
    check("the other run is chained separately",
          pc.next_in_series(items, 1, t2) == "o2")
    check("the last of a run has no next", pc.next_in_series(items, 2, t2) is None)
    gap = [(0, "g1"), (1, "g5")]
    tg = {"g1": "Course - 1 - A", "g5": "Course - 5 - E"}
    check("a numbering gap still chains to the next member present",
          pc.next_in_series(gap, 0, tg) == "g5")
    check("an unnumbered video has no series successor",
          pc.next_in_series([(0, "u1")], 0, {"u1": "One-off talk"}) is None)

    print("\n[6] malformed membership rows are reported, not swallowed")
    import json as _json, tempfile as _tf, os as _os
    rows = [{"playlist_id": "P", "playlist_title": "T", "position": 0, "video_id": "a"},
            {"playlist_id": "P", "playlist_title": "T", "pos": 1, "video_id": "b"}]
    with _tf.TemporaryDirectory() as d:
        f = _os.path.join(d, "m.json")
        _json.dump(rows, open(f, "w"))
        pls, skipped = pc.load_rows(f)
    check("the bad row is counted", len(skipped) == 1, f"{skipped}")
    check("the good row survives", sum(len(v) for v in pls.values()) == 1)

    print("\n[7] dates and leading numbers")
    for t in ("Topology Seminar 2026-05-03: Hodge theory", "Live 2026-05-03",
              "Seminar - 2026 - Hodge theory"):
        check(f"a date is not a series: {t[:30]!r}", pc.series_key_no(t) is None)
    check("a leading number uses the text after it",
          pc.series_key_no("Part 1 - Introduction") == ("introduction", (1,)))
    check("a non-string title does not crash",
          pc.series_key_no(None) is None)

    print("\n[8] end-to-end: one row per video, marked fallbacks")
    import json as _j, subprocess as _sp, sys as _s, tempfile as _tf, os as _o
    script = _o.path.join(_o.path.dirname(_o.path.abspath(__file__)),
                          _o.pardir, "scripts", "plan-cards.py")
    mem = [{"playlist_id": "PL1", "playlist_title": "A course",
            "position": i, "video_id": v}
           for i, v in enumerate(["c1", "u1", "u1", "c2"])]
    mem += [{"playlist_id": "PZ", "playlist_title": "Z uploads",
             "position": i, "video_id": v} for i, v in enumerate(["c1", "s1"])]
    tt = {"c1": "Course - 1 - A", "c2": "Course - 2 - B",
          "u1": "One-off talk", "s1": "Seminar 2026-05-03: X"}
    with _tf.TemporaryDirectory() as d:
        mf, tf_, of = (_o.path.join(d, n) for n in ("m.json", "t.json", "o.md"))
        _j.dump(mem, open(mf, "w")); _j.dump(tt, open(tf_, "w"))
        proc = _sp.run([_s.executable, script, "--memberships", mf,
                        "--titles", tf_, "--out", of],
                       capture_output=True, text=True)
        doc = open(of).read() if _o.path.exists(of) else ""
    check("the script succeeds", proc.returncode == 0, proc.stderr[:120])
    table = doc[doc.find("## Set these end screens"):doc.find("## Videos whose")]
    rows = [l for l in table.split("\n") if l.startswith("| `")]
    check("one row per video, not one per playlist membership",
          sum(1 for r in rows if r.startswith("| `c1`")) == 1,
          f"{len(rows)} rows")
    check("a fallback target is marked (adjacent)", "(adjacent)" in table)
    c1row = next(r for r in rows if r.startswith("| `c1`"))
    check("a series-derived target is NOT marked adjacent",
          "(adjacent)" not in c1row, c1row)
    u1row = next(r for r in rows if r.startswith("| `u1`"))
    check("only the fallback row carries the mark", "(adjacent)" in u1row, u1row)
    check("no video points at itself",
          not any(r.split("`")[1] == r.split("`")[3] for r in rows if r.count("`") >= 4))
    check("conflicting playlists are reported", "Videos whose playlists disagree" in doc
          and "`c1`" in doc[doc.find("## Videos whose"):])

    print("\n[9] a memberships file of the wrong shape is refused")
    with _tf.TemporaryDirectory() as d:
        mf, tf_, of = (_o.path.join(d, n) for n in ("m.json", "t.json", "o.md"))
        _j.dump({"not": "a list"}, open(mf, "w")); _j.dump({}, open(tf_, "w"))
        proc = _sp.run([_s.executable, script, "--memberships", mf,
                        "--titles", tf_, "--out", of], capture_output=True, text=True)
    check("a JSON object instead of a list exits non-zero", proc.returncode != 0,
          f"exit={proc.returncode}")

    print(f"\n{'ALL PASS' if not FAILED else str(len(FAILED)) + ' FAILED'}")
    return 1 if FAILED else 0


if __name__ == "__main__":
    sys.exit(main())
