---
name: create-nsf-grant
description: Create a complete NSF research proposal folder (project summary, 15-page project description, references, data management plan, facilities, budget justification, REVIEW.md) from the PI's research repositories in ~/repos and the PI's instructions, following Grants/GRANT-STYLE.md and Grants/GRANT-FORMAT.md, then run check-grant-style and check-grant-format. Use when asked to "write an NSF proposal", "draft the grant", "create-nsf-grant", "new ANT proposal", or to rebuild a proposal from the template.
---

# create-nsf-grant

Produces one proposal folder under `Grants/` from the template, the
research repositories, and the PI's decisions. Human-driven: the PI
chooses the program, title, headline, projects, collaborators and
budget shape (see `Grants/CONTEXT.md`, `Grants/docs/adr/`); this skill
assembles and drafts, holds unverified claims out of the text, and
checks the result.

## Inputs (ask only for what the decision record lacks)

- Program and target date; title; one-line headline (agreed with the PI
  and recorded as an ADR; see `pd-overview`).
- Project list with, for each: repos, role (prior support / proposed),
  collaborators to name, collaborators not to name.
- Broader-impact items (each must already exist: repo + license + size,
  channel + count, textbook + URL).
- Budget shape (default: the 2024 award shape, see
  `NSF-three-year-template/proposal/tex/budget-justification.tex`).
- Reviewer list (optional).

## Procedure

1. **Scaffold from the call.** Run `template-proposal` with the
   solicitation: it reads the call and the PAPPG chapter in effect,
   writes `CALL.md` (documents, headings, limits, dates, language to
   quote) and instantiates the template set into
   `Grants/NSF-<year>-<program>-<topic>`. Do not copy an old proposal
   folder as the scaffold; the call's requirements, not last cycle's,
   go in the template headers. Fill `README.md`; claim the beads task.
2. **Inventory.** For each project, dispatch one `Explore` agent per repo
   cluster with the brief: section headings; every established statement
   in plain words with file:line; proved / sketch / computational /
   conjectured; who produced it (human or agent) and whether the PI
   verified it; open questions; collaborators; status and dates. Save
   the reports under `<folder>/inventory/`.
3. **Triage into REVIEW.md** before writing prose: §1 results the draft
   will state (published, submitted-with-statement-intact, or
   PI-verified); §2 agent-produced results held out; §3 every number
   with its as-of date and source. Overclaims found in the repos (e.g.,
   a survey asserting a theorem whose proof a referee rejected) go in
   §2 with a note; the draft never repeats them (S8).
4. **Draft `description.tex`** by routing each section through
   `using-pdpowers` (`pd-overview`, `pd-background`, `pd-ai-statement`,
   `pd-prior-support`, one `pd-project` per project, `pd-method`,
   `pd-broader-impacts`, with `pd-data-table` for evidence tables). Page
   limits and required headings come from `CALL.md`, not from memory.
   No URLs (F8). Collaborators named only as the PI directed.
5. **Draft the rest.** `summary.tex` last, from the finished description
   (`pd-overview`); the other documents through `using-grantpowers`
   (`gp-references`, `gp-data-management`, `gp-facilities`,
   `gp-budget-justification`, `gp-mentoring-plan` when a student or postdoc
   is budgeted); `submission-docs/reviewers.txt`.
6. **Build.** `./build.sh`; fix build errors.
7. **Check.** Run `check_pd_policy.py`, `check-grant-style`, then
   `check-grant-format`. Fix FAILs; rebuild; rerun until clean. Record the
   outputs in `README.md` with the date.
8. **Hand to the PI.** Run `pd-fact-check`, then `gp-potential-reviewers`,
   `pd-review-as` from every listed perspective and `pd-apply-feedback`; only
   then `pd-section-walk`, `grill-with-docs` for decisions, apply, recheck.
9. **Pair proposal.** If a sibling proposal targets the same panel, run
   the S14 overlap check against it.

## Not this skill's job

SciENcv biosketch and CPS, the COA spreadsheet, the budget, Research.gov,
UVMClick and SPA's internal route belong to `using-grantpowers` and its
`gp-*` leaves; this skill lists them in `README.md` with dates and marks
them CONFIRM.
