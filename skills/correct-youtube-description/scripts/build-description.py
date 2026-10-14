#!/usr/bin/env python3
"""Assemble a description from its parts, in a fixed order.

    build-description.py --spec spec.json --out DESC.txt

spec.json keys, all optional except summary:

    summary        one sentence; becomes the search snippet
    chapters       [{"t": "0:00", "label": "Intro"}, ...]
    corrections    [{"t": "6:43", "text": "...", "verbatim": true}, ...]
    references     [{"cite": "...", "url": "...", "verified": true}, ...]
    series         {"previous": {...}, "next": {...}, "playlist": {...}}
                   each {"title": "...", "url": "..."}
    related        [{"title": "...", "url": "..."}, ...]
    provenance     {"original_published": "YYYY-MM-DD", "reuploaded":
                    "YYYY-MM-DD", "reason": "...", "original_url": "..."}
    attribution    {"model": "...", "author": "...", "automated": "...",
                    "tools_url": "..."}

An unverified reference is dropped, not printed. That is the whole point of
the flag: a citation nobody checked is worse than a missing one.
"""
from __future__ import annotations

import argparse
import json
import sys

RULE = "-----"
STAMP = __import__("re").compile(r"^(?:\d+:)?\d{1,2}:\d{2}$")


def _flag(value, where):
    """Booleans only. A string such as "no" is truthy, and treating it as a
    yes once published an unverified citation and once attributed a machine
    sentence to the speaker."""
    if value is not True and value is not False:
        raise ValueError(f"{where} must be boolean true or false, not "
                         f"{value!r}; a non-boolean would be read as yes")
    return value


def _text(value, where):
    """A non-empty single-line string.

    Newlines are refused: a correction body containing "\n3:00 Bonus" emits a
    line-leading timestamp, which YouTube reads as a real chapter and the
    checker passes clean - silently inventing a chapter out of an erratum."""
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{where} must be a non-empty string")
    if "\n" in value or "\r" in value:
        raise ValueError(f"{where} must be a single line; it contains a newline, "
                         f"which can inject a chapter line into the description")
    return value


def _stamp(value, where):
    if not isinstance(value, str) or not STAMP.match(value.strip()):
        raise ValueError(f"{where}: {value!r} is not a timestamp like 0:00, "
                         f"6:43 or 1:02:03")
    return value.strip()


def section(title, lines):
    return [title] + lines + [""] if lines else []


