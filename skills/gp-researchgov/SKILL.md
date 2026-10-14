---
name: gp-researchgov
description: Do the NSF Research.gov proposal-preparation work in Chrome — create or open the proposal, fill the cover sheet, upload each document, enter the budget form, share with SPO/AOR, add Other Authorized Users, and clear Check Errors. Use for "enter it in Research.gov", "upload the PDFs", "check errors", "add her on research.gov", "fill the budget form", or before opening research.gov.
---

# gp-researchgov

Read `~/.claude/skills/using-grantpowers/references/browser.md` first.
The PI signs in (NSF ID route); never type a password. The AOR submits.
Uploading, editing and saving are in scope. Certifications, "Submit"
and "Share" changes need the PI's explicit go-ahead in chat.

## Procedure

1. **Open** Proposals → Prepare & Submit → In Progress → Full Proposals →
   the temporary ID. Note the temp ID and proposal ID from the URL in
   `README.md`.
2. **Cover sheet.**
   - Check the funding opportunity, division and program, the duration
     and start date, and the title.
   - International activities: check the box and list the countries if
     there is foreign travel or a collaborator abroad.
   - Leave all other compliance boxes as they are unless the PI says
     otherwise. Read every checkbox label before clicking it.
3. **Uploads.** Upload each PDF from `proposal/final-pdfs/` and each
   file from `submission-docs/` into its section: Summary, Description,
   References, Budget Justification, Facilities, Data Management (DMSP),
   Mentoring Plan, Senior Personnel Documents (biosketch, CPS,
   synergistic activities, COA), Single Copy (suggested reviewers).
   After each upload, read the section's status line.
4. **Budget form** (numbers from `gp-budget`):
   - Year 1: senior personnel months and salary; other personnel count
     and salary; fringe; travel (domestic, foreign); materials and
     supplies; publication; computer services; other (visitors + tuition);
     indirect rate and base.
   - Type the base by real keystrokes.
   - Copy year 1 into years 2 and 3, then edit them.
   - Save. Retry once on a system error.
   - Read back the cumulative totals and compare them with the sheet.
5. **Access.**
   - Proposal Access → share with SPO/AOR, edit access. Get the PI's
     go-ahead first.
   - Manage Personnel → Add Other Authorized User, by NSF ID or by email.
     If the email finds no account, ask the person for their NSF ID.
6. **Check Errors.** Run it. Fix every error and re-run until there are
   0 errors. Report every remaining warning with its exact text.
   - "Mentoring plan required" → `gp-mentoring-plan`.
   - A References spacing warning → set `\bibliofont` to `\normalsize`.
     If the warning persists, report it; it is only a warning.
7. **Report:** temp ID, errors and warnings, the budget totals by year,
   and who has access.

## Red flags

| Thought | Reality |
|---|---|
| "I'll click this checkbox to see what it does" | Read the label first. Dual Use and similar boxes carry attestations. |
| "The script set the field" | Ember ignores plain `.value`. Use the native setter, and type the base for real. |
| "The PI can't upload a budget" | The PI can fill the budget form. Do it, and tell SPA. |
