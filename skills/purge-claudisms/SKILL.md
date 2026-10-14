---
name: purge-claudisms
description: Remove machine tells ("claudisms") from a .tex or .md draft — stock LLM vocabulary (delve, pivotal, robust, leverage), importance frames ("it is worth noting", "the point is", "this is exactly the failure mode"), negative parallelism ("not X but Y"), triads, semicolon and colon chains, em-dash splices, run-in labels, summary tails. Scans against a dated, monthly-maintained list, then rewrites each hit in place preserving meaning, then rescans to zero. Use when asked to "purge claudisms", "this sounds like AI", "de-slop", "too many claudeisms", "remove AI tells", "humanize this", or before check-grant-style / referee-report on an agent-drafted file.
---

# purge-claudisms

A claudism is a word, frame, or shape that an LLM reaches for by default and
a careful human author would not: it announces, hedges, triples, or praises
instead of stating the fact. The list is `references/claudisms.md` (dated
rows, four types: lexical, syntactic, structural, rhetorical; a separate
section for mathematical writing). This skill is the list, a mechanical scan,
and rewrite rules. It does not judge style (`check-style`,
`check-grant-style` S9), register (`PD-POLICY` P1/P4/P5/P12), or AI
disclosure (`latex-ai-statement` AI18); it runs before them.

## Procedure

1. Scan. From the skill directory:

   ```bash
   python3 scripts/scan_claudisms.py <file.tex|file.md> [more files]
   ```

   One row per hit: `file:line  id  FAIL|WARN/type  "match"  pattern  -> replacement`,
   then counts by type and the top 20 patterns (`--top N`, `--quiet` for the
   summary only). Exit 1 while any lexical or structural hit remains; syntactic
   and rhetorical hits are WARN. Comments, `\taylor{}` markers, `\cite`/`\ref`/
   `\label`/`\url` arguments, verbatim and bibliography blocks, Markdown fences
   and `.bib` files are skipped. Paragraph-level checks (em-dash density,
   semicolon triads, `X, Y, and Z` triads, colon chains, one-sentence
   punchline paragraphs, parenthetical density, transition chains, restatement
   chains) report the paragraph's first line. `X, Y, and Z` triads are WARN:
   a real triad stays; judge each. In the table a literal backslash in a regex
   is written `\x5c` (the publisher's path scanner reads `\\emph` as a UNC path).

2. Rewrite every hit in place, preserving the mathematics and the claim. The
   rules, in order of preference:
   - Say the fact. Delete the frame sentence or clause ("it is worth noting
     that", "the point is", "the reason to care is", "crucially") and keep
     what it framed.
   - Replace a contrast frame with the positive claim: "not X but Y", "it's
     not just X, it's Y", "Y rather than X", "the correct statement is Y" all
     become "Y", unless X was asserted earlier in the text and is being
     corrected, in which case name where.
   - Break triads to the number of items the content has; "A; B; C" becomes
     separate sentences or two clauses; a colon chain becomes one colon or
     none.
   - Replace a stock word with the specific word (the table's replacement
     column), or cut it when the sentence loses nothing. "Comprehensive",
     "robust", "ensures" become the scope, the thing withstood, the check.
   - Fold a run-in `\emph{Label.}` or `\textbf{Label.}` into its sentence or
     promote it to a `\subsubsection`; replace Step-N scaffolding with prose
     or a proof program with the real number of steps.
   - Delete a sentence whose only content is importance, summary, or a reveal
     ("The result? ...", "In short, ...", "X matters.").
   - One em dash per paragraph at most; otherwise a comma, period or
     parentheses. One restatement frame ("equivalently", "in other words")
     per paragraph.
   - Never introduce a new claim, a new hedge, or a synonym cycle while
     rewriting; never touch `\taylor{}` text or quoted sources.

3. Rescan until exit 0. Report remaining WARN rows with a one-line reason each
   (legitimate "rather than", a real triad, a quoted phrase). If a WARN row
   is a false positive that will recur, tighten its regex in the table rather
   than ignoring it, and note the date.

4. For a proposal, then run `check-grant-style` and `check_pd_policy.py`;
   for a manuscript, `check-style`. Those catch what this list does not.

## Maintenance (monthly)

On the first of each month, or when the PI names a new tell:

1. Search (WebSearch) for new entries: "AI writing tells", "signs of AI
   writing", "ChatGPT-isms", "Claude-isms", "LLM slop words", the Wikipedia
   page `Wikipedia:Signs_of_AI_writing` (its vocabulary list is versioned by
   model era), and new lexical-fingerprint papers (Kobak et al. 2025 is the
   anchor). Also grep the PI's recent `\taylor{}` comments and `COMMENTS.md`
   files for phrases the PI struck.
2. Append rows to the table with the next `C###` id, a regex when the pattern
   is mechanical, the source key, and that day's date in `added`. Add the
   source key to the Sources paragraph if new.
3. Never delete a row. To retire one, set `type` to `retired` and append
   `; retired YYYY-MM-DD` to `added`; the scanner skips retired rows.
4. Rerun the scan on one recent draft to confirm no regex error and no
   obvious new false positive; record the run date in the Sources paragraph
   (`read YYYY-MM-DD`).

## Boundaries

Read the hit, not the id: a flagged word inside a quotation, a title, or a
defined term stays. The scan is evidence for the rewrite, not the verdict;
the verdict is the rewritten sentence read aloud. Do not add the table's words
to `check-grant-style`'s banned list; point that skill here instead.
