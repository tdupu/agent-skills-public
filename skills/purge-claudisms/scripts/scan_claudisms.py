#!/usr/bin/env python3
"""Mechanical scan for claudisms in a .tex or .md file.

Usage: scan_claudisms.py [--table PATH] [--top N] [--quiet] FILE [FILE ...]
Reads the regex column of references/claudisms.md (sibling of this script's
parent), applies every pattern per line (case-insensitive) after stripping
LaTeX comments, \\taylor{} markers, \\cite/\\ref/\\label/\\url arguments,
verbatim blocks, thebibliography, Markdown code fences and HTML comments,
and runs the paragraph-level builtin checks named `builtin:<name>`.
.bib files are skipped. Output: one row per hit
`FILE:LINE  ID  TYPE  "match"  pattern  -> replacement`, then a summary by
type. Exit 1 if any lexical or structural hit, else 0 (syntactic and
rhetorical hits are WARN). Exit 2 on a usage or table error.
"""
from __future__ import annotations

import argparse
import collections
import re
import sys
from pathlib import Path

BS1 = chr(92)      # one literal backslash
BS = BS1 * 2       # regex for one literal backslash; spelled this way so path scanners do not read patterns as UNC paths
DEFAULT_TABLE = Path(__file__).resolve().parent.parent / "references" / "claudisms.md"
HARD = {"lexical", "structural"}
SENT_END = re.compile(r"(?<=[.!?])\s+")
# structural lines dropped from paragraph-level checks; \item keeps its text
SKIP_LINE = re.compile(BS + r"(begin|end|(sub)*section\*?|title|author|date|maketitle|label|vspace\*?|newpage|clearpage|documentclass|usepackage|(re)?newcommand|input|include|bibliography(style)?|paragraph\*?)(\[[^\]]*\])?(\{(?:[^{}]|\{[^{}]*\})*\})?|" + BS + r"item(\[[^\]]*\])?")


def load_table(path: Path):
    """Return list of dicts: id, pattern, type, why, replacement, regex, source, added."""
    rows = []
    for ln in path.read_text(encoding="utf-8").splitlines():
        if not ln.startswith("| C"):
            continue
        cells = [c.strip() for c in re.split(r"(?<![\x5c])\|", ln)[1:-1]]
        if len(cells) != 8:
            raise ValueError(f"table row with {len(cells)} cells: {ln[:60]}")
        cells = [c.replace(r"\|", "|") for c in cells]  # regexes spell a literal backslash as \x5c
        rx = cells[5].strip("`")
        rows.append(dict(id=cells[0], pattern=cells[1], type=cells[2], why=cells[3],
                         replacement=cells[4], regex=rx, source=cells[6], added=cells[7]))
    if not rows:
        raise ValueError(f"no rows found in {path}")
    return rows


def strip_tex(text: str) -> str:
    """Blank (keep line count) comments, PI markers, citation keys, labels, URLs, verbatim, bibliography."""
    text = re.sub(BS + r"taylor\{(?:[^{}]|\{[^{}]*\})*\}", "", text)
    for env in ("verbatim", "lstlisting", "thebibliography", r"filecontents\*?", "minted"):
        text = re.sub(BS + r"begin\{" + env + r"\}.*?" + BS + r"end\{" + env + r"\}",
                      lambda m: re.sub(r"[^\n]", "", m.group(0)), text, flags=re.S)
    text = re.sub(BS + r"(cite[a-z]*|ref|eqref|label|url|href|input|include|bibliography)\*?(\[[^\]]*\])?\{[^{}]*\}", "", text)
    return "\n".join(re.sub(r"(?<!\\)%.*$", "", ln) for ln in text.splitlines())


def strip_md(text: str) -> str:
    text = re.sub(r"```.*?```", lambda m: re.sub(r"[^\n]", "", m.group(0)), text, flags=re.S)
    text = re.sub(r"<!--.*?-->", lambda m: re.sub(r"[^\n]", "", m.group(0)), text, flags=re.S)
    text = re.sub(r"`[^`\n]*`", "", text)
    return text


def paragraphs(lines):
    """Yield (first_line_no, text) for blank-line-separated paragraphs."""
    start, buf = None, []
    for i, ln in enumerate(lines, 1):
        t = SKIP_LINE.sub("", ln.strip())
        if t:
            if start is None:
                start = i
            buf.append(t)
        elif buf:
            yield start, " ".join(buf)
            start, buf = None, []
    if buf:
        yield start, " ".join(buf)


