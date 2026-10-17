---
name: pr-pipeline-tauceti
description: Use when a Lean or Mathlib-style change is intended for a TauCetiProject/TauCeti pull request, including local readiness, PR drafting, review iteration, or current-head review checks.
---

<SUBAGENT-STOP>
If dispatched for one bounded PR stage, execute that stage only and return its evidence.
</SUBAGENT-STOP>

Input: checkout, diff/context, write scope. Read `references/tauceti-contract.md`; the live `AGENTS.md` overrides it and requests. Empty diff: roadmap-only; verify target/claim, return evidence/blockers, then stop read-only: no `lean-prepare-pr`, Lean/build, PR draft, branch, PR, or write. If formalization is needed, `using-leanpowers` completes first; **REQUIRED SUB-SKILL:** one `lean-prepare-pr` on exact snapshot; validate; rerun if stale. Use `lean-apply-feedback`.

1. Resolve checkout/remote/base/head/branch/in-flight. Read `AGENTS.md`, `README.md`, `COORDINATION.md`, PR template, and `TauCetiRoadmap`. New math needs an exact merged-roadmap target and a live claim: an intention issue the requesting human filed, assigned to their login and unexpired (TauCetiRoadmap README §Coordinating work; body gets `Closes TauCetiProject/TauCetiRoadmap#N`), or our worker lease `refs/tauceti-claims/author/<focus>/<id>`. None, or any live claim by another owner: stop. Upstream both are cooperative; the stop is local policy. Maintenance names its area or uses `Roadmap: none` only for genuinely general, cross-cutting, infrastructure, or dependency work.
2. Keep one topic; no stacked PRs, drafts included: a dependent opens only after its prerequisite lands on `main`. Inspect paths; reuse Tau Ceti/Mathlib first. List each rule of `AGENTS.md` §The rules of the repo at the observed commit with its check; reject violations and accidental human-owned edits. Preserve intentional `scripts/`, `.github/`, or lakefile changes and stop for human review; only documented pin files may move forward. Code from another pin goes through `lean-upgrade` to TauCeti's current pin first.
3. Validate the one `lean-prepare-pr` result: paths/diff, style/review/fidelity/verification receipts, checks, linter, `lake build`, and axiom/full-type inspection. Record commit, pins, failures, and stale evidence; green build is not semantic or roadmap approval.
4. Draft the live PR body with one standalone `Roadmap:` line, result, receipts, scope, limits. Add `<!--tauceti-target:v1 {"focus":"<area>","id":"<canonical-target-id>"}-->` for roadmap work. The newest literal `tauceti-scoreboard` comment must contain `tauceti-meta:v1.head_sha` exactly equal to the actual PR head; otherwise unreviewed.
5. Stop at readiness unless remote mutation is explicitly authorized now. Record the observed head. New branch: `git push --force-with-lease=<branch>: <remote> HEAD:<branch>`. Existing branch: `git push --force-with-lease=<headRefName>:<observed_oid> <remote> HEAD:<headRefName>`. A stale lease means re-observe, never plain/force push. Run `gh pr create` only after body approval.
6. After CI, run `tauceti-review <PR>` (read-only); `--post` only when authorized. Done means CI green and every blocking rubric green for the current head; new commits need fresh review. Contest contradictions. Stop there: merging, closing and de-duplicating are the repo's CI and bors (README §Contributing with the worker CLI), never the agent; never `--admin`.

Return paths/diff, claim evidence, receipts, draft body, remote actions, review status, and blockers.
