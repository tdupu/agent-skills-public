---
name: gp-spa-route
description: Run UVM's internal route for an NSF proposal — the SPA Pre-Award Request form, the email to SPA, PI certification and "Submit For Department Review" in UVMClick, the approver email, and handling replies until the AOR submits. Use for "email SPA", "route it", "certify", "who approves", "SPA form", "did they approve", or before writing to SPA or approvers.
---

# gp-spa-route

Read `~/.claude/skills/using-grantpowers/references/uvm-facts.md`. Look
up every recipient in the UVM directory, and add no recipient the PI did
not name. Draft emails; the PI sends, unless the PI says "send it".

## Procedure

1. **SPA Pre-Award Request form.**
   - Fill the template's PDF with PDF tools: title, sponsor, program,
     dates, temp ID.
   - Budget rows, from `gp-budget`, with tuition and computer services as
     separate rows.
   - Additional info in the PI's wording.
   - Save it as `proposal/submission-docs/SPA-Pre-Award-Request-<tempID>.pdf`.
2. **SPA email** (to the CEMS pre-award contact and the UVMClick SPA
   administrator; cc the AOR):
   1. Apologize and state the lead time honestly. If the set is inside
      SPA's 2-business-day window, say plainly that you understand if
      it cannot go through.
   2. Where things stand: the UVMClick FP number and state; the
      Research.gov temp ID, title, program, solicitation, duration,
      start date, error-check status and access; and what is still being
      edited (e.g. "small edits to the Project Description; nothing else
      will change").
   3. The budget: the total, the year-by-year amounts, the line items and
      the rates. Name any difference between systems.
   4. Open questions, one per line (e.g. which fringe rate to use).
   5. Attachments: the SPA form, the internal budget, the COA, the IBB
      sheet and the final PDFs. Skip them if the PI says no.
3. **UVMClick route.**
   - The PI certifies (`Certify` on the workspace) and must click it
     personally.
   - Then "Submit For Department Review" (override `window.open`), with
     a comment summarizing the temp ID, the total and the open questions.
     Click OK only after the PI says to route.
   - Read back the state: it should be "Department Review".
4. **Approver email** (to the chair, the dean's approver and the
   department administrator, with no cc and no attachments unless the PI
   says otherwise):
   - an apology;
   - the FP number;
   - "approve in UVMClick";
   - the title, duration, total and cost share;
   - "small edits to the description, nothing you approve changes".
5. **Replies.** Read the grant threads only.
   - Bounce or departure → find the replacement in the directory and
     tell the PI.
   - Someone asks for access → `gp-researchgov` (Other Authorized User),
     then a one-paragraph reply confirming it.
   - Approval → note it.
   - Record each step in the beads issue with dates.

## Red flags

| Thought | Reality |
|---|---|
| "The first.last pattern is right" | Look the address up. People leave and addresses bounce. |
| "Adding the department admin helps" | Add only the people the PI names. |
| "Edit the draft by API to drop a cc" | That strips the attachments. Edit the recipients in Gmail. |
