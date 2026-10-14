#!/usr/bin/env python3
"""Mechanical part of using-pdpowers/references/PD-POLICY.md (rules tagged [M]).

Usage: check_pd_policy.py <description.tex>
Prints `rule  PASS|FAIL|CONFIRM|INFO  evidence`; exits 1 if any rule FAILs.
CONFIRM rows are heuristic hits the agent judges against the policy text.
"""
import os
import re
import sys

BS = chr(92) * 2  # regex for one literal backslash; spelled this way so path scanners do not read patterns as UNC paths
THEOREM_ENVS = ["theorem", "proposition", "lemma", "corollary", "conjecture",
                "definition", "problem", "question"]
RELATIVE_TIME = r"\b(recently|currently|last year|this year|next year|soon|now|upcoming|forthcoming|ongoing)\b"
PREACHY = r"\bit is (important|essential|crucial|vital|imperative)\b|\bwe believe\b|\bbest practices?\b"


def strip(tex):
    """Drop comments and the contents of \\taylor{...} PI markers (the PI's own voice)."""
    tex = re.sub(BS + r"taylor\{(?:[^{}]|\{[^{}]*\})*\}", "", tex)
    return "\n".join(re.sub(r"(?<!\\)%.*$", "", ln) for ln in tex.splitlines())


def hits(text, pat, flags=re.I, width=90):
    return [(i, ln.strip()[:width]) for i, ln in enumerate(text.splitlines(), 1)
            if re.search(pat, ln, flags)]


def fmt(h, n=12):
    return "; ".join(f"L{i}: {t}" for i, t in h[:n]) + (f"; +{len(h) - n} more" if len(h) > n else "")


def env_mask(text, env):
    """Line numbers inside \\begin{env}...\\end{env}."""
    inside, out = False, set()
    for i, ln in enumerate(text.splitlines(), 1):
        if re.search(BS + r"begin\{%s\}" % env, ln):
            inside = True
        if inside:
            out.add(i)
        if re.search(BS + r"end\{%s\}" % env, ln):
            inside = False
    return out


def section_block(text, title):
    m = re.search(BS + r"section\*?\{%s\}(.*?)(?=" % title + BS + r"section\*?\{|\Z)", text, re.S)
    return m.group(1) if m else ""


def main(path):
    raw = open(path, encoding="utf-8", errors="replace").read()
    tex = strip(raw)
    rows = []

    # P1 third person
    p1 = hits(tex, r"\bwe propose\b|\bour\b")
    rows.append(("P1", "FAIL" if p1 else "PASS", fmt(p1) or "no 'we propose'/'our'"))
    we = hits(tex, r"\bwe\b")
    if we:
        rows.append(("P1", "CONFIRM", f"{len(we)} lines use 'we'; third person preferred: " + fmt(we, 8)))

    # P2 definitions outside definition environments (heuristic)
    in_def = env_mask(tex, "definition")
    p2 = [(i, t) for i, t in hits(tex, r"\b(A|An)\s+" + BS + r"emph\{[^}]+\}\s+(is|are)\b|is called (a|an)\s+" + BS + r"emph\{")
          if i not in in_def]
    rows.append(("P2", "CONFIRM" if p2 else "PASS",
                 (f"{len(p2)} definition-shaped sentences outside definition env: " + fmt(p2)) if p2
                 else "no definition-shaped sentences outside definition env"))

    # P4 scaffolding labels
    p4 = hits(tex, BS + r"emph\{(Built on|Where it stands|What is new|Plan\.|Deliverables)|\bwhat is new\b|^\s*" + BS + r"textbf\{[^}]{1,40}[.:]\}")
    rows.append(("P4", "FAIL" if p4 else "PASS", fmt(p4) or "no run-in labels"))

    # P5 step items
    p5 = hits(tex, BS + r"item\[Step")
    rows.append(("P5", "FAIL" if p5 else "PASS", fmt(p5) or "no \\item[Step]"))

    # P7 referee comments
    p7 = hits(tex, r"\breferee")
    rows.append(("P7", "FAIL" if p7 else "PASS", fmt(p7) or "no 'referee'"))

    # P8 private notes
    p8 = hits(tex, r"\b(our|the PI's|my|private|unpublished|internal)\s+(\w+\s+)?notes?\b|\bnotes?\s+(of the PI|in preparation)\b")
    rows.append(("P8", "FAIL" if p8 else "PASS", fmt(p8) or "no private-notes appeals"))

    # P9 relative time words
    p9 = hits(tex, RELATIVE_TIME)
    rows.append(("P9", "CONFIRM" if p9 else "PASS",
                 (f"{len(p9)} relative-time words; each needs a date: " + fmt(p9)) if p9 else "no relative-time words"))

    # P10 award numbers
    p10 = [(i, t) for i, t in hits(tex, r"\b(previous|prior|last|earlier) (award|grant|proposal)\b|\bthe 20\d\d award\b")
           if not re.search(r"DMS-\d{7}", t)]
    rows.append(("P10", "FAIL" if p10 else "PASS", fmt(p10) or "awards named by number"))

    # P11 long quotations
    p11 = []
    for i, ln in enumerate(tex.splitlines(), 1):
        ln_q = re.sub(BS + "[`'\"]", "", ln)  # ignore accent macros (\`a, \'e, \"o)
        for q in re.findall(r"``(.*?)''|\"(.*?)\"", ln_q):
            words = len((q[0] or q[1]).split())
            if words > 25:
                p11.append((i, f"{words}-word quotation"))
    rows.append(("P11", "FAIL" if p11 else "PASS", fmt(p11) or "no quotation over 25 words"))

    # P12 preachy
    p12 = hits(tex, PREACHY)
    rows.append(("P12", "FAIL" if p12 else "PASS", fmt(p12) or "no exhortation phrases"))

    # P13 item references and labels
    p13 = hits(tex, r"(?<!" + BS + r")\bitems? (\d|" + BS + r"ref)")
    prior = section_block(tex, "Results from Prior NSF [Ss]upport")
    unlabeled = [t for t in prior.splitlines() if re.match(r"\s*" + BS + r"item\b", t) and r"\label{" not in t]
    ev = []
    if p13:
        ev.append("prose refers to items by number: " + fmt(p13))
    if unlabeled:
        ev.append(f"{len(unlabeled)} \\item without \\label in prior-support enumerate")
    rows.append(("P13", "FAIL" if ev else "PASS", "; ".join(ev) or "items labelled and referenced by \\eqref"))

    # P15 reviewer-perspective pass
    folder = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(path))))
    rdir = os.path.join(folder, "reviews")
    revs = sorted(f for f in os.listdir(rdir)) if os.path.isdir(rdir) else []
    revs = [f for f in revs if f.startswith("review-as-") and f.endswith(".md")]
    stale = [f for f in revs if os.path.getmtime(os.path.join(rdir, f)) < os.path.getmtime(path)]
    rows.append(("P15", "PASS" if revs and not stale else "CONFIRM",
                 f"{len(revs)} review-as files, {len(stale)} older than description.tex" if revs
                 else "no reviews/review-as-*.md; run pd-review-as before the PI walk"))

    # P16 environment inventory
    counts = {e: len(re.findall(BS + r"begin\{%s\}" % e, tex)) for e in THEOREM_ENVS}
    rows.append(("P16", "INFO", ", ".join(f"{e}={n}" for e, n in counts.items())))

    for r in rows:
        print(f"{r[0]:4} {r[1]:8} {r[2]}")
    fails = [r for r in rows if r[1] == "FAIL"]
    print(f"\n{len(fails)} FAIL")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
