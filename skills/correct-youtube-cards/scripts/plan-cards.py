#!/usr/bin/env python3
"""Plan end screens from playlist order, and report what is broken.

    plan-cards.py --memberships M.json --titles T.json --out CARDS.md
                  [--replaced ids.txt] [--id-map old-new.psv]

memberships.json: [{"playlist_id","playlist_title","position","video_id"}, ...]
titles.json:      {"<video_id>": "<title>", ...}

Cards and end screens are absent from the YouTube Data API, so this writes a
worksheet for a person to apply. Nothing here touches a channel.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict

PATTERNS = (r"[-–]\s*(\d+(?:\.\d+)*)\s*[-–]",
            r"\bpart\s*0*(\d+(?:\.\d+)*)",
            r"\bpt\.?\s*0*(\d+(?:\.\d+)*)")


YEARLIKE = range(1900, 2101)


def series_key_no(title):
    """(series name, episode number), or None if the title advertises none.

    The name matters as much as the number: a playlist often holds several
    numbered runs, and ordering on the bare number interleaves them.

    Two title shapes are deliberately rejected, both of which fabricated runs:

      * a date. "Seminar 2026-05-03: Motives" would otherwise read as series
        "seminar 2026", episode 5, collapsing a year of talks into one bogus
        run chained month to month. Rejected when the text before the number
        ends in a year, or when the number itself is year-like.
      * nothing before the number is not a reason to give up. "Part 1 -
        Introduction" has an empty prefix; the text AFTER the number is used
        instead, so leading-number series are visible.
    """
    if not isinstance(title, str):
        return None
    for pattern in PATTERNS:
        m = re.search(pattern, title, re.I)
        if not m:
            continue
        number = tuple(int(x) for x in m.group(1).split("."))
        if len(number) == 1 and number[0] in YEARLIKE:
            return None
        head = title[:m.start()]
        if re.search(r"\b\d{4}\s*$", head):
            return None
        key = re.sub(r"[^a-z0-9]+", " ", head.lower()).strip()
        if len(key) < 3:
            tail = re.sub(r"[^a-z0-9]+", " ", title[m.end():].lower()).strip()
            key = tail
        return (key, number) if len(key) >= 3 else None
    return None


def load_idmap(path):
    """old|new pairs, with a count of what could not be parsed.

    A file written with "->" instead of "|" parses to nothing, and a silent
    empty map makes every replaced target print "new id pending" - so the
    reader leaves the card on the dead id believing no replacement exists."""
    pairs, bad = {}, 0
    with open(path, encoding="utf8") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split("|")
            if len(parts) < 2 or not parts[1].strip():
                bad += 1
                continue
            pairs[parts[0].strip()] = parts[1].strip()
    return pairs, bad


def load_rows(path):
    """Returns (playlists, skipped). A dropped row silently removes a video
    from a card chain, so the count is returned and reported rather than
    swallowed."""
    with open(path, encoding="utf8") as fh:
        rows = json.load(fh)
    if not isinstance(rows, list):
        raise SystemExit(f"{path}: expected a LIST of membership rows, got "
                         f"{type(rows).__name__}")
    out, skipped = defaultdict(list), []
    for i, r in enumerate(rows):
        try:
            out[(r["playlist_id"], r["playlist_title"])].append(
                (int(r["position"]), r["video_id"]))
        except (KeyError, TypeError, ValueError) as exc:
            skipped.append(f"row {i}: {exc}")
    for key in out:
        out[key].sort()
    return out, skipped


def next_in_series(items, index, titles):
    """The next video of the same run, or None at the end of that run.

    Playlist order is NOT the answer: a playlist often holds several numbered
    runs, so the next entry can belong to a different series entirely. Chaining
    neighbours sent "Course part 1" to "Other part 1".
    """
    _pos, vid = items[index]
    key = series_key_no(titles.get(vid, ""))
    if key is None:
        return None
    best, best_no = None, None
    for j in range(len(items)):
        if j == index or items[j][1] == vid:
            continue
        other = series_key_no(titles.get(items[j][1], ""))
        if other is None or other[0] != key[0] or other[1] <= key[1]:
            continue
        if best_no is None or other[1] < best_no:
            best, best_no = j, other[1]
    return items[best][1] if best is not None else None


def anomalies(items, titles):
    """Per-series faults in one playlist: duplicates, and out-of-order runs."""
    order = [v for _p, v in items]
    seen, dupes = set(), []
    for v in order:
        if v in seen:
            dupes.append(v)
        seen.add(v)
    runs = defaultdict(list)
    for i, v in enumerate(order):
        k = series_key_no(titles.get(v, ""))
        if k:
            runs[k[0]].append((i, k[1], v))
    unordered = {}
    for key, members in runs.items():
        if len(members) < 2:
            continue
        nums = [n for _i, n, _v in members]
        if nums != sorted(nums):
            unordered[key] = members
    return sorted(set(dupes)), unordered


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--memberships", required=True)
    ap.add_argument("--titles", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--replaced", help="file of video ids whose URL changed")
    ap.add_argument("--id-map", help="old|new per line, once replacements exist")
    a = ap.parse_args()

    playlists, skipped = load_rows(a.memberships)
    titles = json.load(open(a.titles, encoding="utf8"))
    replaced = set()
    if a.replaced:
        replaced = {l.strip() for l in open(a.replaced, encoding="utf8") if l.strip()}
    idmap, idmap_bad = {}, 0
    if a.id_map and not a.replaced:
        sys.exit("--id-map does nothing without --replaced: stale-target "
                 "detection is gated on the replaced set. Pass both, or pass "
                 "--replaced alone.")
    if a.id_map:
        idmap, idmap_bad = load_idmap(a.id_map)
        if not idmap:
            sys.exit(f"{a.id_map}: no 'old|new' pairs parsed ({idmap_bad} "
                     f"unparsable line(s)). Without them every replaced target "
                     f"would print 'new id pending' and the card would be left "
                     f"on the dead id.")

    # One decision per video. A video usually sits in several playlists -- an
    # uploads playlist, a topic playlist, a year playlist -- and a per-playlist
    # table hands the operator several contradictory instructions for the same
    # video with no precedence. There is one end screen per video, so there is
    # one row per video here. Precedence: a target derived from the video's own
    # numbered run beats one derived from playlist adjacency; between two runs,
    # the smaller playlist wins as the more specific.
    cross = []
    proposals = defaultdict(list)
    for (pid, ptitle), items in playlists.items():
        if len(items) < 2:
            continue
        for i, (_pos, vid) in enumerate(items):
            nxt = next_in_series(items, i, titles)
            source = "series"
            if nxt is None:
                source = "neighbour"
                nxt = items[i + 1][1] if i + 1 < len(items) else None
                if nxt == vid:
                    nxt = None
            proposals[vid].append((source, nxt, pid, ptitle, len(items)))

    def rank(p):
        return (0 if p[0] == "series" else 1, p[4], p[3])

    out = ["# End screen and card worksheet", "",
           "Cards are Studio-only; the Data API cannot read or write them, and it",
           "cannot see what a card currently points at. This proposes what each",
           "end screen SHOULD point at.", "",
           "Rule: the next video in the same numbered run. Where a video is in no",
           "run, the next entry in the playlist is offered instead and is marked",
           "**(adjacent)** - that is a guess, not a series.", ""]
    if skipped:
        out += [f"**{len(skipped)} membership row(s) were unreadable and are "
                f"missing from everything below.** Reconcile the row count "
                f"against your export before using this.", ""]
        out += [f"- {s_}" for s_ in skipped[:5]] + [""]
    if idmap_bad:
        out += [f"**{idmap_bad} unparsable line(s) in the id map.**", ""]

    out += ["## Set these end screens", "",
            "One row per video. This is the table to work through.", "",
            "| video | end screen | from |", "|---|---|---|"]
    conflicts = []
    for vid in sorted(proposals, key=lambda v: titles.get(v, "")):
        cands = [p for p in proposals[vid] if p[1]]
        if not cands:
            continue
        cands.sort(key=rank)
        source, nxt, pid, ptitle, _n = cands[0]
        distinct = {c[1] for c in cands}
        if len(distinct) > 1:
            conflicts.append((vid, cands))
        mark = "" if source == "series" else " **(adjacent)**"
        tgt = f"`{nxt}` {titles.get(nxt, '(unknown)')[:34]}{mark}"
        if nxt in replaced:
            tgt += (f" **[URL CHANGED -> `{idmap[nxt]}`]**" if nxt in idmap
                    else " **[URL CHANGED - new id pending]**")
            if vid not in replaced:
                cross.append((vid, titles.get(vid, "(unknown)"), nxt, ptitle))
        out.append(f"| `{vid}` {titles.get(vid, '(unknown)')[:40]} | {tgt} | "
                   f"{ptitle[:24]} |")
    out.append("")

    out += ["## Videos whose playlists disagree", "",
            "Each appears in more than one playlist suggesting a different next",
            "video. The table above picked one by the precedence rule; check these",
            "by hand.", ""]
    if conflicts:
        for vid, cands in conflicts:
            out.append(f"- `{vid}` {titles.get(vid, '(unknown)')[:40]}")
            for source, nxt, _pid, ptitle, _n in cands:
                out.append(f"    - {ptitle[:30]}: `{nxt}` "
                           f"{titles.get(nxt, '(unknown)')[:30]} ({source})")
        out.append("")
    else:
        out += ["None.", ""]

    out += ["## Supporting detail, by playlist", ""]
    faults = []
    for (pid, ptitle), items in sorted(playlists.items(), key=lambda kv: kv[0][1].lower()):
        if len(items) < 2:
            continue
        dupes, unordered = anomalies(items, titles)
        if dupes or unordered:
            faults.append((ptitle, dupes, unordered, items))
        out += [f"## {ptitle}", "", f"`{pid}` - {len(items)} videos", "",
                "| # | video | end screen points at |", "|---|---|---|"]
        for i, (pos, vid) in enumerate(items):
            title = titles.get(vid, "(unknown)")[:44]
            nxt = next_in_series(items, i, titles)
            adjacent = ""
            if nxt is None:
                nxt = items[i + 1][1] if i + 1 < len(items) else None
                if nxt == vid:
                    nxt = None
                adjacent = " **(adjacent)**"
            if nxt:
                target = f"`{nxt}` {titles.get(nxt, '(unknown)')[:34]}"
                if nxt in replaced:
                    target += (f" **[URL CHANGED -> `{idmap[nxt]}`]**" if nxt in idmap
                               else " **[URL CHANGED - new id pending]**")
                    if vid not in replaced:
                        cross.append((vid, titles.get(vid, "(unknown)"), nxt, ptitle))
            else:
                target = f"playlist `{pid}` (end of run)"
            out.append(f"| {pos} | `{vid}` {title} | {target} |")
        out.append("")

    out += ["## Sequences that do not make sense", "",
            "Fix these before building cards: an end screen built from a wrong",
            "order sends the viewer backwards.", ""]
    if faults:
        for ptitle, dupes, unordered, items in faults:
            out += [f"### {ptitle}", ""]
            for v in dupes:
                out.append(f"- duplicate entry: `{v}` {titles.get(v, '(unknown)')[:44]}")
            for key, members in unordered.items():
                out.append(f"- run \"{key}\" is out of order:")
                for _i, num, v in members:
                    out.append(f"    - {'.'.join(str(x) for x in num)}"
                               f"  `{v}` {titles.get(v, '(unknown)')[:40]}")
            out.append("")
    else:
        out += ["None.", ""]

    out += ["## Cards pointing at a video whose URL changed", "",
            "The old id still resolves, so nothing errors - the viewer is sent to",
            "the superseded copy. Videos not themselves re-uploaded are the ones",
            "most likely to be missed.", ""]
    if cross:
        out += ["| video to edit | its card points at | series |", "|---|---|---|"]
        for vid, title, nxt, ptitle in sorted(set(cross)):
            new = idmap.get(nxt)
            out.append(f"| `{vid}` {title[:40]} | `{nxt}`"
                       f"{' -> `' + new + '`' if new else ' (pending)'} | {ptitle[:28]} |")
        out.append("")
    else:
        out += ["None.", ""]

    known = set(titles)
    foreign = sorted({v for items in playlists.values() for _p, v in items} - known)
    out += ["## Entries outside the known set", "",
            "Someone else's video, or one already deleted. Check before relying on",
            "a card that points at one.", ""]
    out += ([f"- `{v}`" for v in foreign] if foreign else ["None."]) + [""]

    open(a.out, "w", encoding="utf8").write("\n".join(out) + "\n")
    print(f"wrote {a.out}: {len(playlists)} playlists, {len(faults)} with faults, "
          f"{len(set(cross))} stale card targets, {len(foreign)} unknown entries")
    if skipped:
        print(f"WARNING: {len(skipped)} membership row(s) were unreadable and are "
              f"MISSING from every table:", file=sys.stderr)
        for s_ in skipped[:5]:
            print(f"  {s_}", file=sys.stderr)


if __name__ == "__main__":
    main()
