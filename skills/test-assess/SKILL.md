---
name: test-assess
description: Use when assessing a test strategy, suite quality, risk coverage, flakiness, or whether existing tests provide meaningful confidence.
---

Read `../using-testpowers/references/testing-contract.md`. Identify the
behavior and risks, test layers present, missing representative/empty/boundary/
invalid cases, historical bugs, entrypoint coverage, runner commands, speed,
isolation, and environment assumptions.

Do not edit. Reject tautological assertions, green-suite overclaims, tests that
only exercise mocks, and coverage percentages presented as correctness. Rank
findings by user risk and name the smallest suitable leaf (`test-unit`,
`test-integration`, `test-regression`, `test-property`, `test-snapshot`,
`test-smoke`, `test-entrypoint`, or `test-coverage`).

Return exact evidence paths, commands tried, unavailable tooling, and a
prioritized test plan.
