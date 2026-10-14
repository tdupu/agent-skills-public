---
name: create-issue-tauceti
description: Use when an observation, bug, feature request, or documentation correction must be reported to TauCetiProject/TauCeti, including when asked to draft or file a Tau Ceti GitHub issue.
---

<SUBAGENT-STOP>
If dispatched for one bounded issue stage, follow that brief and return its evidence; do not restart.
</SUBAGENT-STOP>

Prepare an issue for `TauCetiProject/TauCeti`; if not issue-shaped, return to the router. Do not edit the roadmap or file before exact-body approval.

1. Resolve and state target, kind (`bug`, `feature`, or `docs`), observed commit, and whether it is local-only. Read current `AGENTS.md`, `README.md`, `COORDINATION.md`, and default-branch issue forms.
2. Confirm `gh` authentication. Search all-state issues and PRs with three queries (symptom, symbol/file, area). Comment on a match rather than duplicate it; draft that comment and use the approval gate below. Verify on current `main`.
3. For a bug, record expected/actual behavior, a minimal reproduction or `not yet reduced — reduction is step 1`, and file/line evidence. For a feature, perform a reuse/wheel check and identify an exact roadmap target; unverifiable fit blocks contribution advice and requires roadmap-owner input. For docs, show corrected usage. Check policy text and open work.
4. Read the live template at draft time. Fill required fields in order; never invent versions, line numbers, reproduction, labels, or causes. Without a form, use Summary, Evidence, Reproduction/Usage, Policy/Roadmap fit, Alternatives, and Context.
5. Check labels with `gh label list`; unknown labels are omitted from the final command. Return target/template, search receipts, current-main result, policy/roadmap result, evidence, exact body, verified labels, and recommendation.

**Approval gate:** show the complete title and body for the issue or comment and stop. On `REVISE`, redraft; on `REJECT`, stop. Only after explicit `APPROVE` may you run `gh issue create --repo TauCetiProject/TauCeti --title ... --body-file ...` with verified labels, or post the approved comment. Report the URL; do not close, merge, or alter a roadmap item.

Red flags: “the issue is obvious,” “main probably still has it,” “the template is stable,” and “I can file now and fix the body later.” Each means return to the corresponding gate.
