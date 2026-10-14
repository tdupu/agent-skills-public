---
name: gp-current-pending
description: Prepare the NSF Current and Pending (Other) Support entries for a senior person — every current award, pending proposal (including this one), in-kind support and its person-months — for the PI to enter and certify in SciENcv. Use for "current and pending", "CPS", "other support", "list my awards".
---

# gp-current-pending

Generated and certified in SciENcv by the person (Gate). The agent
assembles a complete, checked list.

## Procedure

1. **Collect** from the PI's records (Research.gov Awards, NSF award
   letters in `award/`, UVMClick FP records, emails):
   - Current awards: sponsor, number, title, PI role, start/end, total
     amount, person-months per year (calendar/academic/summer).
   - Pending proposals, **including the one being prepared**: same fields,
     proposed dates and amount.
   - In-kind contributions (visiting positions, lab/compute access with
     value or "no monetary value").
   - Any appointments or support outside UVM.
2. **Check the person-month overlap.** The summer months requested across
   all NSF awards and proposals must not exceed 2 per year. If they do,
   state the overlap and how the PI intends to handle it.
3. **Write** `proposal/submission-docs/cps-input.md` as a table with one
   row per item, plus an "Overall objectives" and a "statement of
   potential overlap" for each item. SciENcv requires both.
4. **Hand off to the PI:** SciENcv → NSF Current and Pending (Other)
   Support. Enter the rows, certify, and export the PDF to
   `submission-docs/cps-<PI>-<year>.pdf`.
5. **Verify** the exported PDF:
   - every row from step 3 is present;
   - this proposal is listed as pending with the right amount and dates;
   - the certification is present.
6. **Upload** with `gp-researchgov`.
