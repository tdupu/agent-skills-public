# using-testpowers router specification

## Trigger

Route requests to design, add, repair, review, or audit tests for software,
packages, skills, packs, or mathematical projects.

## Anti-trigger

Do not route a documentation-only request. Do not infer unit testing from the
word “test” when the risk requires integration, regression, property,
snapshot, smoke, or entrypoint testing.

## Failure class

Tautological assertions, a test at the wrong layer, missing boundary/error
cases, lost historical regressions, non-repeatable tests, false confidence
from coverage, or a green suite that does not exercise the user entry point.

## Observable predicates and precedence

1. Existing ecosystem/package predicate (`test-magma`, `test-sage`,
   `test-m2`, `test-lean`, `test-latex`).
2. Explicit risk: historical bug, integration seam, property, snapshot, smoke,
   user entrypoint, or coverage audit.
3. Generic unit testing (`test-unit`) or assessment (`test-assess`).
4. Review (`test-review`) when no mutation is requested.

Choose one primary leaf. If a public contract changes, compose a documentation
leaf after the test work. Never call `using-docpowers` recursively.

## Leaves

See the router dispatch table in `SKILL.md` and the shared contract in
`references/testing-contract.md`.

## Budgets

Router: under 200 words outside its dispatch table. Leaves: under 500 words.
Each test must state its command, signal, scope, and limitation.

## Pressure scenarios

Test a historical Magma bug, a Sage doctest, a Lean build/test split, a LaTeX
golden file, a pack manifest smoke test, a property with shrinking, and a
request that says “unit test” for an integration-only failure.
