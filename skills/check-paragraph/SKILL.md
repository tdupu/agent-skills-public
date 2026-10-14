---
name: check-paragraph
description: Judge ONE paragraph of prose (LaTeX allowed) as its stated reader and return a fixed six-line verdict — topic sentence, one idea, reader can follow, claim strength, machine tells, keep/rewrite/split/delete. Use for "check this paragraph", "is this paragraph good", "run check-paragraph over the manuscript"; dispatch one independent subagent per paragraph. Read-only; never edits.
---

# check-paragraph

**Input.** One paragraph, plus one line of context: the section it sits in and
who the reader is (e.g. "Background; NSF panelist outside differential algebra").

**Rules.** Judge the paragraph alone, as the stated reader, with no other text
in view. No edits, no praise, no restating the paragraph. Flag every sentence
whose deletion loses no fact. Quote; do not paraphrase. If the context line is
missing, assume "a competent non-specialist" and say so in line 3.

**Output** — exactly these six lines, then at most two sentences of guidance:

```
topic-sentence: yes/no ("<first sentence, quoted>")
one-idea: yes/no (<extra ideas, named>)
reader-can-follow: yes/no (<first term or reference the reader would not know>)
claim-strength: ok/over/under ("<quoted phrase>")
machine-tells: none / <list: hedging stacks, "importantly", triplets, summary tail, ...>
verdict: keep / rewrite / split / delete
```

Guidance names what the rewrite must do (new first sentence, where to split,
what to cut); it never supplies the rewritten prose.

## Parallel dispatch

To check a whole file, the caller runs
`python3 scripts/split_paragraphs.py <file.tex>`, which prints one JSON line
per paragraph `{n, line_start, line_end, section, text}` with comments and
`\taylor{...}` notes removed, the preamble skipped, and environment bodies
(`itemize`, `figure`, theorem-like) attached to the preceding paragraph.
The caller then runs one independent subagent per paragraph (or per batch of
five, each paragraph answered with its own six-line block) with this skill
and the context line built from `section` plus the reader, and collects the
results into `<folder>/reviews/paragraphs-<file>-<date>.md` as a table with
columns: paragraph #, first words, verdict, guidance. The caller does not
edit the source; the table is for the author.
