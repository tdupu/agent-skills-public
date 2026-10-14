---
name: assemble-recording-series
description: >-
  Assemble one lecture or talk video from a folder of raw takes, whatever the
  capture tool wrote - flat screen-capture files, or per-session folders with
  the video and a separate mixed audio track. Use when a recording session
  produced several takes that need selecting, ordering, trimming and joining
  before anything else is done to them.
---

# Assemble a series of takes into one video

A recording session leaves a pile of takes: false starts, a take that was
abandoned, two attempts at the same segment, and the good ones. This selects
and joins them. It does **not** add commentary, captions or titles - run
`youtube-color-commentary` on the assembled file afterwards, once the examples
are in their final order and the timestamps are stable.

## Two capture layouts

| Layout | Shape | Audio |
|---|---|---|
| Flat | `NN_topic_take-N.mov` beside each other | in the video file |
| Session folders | `Default_<date>_<n>_<time>/` per take | a separate mixed `.wav` alongside the video |

The session layout is what field recorders and multitrack capture apps write.
Its separate mix is usually the better audio - it is the board mix rather than
whatever the camera picked up - so the manifest can name an audio file per take
and it will be used in place of the embedded track.

Discovery only lists candidates. **Which takes are used, in what order, and
where they are cut is a human decision recorded in a manifest**, never inferred
from filenames: "take-2" is not reliably better than "take-1", and a long take
is not reliably the good one.

## The manifest

`manifest.json`:

```json
{
  "output": "assembled/lecture.mp4",
  "takes": [
    {"video": "rec/Default_1/Default_1.mp4",
     "audio": "rec/Default_1/Audio/Live-Mix.wav",
     "label": "squaring map on P^1",
     "start": 12.0, "end": 880.5},
    {"video": "rec/Default_2/Default_2.mp4", "label": "second example"}
  ],
  "excluded": [
    {"video": "rec/Default_0/Default_0.mp4", "why": "test recording, 6 seconds"}
  ]
}
```

`start`/`end` are seconds and both optional. `excluded` is not used by the
build; it exists so the reason a take was dropped survives in the repository
rather than in someone's memory.

## What the build does

1. Normalises every take to one encode (same resolution, frame rate, pixel
   format, audio layout). Takes from one session usually already match, but
   concatenating mismatched streams produces a file that plays wrongly from the
   join onwards rather than failing.
2. Applies each take's trim.
3. Concatenates, and **checks the result against the sum of the trimmed
   inputs**. A silently short concatenation is the characteristic failure here,
   and it looks fine until someone watches the end.
4. Writes `<output>.manifest.md` beside the video: every take, its source, its
   trim, its duration and its start offset in the finished file. Those offsets
   are what the commentary step needs, so it is produced automatically rather
   than reconstructed later.

## Procedure

1. `scripts/discover-takes.py --root DIR` to list candidates with durations.
2. Watch them. Write `manifest.json`.
3. `scripts/assemble.py --manifest manifest.json` (add `--dry-run` first).
4. Check the reported duration and the offsets in the generated manifest.
4b. Only if the recording wants it: `scripts/trim-dead-air.py --video IN --out
   OUT --map OUT.map.json --min-silence N` (no default; see above), then
   `scripts/remap-times.py --map OUT.map.json --notes n.json --out n2.json` to
   move any existing cue times onto the cut timeline. `--map` is optional but
   required for that, so always pass it.
5. Then, and only then, `youtube-color-commentary`.

## A series, not one video

Lecture material usually arrives as a run of recordings that becomes several
published parts, and the parts have to read as one thing. What makes that work
is cheap and worth doing at assembly time, while the structure is in front of
you:

- **Split on take joins, not on the clock.** A part boundary that falls inside
  a take cuts an argument in half; the joins are already where the speaker
  stopped and restarted. If the author has a slide deck or notes per part, the
  blocks usually land on those joins, and that mapping is worth checking before
  choosing split points.
- **A short title card on each part**, same design throughout, carrying the
  series name, `N / total`, the part's own title, the authors (alphabetical
  unless told otherwise), and where the links live. Match the recording's own
  palette so the cut into the footage is not a flash.
- **The same opening note on every part**, so a viewer landing in the middle
  learns the same things a viewer of part one did.
- **Each part's description carries the whole series list**, so the parts
  cross-link without depending on cards or playlists.

Prepending a card shifts every chapter timestamp in that part's description by
the length of the card. Generate the chapters after the card is attached, not
before.

## Dead air, and why the default will ruin a lecture

`scripts/trim-dead-air.py` cuts a gap only when it is both silent and visually
static. That is meant to keep pauses spent writing - but the still check
compares two downscaled frames, so a pause where the pen barely moves reads as
static and is cut. On one lecture it kept 78 of 630 gaps as "writing" and
removed the rest; most of those were the speaker thinking, not idle.

**`--min-silence` is the main lever, and it has no default** - the script
refuses to run until you choose, because the value depends entirely on the
recording. `--still-threshold`, `--noise` and `--keep` also change what is cut. A lecturer pauses for
about that long between phrases, constantly, while writing - so at the default
the tool removes the speaker's own rhythm and the result sounds clipped and
rushed. Measured on one 102-minute lecture: 1.2s cut 552 gaps, 5.4 per minute,
and of the 17 minutes it removed only about 2 were genuine dead air. At 4s it
cut 32 gaps, one every three minutes. The speaker's verdict on 1.2s was that
the rhythm of the speech was destroyed; on the untrimmed version, that it was
the best of the three.

So read the **cuts per minute of source**, not the minutes removed. Minutes
removed is the number that looks like success and grows as the damage grows.
Past roughly one cut per minute of source you are editing the delivery.

For a lecture recorded at a board, the honest default is **not to trim at all**:
that is what the speaker chose here after hearing 1.2s, 4s and untrimmed. Trim
the head and tail if they are dead, and leave the middle alone.

And listen to a sample before committing the encode. Cut a few minutes at the
proposed setting and at the original, and compare - it costs minutes against
hours, and it is the only check that catches this. A trim that reports well and
sounds wrong is the characteristic failure here; nothing in the log will say so.

`scripts/remap-times.py` moves annotation timestamps from the untrimmed video
onto the trimmed one. Any cut invalidates every later cue, so run it after any
trim and before burning.

## Limitations

- Requires `ffmpeg` and `ffprobe`; `trim-dead-air.py` also needs Pillow, which
  it imports lazily - a missing Pillow fails only after the full silence scan.
- Re-encodes. Joining without re-encoding is faster but only safe when every
  take shares an encode exactly, and that is not checkable from the container
  alone.
- Trims are cut on the nearest frame, not sample-accurate on audio.
- It does not detect duplicate takes of the same content, remove filler, or
  choose between two attempts. Those need someone who watched them.
