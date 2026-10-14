---
name: gp-budget
description: Build the NSF proposal budget — the internal UVM budget spreadsheet and the year-by-year numbers that Research.gov, the budget justification, the SPA form and UVMClick must all match. Use for "make the budget", "what's my salary", "add AI compute", "change the travel", "budget numbers", or before editing any budget figure.
---

# gp-budget

One set of numbers, built once in the internal spreadsheet, then copied
everywhere else. Read `~/.claude/skills/using-grantpowers/references/uvm-facts.md` first.

## Procedure

1. **Start from the last funded or submitted UVM sheet.** Copy it into
   `proposal/budget/<PI>-NSF<year>-<tempID>-InternalBudget.xlsx`, e.g.
   `NSF-Intersection-Theory/budget/…InternalBudget_V4.xlsx`. Keep its
   formulas and its Lookups sheet.
2. **Collect the inputs and show them to the PI as one table:**
   - start date and duration;
   - PI summer months per year (at most 2);
   - the salary base, from the PI's salary letter, never the public list.
     If there is no letter, ask for it;
   - students and percentages;
   - travel: trips per year × cost, domestic and foreign;
   - visitors;
   - supplies and software, named;
   - computing (e.g. AI computing resources at $1,000/month = $12,000/yr,
     under Computer Services);
   - publication costs and the year they fall in;
   - tuition.
   Use the PI's words for anything new, and keep vendor and usage
   descriptions as vague as the PI wants them.
3. **Edit in Excel by AppleScript**, wrapped in
   `with timeout of 90 seconds`. Use `set formula of range` for
   salaries (`=(SALARY/9)*3` gives the summer base),
   `set value of range "O33:Q33" … to {{a,b,c}}` for year rows, then
   `calculate`, `save`, and read back the totals and year rows. Update
   the Lookups rates (fringe, F&A) to the current fiscal year.
4. **Check the arithmetic by hand:**
   - personnel × fringe;
   - MTDC = direct − tuition − equipment;
   - F&A = 53.5% × MTDC;
   - year totals and grand total.
   Record the final year-by-year table in `REVIEW.md` §3, with the date.
5. **Propagate the same numbers** to:
   - the budget justification (`gp-budget-justification`);
   - the Research.gov budget form (`gp-researchgov`);
   - the SPA Pre-Award form and the SPA email (`gp-spa-route`);
   - the UVMClick budget (`gp-uvmclick`).
   Differences of up to about $15, from salary rounding, are acceptable.
   State them in the SPA email.
6. **A graduate student or postdoc** in the budget requires a mentoring
   plan: `gp-mentoring-plan`.

## Red flags

| Thought | Reality |
|---|---|
| "The public salary list is close enough" | It is last year's base. Use the salary letter. |
| "I'll fix the justification later" | Change every copy in the same turn, or the numbers drift. |
| "SPA enters the budget" | The PI can enter it in Research.gov, and SPA needs numbers to check. Build it. |
