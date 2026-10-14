---
name: gp-biosketch
description: Prepare the NSF Biographical Sketch (SciENcv common form) and the separate Synergistic Activities document for a senior person — products list, appointments, synergistic activities — ready for the PI to certify in SciENcv. Use for "do the biosketch", "SciENcv", "synergistic activities", "update my products".
---

# gp-biosketch

NSF requires the biosketch to be generated in SciENcv and certified by
the person. The agent prepares the inputs and the synergistic-activities
PDF; **the PI certifies in SciENcv and exports the PDF** (Gate).

## Procedure

1. **Identity.**
   - Name as it appears in Research.gov, and ORCID.
   - Current appointments, newest first, with dates (from the CV or
     `README.md`).
   - Education and training: institution, field, degree, year.
2. **Products** (up to 10, NSF's current limit; check the PAPPG version).
   - Choose the products most closely related to the proposal, first by
     topic and then by recency.
   - Take each from arXiv, MathSciNet or the journal.
   - Write `proposal/submission-docs/biosketch-products.ris` (one RIS
     record per product) for SciENcv import, or a citation list if the PI
     prefers to type them.
   - Statuses must be true: published, to appear, submitted, or preprint.
3. **Synergistic activities** (up to 5, each one or two sentences with a
   date and a number):
   - Write them in `proposal/tex/synergistic.tex`, 11pt, 1in margins.
   - Each activity must exist: a repo with its license, a channel with
     its subscriber count, a seminar with its years, an editorial role.
   - Cite the PI's own records; don't round up.
4. **Hand-off to the PI**, as a checklist:
   - SciENcv → Create Document → NSF Biographical Sketch.
   - Import the RIS file and fill in appointments.
   - Certify.
   - Download the PDF to `submission-docs/biosketch-<PI>-<year>.pdf`.
5. **Verify** the exported PDF:
   - name, page count, and that the product statuses match step 2;
   - the certification statement is present.
6. **Upload** both files with `gp-researchgov` (Senior Personnel
   Documents).
