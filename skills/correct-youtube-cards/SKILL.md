---
name: correct-youtube-cards
description: >-
  Work out what every end screen on a YouTube channel should point at, from the
  numbered series in its playlists, and flag proposed targets whose URL has
  changed. Use when auditing a series, after re-uploading a video, or whenever
  a video's URL changes.
---

# Make the end cards point somewhere sensible

An end screen should send a viewer to the next thing to watch: the next video
in the **same series**, and at the end of a run, the playlist.

**End screens and cards are absent from the YouTube Data API** - it has no
resource for them (the Annotations API was retired in 2017 with no
replacement), so they cannot be read or written programmatically. This writes a
worksheet; a person applies it in Studio. The script imports no networking and
touches no channel.

## Series, not playlist order

The target is the next member of the same run, found by the text before the
number in the title. Chaining playlist *neighbours* is wrong whenever a
playlist holds more than one run - a course plus one-offs, or two sub-series
interleaved - and sends "Course part 1" to "Other part 1".

Numbers are detected from three patterns and **only** these: `- 12.1 -`,
`part 03`, `pt. 4`. `Lecture 3`, `Episode 7`, `(3/8)` and `#4` are invisible.

Two shapes are deliberately refused, because both invented runs:

- **Dates.** `Seminar 2026-05-03: Motives` would read as series "seminar 2026",
  episode 5, collapsing a year of talks into one run chained month to month and
  raising a fault that does not exist. Rejected when the text before the number
  ends in a year, or when the number itself is year-like.
- **A series name under three characters** (`AG - 3 - sheaves`). But a title
  that *leads* with its number is fine: `Part 1 - Introduction` keys on the
  text after the number.

A video in no detected run is given the **next playlist entry** instead, marked
`(adjacent)` in the worksheet. That is a guess from adjacency, not a series.

## Faults reported, before you build any cards

Fix these first; cards built on a broken order teach a broken order.

- **Duplicate entries** - the same video listed twice. Remove the entry, not
  the video.
- **A run out of order** - part 4 before parts 1 and 2. Ordering is judged
  within a run only, so two correctly-ordered runs interleaved are not a fault.
- **Unreadable membership rows** - reported with a count. A dropped row removes
  a video from a chain silently, so reconcile the count against your export.

Not detected: duplicate episode *numbers* and gaps in a run.

## The outputs

1. **Set these end screens** - **one row per video**, which is the table to
   work through. A video usually sits in several playlists, and a per-playlist
   view hands you contradictory instructions for the same video. There is one
   end screen per video, so there is one row. Precedence: a target from the
   video's own numbered run beats one from adjacency; between two runs, the
   smaller playlist wins as the more specific.
2. **Videos whose playlists disagree** - where that precedence had to choose.
   Check these by hand.
3. **Proposed targets whose URL changed** - note the wording: the script cannot
   read existing cards (no API exposes them), so this says a *proposed* target
   has moved. It is a statement about your current cards only insofar as they
   already follow the series rule. The old id still resolves if the superseded
   copy was kept, so nothing errors and the viewer lands on the old version. A
   private or unlisted original cannot be chosen as an end-screen target at all.
4. **Sequences that do not make sense** - the faults above.
5. **Entries outside the known set** - someone else's video, or one deleted.

Unreadable membership rows are counted **in the worksheet**, not only on the
terminal, because the worksheet outlives the terminal.

## Procedure

1. Export playlist membership with positions (`playlistItems.list`, paging
   through each playlist) as
   `[{"playlist_id","playlist_title","position","video_id"}]`, and a
   `{"<id>": "<title>"}` map. Check the row count against your export.
2. `scripts/plan-cards.py --memberships M.json --titles T.json --out CARDS.md`,
   adding `--replaced ids.txt` (one id per line) when URLs have changed and
   `--id-map old-new.psv` (`old|new`) once replacements exist. `--id-map`
   without `--replaced` is refused, because stale-target detection is gated on
   the replaced set and would silently report none; an id map that parses to
   nothing is also refused, rather than leaving every target "pending".
3. Fix the faulted playlists, regenerate, then work through it in Studio.

Tests: `python3 tests/test_plan_cards.py`.

## Limitations

- Title-based series detection only; see the closed pattern list above.
- One end screen per video, which is why output 1 is per video rather than per
  playlist. Mid-video cards need a human.
- It cannot check whether a target is public or still exists without an API
  call. Playlists with fewer than two entries produce no table.
- Titles are truncated in the worksheet, so two videos sharing a long prefix
  can look alike.
