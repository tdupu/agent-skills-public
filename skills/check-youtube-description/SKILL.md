---
name: check-youtube-description
description: >-
  Check a proposed YouTube video description against the API's hard limits and
  against rules that keep it trustworthy, before it is uploaded. Use after
  drafting or generating a description and before publishing it.
---

# Check a description before it ships

A description is rejected, silently truncated, or quietly ineffective for
reasons that are easy to miss while composing it. This checks those and fails
loudly, so the problem is caught locally rather than by an API error or by a
reader.

Run it on the exact bytes that will be uploaded. Note that most editors append
a trailing newline, which counts.

Exit status: `0` clean, `1` a description failure, `2` an input error (missing,
unreadable, a directory, or not UTF-8), so a bad path is distinguishable from a
bad description.

## The hard limits

| Rule | Why |
|---|---|
| **5000 bytes** | Not characters. Every `—`, `≅`, `ℚ`, `ε` costs 2-3 bytes, so a 4980-character description can be 5589 bytes and be refused |
| No `<` or `>` | The field forbids them and the update is rejected whole as `invalidDescription`; the message names no character. For an inequality, write it out or use a Unicode form |
| No control or invisible characters | Zero-width spaces, non-breaking spaces, BOM and bidi overrides survive the round trip and are invisible while they break things |
| At most 60 hashtags | Past that every hashtag on the video is ignored, and over-tagging risks removal. The platform counts the title's hashtags too; this sees only the description, so it can undercount |

Sources, checked 2026-09-27: `developers.google.com/youtube/v3/docs/videos`
(description: 5000 bytes, no `<` or `>`),
`.../videos/update` (`invalidDescription`),
`support.google.com/youtube/answer/9884579` (chapters),
`support.google.com/youtube/answer/6390658` (hashtags). That `<` specifically
triggers `invalidDescription` is an inference joining the field spec to the
error list; the docs do not say so in one place.

## Chapters, if present

Chapters activate only if **all** of these hold, and fail as a group otherwise:

1. the first timestamp is `0:00` (the docs write `00:00`),
2. at least three timestamps, in ascending order,
3. every chapter is at least ten seconds, including the last,
4. each timestamp has a title, on the same line.

Conditions 1-3 are stated verbatim in the support article. **Condition 4 and
the rule that a timestamp is read only at the start of a line are inference**:
the article says to add "a list of timestamps and titles" and is silent on
layout. They are enforced here because the observed convention is
timestamp-first, but treat them as less certain than 1-3.

A line whose timestamp comes *after* its label, such as `Intro - 0:00`, is
reported - whether or not a chapter block is also present. Ordinary prose
containing a clock time is not: the rule only fires on a line that is a label
and a timestamp and nothing else.

The final chapter and a timestamp past the end of the video can only be checked
if you pass `--duration SECONDS`. Without it, both go unchecked.

## The trust rules

Not platform rules - what keeps a description honest.

- **Unverified-citation markers** (`PENDING VERIFICATION`, `TODO`, `TBD`,
  `[cite]`) are refused. This catches text that self-incriminates; it cannot detect an
  unverified citation that simply looks confident. `--allow-pending` permits
  legitimate prose like "next date: TBD".
- **Links** are parsed, and duplicates are detected after normalising scheme
  and trailing slash. A link ending in punctuation is flagged as malformed.
- **Attribution**: `--require-attribution` fails unless the text says it was
  generated automatically. It is a keyword match, so it confirms a statement
  exists, not that the statement is accurate.
- **Referenced videos** must be in `--known-ids` when that is supplied; without
  it the rule is inert. the `youtu.be`, `watch?v=`, `shorts`, `live` and
  `embed` URL forms are recognised.

## Procedure

1. Write the description to a file, exactly as it will be uploaded.
2. `scripts/check-description.py --file DESC.txt [--duration S]
   [--known-ids IDS.txt] [--require-attribution] [--allow-pending]
   [--max-bytes N]` - paths are relative to this skill directory.
3. Fix what it reports and re-run until the exit status is 0.
4. `correct-youtube-description` is the *builder* that produces the file and
   then calls this checker; it is not a downstream step. Use it to assemble the
   description in the first place.

Tests: `python3 tests/test_check_description.py`.

## Limitations

- It checks link *form*, not whether a link resolves. That needs a network call
  the caller should make deliberately.
- It cannot judge whether a citation is correct, only whether the text admits
  to being unverified.
- Platform rules change. The sources above are dated; re-check them.
