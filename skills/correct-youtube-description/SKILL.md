---
name: correct-youtube-description
description: >-
  Assemble a complete YouTube description - summary, chapters, errata, pinpoint
  references, series navigation, related material, re-upload provenance and
  attribution - and apply it. Use when publishing, re-uploading, or repairing a
  talk or lecture video's description.
---

# Build the description the video deserves

Most descriptions on a technical channel are one sentence written years ago.
The description is the only place a viewer can be handed a citation they can
follow, told that a claim at 6:43 was wrong, or pointed at the next video.

Draft, **check with `check-youtube-description`**, then apply. The failures
here are quiet: the API rejects an update over one character, and chapters that
look fine may simply never appear.

## The spec file

`build-description.py` reads one JSON object. Full schema in its docstring
(`scripts/build-description.py --help`); the shape is:

```
summary      required, one sentence
chapters     [{"t": "0:00", "label": "Intro"}]
corrections  [{"t": "6:43", "text": "...", "verbatim": true}]
references   [{"cite": "...", "url": "...", "verified": true}]
series       {"previous"|"next"|"playlist": {"title": "...", "url": "..."}}
related      [{"title": "...", "url": "..."}]
provenance   {"original_published", "reuploaded", "reason",
              "original_url", "original_state"}
attribution  {"model", "author", "automated", "tools_url"}
```

Top-level keys are optional except `summary`. Within an entry, `chapters`,
`corrections`, `references`, `series` and `related` have required keys and a
missing one raises a named error naming the index. **`provenance` and
`attribution` sub-keys, and `references[].url`, are all optional** and are
quietly defaulted or omitted - a typo in one of those is not caught.

Values are validated, not just presence: `t` must parse as `0:00`, `6:43` or
`1:02:03`; `verbatim` and `verified` must be boolean (a string such as `"no"`
is refused, because it is truthy and would read as yes); and no free-text field
may contain a newline, since a correction body holding `\n3:00 Bonus` would
inject a line-leading timestamp that YouTube reads as a real chapter.

## The order, and why

1. **Summary.** The first ~157 characters are the search snippet. Nothing
   measures this; it is your responsibility.
2. **Chapters.** Subject to all the chapter rules at once.
3. **Corrections**, each tagged `[speaker]` (the speaker's own wording,
   reproduced verbatim) or `[derived]` (produced automatically, not their
   words). The tag is per line, because a blanket footnote leaves a reader
   unable to tell which is which.
   Written as `at 6:43 - ...`, **not** as a line-leading timestamp: YouTube
   reads a chapter timestamp at the start of a line, so the obvious formatting
   turns every erratum into a broken chapter and the description can never pass
   the checker.
4. **References, pinpointed.** A tag number, a theorem number, a paper with a
   section. `verified` must be boolean `true`; a string such as `"no"` or
   `"pending"` is refused rather than silently published.
5. **Series navigation.** Previous, next, then the playlist.
6. **Related material.** Avoid repeating the playlist URL from (5); the checker
   flags duplicate links.
7. **Provenance** for a re-upload: when the original went up, why it was
   replaced, where it is now and in what state. A re-upload loses its
   publication date and view count.
8. **Attribution** when any of this was assembled automatically.

## What not to do

- Do not fence blocks with anything containing `<` or `>`.
- Do not write a citation from memory. Verify it or omit it.
- Do not claim corrections were restored on a video that never had any.
- Do not let an automated description pass as the author's own writing.

## Procedure

1. Gather the material and write `spec.json` in the shape above.
2. `scripts/build-description.py --spec spec.json --out DESC.txt`
3. `../check-youtube-description/scripts/check-description.py --file DESC.txt
   [--duration S]`, adding `--require-attribution` **only if** the spec carries
   an `attribution` block. Fix and repeat until the exit status is 0. A
   description with corrections and no chapters passes: corrections are written
   `at 6:43 - ...` precisely so they are not read as a chapter list.
4. Apply by **read-modify-write**: `videos.list(part="snippet")`, change
   `description` on the object you get back, send that object to
   `videos.update`. Do not hand-build a snippet: update overwrites the mutable
   properties of the parts you name, so a body carrying only four fields clears
   others such as `defaultLanguage`, and omitting the required `title` or
   `categoryId` errors outright.

Tests: `python3 tests/test_build_description.py` (includes an end-to-end pass
through the checker with corrections and chapters together).

## Limitations

- It composes; it does not research. Verified references must arrive verified.
- It cannot backdate a video, and **do not try with `status.publishAt`**. The
  YouTube Data API reference states: *"If your request schedules a video to be
  published at some time in the past, the video will be published right away.
  As such, the effect of setting the status.publishAt property to a past date
  and time is the same as of changing the video's privacyStatus from private to
  public."* So a backdating attempt does not fail - it publishes a private
  video immediately. `snippet.publishedAt` is not listed among the writable
  properties, which is why it cannot be set, though the reference does not
  label it read-only in so many words. The provenance line is the only remedy.
  (developers.google.com/youtube/v3/docs/videos, checked 2026-09-27.)
- Applying needs a client with write scope, which also permits deletion.
