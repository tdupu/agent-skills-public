---
name: gp-review-package
description: Review a whole NSF proposal package before it goes to SPA or the AOR — every required document present and current, every number identical across the budget sheet, justification, Research.gov, SPA form and UVMClick, every person consistent across COA, biosketch and description, and both grant checkers clean. Use for "is it ready", "review the package", "what's left to do", "before I send to SPA".
---

# gp-review-package

The review produces a table, and every row carries evidence: a file
path, a page, or a read-back from a site. Fix nothing silently. Report,
then fix only what the PI approves.

## Checks

1. **Document set** (Research.gov names):
   - summary, description, references, budget justification,
     facilities, data management;
   - mentoring plan, if a student or postdoc is budgeted;
   - biosketch, CPS and synergistic activities for each senior person;
   - COA;
   - suggested reviewers (optional).
   Each must be newer than its source (`.tex` or SciENcv export date).
2. **Checkers.** Run `check-grant-style`, then `check-grant-format`.
   Paste the FAIL lines.
3. **Numbers.** Build a table of the year-by-year totals and each line
   item from each source:
   - internal sheet;
   - budget-justification PDF text;
   - Research.gov budget read-back;
   - SPA form fields;
   - UVMClick workspace totals.
   Flag any cell that differs by more than $15.
4. **Rates.** Check fringe, F&A and escalation against
   `using-grantpowers/references/uvm-facts.md`, and flag any default the
   systems disagree on.
5. **People.**
   - Each COA Table 4 name appears among the papers in the biosketch,
     the description or the repos (spot-check five).
   - Advisees match the mentoring plan.
   - Collaborators named in the description are on the COA.
6. **Dates.** Start date, duration and end date are the same in
   Research.gov, UVMClick (periods) and the justification.
7. **Research.gov Check Errors.** Read back: 0 errors, with any warnings
   listed.
8. **Route state.** The UVMClick state, the approvals received, and
   SPA's replies (`gp-spa-route`).

## Output

A table with columns Check | Status (OK / FIX / ASK) | Evidence. Then a
short list of what the PI must decide, one item at a time.
