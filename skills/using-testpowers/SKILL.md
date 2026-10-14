---
name: using-testpowers
description: Use when designing, adding, repairing, reviewing, or auditing tests for software, packages, skills, packs, or mathematical projects.
---

Invoke `using-superpowers` once and reuse the active coordinator. Read
`references/testing-contract.md`. Choose a route from the stated risk and
observable repository/toolchain evidence, not from the word “unit”. Preserve
existing ecosystem-specific routes. Never recursively invoke
`using-docpowers`.

| Evidence in the request or repository | Primary route |
|---|---|
| Magma, Sage, Macaulay2, Lean, or LaTeX layout/toolchain | `test-magma`, `test-sage`, `test-m2`, `test-lean`, or `test-latex` (compose `test-regression` for a fixed bug) |
| Fixed historical bug or explicit regression request without a more specific adapter | `test-regression` |
| Module/component/service boundary | `test-integration` |
| Invariant, round-trip, algebraic law, or broad input family | `test-property` |
| Stable serialized/rendered/generated output | `test-snapshot` |
| Install, startup, package load, or one representative user action | `test-smoke` |
| Documented public install/CLI/REPL/build path | `test-entrypoint` |
| Coverage measurement or uncovered-risk analysis | `test-coverage` |
| Agent skill, router, catalogue, manifest, or trigger behavior | `test-skill` |
| Read-only design critique | `test-review` |
| Fast isolated local behavior | `test-unit` |
| Unclear risk, broad audit, or strategy request | `test-assess` |

For mixed work, test first and name the documentation handoff when the public
contract or examples change. Return changed paths or findings, commands,
results, scope, limitations, and unavailable toolchains.