def build(spec):
    out = []
    summary = (spec.get("summary") or "").strip()
    if not summary:
        raise ValueError("summary is required: it is the search snippet")
    _text(summary, "summary")
    out += [summary, ""]

    ch = spec.get("chapters") or []
    if ch:
        for i, c in enumerate(ch):
            for key in ("t", "label"):
                if key not in c:
                    raise ValueError(f"chapters[{i}]: missing {key!r}")
            _stamp(c["t"], f"chapters[{i}].t")
            _text(c["label"], f"chapters[{i}].label")
        out += section("CHAPTERS", [f"{c['t']} {c['label']}" for c in ch])

    corr = spec.get("corrections") or []
    if corr:
        lines, verbatim_any, derived_any = [], False, False
        for i, c in enumerate(corr):
            for key in ("t", "text"):
                if key not in c:
                    raise ValueError(f"corrections[{i}]: missing {key!r}")
            _stamp(c["t"], f"corrections[{i}].t")
            _text(c["text"], f"corrections[{i}].text")
            if "verbatim" in c:
                _flag(c["verbatim"], f"corrections[{i}].verbatim")
            # "at 6:43" rather than a line-leading "6:43": YouTube reads a
            # chapter timestamp at the start of a line, so a correction written
            # that way is parsed as a broken chapter list and the description
            # can never pass the checker.
            mark = "[speaker]" if c.get("verbatim") is True else "[derived]"
            lines.append(f"  {mark} at {c['t']} - {c['text']}")
            verbatim_any |= c.get("verbatim") is True
            derived_any |= c.get("verbatim") is not True
        note = []
        if verbatim_any:
            note.append("[speaker] items reproduce the speaker's own wording "
                        "verbatim.")
        if derived_any:
            note.append("[derived] items were produced automatically and are "
                        "not the speaker's words.")
        out += section("CORRECTIONS", lines + ([" ".join(note)] if note else []))

    refs = spec.get("references") or []
    if not isinstance(refs, list):
        raise ValueError("references must be a list")
    for i, r in enumerate(refs):
        if not isinstance(r, dict):
            raise ValueError(f"references[{i}] is not an object")
        flag = r.get("verified", False)  # noqa: E501
        # Exactly True. A bare truthiness test published the citation for
        # "verified": "no" / "pending" / "false", which is the one guarantee
        # this section exists to make.
        _flag(flag, f"references[{i}].verified")
        if "cite" in r:
            _text(r["cite"], f"references[{i}].cite")
    kept = [r for r in refs if r.get("verified") is True]
    dropped = len(refs) - len(kept)
    if kept:
        lines = []
        for r in kept:
            if "cite" not in r:
                raise ValueError(f"references[{refs.index(r)}]: missing 'cite'")
            line = f"  {r['cite']}"
            if r.get("url"):
                line += f" - {r['url']}"
            lines.append(line)
        out += section("REFERENCES", lines)

    series = spec.get("series") or {}
    nav = []
    for key, label in (("previous", "Previous"), ("next", "Next"),
                       ("playlist", "Full playlist")):
        item = series.get(key)
        if item:
            for k in ("title", "url"):
                if k not in item:
                    raise ValueError(f"series.{key}: missing {k!r}")
            nav.append(f"  {label}: {item['title']} - {item['url']}")
    out += section("THIS SERIES", nav)

    rel = spec.get("related") or []
    if rel:
        for i, r in enumerate(rel):
            for k in ("title", "url"):
                if k not in r:
                    raise ValueError(f"related[{i}]: missing {k!r}")
        out += section("RELATED", [f"  {r['title']} - {r['url']}" for r in rel])

    prov = spec.get("provenance") or {}
    if prov:
        lines = [RULE, "ABOUT THIS UPLOAD"]
        if prov.get("reuploaded") and not prov.get("original_published"):
            lines.append(f"Re-uploaded {prov['reuploaded']}.")
        if prov.get("original_published"):
            lines.append(f"Originally published {prov['original_published']}."
                         + (f" Re-uploaded {prov['reuploaded']}."
                            if prov.get("reuploaded") else ""))
        if prov.get("reason"):
            lines += ["", prov["reason"]]
        if prov.get("original_url"):
            state = prov.get("original_state")
            # No punctuation immediately after a URL: it is ambiguous to a
            # reader and the description checker flags it as malformed.
            lines += ["", (f"The original upload{' remains ' + state + ' and' if state else ''}"
                           f" is at {prov['original_url']}")]
        out += lines + [""]

    att = spec.get("attribution") or {}
    if att:
        who = att.get("model", "an automated tool")
        lines = [RULE, "HOW THIS DESCRIPTION WAS MADE",
                 f"Parts of this description were assembled automatically by {who}"
                 + (f", at {att['author']}'s request" if att.get("author") else "")
                 + "."]
        if att.get("automated"):
            lines.append(att["automated"])
        if att.get("tools_url"):
            lines.append(f"Tools: {att['tools_url']}")
        out += lines

    text = "\n".join(out).rstrip() + "\n"
    return text, dropped


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--spec", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    spec = json.load(open(a.spec, encoding="utf8"))
    try:
        text, dropped = build(spec)
    except ValueError as exc:
        sys.exit(str(exc))
    open(a.out, "w", encoding="utf8").write(text)
    print(f"wrote {a.out}: {len(text)} chars")
    if dropped:
        print(f"{dropped} unverified reference(s) omitted; verify them or leave "
              f"them out")
    print("now run check-description.py against this file before publishing")


if __name__ == "__main__":
    main()
