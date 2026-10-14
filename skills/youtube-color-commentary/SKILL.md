---
name: youtube-color-commentary
description: >-
  Burn attributed commentary notes into a lecture or screencast video without
  covering what is written on screen. Use when re-uploading or re-cutting a
  recording and you want added explanation, corrections, or asides to be
  permanent, legible, and clearly marked as machine-added.
---

# Color commentary burned into a video

These are on-screen annotations in the old YouTube sense, written by the agent
and burned into the frame. The medium is text; “commentary”, “notes”, “glosses”
and “annotations” all mean that here, and an instruction about them that
mentions recording does not call for audio.

Adds two kinds of on-screen note to a recording: **clarification** of what the
speaker meant (`gloss`), and **asides** about the material (`aside`). Notes are
composited into the frame, so they survive re-encoding, embedding, and any
platform change that drops an overlay layer. That permanence is the point and
also the risk: a burned-in note cannot be edited later without re-rendering and
re-uploading.

Use this when a recording says less than it shows - the speaker points and says
"this one, this one", or writes a definition without naming it.

## Dependencies

`ffmpeg` and `ffprobe` on PATH, Python 3.10+, and Pillow. `latex` and
`dvipng` typeset the note bodies; without them `panel()` falls back to Pillow
and renders LaTeX as its own source. **Pillow must have
FreeType**: text is laid out at a chosen pixel size, and Pillow's non-scalable
fallback font has no size attribute. Without it `scripts/notes.py` raises
`NoFontError` telling you to install a TrueType font or set `COMMENTARY_FONT`.
If FreeType is present but none of DejaVu, Liberation or Arial is, Pillow's
bundled face is used (Pillow 10.1+ for a sized fallback), which has a narrower
character set.
Compositing images instead of using ffmpeg's `drawtext` moves the FreeType
dependency from ffmpeg to Pillow; it does not remove it.

## Three rules

**Attribution on every panel.** Each carries who added it, when, and on whose
instruction. `--author` and `--model` are required; `panel()` raises without
them. Never imply the speaker wrote these.

**Short, then long enough to read.** A panel is read at a glance over moving
video, so it is a handful of words - ten or fifteen, not a paragraph.
`reading_seconds` is `units/rate + 0.8`, clamped to **[4.5, 14] seconds** at
2.6 units/sec, where a maths span is charged by its symbols, not as one word.
`validate()` refuses a note over 35 units. Detail that will not fit goes to
`correct-youtube-description`, which owns pinpointed references and errata - but
a citation is not deferrable detail: a correction with its source moved offscreen
is an unsourced assertion burned into the frame. Keep the pointer in the panel.

**Never over the content** - to a stated budget. A position is accepted when
the content under it is **no more than 0.1% of the panel's area, and never
more than 12 mask pixels**. The absolute cap is what matters: a dilated mark is
at least 25 mask pixels, and 0.1% of a large 4K panel is around 90, so the
fraction alone would hide three real marks under a panel and still report the
note placed.

## Finding a spot that is genuinely empty

Ink is selected in **HSV as dark AND desaturated**. On a lit page filmed over a
wooden desk that separates three classes without tuning a grey threshold:

```
desk / table   S high, V low    dark but strongly coloured
paper / board  S low,  V high   bright
pen stroke     S low,  V low    dark and neutral
```

It is a heuristic about *that* setup, not a law. **A neutral grey or black
desk, letterbox bars and deep shadow are also dark and desaturated**, so they
read as content - safe, but they can leave nowhere to place anything. Hands are
excluded on both counts - skin is bright *and* sits well above the saturation
threshold - so a hand in shadow is still unlikely to read as content. No test
covers a hand; this is reasoning about the thresholds, not a measurement.

Three further properties, each load-bearing:

- **Union over the whole window.** A page is written progressively; a spot
  blank when a note appears can be covered before it leaves.
- **Panels already on screen are not free space.** Placement that considers
  only video ink puts every note in the first clear corner, so two notes whose
  windows overlap stack and the second hides the first - with both reported
  placed. Overlapping panels are passed as blocked rectangles.
- **Shrink before dropping.** Widths 0.42, 0.34, 0.28, 0.23 of frame width are
  tried in order. Height does **not** move in one direction. On the typeset
  path the glyph size is fixed (264 dpi, about 44px) and independent of panel
  width, so narrowing only adds lines and the panel grows taller each rung; on
  the Pillow fallback font size follows width, which can shrink both
  dimensions. Either way the narrowest rung is not the shortest panel, which is
  why the whole ladder is retried rather than one rung. Illustrative heights,
  pre-typeset renderer, 40-word note:

  ```
  1280 wide   175  200  250  291   taller each rung
  1920 wide   246  216  191  216   shorter, then taller
  3840 wide   501  409  334  271   shorter each rung
  ```

  Font size is derived from panel width with a floor, so narrowing can shrink
  the panel in both dimensions rather than growing it. **These numbers are
  illustrative only**: they move with the note's wording and with the length of
  the author and model labels in the footer. Measure your own case before
  tuning the ladder. There is no truncation rung.

