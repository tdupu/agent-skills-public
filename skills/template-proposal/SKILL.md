---
name: template-proposal
description: Instantiate a complete NSF proposal folder from a call for proposals. Reads the solicitation and the PAPPG chapter it defers to, records what the call requires (documents, headings, order, page limits, special language), and copies the template set (description, summary, references, data management, facilities, budget justification, mentoring, COA, reviewers, README, REVIEW, RESEARCHGOV, build.sh) into a new folder with the call's requirements written into each template's header. Use for "template the proposal", "set up the proposal folder for NSF xx-yyy", "what does this call require", or before create-nsf-grant drafts any prose.
---

# template-proposal

Input: a call for proposals (solicitation number or URL) and a title.
Output: a proposal folder whose templates already carry the call's
requirements, plus `CALL.md` recording where each requirement came from.
No prose is drafted here; that is `create-nsf-grant` and the `pd-*` leaves.

## Procedure

1. **Read the call, do not recall it.** Fetch the solicitation page
   (nsf.gov `.../nsf<NN>-<NNN>/solicitation`) and the program page it links.
   From Section V take the preparation instructions; from Section II the
   program description and any program-specific guidance; note the
   "Posted" and "Last updated" dates. Then read the PAPPG chapter it defers
   to (II.D.2 in PAPPG 24-1; "the version in effect on the due date") for
   the Project Description, Project Summary, References, Facilities,
   Budget Justification, DMSP, Mentoring, Biosketch/CPS and COA rules.
   Also read `references/nsf-26-520.md` for the last reading of the MPS
   consolidated solicitation and update it if the page changed.
2. **Write `CALL.md`** in the new folder: a table `requirement | value |
   source (section, date read)` covering: documents required; Project
   Description page limit and required headings; prior-support rules;
   Summary structure; DMSP, Facilities, Budget Justification, Mentoring
   limits; target or due date (write "none; accepted anytime" when the
   call says so); solicitation-specific language worth quoting (for
   NSF 26-520: the formal-mathematics/AI paragraph and the six "measures
   of success"); review criteria; contacts.
3. **Instantiate.** Copy `templates/` into
   `<workspace>/NSF-<year>-<program>-<topic>/proposal/tex/` dropping the
   `_template` suffix (`description_template.tex` → `description.tex`,
   …); the COA xlsx (see `templates/COA_template.md`) goes to `proposal/submission-docs/`; the folder
   files (`README.md`, `REVIEW.md`, `RESEARCHGOV.md`, `build.sh`,
   `reviewers.txt`) to their places in the layout below. Replace every
   `<<...>>` token with the call's value from `CALL.md`; leave none behind.
   Delete `mentoring.tex` only if no student or postdoc will be budgeted.
4. **Check** the instantiated set: `grep -rn '<<' proposal/` is empty;
   `./build.sh` runs on the empty templates; the format checker's
   headings (summary: Overview, Intellectual Merit, Broader Impacts;
   description: Results from Prior NSF Support, Broader Impacts) are
   present.
5. Hand to `create-nsf-grant` (inventory, REVIEW.md triage, drafting).

## Layout produced

```
NSF-<year>-<program>-<topic>/
├── CALL.md  README.md  REVIEW.md  RESEARCHGOV.md  build.sh
├── inventory/            Explore reports (create-nsf-grant step 2)
├── budget/
└── proposal/
    ├── tex/              description summary references data facilities
    │                     budget-justification [mentoring] references.bib
    ├── final-pdfs/
    └── submission-docs/  COA.xlsx reviewers.txt (biosketch, cps from SciENcv)
```

## Template conventions

- Every template begins with a comment block naming the governing rule and
  the limit the call sets; the drafting skills read it before writing.
- `description_template.tex` orders sections the way the panel reads
  (Overview; Background; Results from Prior NSF Support; Method and
  Standards; Proposed Research with one `\subsection` per project;
  Intellectual Merit; Broader Impacts). The PAPPG fixes only the headings
  "Results from Prior NSF Support", "Intellectual Merit"/"Broader Impacts"
  inside it, and "Broader Impacts" on its own line; everything else is a
  choice, and the call may override the order — record that in `CALL.md`
  and reorder the template copy, not the template.
- The COA template is NSF's own xlsx (five tables); never retype its
  columns. If NSF has issued a newer template than the one shipped here,
  download it and replace the copy in `submission-docs/`.

## Red flags

| Thought | Reality |
|---|---|
| "The page limits are the usual 15/1/2/5" | Read them from the PAPPG in effect; the call may differ. |
| "The target date is the first Tuesday in October" | NSF 26-520 has none for ANT; write what the call says. |
| "I can start writing the overview now" | Instantiate and record the call first; prose comes from create-nsf-grant. |
