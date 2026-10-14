#!/usr/bin/env python3
"""Mechanical audit of an NSF proposal folder against Grants/GRANT-FORMAT.md.

Usage: check_format.py <proposal-folder>
Exit 1 if any rule FAILs.
"""
import os
import re
import subprocess
import sys

ROWS = []


def row(rule, result, measured, where=""):
    ROWS.append((rule, result, str(measured), where))


def run(cmd):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=120).stdout
    except Exception as e:  # noqa: BLE001
        return f"ERROR {e}"


def pages(pdf):
    out = run(["pdfinfo", pdf])
    m = re.search(r"Pages:\s+(\d+)", out)
    return int(m.group(1)) if m else -1


def pdftext(pdf):
    return run(["pdftotext", "-layout", pdf, "-"])


def read(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            return f.read()
    except FileNotFoundError:
        return ""


def strip_comments(tex):
    return "\n".join(re.sub(r"(?<!\\)%.*$", "", ln) for ln in tex.splitlines())


def main(folder):
    tex = os.path.join(folder, "proposal", "tex")
    pdfs = os.path.join(folder, "proposal", "final-pdfs")
    sub = os.path.join(folder, "proposal", "submission-docs")

    # F1 file set
    required = {"summary.pdf", "description.pdf", "references.pdf",
                "data-management.pdf", "facilities.pdf", "budget-justification.pdf"}
    present = set(os.listdir(pdfs)) if os.path.isdir(pdfs) else set()
    bj = strip_comments(read(os.path.join(tex, "budget-justification.tex")))
    # F16 (2026-10-12): mentoring plan required when a postdoc OR a graduate
    # student is budgeted (PAPPG 24-1 II.D.2.i(i)).
    postdoc = (bool(re.search(r"post[- ]?doc", bj, re.I)) and not re.search(r"no post[- ]?doc", bj, re.I)) \
        or bool(re.search(r"graduate (research )?(assistant|student)", bj, re.I))
    if postdoc:
        required.add("mentoring.pdf")
    missing = required - present
    extra = present - required
    row("F1", "PASS" if not missing and not extra else "FAIL",
        f"missing={sorted(missing)} extra={sorted(extra)}", pdfs)

    # F2 fonts
    bad = []
    for name in sorted(present):
        out = run(["pdffonts", os.path.join(pdfs, name)])
        for ln in out.splitlines()[2:]:
            if ln.strip() and "Type 3" in ln:
                bad.append(f"{name}: Type 3 font (bitmap)")
    desc_tex = read(os.path.join(tex, "description.tex"))
    m = re.search(r"\\documentclass\[(.*?)\]", desc_tex)
    pt = re.search(r"(1[0-2])pt", m.group(1)) if m else None
    size_ok = pt is not None and int(pt.group(1)) >= 11
    row("F2", "PASS" if size_ok and not bad else "FAIL",
        f"documentclass size={pt.group(1) if pt else '?'}pt; {bad or 'no Type3'}", "description.tex")

    # F3 margins / paper
    for name in sorted(present):
        out = run(["pdfinfo", os.path.join(pdfs, name)])
        ps = re.search(r"Page size:\s+([\d.]+) x ([\d.]+)", out)
        ok = ps and abs(float(ps.group(1)) - 612) < 2 and abs(float(ps.group(2)) - 792) < 2
        if not ok:
            row("F3", "FAIL", f"page size {ps.group(0) if ps else '?'}", name)
    srcs = {n: strip_comments(read(os.path.join(tex, n))) for n in os.listdir(tex) if n.endswith(".tex")} if os.path.isdir(tex) else {}
    for n, s in srcs.items():
        if "\\documentclass" in s:
            if "fullpage" in s or re.search(r"geometry.*margin=1(\.\d+)?in", s):
                continue
            if re.search(r"margin=0?\.[0-9]+in", s):
                row("F3", "FAIL", "margin < 1in", n)
    if not any(r[0] == "F3" for r in ROWS):
        row("F3", "PASS", "letter paper; fullpage/geometry>=1in", "")

    # F4 summary
    sp = os.path.join(pdfs, "summary.pdf")
    if os.path.exists(sp):
        t = pdftext(sp)
        tl = re.sub(r"\s+", "", t.lower())  # small-caps headings extract with spaces
        order = [tl.find(h) for h in ("overview", "intellectualmerit", "broaderimpacts")]
        ok = pages(sp) == 1 and all(i >= 0 for i in order) and order == sorted(order)
        row("F4", "PASS" if ok else "FAIL", f"pages={pages(sp)} heading positions={order}", "summary.pdf")
    else:
        row("F4", "FAIL", "summary.pdf missing", "")

    # F5 description pages and prior-support span
    dp = os.path.join(pdfs, "description.pdf")
    if os.path.exists(dp):
        n = pages(dp)
        aux = read(os.path.join(tex, "description.aux"))
        span = "?"
        labels = re.findall(r"\\newlabel\{S:(\w+)\}\{\{[^}]*\}\{(\d+)\}", aux)
        d = {k: int(v) for k, v in labels}
        if "prior" in d and "proposed" in d:
            span = d["proposed"] - d["prior"] + 1
        ok = 0 < n <= 15 and (span == "?" or span <= 5)
        row("F5", "PASS" if ok else "FAIL", f"pages={n}; prior-support span={span}", "description.pdf")
    else:
        row("F5", "FAIL", "description.pdf missing", "")

    # F6 / F7 headings and prior support items
    body = strip_comments(desc_tex)
    has_bi = re.search(r"\\section\*?\{Broader Impacts\.?\}", body) is not None
    has_prior = re.search(r"\\section\*?\{Results from Prior NSF [Ss]upport\}", body) is not None
    row("F6", "PASS" if has_bi and has_prior else "FAIL",
        f"Broader Impacts section={has_bi}; Prior Support section={has_prior}", "description.tex")
    items = {
        "a: award number": r"DMS-\d{7}",
        "a: amount": r"\\\$\s?\d{2,3}[,{]",
        "a: period": r"20\d\d\s*--?\s*(May|June|20)",
        "c: Intellectual Merit heading": r"\\subsubsection\*?\{Intellectual Merit",
        "c: Broader Impacts heading": r"\\subsubsection\*?\{Broader Impacts",
        "d: publications list": r"\\subsubsection\*?\{Publications",
        "d: citations present": r"\\cite",
        "e: products/availability": r"(GitHub|LMFDB|arXiv|repository|database)",
        "f: relation to proposed work": r"Relation to the proposed work",
    }
    prior_block = body
    mm = re.search(r"\\section\*?\{Results from Prior NSF [Ss]upport\}(.*?)\\section\*?\{", body, re.S)
    if mm:
        prior_block = mm.group(1)
    missing_items = [k for k, pat in items.items() if not re.search(pat, prior_block, re.S)]
    row("F7", "PASS" if not missing_items else "FAIL", f"missing={missing_items}", "description.tex")

    # F8 URLs
    urls = re.findall(r"\\url|\\href|https?://|www\.", body)
    row("F8", "PASS" if not urls else "FAIL", f"{len(urls)} URL tokens", "description.tex")

    # F9 build log
    log = read(os.path.join(tex, "description.log"))
    undef = len(re.findall(r"undefined", log, re.I))
    multi = len(re.findall(r"multiply.defined", log, re.I))
    over = [float(x) for x in re.findall(r"Overfull \\hbox \(([\d.]+)pt", log)]
    qq = pdftext(dp).count("??") if os.path.exists(dp) else -1
    ok = undef == 0 and multi == 0 and qq == 0 and all(o <= 20 for o in over)
    row("F9", "PASS" if ok else "FAIL",
        f"undefined={undef} multiply={multi} ??={qq} overfull>20pt={sum(o > 20 for o in over)}", "description.log")

    # F10 references
    rt = strip_comments(read(os.path.join(tex, "references.tex")))
    prose = re.search(r"\\section|\\subsection|\\begin\{itemize\}", rt)
    row("F10", "PASS" if rt and not prose else "FAIL", "bibliography-only" if not prose else "prose found", "references.tex")

    # F13 DMP
    dm = os.path.join(pdfs, "data-management.pdf")
    if os.path.exists(dm):
        t = pdftext(dm)
        topics = {k: bool(re.search(p, t, re.I)) for k, p in {
            "products": r"manuscript|software|database|video",
            "where": r"arXiv|GitHub|LMFDB|Zenodo|YouTube",
            "when": r"at\s+the\s+time\s+of\s+publi|upon\s+publi|public\s+at|on\s+submission|within",
            "preservation": r"preserv|archiv|DOI|license",
        }.items()}
        row("F13", "PASS" if pages(dm) <= 2 and all(topics.values()) else "FAIL",
            f"pages={pages(dm)} topics={topics}", "data-management.pdf")
    else:
        row("F13", "FAIL", "data-management.pdf missing", "")

    # F14 facilities
    ft = strip_comments(read(os.path.join(tex, "facilities.tex")))
    row("F14", "PASS" if "\\$" not in ft else "FAIL", "no dollar figures" if "\\$" not in ft else "dollar figure present", "facilities.tex")

    # F15 budget justification
    bp = os.path.join(pdfs, "budget-justification.pdf")
    months = re.findall(r"(\w+|\d+)\s+months? of summer", bj)
    too_many = [m for m in months if m.lower() in ("three", "four", "five", "3", "4", "5")]
    row("F15", "PASS" if os.path.exists(bp) and pages(bp) <= 5 and not too_many else "FAIL",
        f"pages={pages(bp) if os.path.exists(bp) else '?'}; summer months mentions={months}", "budget-justification")

    # F16 mentoring
    has_m = "mentoring.pdf" in present
    row("F16", "PASS" if has_m == postdoc else "FAIL", f"postdoc/graduate budgeted={postdoc}; mentoring.pdf={has_m}", "")

    # F17 reviewers not in description
    rv = read(os.path.join(sub, "reviewers.txt"))
    names = [ln.split(",")[0].strip().split()[-1] for ln in rv.splitlines() if "," in ln]
    hits = [n for n in names if re.search(r"\b" + re.escape(n) + r"\b.{0,40}\b(suggested reviewer|as a reviewer|reviewers?:)", body) or re.search(r"\b(suggested reviewers?|reviewers?:).{0,40}\b" + re.escape(n) + r"\b", body)]
    row("F17", "PASS" if not hits else "FAIL", f"reviewer surnames in description near 'review': {hits}", "")

    # Judgment confirms
    for rule, q in (("F11", "SciENcv biosketch (<=3pp) and CPS exported and certified?"),
                    ("F12", "COA on NSF's current xlsx template?"),
                    ("F18", "Date SPA received the submission-ready set (>=2 business days before target)?")):
        row(rule, "CONFIRM", q, "README.md")

    w = max(len(r[2]) for r in ROWS)
    print(f"{'rule':5} {'result':8} {'measured':{w}}  where")
    for r in ROWS:
        print(f"{r[0]:5} {r[1]:8} {r[2]:{w}}  {r[3]}")
    fails = [r for r in ROWS if r[1] == "FAIL"]
    print(f"\n{len(fails)} FAIL, {sum(r[1]=='PASS' for r in ROWS)} PASS, {sum(r[1]=='CONFIRM' for r in ROWS)} CONFIRM")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main(os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "."))