## Why dropped notes name a reason

A note dropped because ffmpeg could not decode a frame and a note dropped
because the page is full need different fixes, so the reason is **established,
not assumed**. When placement fails and other panels were on screen, the **whole width
ladder** is retried with them ignored; only if some rung then succeeds are they
blamed. Retrying a single rung under-detects, because the narrowest rung is not
the shortest panel. A board
that is simply full fails identically either way, and saying otherwise would
send you to re-time notes when the fix is a different timestamp.

Reasons: `could not read the picture`, `no clear space in the picture`, `the
only clear space was under a panel already on screen`, and a window squeezed by
the end of the video. A timestamp past the end is rejected by validation up
front.

## Writing the notes

ASCII only - `panel()` refuses the rest and names the offending characters; a
common sans face has no `U+208A`, so Unicode subscripts render as tofu. Maths
in the body is typeset through `scripts/mathrender.py` when a TeX is present,
so write it as the source does (`$B \cap \Sing(Y)$`) and it renders as maths
rather than as its own markup. A note that does not compile raises.

**No private identifiers.** A panel ships with the video and its reader has only
the video. A source filename (`notes.tex`) and an internal label (`prop:key`,
`thm:wild`) name nothing a viewer can reach, whatever the source's status, and
they publish the source tree's structure along with the note; `validate()`
refuses both shapes and names the index. Cite what the reader can follow - a
published theorem, a Stacks tag, an arXiv number, a page - and otherwise state
the result by what it says. Never write a citation from memory: verify it or
state the result plainly. What is on screen, and the title and authors of a
forthcoming paper, are followable; a label is not. The notes file and the
description are published too.

**The attribution panel.** Every video opens with one `aside` reading
`Comments added by the flavor bot: <model>, <harness>`, naming the model and
harness that wrote them. Each panel also carries its own footer; the opening
aside is what a viewer who reads one panel sees. Use the same wording on every
part of a series, so the series reads as one thing.

Content that earns its place: naming an object the speaker only gestures at;
stating which of two readings is meant; confirming something the speaker hedged
on when it is in fact correct; a dry aside, sparingly. Past roughly one note
per thirty seconds a viewer stops reading them.

## Procedure

1. Obtain a timed transcript; decide where the recording is underspecified.
2. Write `notes.json`: `{"notes": [{"kind", "at", "text"}, ...]}`, `at` in
   seconds. Malformed entries, and notes carrying a private identifier, are
   rejected with a message naming the index - before anything is encoded.
3. From the skill directory:
   `scripts/burn-notes.py --video IN --notes notes.json --out OUT
   --author NAME --model LABEL [--vf transpose=2] [--rate 2.6]`
   Output geometry is **always measured** by decoding one frame, with or
   without `--vf`. That matters even with no filter: a phone recording tagged
   `rotation:90` has a coded size that is not what ffmpeg composites, and
   trusting it put a panel over the whole page. `transpose=2,transpose=2`,
   `rotate=` and `scale=` are all handled. Add `--vf transpose=...` only for a
   recording that is sideways *without* a rotation tag - one that already has
   the tag is corrected on decode, and a filter would turn it twice.
4. Read the report. Exit status is nonzero if any note was dropped.
5. **Extract a frame at the MIDPOINT of each note's window and look at it.**
   A template command for the first note is printed at the end of a successful
   run; repeat it per note. Do not skip this: a panel sitting on a definition
   renders and plays perfectly.
6. Tests: `python3 tests/test_notes.py` (placement and layout) and
`python3 tests/test_burn_notes.py` (the CLI: geometry, validation, drop
reasons; needs ffmpeg).

## Cost and limitations

- Placement costs `--samples` (default 6) ffmpeg invocations per note, plus a
  pure-Python integral image per width attempt. Budget minutes before encoding
  starts. Output is a full re-encode (libx264 CRF 18, AAC 192k).
- Tuned for dark strokes on a light surface. Light-on-dark needs the thresholds
  inverted; they are parameters of `ink_mask`, not exposed on the CLI.
- Placement is measured on sampled frames, not every frame. Raise `--samples`
  where the picture changes quickly.
- The run aborts if `ffprobe` cannot read the source duration, because both the
  past-the-end check and the truncation guard depend on it.
- The render is compared with the source duration and discarded if it differs
  in either direction; the previous output is left untouched. A failed ffmpeg
  run can leave an `OUT.mp4.partial.mp4` behind.
- A note whose window would be squeezed under the 4.5s minimum by the end of
  the video is dropped rather than shown too briefly.
- Panel images are written to a temporary directory that is removed on exit.
- Burned-in text is permanent. Decide the wording before rendering, and show
  the note list to whoever is accountable for the video before encoding: a
  table of every panel, per video, is cheap; a re-render is not.
- Render to a new path. Never overwrite a source, an assembly, or a previous
  render: an annotation pass is not reversible from its output, and the take it
  was built from is the only copy of what was said.
