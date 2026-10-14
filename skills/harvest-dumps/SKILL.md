---
name: harvest-dumps
description: Turn selected frontier dumps or related research files into a coherent, reviewed mathematical presentation through using-latexpowers. Use when asked to harvest dumps or selected topics into notes.tex or another specified manuscript.
---

# Harvest selected dumps

Carry the user's selected research through context gathering, an audience-aware
prototype, filling, and reviewed integration. Default to `notes.tex`; honor an
explicit destination. An outline-only or other bounded request stops at its
requested stage.

## Select the harvest

Accept files, directories, globs, dump packages, topics, particular results, or
sections within files. The selection may be the whole corpus. Resolve selectors
to exact paths and sections; for a topic, inspect the indicated corpus and name
the proposed subset. Ask only when ambiguity materially changes scope. Do not
silently harvest adjacent material or treat an empty match as the whole corpus.
If no corpus is identified by the request or active context, ask where to look.

## Frontier-dump manuscript front matter

When the request explicitly identifies the selected corpus as a frontier dump,
or selects a file or directory inside a dated dump package containing the
frontier-dump package's `report.md`, `ai-usage.md`, and `tokens.md`, carry this
front-matter contract into the shared `using-latexpowers` workflow whenever it
creates a new manuscript or prepares bounded new-manuscript front matter. If
the request explicitly calls the output a frontier-dump manuscript, that
classification controls even when ordinary supporting material is included;
an ordinary corpus with no such identification remains outside this contract.

- Use the exact title form `FRONTIER DUMP FOR <user> on <YYYY-MM-DD> on
  <topic>`, with the user's name, the manuscript's creation date in the
  user's local timezone, and a concise topic.
- Attach a title footnote using the document class's supported mechanism. It
  must link to [mathcity](https://github.com/tdupu/mathcity), then to the
  [`using-latexpowers` skill](https://github.com/tdupu/mathcity/blob/main/subdomains/latex/skills/using-latexpowers/SKILL.md),
  and then to the active repository's master `ai/ai-usage.md` statement for
  the generation details. Resolve the reader-facing URL from the active
  repository's declared remote, including the exact repository URL when it is
  private, and record any access limitation in the provenance record; never
  insert another repository's ledger URL or an unresolvable relative link.
- Apply this only when creating a new manuscript from frontier dumps or
  preparing its bounded front matter. Do not retitle an existing manuscript,
  an ordinary research-file harvest, a revision, or a bounded insertion into
  an existing manuscript unless the user explicitly requests it.

The front matter is part of the requested artifact, so verify its title and
three provenance destinations before the manuscript leaves the synthesis
workflow.

Pass the selection, exclusions, topic or target result, audience/background,
intended depth, destination, and requested stopping stage to the shared workflow
for its existing plan/spec. Infer reasonable unspecified audience/depth and state those
assumptions. Preserve originals and source locators; summaries do not substitute
for reading the selected evidence, including corrections and negative results.

## Execute the shared workflow

Read and invoke `using-latexpowers` with that request, reusing any active
`math-workflow`. Its selected-file synthesis sequence owns contract resolution,
context gathering via `create-exposition`, the combined outline/skeleton via
`rapid-prototype`, filling via `fill-in-prototype`, and integration. Run the
sequence, not merely a referral or list of suggested next skills.

Resolve the destination before writing: `notes.tex` is the fallback, not license
to bypass repository manuscript declarations. Preserve existing text and use
the shared contract-adoption gate for missing or conflicting declarations.

Use the sequence's separate `fp-finder-latex` reviews for the prototype, filled
presentation, and integrated manuscript; acceptance does not transfer between
stages. It also governs theorem-first planning with prerequisite backfill,
focused follow-up research for gaps, dependency-aware ordering, writer hygiene,
provenance/accounting, and reruns without duplicate insertion. Research gaps
remain explicit; do not turn a desired theorem into an established result.

These named skills and the `math-workflow` synthesis reference are required
dependencies, resolved through the available skill installation. If that route
is missing or lacks selected-file synthesis, report the missing capability;
do not substitute browser-chat priming or invent a parallel workflow.

Report what was harvested and excluded, the destination, stages actually
completed, review/build status, and unresolved obligations. Do not call source-
only review final manuscript acceptance.

Examples:

- “Harvest the descent topic from `dumps/session-*.md` for a first-year graduate
  reader.” Default destination: `notes.tex`.
- “Harvest only Proposition 3 and its supporting material from `dumps/run-a/`
  into `chapters/descent.tex`; start from the full target statement and backfill.”
