# Testing contract

Start with a falsifiable question: what behavior, risk, or past failure should
this test distinguish? Select the cheapest layer that retires that risk, then
add a higher layer only when the seam or user entrypoint requires it.

## Quality floor

- Tests are fast enough for their layer, isolated, repeatable, and
  self-validating.
- Include representative, empty, boundary, invalid, and environment-sensitive
  cases when those states are plausible.
- Assert externally meaningful behavior, not merely that a line ran or a mock
  was called.
- Every fixed bug gets a durable regression test and a short bug reference.
- Coverage is evidence about exercised structure, never proof of correctness.
- Record command, expected result, scope, cost, and known limitation.

## Layer choices

Use `test-unit` for local logic, `test-integration` for component seams,
`test-entrypoint` or `test-smoke` for install/user-path confidence,
`test-regression` for historical failures, `test-property` for invariants,
`test-snapshot` for deliberate serialized/golden output, and `test-coverage`
for a gap analysis. Use `test-review` for read-only critique.

## Handoff

Return changed test paths, runner commands, expected signal, evidence, gaps,
and any unavailable toolchain. If a public interface changed, hand off to a
documentation leaf after tests are designed.
