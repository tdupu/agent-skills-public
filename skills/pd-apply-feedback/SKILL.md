---
name: pd-apply-feedback
description: Apply a comment log to an NSF Project Description — the PI's verbatim comments in COMMENTS.md (from pd-section-walk) and/or the reviewer-perspective tables in reviews/review-as-*.md (from pd-review-as) — grouping by section, resolving conflicts with the PI's comment winning, editing the tex, marking every comment applied or deferred with the line changed, rebuilding, and rerunning check_pd_policy.py, check-grant-style and check-grant-format. Use for "apply the comments", "apply the feedback", "work through COMMENTS.md", "fold in the reviews", "apply the corrections from the review-as passes". Never silently drops a comment.
---

# pd-apply-feedback

Turns a comment log into edits and a receipt. Every comment ends `applied`
(with the lines changed) or `deferred` (with the reason and who decides);
no third state. Edits follow `using-pdpowers/references/PD-POLICY.md` and
the `pd-*` leaf for the section being changed; this skill does not write
new sections, it corrects existing ones.

## Inputs

- `COMMENTS.md`: `| id | line | section | PI comment (verbatim) | status |`.
- `reviews/review-as-*.md`: `| location | question | what the draft says |
  proposed fix | severity |`, one file per perspective.
- `REVIEW.md` (what may be claimed), `CALL.md` (limits).

## Procedure

1. **Collect.** Read every open row of `COMMENTS.md` and every row of each
   `review-as` table. Give review rows ids `R<slug>-<n>`. Nothing is
   skipped for being unclear; an unclear comment is `deferred: needs PI`
   with the question written out.
2. **Group by section**, in document order, using the `section` column and
   the `location` lines (re-resolve line numbers against the current tex;
   lines move).
3. **Resolve conflicts** inside each group before editing: a PI comment
   wins over any review row; among review rows, `blocking` over `major`
   over `minor`; two review rows that ask for opposite things are both
   `deferred: conflict` with one line stating the choice for the PI.
   Comments that ask for a claim `REVIEW.md` does not support are
   `deferred: unverified` and sent to `pd-fact-check`, never applied.
4. **Edit**, one group at a time, through the leaf for that section
   (`pd-overview`, `pd-background`, `pd-project`, `pd-method`,
   `pd-prior-support`, `pd-broader-impacts`). Each edit: third person, no
   run-in labels, no step lists, definitions in `definition`, conjectures in
   `conjecture`, items labelled and referenced by `\eqref` (P1–P13). A
   comment such as "cite" or "give the grant number" is applied with the
   exact key or number from `references.bib` or `REVIEW.md`, or deferred.
   Remove the `\taylor{}` marker a comment came from only when the comment
   is applied.
5. **Mark.** Update `COMMENTS.md` status to `applied (L<from>→L<to>)` or
   `deferred: <reason>`; append the review rows and their statuses in a
   new table under the review's file name. Dates on every status.
6. **Rebuild and recheck.** `./build.sh`; then
   `check_pd_policy.py proposal/tex/description.tex`, `check-grant-style`,
   `check-grant-format`. A new FAIL introduced by an edit is fixed before
   reporting. Page limit from `CALL.md`, not memory.
7. **Report**: counts applied/deferred per source; the deferred list with
   reasons; the three checker summaries; what the PI must decide. Never
   commit or push unless asked.

## Red flags

| Thought | Reality |
|---|---|
| "This comment is vague, skip it" | `deferred: needs PI`, with the question written out. |
| "The reviewer and the PI disagree; split the difference" | The PI's comment wins; record the review row as deferred. |
| "I applied it in spirit" | Record the exact lines changed or it is not applied. |
| "Remove all the \taylor markers, the draft is cleaner" | A marker leaves with its applied comment, not before. |
| "Add a step list, the reviewer asked for a plan" | A plan is prose or sub-subsections (P5). |
| "The check failed on something unrelated to my edit" | Report it; fix only what the comments and the new FAILs cover. |
