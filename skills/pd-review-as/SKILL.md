---
name: pd-review-as
description: Review an NSF Project Description from one named reviewer perspective — a role (birational geometer, model theorist, analytic number theorist, commutative algebraist, computational number theorist, Lean/formalization person, program officer) or a concrete person with known interests — anticipating the questions that reviewer would ask and listing where the draft fails to answer them. Use for "review as a model theorist", "read this as Pillay would", "reviewer-perspective pass", "anticipate the panel's questions", "what would an analytic number theorist ask", or when create-nsf-grant or using-pdpowers reaches the pre-walk review. Dispatchable as parallel subagents, one per perspective.
---

# pd-review-as

The PI's instruction, baked in: go over the entire proposal with the mindset
of a reviewer, anticipate their questions, and answer them preemptively. The
panel is several people from several fields; one pass per perspective. The
goal is to write the panel summary for them: every question a reviewer would
raise is answered in the text before it is asked.

Read-only on the proposal. Output goes to `<folder>/reviews/`; edits are
`pd-apply-feedback`'s job.

## Inputs

- `proposal/tex/description.tex` (and `summary.tex`), `REVIEW.md`, `CALL.md`.
- One perspective: a role from the list in the description, or a named
  person. Named perspectives come from `submission-docs/reviewers.txt` and
  `submission-docs/potential-reviewers.md` (`gp-potential-reviewers`).
- For a named person: their research interests from their recent papers
  (`search-scholar`, `search-arxiv`), never from memory alone. Record what
  was read.

## Procedure

1. **Adopt the perspective.** Write three lines at the top of the output:
   who the reviewer is, what they know well, what they will not know. A
   model theorist knows differential fields and definability, not Magma
   packages; a program officer reads the Summary, Prior Support, Broader
   Impacts and the budget-shaped sentences first; a commutative algebraist
   asks for the ring and the ideal; a Lean person asks what "formalized"
   means and what gets checked.
2. **Read in panel order** (Summary, Overview, Prior Support, each project,
   Broader Impacts). At each paragraph ask: what would this reviewer want
   to know here, and does the text say it? Typical questions: why should I
   care about this object; is this hard or is it a one-shot for a model;
   what exactly will exist afterwards; who else has done this and how is it
   different; where is the definition; what is the date and status; does
   the PI's record support this; what does "scientifically justified rather
   than incidental" look like here; will my own work be cited fairly?
3. **Check fairness** (PD-POLICY P14): every senior person whose problems or
   results the draft uses is named and cited; nothing reads as a slight to
   a likely panelist. List omissions.
4. **Write the table** to `reviews/review-as-<slug>.md` (slug: role or
   surname, lowercase), dated, with columns:

   | location | question the reviewer would ask | what the draft says | proposed fix | severity |

   Location is `description.tex:LINE` or a `\label`. Severity: `blocking`
   (a reviewer would score down), `major`, `minor`. "What the draft says" is
   a quote or "nothing". Proposed fix is one sentence of prose to add or
   change, in third person, policy-conformant (no run-in labels, no steps).
   End with a five-line summary the panel summary would contain if nothing
   changed, and the three questions this reviewer would ask in panel.
5. **Hand off.** Report the file path and the count by severity. Do not
   edit the proposal.

## Parallel dispatch

The caller runs one subagent per perspective with this skill, the same
inputs and a distinct slug; perspectives are the seven roles plus every name
in `potential-reviewers.md` marked "likely panelist". `pd-apply-feedback`
merges the tables; conflicts between perspectives are resolved there, PI
comments winning.

## Red flags

| Thought | Reality |
|---|---|
| "The draft explains this already" | Quote the line; if it needs the PI's context to read, it is not explained. |
| "A reviewer would never ask that" | The panel has a program officer and someone outside the field; they ask it. |
| "Fix it while I am here" | Read-only; the fix goes in the table for `pd-apply-feedback`. |
| "I know what this person works on" | Read two recent abstracts first; record them. |
| "One combined review is faster" | One perspective per pass; a merged voice asks nobody's questions. |
