---
name: pd-fact-check
description: Adversarially verify every factual claim in an NSF proposal — results, counts, dates, publication statuses, attributions, literature scope, and theorem pinpoints — against the PI's repositories, data, databases and the cited papers, before the PI is asked anything. Writes findings with evidence to the proposal folder and updates REVIEW.md. Use for "fact-check the proposal", "is this true", "check the citations", "check the dates", or before showing a section to the PI.
---

# pd-fact-check

Assume each claim is overstated until a file, a fresh count, or the cited
paper shows otherwise. Report problems, not confirmations, except where a
confirmation settles an open question.

## What to check, and against what

| Claim type | Evidence |
|---|---|
| A mathematical result of the PI | the proof in the source file; who wrote it (commit author, agent markers); whether it imports theorems and within their hypotheses |
| A computed fact or count | recount from the data (ignore OS metadata files); give the command |
| A publication status | referee reports and responses in the repo; journal or arXiv records; never "submitted" or "under revision" without a record |
| Dates relative to the award period | arXiv versions, received/accepted/online dates |
| Literature scope ("X proved Y for Z") | the paper's main theorems and hypotheses; check weight, level, field, and whether it is conditional |
| A theorem number | the published version; note when only a preprint was available and how numbering differs |
| Novelty ("first", "no one has") | a search for prior constructions and computations; name what must be cited and distinguished |
| Databases (e.g. LMFDB labels, signs, counts) | a live query |

## Procedure

1. Extract claims section by section; batch independent checks into
   parallel subagents when the scope is broad (literature; repository
   results; numbers and statuses). Give each a narrow brief and require
   evidence (file and line, or theorem pinpoint) and a corrected sentence.
2. Write each report to the proposal folder's fact-check directory.
3. Update `REVIEW.md`: one row per claim or number with status
   (`verified-in-file`, `computed`, `conditional`, `contradicted`, `held`,
   `PI-verified` only when the PI says so).
4. Apply corrections only when the walk or the PI has authorized edits;
   otherwise hold them in `REVIEW.md` for the revision pass.

## Rules

- Verify before asking. Bring the PI only what evidence cannot settle.
- A paper that could not be opened is cited without a theorem number and
  listed as unverified; never guess a pinpoint.
- Agent review is not PI verification; never record it as such.
- A second independent pass on the final draft is cheap and catches the
  overstatements the rewrite introduced; offer it before submission.
