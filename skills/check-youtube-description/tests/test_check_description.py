#!/usr/bin/env python3
"""Tests for the description policy checker.

Run: python3 tests/test_check_description.py
Standard library only; drives the CLI so exit codes are covered too.
"""
from __future__ import annotations

import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
CHECK = os.path.join(HERE, os.pardir, "scripts", "check-description.py")
FAILED = []


def check(name, ok, detail=""):
    print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f"  [{detail}]" if detail and not ok else ""))
    if not ok:
        FAILED.append(name)


def run(text, *extra):
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "d.txt")
        open(path, "w", encoding="utf8").write(text)
        proc = subprocess.run([sys.executable, CHECK, "--file", path, *extra],
                              capture_output=True, text=True)
        return proc.returncode, proc.stdout


def main():
    print("[1] hard limits")
    code, out = run("A clean description with no problems at all.")
    check("a clean description passes", code == 0, out)
    code, out = run("x" * 5001)
    check("over 5000 BYTES fails", code == 1 and "bytes" in out)
    code, out = run("see <!-- fence --> here")
    check("angle brackets fail", code == 1 and "invalidDescription" in out)
    check("the failure quotes the surrounding text", "fence" in out)
    code, out = run("bell\x07here")
    check("control characters fail", code == 1 and "control characters" in out)

    code, out = run("x" * 4980 + "\u2014" * 200)
    check("a description under 5000 CHARS but over 5000 BYTES fails",
          code == 1 and "too long" in out, out.splitlines()[0] if out else "")
    code, out = run("0:00 A\n1:00 B\n2:00 C\n" + "#tag " * 61)
    check("over 60 hashtags fails", code == 1 and "hashtags" in out)

    print("\n[2] chapters fail as a group, so all four rules are checked")
    good = "0:00 Intro\n1:00 Middle\n2:00 End\n"
    code, out = run(good)
    check("a valid chapter list passes", code == 0, out)
    code, out = run("1:00 Intro\n2:00 Middle\n3:00 End\n")
    check("not starting at 0:00 fails", code == 1 and "not 0:00" in out)
    code, out = run("0:00 Intro\n1:00 End\n")
    check("fewer than three fails", code == 1 and "at least 3" in out)
    code, out = run("0:00 A\n0:05 B\n1:00 C\n")
    check("a chapter under 10s fails", code == 1 and "shorter than 10s" in out)
    code, out = run("0:00 A\n2:00 B\n1:00 C\n")
    check("out-of-order timestamps fail", code == 1 and "ascending" in out)
    code, out = run("0:00\n1:00\n2:00\n")
    check("timestamps with no title fail", code == 1 and "no title" in out)
    code, out = run("Intro - 0:00\nMiddle - 1:00\nEnd - 2:00\n")
    check("label-first lines are reported, not silently ignored",
          code == 1 and "after the label" in out)
    code, out = run("0:00 A\n1:00 B\n2:00 C\nBonus - 3:00\n")
    check("a label-first line is reported even among valid chapters",
          code == 1 and "after the label" in out)
    code, out = run("Recorded at 10:30 in Room 2 on a Tuesday.\n")
    check("ordinary prose with a clock time is NOT flagged", code == 0, out)
    code, out = run("0:00 A\n1:00 B\n2:00 C\n", "--duration", "125")
    check("a too-short final chapter fails with --duration",
          code == 1 and "final chapter" in out)
    code, out = run("0:00 A\n1:00 B\n2:00 C\n", "--duration", "600")
    check("a long final chapter passes", code == 0, out)

    print("\n[3] trust rules")
    code, out = run("Ref: Lemma 1 PENDING VERIFICATION")
    check("an unverified citation marker fails", code == 1 and "unverified" in out)
    dup = "a https://example.com/x b https://example.com/x"
    code, out = run(dup)
    check("a duplicate link fails", code == 1 and "duplicate link" in out)
    code, out = run("see https://example.com/page.")
    check("a link ending in punctuation fails", code == 1 and "malformed" in out)

    print("\n[3b] input errors are distinguishable from bad descriptions")
    proc = subprocess.run([sys.executable, CHECK, "--file", "no-such-file-here.txt"],
                          capture_output=True, text=True)
    check("a missing file exits 2, not 1", proc.returncode == 2, str(proc.returncode))
    code, out = run("Next stream: TBD", "--allow-pending")
    check("--allow-pending permits legitimate TBD prose", code == 0, out)

    print("\n[4] optional gates")
    code, out = run("Plain text with no notice.", "--require-attribution")
    check("missing attribution fails when required", code == 1 and "automatic" in out.lower())
    code, out = run("This was generated automatically.", "--require-attribution")
    check("a stated notice satisfies it", code == 0, out)

    with tempfile.TemporaryDirectory() as tmp:
        ids = os.path.join(tmp, "ids.txt")
        open(ids, "w", encoding="utf8").write("abcdefghijk\n")
        code, out = run("next: https://youtu.be/zzzzzzzzzzz", "--known-ids", ids)
        check("an unknown video id fails", code == 1 and "not in the known set" in out)
        for url in ("https://youtube.com/shorts/zzzzzzzzzzz",
                    "https://youtube.com/live/zzzzzzzzzzz",
                    "https://youtube.com/watch?app=desktop&v=zzzzzzzzzzz"):
            code, out = run(f"see {url}", "--known-ids", ids)
            check(f"unknown id caught in {url.split('/')[-1][:12]} form",
                  code == 1 and "not in the known set" in out, out)
        code, out = run("next: https://youtu.be/abcdefghijk", "--known-ids", ids)
        check("a known video id passes", code == 0, out)

    print(f"\n{'ALL PASS' if not FAILED else str(len(FAILED)) + ' FAILED'}")
    return 1 if FAILED else 0


if __name__ == "__main__":
    sys.exit(main())
