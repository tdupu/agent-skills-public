---
name: using-taucetipowers
description: Use for any Tau Ceti work — contributing an existing Lean development, roadmap PRs, intentions, issues, code PRs, comments on others' PRs, or review feedback.
---

<SUBAGENT-STOP>
If dispatched as a subagent, follow its stage and return evidence; do not restart routing.
</SUBAGENT-STOP>

<EXTREMELY-IMPORTANT>
Invoke any possibly applicable skill before any response or action. If it applies, use it; if wrong, stop using it. This is mandatory.
</EXTREMELY-IMPORTANT>

## The Rule

**Invoke relevant or requested skills BEFORE any response or action** — including questions, exploration, or file checks. If it turns out wrong, you need not use it.

Resolve target/kind/policy/authorization; unresolved: stop. Authorization is the human's own instruction. Subagents never push, post, or open PRs or issues: they return readiness and the exact command, which the main session runs on the human's direct instruction, or the human runs. If the harness permission check blocks it, report that; never retry by another route.

| Observable request | Route |
|---|---|
| Contribute an existing Lean development to Tau Ceti, or resume one | `contribute-to-tauceti` |
| Tau Ceti issue | `create-issue-tauceti` |
| Tau Ceti PR | `pr-pipeline-tauceti` + `lean-prepare-pr`; no push before its local rubric gate (step 5); feedback → `lean-apply-feedback` |
| Formalize first | `using-leanpowers` → `pr-pipeline-tauceti` |
| Roadmap-only intake | read-only `pr-pipeline-tauceti`: target/claim only; no diff/package, file/branch/remote/PR writes; return evidence/blockers |
| Issue plus PR | approved body+URL—or explicit no-issue decision—then fresh PR intake; no stale issue evidence |
| Lean contribution outside Tau Ceti | `lean-prepare-pr` |
| Human asks for a new roadmap area or change | `draft-roadmap` for the decomposition, then `roadmap-pr-tauceti` for format, checks and hand-off; the human opens it |
| Change roadmap, no human request | stop; ask its owner |
| Triage existing Lean against roadmaps, TauCeti code, or mathlib4 PRs | `tauceti-triage` (read-only) |
| Comment on someone else's PR or issue (TauCetiRoadmap, TauCeti, mathlib4, other trackers) | draft; post only when it adds something concrete (a missing Stacks tag, a confirmed bug reproduction with a fix) and only after the human approves the exact text; the human posts it, or authorizes posting it from their account. Mention the source repo only when it helps the reader. :robot: + model, defects first (TauCetiRoadmap `AGENTS.md`, CONTRIBUTING). On a queued TauCeti code PR, check TauCeti `COORDINATION.md` §5 (a commenter becomes its steward); assess with read-only `tauceti-review <PR>` |
| Intention issue for a roadmap target | `create-issue-tauceti` TauCetiRoadmap draft; the human files and claims it |
| Human asks you to fill a GitHub form in Chrome | `references/github-forms.md` |
| Port code from another Lean/Mathlib pin | `lean-upgrade` to TauCeti's current pin, then the PR route |

| Thought | Reality |
|---|---|
| “CI will catch anything.” | CI does not check roadmap, reuse, scope, or attribution; the AI reviewer judges those against TauCetiReview's rubrics, which run locally before push. |
| “The proof is already done; skip duplicate and roadmap checks.” | Effort does not establish eligibility. |
| “Push the branch and use Roadmap: none so review is faster.” | Speed cannot make false metadata true. |

User instructions (CLAUDE.md, AGENTS.md, GEMINI.md, etc, direct requests) take precedence over skills, which in turn override default behavior. Only skip skill workflows or instructions when your human partner has explicitly told you to.

User requests do not waive repository hard gates.
