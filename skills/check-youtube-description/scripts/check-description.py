#!/usr/bin/env python3
"""Check a description against YouTube's limits and against trust rules.

    check-description.py --file DESC.txt [--known-ids IDS.txt] [--duration S]
                         [--require-attribution] [--allow-pending]

Exit 0 clean, 1 on a description failure, 2 on an input error (missing or
unreadable file), so a typo'd path is distinguishable from a bad description.

Sources for the platform rules, checked 2026-09-27:
  developers.google.com/youtube/v3/docs/videos            snippet.description
  developers.google.com/youtube/v3/docs/videos/update     invalidDescription
  support.google.com/youtube/answer/9884579               chapters
  support.google.com/youtube/answer/6390658               hashtags
"""
from __future__ import annotations

import argparse
import re
import sys
import unicodedata
import urllib.parse

MAX_BYTES = 5000
MAX_HASHTAGS = 60
# YouTube reads a chapter timestamp only at the start of a line, followed by a
# title. A timestamp elsewhere on the line does not make a chapter.
CHAPTER_LINE = re.compile(r"^[ \t]*((?:\d+:)?\d{1,2}:\d{2})[ \t]+(\S.*)$", re.M)
BARE_STAMP_LINE = re.compile(r"^[ \t]*((?:\d+:)?\d{1,2}:\d{2})[ \t]*$", re.M)
# A line that is ONLY "Label - 0:00": someone meant a chapter and put the
# timestamp last. Matching any timestamp anywhere flagged ordinary prose
# ("Recorded at 10:30 in Room 2") and flagged every erratum written "at 6:43 -
# ...", which made a corrections-only description impossible to pass.
LABEL_FIRST = re.compile(r"^[ \t]*(?!(?:\d+:)?\d{1,2}:\d{2})"
                         r"(\S[^\n]{0,48}?)[ \t]*[-\u2013:][ \t]*"
                         r"((?:\d+:)?\d{1,2}:\d{2})[ \t]*$", re.M)
LINK = re.compile(r"https?://[^\s<>\)\]]+")
PENDING = re.compile(r"PENDING\s+VERIFICATION|TODO|TBD|\[cite\]", re.I)
YT_ID = re.compile(r"(?:youtu\.be/|youtube\.com/(?:shorts/|live/|embed/))"
                   r"([A-Za-z0-9_-]{11})"
                   r"|[?&]v=([A-Za-z0-9_-]{11})")
INVISIBLE = {"​", "‌", "‍", " ", "﻿",
             "‪", "‫", "‬", "‭", "‮"}


def to_seconds(stamp):
    parts = [int(p) for p in stamp.split(":")]
    while len(parts) < 3:
        parts.insert(0, 0)
    return parts[0] * 3600 + parts[1] * 60 + parts[2]


