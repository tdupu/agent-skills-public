#!/usr/bin/env python3
"""Mechanical part of check-grant-style (GRANT-STYLE S4, S5, S7, S8, S9, S10, S11).

Usage: check_style.py <proposal-folder>
"""
import os
import re
import sys

BANNED = ["exciting", "transformative", "robust", "cutting-edge", "cutting edge",
          "synergy", "synergistic", "state-of-the-art", "paradigm", "groundbreaking",
          "world-class", "unprecedented", "pioneering", "unique opportunity"]
BANNED_AI = ["AI-driven", "AI driven", "autonomous discovery", "the AI found",
             "the AI discovered", "AI-generated proof"]
GERUNDS = r"\\subsection\*?\{(Studying|Exploring|Investigating|Understanding|Developing|Extending|Examining|Analyzing)\b"


def read(p):
    try:
        return open(p, encoding="utf-8", errors="replace").read()
    except FileNotFoundError:
        return ""


def strip(tex):
    return "\n".join(re.sub(r"(?<!\\)%.*$", "", ln) for ln in tex.splitlines())


def lines_matching(text, pat, flags=0):
    out = []
    for i, ln in enumerate(text.splitlines(), 1):
        if re.search(pat, ln, flags):
            out.append((i, ln.strip()[:110]))
    return out


def main(folder):
    tex = os.path.join(folder, "proposal", "tex")
    desc = strip(read(os.path.join(tex, "description.tex")))
    summ = strip(read(os.path.join(tex, "summary.tex")))
    review = read(os.path.join(folder, "REVIEW.md"))
    rows = []

    # S4 prior support fields
    m = re.search(r"\\section\*?\{Results from Prior NSF [Ss]upport\}(.*?)\\section\*?\{", desc, re.S)
    block = m.group(1) if m else ""
    need = {"award number": r"DMS-\d{7}", "amount": r"\\\$", "period": r"20\d\d",
            "Intellectual Merit": r"Intellectual Merit", "Broader Impacts": r"Broader Impacts",
            "citations": r"\\cite"}
    miss = [k for k, p in need.items() if not re.search(p, block)]
    rows.append(("S4", "PASS" if block and not miss else "FAIL", f"missing={miss}" if block else "no prior-support section"))

    # S5 environments
    envs = lines_matching(desc, r"\\begin\{(theorem|proposition|lemma|corollary)\}")
    rows.append(("S5", "PASS" if len(envs) <= 2 else "FAIL", f"{len(envs)} theorem-class environments: " + "; ".join(f"L{i}" for i, _ in envs)))

    # S7 gerund titles
    g = lines_matching(desc, GERUNDS)
    rows.append(("S7", "PASS" if not g else "FAIL", "; ".join(f"L{i}: {t}" for i, t in g) or "no gerund titles"))

    # S9 banned words
    hits = []
    for w in BANNED:
        for i, t in lines_matching(desc + "\n" + summ, r"\b" + re.escape(w) + r"\b", re.I):
            hits.append(f"L{i} '{w}'")
    lev = lines_matching(desc + "\n" + summ, r"\bleverag(e|es|ing)\b", re.I)
    hits += [f"L{i} 'leverage'" for i, _ in lev]
    rows.append(("S9", "PASS" if not hits else "FAIL", "; ".join(hits[:20]) or "banned list absent"))

    # S10 AI framing
    bad = []
    for w in BANNED_AI:
        bad += [f"L{i} '{w}'" for i, _ in lines_matching(desc + "\n" + summ, re.escape(w), re.I)]
    good = bool(re.search(r"human-driven", desc, re.I)) and bool(re.search(r"AI-assisted", desc, re.I))
    rows.append(("S10", "PASS" if not bad and good else "FAIL",
                 f"banned={bad or 'none'}; says human-driven and AI-assisted={good}"))

    # S11 numbers have REVIEW rows
    nums = set()
    for i, ln in enumerate(desc.splitlines(), 1):
        if re.search(r"\\(cite|ref|label|eqref|section|subsection|documentclass|usepackage|newtheorem|includegraphics)", ln):
            continue
        for n in re.findall(r"(?<![\w.$^_{}\\-])(\d{1,3}(?:,\d{3})+|\d{3,}|\d+(?:\.\d+)?\s?(?:GB|TB|K|k|%))(?![\w$^_}])", ln):
            if re.fullmatch(r"(1[6-9]|20)\d\d", n):
                continue  # years are not counts
            nums.add((n, i))
    rev_nums = set(re.findall(r"\|\s*([\d,.]+\s?(?:GB|TB|K|k|%)?)\s*\|", review))
    rev_flat = {re.sub(r"\s", "", x) for x in rev_nums}
    unsourced = sorted({f"L{i} {n}" for n, i in nums if re.sub(r"\s", "", n) not in rev_flat})
    rows.append(("S11", "PASS" if not unsourced else "FAIL",
                 f"{len(unsourced)} numbers without REVIEW.md row: " + "; ".join(unsourced[:25])))

    # S8 result sentences
    res = lines_matching(desc, r"\b(we|I|the PI) (proved|showed|established|classified|computed|constructed)\b", re.I)
    verified = set(re.findall(r"\|\s*(R\d+)\s*\|.*PI-verified", review))
    rows.append(("S8", "CONFIRM", f"{len(res)} result sentences; {len(verified)} REVIEW.md rows PI-verified. Judgment pass maps each: " +
                 "; ".join(f"L{i}" for i, _ in res[:30])))

    w = max(len(r[2]) for r in rows)
    for r in rows:
        print(f"{r[0]:4} {r[1]:8} {r[2]}")
    fails = [r for r in rows if r[1] == "FAIL"]
    print(f"\n{len(fails)} FAIL")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main(os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "."))
