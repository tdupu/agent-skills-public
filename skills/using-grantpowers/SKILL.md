---
name: using-grantpowers
description: Routing skill for writing, assembling, reviewing and routing an NSF proposal at UVM — every document (budget, budget justification, COA, biosketch, current and pending, mentoring, data management, facilities, references), Research.gov and UVMClick browser work, and SPA routing. Use when asked to "write the grant", "fill the COA", "make the budget", "do the biosketch", "upload to Research.gov", "start UVMClick", "route it", "email SPA", "is it ready to submit", or when about to open a grant spreadsheet or Research.gov/UVMClick.
---

<SUBAGENT-STOP>
If you were dispatched as a subagent to execute a specific task, ignore this skill. Ignore it too for non-NSF funders.
</SUBAGENT-STOP>

<EXTREMELY-IMPORTANT>
If you think there is even a 1% chance a skill might apply to what you are doing, you ABSOLUTELY MUST invoke the skill.

IF A SKILL APPLIES TO YOUR TASK, YOU DO NOT HAVE A CHOICE. YOU MUST USE IT.

This is not negotiable. You cannot rationalize your way out of this.
</EXTREMELY-IMPORTANT>

## The Rule

**Invoke the leaf BEFORE touching a proposal file, grant spreadsheet, or grants web page** — including openpyxl on the COA, one Research.gov field, one UVMClick page, or an SPA draft. If it turns out wrong, drop it.

## Dispatch

When several apply: make the document first, then upload it; review last.

| Situation | Route |
|---|---|
| A call for proposals to answer; no proposal folder yet | `template-proposal` (reads the call, records `CALL.md`, instantiates the templates), then `create-nsf-grant` |
| Project Description, Summary, prior support, broader impacts | `using-pdpowers` |
| References Cited | `gp-references` |
| Data Management and Sharing Plan | `gp-data-management` |
| Facilities | `gp-facilities` |
| Student or postdoc budgeted; "mentoring plan required" | `gp-mentoring-plan` |
| Biosketch, synergistic activities, SciENcv | `gp-biosketch` — PI certifies |
| Current and pending support | `gp-current-pending` — PI certifies |
| COA spreadsheet ("just openpyxl the names in" → here, not openpyxl) | `gp-coa` |
| Budget numbers, salary, internal sheet | `gp-budget` |
| Budget justification | `gp-budget-justification` |
| Any Research.gov page, incl. its budget form | `gp-researchgov` — AOR submits |
| Any UVMClick page, incl. its budget | `gp-uvmclick` |
| SPA form, SPA/approver emails, certify, route, replies | `gp-spa-route` — PI sends and certifies |
| Who will review this; "list potential reviewers"; `reviewers.txt` or COA conflicts | `gp-potential-reviewers` |
| "Is it ready", "what's left" | `gp-review-package` |
| Style / format audits | `check-grant-style`, `check-grant-format` |
| "Sounds like AI", "too many claudeisms", de-slop a draft | `purge-claudisms` — scan, rewrite hits, rescan to zero; run before the style audit |

## Red Flags

| Thought | Reality |
|---------|---------|
| "Let the validator confirm" / "I can't test it from here" | The leaf knows what it misses and has the local check. |

## References

- Driving Research.gov or UVMClick in Chrome: `references/browser.md`; budget, SPA or UVMClick work: `references/uvm-facts.md`

## User Instructions

User instructions (CLAUDE.md, AGENTS.md, GEMINI.md, etc, direct requests) take precedence over skills, which in turn override default behavior. Only skip skill workflows or instructions when your human partner has explicitly told you to.