def normalise_link(url):
    """For duplicate detection: ignore scheme and a trailing slash."""
    p = urllib.parse.urlsplit(url)
    path = p.path.rstrip("/")
    return (p.netloc.lower(), path, p.query)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--file", required=True)
    ap.add_argument("--known-ids")
    ap.add_argument("--duration", type=float,
                    help="video length in seconds; enables the final-chapter "
                         "and past-the-end checks")
    ap.add_argument("--require-attribution", action="store_true")
    ap.add_argument("--allow-pending", action="store_true",
                    help="permit TODO/TBD, for a legitimate 'date: TBD'")
    ap.add_argument("--max-bytes", type=int, default=MAX_BYTES)
    a = ap.parse_args()

    try:
        text = open(a.file, encoding="utf8").read()
    except FileNotFoundError:
        print(f"INPUT ERROR: no such file: {a.file}", file=sys.stderr)
        return 2
    except UnicodeDecodeError as exc:
        print(f"INPUT ERROR: {a.file} is not valid UTF-8: {exc}", file=sys.stderr)
        return 2
    except OSError as exc:
        print(f"INPUT ERROR: cannot read {a.file}: {exc}", file=sys.stderr)
        return 2

    fails = []
    nbytes = len(text.encode("utf8"))
    # The documented limit is BYTES, not characters. Every non-ASCII character
    # in a mathematical description costs 2-3, so a 4980-character description
    # can be 5589 bytes and be rejected by an API call that a character count
    # said was fine.
    if nbytes > a.max_bytes:
        fails.append(f"too long: {nbytes} bytes ({len(text)} characters), "
                     f"limit {a.max_bytes} bytes")

    for ch in "<>":
        if ch in text:
            at = text.index(ch)
            fails.append(f"contains {ch!r} at offset {at}: the field forbids it and "
                         f"the update is rejected whole as invalidDescription "
                         f"({text[max(0, at - 30):at + 30]!r}). For an inequality "
                         f"write 'greater than' or use the Unicode forms.")
    ctrl = {c for c in text
            if unicodedata.category(c) == "Cc" and c not in "\n\r\t"}
    if ctrl:
        fails.append(f"control characters: {sorted(hex(ord(c)) for c in ctrl)}")
    invis = {c for c in text if c in INVISIBLE}
    if invis:
        fails.append(f"invisible or bidirectional characters: "
                     f"{sorted(hex(ord(c)) for c in invis)}")

    chapters = [(to_seconds(m.group(1)), m.group(2)) for m in CHAPTER_LINE.finditer(text)]
    bare = BARE_STAMP_LINE.findall(text)
    label_first = [m.group(2) for m in LABEL_FIRST.finditer(text)]
    if bare:
        fails.append(f"{len(bare)} timestamp line(s) with no title "
                     f"(first {bare[0]}): a chapter needs a title after the time")
    if chapters:
        times = [t for t, _ in chapters]
        if times[0] != 0:
            fails.append("chapters: first timestamp is not 0:00, so chapters do "
                         "not activate (the conditions fail as a group)")
        if len(times) < 3:
            fails.append(f"chapters: {len(times)} timestamps, at least 3 required")
        if times != sorted(times):
            fails.append("chapters: timestamps are not in ascending order")
        short = [(times[i], times[i + 1]) for i in range(len(times) - 1)
                 if times[i + 1] - times[i] < 10]
        if short:
            fails.append(f"chapters: {len(short)} chapter(s) shorter than 10s, "
                         f"first at {short[0][0]}s")
        if a.duration:
            if times[-1] >= a.duration:
                fails.append(f"chapters: last timestamp {times[-1]}s is at or past "
                             f"the end of the video ({a.duration:.0f}s)")
            elif a.duration - times[-1] < 10:
                fails.append(f"chapters: the final chapter is "
                             f"{a.duration - times[-1]:.0f}s, under the 10s minimum")
    if label_first:
        # Reported whether or not a chapter block exists: a stray "Intro - 0:00"
        # among good chapters is exactly as broken as one on its own.
        fails.append(f"{len(label_first)} line(s) put the timestamp after the "
                     f"label (first {label_first[0]}); a chapter timestamp is "
                     f"read at the START of a line, so these create no chapters")

    # Counts hashtags in the DESCRIPTION only; the platform rule counts those
    # in the title too, so this can undercount.
    tags = re.findall(r"(?:^|\s)#\w+", text)
    if len(tags) > MAX_HASHTAGS:
        fails.append(f"{len(tags)} hashtags, over the {MAX_HASHTAGS} limit: every "
                     f"hashtag is then ignored, and over-tagging risks removal")

    if not a.allow_pending:
        for m in PENDING.finditer(text):
            fails.append(f"unverified-citation marker {m.group(0)!r} would be "
                         f"published; omit the reference, or pass --allow-pending "
                         f"if this is legitimate prose")

    links = LINK.findall(text)
    seen = {}
    for link in links:
        if link.endswith((".", ",", ";")):
            fails.append(f"link ends with punctuation, likely malformed: {link}")
        parts = urllib.parse.urlsplit(link)
        if not parts.netloc or "." not in parts.netloc or " " in link:
            fails.append(f"malformed link: {link}")
            continue
        key = normalise_link(link)
        if key in seen and seen[key] != link:
            fails.append(f"link duplicated in a different form: {link} and {seen[key]}")
        elif key in seen:
            fails.append(f"duplicate link: {link}")
        seen[key] = link

    if a.known_ids:
        try:
            known = {l.strip() for l in open(a.known_ids, encoding="utf8") if l.strip()}
        except OSError as exc:
            print(f"INPUT ERROR: {exc}", file=sys.stderr)
            return 2
        found = {g for m in YT_ID.finditer(text) for g in m.groups() if g}
        for vid in sorted(found - known):
            fails.append(f"references video {vid}, which is not in the known set")

    if a.require_attribution:
        low = text.lower()
        if not any(w in low for w in ("automat", "generated", "machine")):
            fails.append("no statement that this description was generated "
                         "automatically, but --require-attribution was given")

    print(f"{nbytes} bytes ({len(text)} chars), {len(links)} links, "
          f"{len(chapters)} chapter lines, {len(tags)} hashtags")
    for f in fails:
        print(f"FAIL: {f}")
    print("clean" if not fails else f"{len(fails)} failure(s)")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