def builtin_hits(name: str, lines):
    """Paragraph-level checks. Each returns [(line_no, excerpt)]."""
    out = []
    for ln_no, para in paragraphs(lines):
        sents = [s for s in SENT_END.split(para) if s.strip()]
        if name == "emdash":
            n = len(re.findall(r"---|—", para))
            if n > 1:
                out.append((ln_no, f"{n} em dashes in one paragraph"))
        elif name == "semitriad":
            for s in sents:
                core = re.sub(r"\([^()]*\)|\$[^$]*\$", "", s)
                if core.count(";") >= 2:
                    out.append((ln_no, s[:90]))
        elif name == "triad":
            for s in sents:
                if re.search(r"\b(\w+(?: \w+){0,3}), (\w+(?: \w+){0,3}),? (and|or) (\w+(?: \w+){0,3})\b", s) and "$" not in s:
                    m = re.search(r"\b(\w+(?: \w+){0,3}), (\w+(?: \w+){0,3}),? (and|or) (\w+(?: \w+){0,3})\b", s)
                    out.append((ln_no, m.group(0)[:90]))
        elif name == "colonchain":
            for s in sents:
                if len(re.findall(r"(?<!\\)(?<!:):(?!:)", re.sub(r"\$[^$]*\$", "", s))) >= 2:
                    out.append((ln_no, s[:90]))
        elif name == "onesentpara":
            if len(sents) == 1 and len(para.split()) <= 12 and not para.startswith(BS1):
                out.append((ln_no, para[:90]))
        elif name == "parens":
            n = len(re.findall(r"\((?![^)]*\$)[^()]{4,}\)", re.sub(r"\$[^$]*\$", "", para)))
            if len(sents) >= 2 and n * 2 >= len(sents):
                out.append((ln_no, f"{n} parenthetical asides in {len(sents)} sentences"))
        elif name == "transitions":
            heads = [re.match(r"\s*(furthermore|moreover|additionally|in addition|however|thus|hence|therefore|consequently|notably)\b", s, re.I) for s in sents]
            if sum(1 for h in heads if h) >= 3:
                out.append((ln_no, "; ".join(h.group(1) for h in heads if h)))
        elif name == "restate":
            n = len(re.findall(r"\b(in other words|put differently|equivalently|that is to say|said differently)\b", para, re.I))
            if n >= 2:
                out.append((ln_no, f"{n} restatement frames in one paragraph"))
    return out


def scan_file(path: Path, rows):
    raw = path.read_text(encoding="utf-8", errors="replace")
    text = strip_md(raw) if path.suffix.lower() in {".md", ".markdown", ".txt"} else strip_tex(raw)
    lines = text.splitlines()
    hits = []
    for row in rows:
        rx = row["regex"]
        if not rx or row["type"] == "retired":
            continue
        if rx.startswith("builtin:"):
            for ln_no, ex in builtin_hits(rx.split(":", 1)[1], lines):
                hits.append((path, ln_no, row, ex))
            continue
        try:
            pat = re.compile(rx, re.I)
        except re.error as e:
            raise ValueError(f"{row['id']} bad regex {rx!r}: {e}")
        for i, ln in enumerate(lines, 1):
            m = pat.search(ln)
            if m:
                hits.append((path, i, row, m.group(0)[:60]))
    return hits


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("files", nargs="+")
    ap.add_argument("--table", type=Path, default=DEFAULT_TABLE)
    ap.add_argument("--top", type=int, default=20, help="rows in the top-patterns summary")
    ap.add_argument("--quiet", action="store_true", help="summary only")
    a = ap.parse_args(argv)
    try:
        rows = load_table(a.table)
    except (OSError, ValueError) as e:
        print(f"scan_claudisms: {e}", file=sys.stderr)
        return 2
    hits = []
    for f in a.files:
        p = Path(f)
        if p.suffix.lower() == ".bib":
            print(f"skip {p} (bib)")
            continue
        if not p.is_file():
            print(f"scan_claudisms: not a file: {p}", file=sys.stderr)
            return 2
        try:
            hits.extend(scan_file(p, rows))
        except ValueError as e:
            print(f"scan_claudisms: {e}", file=sys.stderr)
            return 2
    hits.sort(key=lambda h: (str(h[0]), h[1]))
    if not a.quiet:
        for p, ln, row, ex in hits:
            flag = "FAIL" if row["type"] in HARD else "WARN"
            print(f"{p}:{ln}  {row['id']}  {flag}/{row['type']}  \"{ex}\"  {row['pattern'][:50]}  -> {row['replacement'][:70]}")
    by_type = collections.Counter(r["type"] for _, _, r, _ in hits)
    by_id = collections.Counter((r["id"], r["pattern"][:55]) for _, _, r, _ in hits)
    print(f"\n{len(hits)} hits in {len(a.files)} file(s); by type: " + ", ".join(f"{k}={v}" for k, v in sorted(by_type.items())) or "none")
    for (i, pat), n in by_id.most_common(a.top):
        print(f"  {n:4d}  {i}  {pat}")
    hard = sum(by_type[t] for t in HARD)
    return 1 if hard else 0


if __name__ == "__main__":
    sys.exit(main())
