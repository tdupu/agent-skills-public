---
name: gp-budget-justification
description: Write budget-justification.tex for an NSF proposal — one paragraph per budget line with its arithmetic, matching the internal budget and Research.gov to the dollar. Use for "write the budget justification", "update the justification", "justification doesn't match the budget".
---

# gp-budget-justification

Source of truth: the internal budget sheet (`gp-budget`). The
justification restates it; it never introduces a number.

## Procedure

1. Read the year-by-year numbers from the sheet, or from `REVIEW.md` §3.
2. Write one paragraph per NSF category, in the order of NSF's budget
   form, each opening with an italic label and the amounts:
   - **A. Senior personnel** — months per year, the base ("the PI's FY27
     nine-month salary of $X, escalated 4% per year"), the amounts per
     year, and the 2-month cap statement.
   - **B. Other personnel** — the role, the percentage, the stipend base,
     the amounts.
   - **C. Fringe** — the rates and the amounts.
   - **D. Equipment** — only if budgeted.
   - **E. Travel** — trips × (days, hotel, per diem, flight) for domestic
     and foreign travel.
   - **F. Participant support** — only if budgeted.
   - **G. Other direct costs** — materials and supplies (software named),
     publication (the year it falls in), computer services (the PI's
     wording, e.g. "AI computing resources to run the PI's open-source
     research tools and the computations described in the Project
     Description"), visitors, tuition remission.
   - **H/I. Indirect** — 53.5% of MTDC, naming the exclusions.
3. Match the PI's wording choices exactly; for example, don't write
   "metered" if the PI asked for it to stay vague.
4. Build the PDF. It must be at most 5 pages (GRANT-FORMAT F15).
   `check-grant-format` covers the page count.
5. Compare every dollar figure in the PDF text against the sheet
   (`pdftotext`, then grep for `$`). Every figure must match before upload.
6. Upload with `gp-researchgov` (Budget Justification).
