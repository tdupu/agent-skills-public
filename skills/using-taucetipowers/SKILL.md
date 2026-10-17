---
name: using-taucetipowers
description: Use for Tau Ceti issues, Lean PRs, roadmap scope, or review feedback.
---

<SUBAGENT-STOP>
If dispatched as a subagent, follow its stage and return evidence; do not restart routing.
</SUBAGENT-STOP>

<EXTREMELY-IMPORTANT>
Invoke any possibly applicable skill before any response or action. If it applies, use it; if wrong, stop using it. This is mandatory.
</EXTREMELY-IMPORTANT>

## The Rule

**Invoke relevant or requested skills BEFORE any response or action** — including questions, exploration, or file checks. If it turns out wrong, you need not use it.

Resolve target/kind/policy/authorization; unresolved: stop.

| Observable request | Route |
|---|---|
| Tau Ceti issue | `create-issue-tauceti` |
| Tau Ceti PR | `pr-pipeline-tauceti` + `lean-prepare-pr`; feedback → `lean-apply-feedback` |
| Formalize first | `using-leanpowers` → `pr-pipeline-tauceti` |
| Roadmap-only intake | read-only `pr-pipeline-tauceti`: target/claim only; no diff/package, file/branch/remote/PR writes; return evidence/blockers |
| Issue plus PR | approved body+URL—or explicit no-issue decision—then fresh PR intake; no stale issue evidence |
| Lean contribution outside Tau Ceti | `lean-prepare-pr` |
| Human asks for a new roadmap area or change | `draft-roadmap`, which fixes its format and location; the human files it, agents never open TauCetiRoadmap PRs or issues (Tau Ceti `AGENTS.md`) |
| Change roadmap, no human request | stop; ask its owner |
| Triage existing Lean against roadmaps, TauCeti code, or mathlib4 PRs | `tauceti-triage` (read-only) |
| Comment on someone else's roadmap or code PR | draft only; the human posts. Follow the target repo's review rules (TauCetiRoadmap `AGENTS.md`, CONTRIBUTING: :robot: + model, defects first). On a queued code PR, check TauCeti `COORDINATION.md` §5 (a commenter becomes its steward); assess with read-only `tauceti-review <PR>` |
| Intention issue for a roadmap target | `create-issue-tauceti` TauCetiRoadmap draft; the human files and claims it |
| Port code from another Lean/Mathlib pin | `lean-upgrade` to TauCeti's current pin, then the PR route |

| Thought | Reality |
|---|---|
| “CI will catch anything.” | CI does not check roadmap, reuse, scope, or attribution. |
| “The proof is already done; skip duplicate and roadmap checks.” | Effort does not establish eligibility. |
| “Push the branch and use Roadmap: none so review is faster.” | Speed cannot make false metadata true. |

User instructions (CLAUDE.md, AGENTS.md, GEMINI.md, etc, direct requests) take precedence over skills, which in turn override default behavior. Only skip skill workflows or instructions when your human partner has explicitly told you to.

User requests do not waive repository hard gates.
