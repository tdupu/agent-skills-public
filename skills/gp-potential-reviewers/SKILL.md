---
name: gp-potential-reviewers
description: Compile the list of people likely to review or sit on the panel for an NSF ANT (Algebra and Number Theory) proposal — the PI's suggested reviewers, recent ANT awardees from the nsf.gov award search (program element 1264, last two years), authors the proposal cites heavily, and senior people in the subfield — minus the proposal's COA conflicts, written to submission-docs/potential-reviewers.md. Use for "who will review this", "list potential reviewers", "who won ANT last year", "target the panel", or before pd-review-as runs its perspective passes. Never guesses emails; never contacts anyone.
---

# gp-potential-reviewers

Produces the perspective list for `pd-review-as` and the fairness list for
PD-POLICY P14 (every senior person whose work the draft uses is named and
cited). It is a reading aid, not a submission document: NSF receives only
`reviewers.txt`. No one on the list is contacted.

## Inputs

- The proposal folder: `proposal/tex/description.tex`, `references.bib`,
  `submission-docs/reviewers.txt`, `submission-docs/COA.xlsx`.
- The program element (ANT is `1264`) and the two most recent fiscal years.

## Procedure

1. **PI's suggested reviewers.** Read `reviewers.txt`; every name goes in,
   marked `suggested`.
2. **Recent awardees.** Query the NSF award search (`nsf.gov/awardsearch`,
   advanced search, program element code 1264, start date within the last
   two fiscal years; the export is CSV). Record PI name, institution, title,
   award number, year. Take all; mark `awardee`. Record the query date and
   the count. If the site cannot be reached, say so and leave the section
   marked `not run`; do not fill it from memory.
3. **Heavily cited authors.** From `references.bib` and the `\cite` counts
   in `description.tex`, list authors cited twice or more or whose theorem
   a project rests on; mark `cited`. Program officers for ANT (from the
   program page, dated) go in marked `program officer`.
4. **Senior people in the subfield.** From the cited authors' coauthor
   networks and the PI's own knowledge of the field, the people whose
   problems the proposal attacks or whose results it uses (for differential
   algebra: the model theorists of differential fields, the Galois-theory
   and D-module people, the computational differential algebra people).
   Mark `senior`. For each, one line on which part of the draft touches
   their work; this is the P14 fairness check input.
5. **Exclude conflicts.** Open `COA.xlsx` read-only (`gp-coa` describes the
   tables): remove anyone in Table 2 (collaborators) or Table 4 (advisors
   and advisees), and anyone at the PI's institution; keep them in a
   separate "conflicted, excluded" list so the exclusion is visible.
6. **Write `submission-docs/potential-reviewers.md`**, dated:

   | name | institution | subfield | source | why they matter to this draft | likely panelist? |

   `source` is one of `suggested`, `awardee <year>`, `cited (n)`, `senior`,
   `program officer`. "Likely panelist" is `yes` for suggested reviewers,
   last year's awardees in the same subfield, and senior people the draft
   leans on; `pd-review-as` runs one pass per `yes`. Then the conflicted
   list, then the queries run with dates and counts.
7. **Report** counts per source and the `yes` list. Do not edit
   `reviewers.txt`; the PI chooses suggested reviewers.

## Red flags

| Thought | Reality |
|---|---|
| "I remember who won ANT in 2025" | Run the award search; record date and count. |
| "Their address is probably name at their institution" | No emails; names and institutions only. |
| "Add them to reviewers.txt too" | The PI chooses suggested reviewers (`gp-researchgov`). |
| "A collaborator would review it fairly" | COA Table 2 and 4 names are excluded, always. |
| "Draft a note to ask if they would review" | No contact of any kind. |
