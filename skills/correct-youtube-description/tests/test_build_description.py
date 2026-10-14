#!/usr/bin/env python3
"""Tests for description assembly.

Run: python3 tests/test_build_description.py
Standard library only. The last test feeds the output through the sibling
checker when it is present, so the two skills cannot drift apart silently.
"""
from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location(
    "build_description", os.path.join(HERE, os.pardir, "scripts",
                                      "build-description.py"))
bd = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bd)
FAILED = []


def check(name, ok, detail=""):
    print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f"  [{detail}]" if detail and not ok else ""))
    if not ok:
        FAILED.append(name)


def main():
    print("[1] a summary is mandatory")
    try:
        bd.build({})
        check("empty spec is refused", False)
    except ValueError:
        check("empty spec is refused", True)
    text, _ = bd.build({"summary": "A talk about widgets."})
    check("summary leads the description", text.startswith("A talk about widgets."))

    print("\n[2] unverified references are dropped, not printed")
    text, dropped = bd.build({
        "summary": "S.",
        "references": [{"cite": "Lemma 1.2", "verified": True},
                       {"cite": "Something half-remembered"},
                       {"cite": "Also unsure", "verified": False}]})
    check("verified reference kept", "Lemma 1.2" in text)
    check("unverified references absent", "half-remembered" not in text
          and "Also unsure" not in text)
    check("the count of dropped references is reported", dropped == 2, f"{dropped}")
    text, _ = bd.build({"summary": "S.", "references": [{"cite": "x"}]})
    check("a references section with nothing verified is omitted",
          "REFERENCES" not in text)

    print("\n[2b] verified must be boolean, not merely truthy")
    for v in ("no", "false", "pending", 0, 1):
        try:
            bd.build({"summary": "S.", "references": [{"cite": "LEAK", "verified": v}]})
            check(f"refuses verified={v!r}", False)
        except ValueError:
            check(f"refuses verified={v!r}", True)

    print("\n[2c] malformed entries raise named errors, not KeyError")
    for bad, want in (({"summary": "S.", "corrections": [{"text": "no t"}]}, "corrections[0]"),
                      ({"summary": "S.", "chapters": [{"t": "0:00"}]}, "chapters[0]"),
                      ({"summary": "S.", "references": "notalist"}, "must be a list"),
                      ({"summary": "S.", "series": {"next": {"title": "T"}}}, "series.next")):
        try:
            bd.build(bad)
            check(f"refuses {want}", False)
        except ValueError as exc:
            check(f"refuses {want}", want in str(exc), str(exc))

    print("\n[3] corrections are labelled by provenance")
    text, _ = bd.build({"summary": "S.", "corrections": [
        {"t": "6:43", "text": "should be tau", "verbatim": True}]})
    check("verbatim corrections carry a per-item mark", "[speaker] at 6:43" in text)
    check("the timestamp survives", "6:43" in text)
    text, _ = bd.build({"summary": "S.", "corrections": [
        {"t": "1:00", "text": "machine found this"}]})
    check("derived corrections carry their own per-item mark",
          "[derived] at 1:00" in text)
    mixed, _ = bd.build({"summary": "S.", "corrections": [
        {"t": "6:43", "text": "a", "verbatim": True}, {"t": "9:10", "text": "b"}]})
    check("mixed provenance is distinguishable per line",
          "[speaker] at 6:43" in mixed and "[derived] at 9:10" in mixed)
    check("corrections do not start a line with a timestamp (chapter clash)",
          not any(l.lstrip()[:1].isdigit() and ":" in l.lstrip()[:6]
                  for l in mixed.split("\n") if "at 6:43" in l or "at 9:10" in l))

    print("\n[4] ordering is fixed")
    text, _ = bd.build({
        "summary": "S.",
        "corrections": [{"t": "0:10", "text": "c"}],
        "references": [{"cite": "r", "verified": True}],
        "series": {"next": {"title": "Part 2", "url": "https://example.com/2"}},
        "attribution": {"model": "M", "author": "A"}})
    order = [text.index(s) for s in ("CORRECTIONS", "REFERENCES", "THIS SERIES")]
    check("corrections, then references, then series", order == sorted(order), f"{order}")
    check("attribution is last", text.index("assembled automatically") > max(order))

    print("\n[5] output survives the policy checker")
    checker = os.path.join(HERE, os.pardir, os.pardir,
                           "check-youtube-description", "scripts",
                           "check-description.py")
    if not os.path.exists(checker):
        check("sibling checker present (skipped)", True)
    else:
        text, _ = bd.build({
            "summary": "A talk about widgets and their many uses.",
            "chapters": [{"t": "0:00", "label": "Intro"},
                         {"t": "1:00", "label": "Middle"},
                         {"t": "2:00", "label": "End"}],
            "references": [{"cite": "Lemma 1.2", "url": "https://example.com/a",
                            "verified": True}],
            "corrections": [{"t": "6:43", "text": "tau not T", "verbatim": True},
                            {"t": "9:10", "text": "derived note"}],
            "provenance": {"original_published": "2015-04-22",
                           "reuploaded": "2026-09-27",
                           "original_url": "https://example.com/old",
                           "original_state": "unlisted"},
            "attribution": {"model": "M", "author": "A",
                            "tools_url": "https://example.com/tools"}})
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "d.txt")
            open(path, "w", encoding="utf8").write(text)
            proc = subprocess.run(
                [sys.executable, checker, "--file", path, "--require-attribution",
                 "--duration", "1800"],
                capture_output=True, text=True)
        check("output WITH corrections AND chapters passes the checker",
              proc.returncode == 0, proc.stdout)
        check("no angle brackets are ever emitted", "<" not in text and ">" not in text)

    print(f"\n{'ALL PASS' if not FAILED else str(len(FAILED)) + ' FAILED'}")
    return 1 if FAILED else 0


if __name__ == "__main__":
    sys.exit(main())
