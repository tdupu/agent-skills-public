# using-docpowers router specification

## Trigger

Route requests to create, repair, audit, or reorganize documentation for a
repository, package, skill, pack, API, or mathematical project.

## Anti-trigger

Do not route a purely code or test request unless a public interface or an
executable example is being changed. Do not replace `improve-documentation`,
`check-documentation-policy`, or `improve-package-README` when their existing
predicates match.

## Failure class

The wrong audience, missing acquisition/use path, untested examples, stale
claims, broken links, undocumented provenance, or a document at the wrong
level.

## Observable predicates and precedence

1. Existing specialized skill/policy predicate.
2. Ecosystem or pack layout (`doc-math-*`, `doc-pack-*`).
3. Requested artifact (`doc-quickstart`, `doc-examples`, `doc-api`,
   `doc-navigation`, `doc-provenance`).
4. Repository-wide assessment (`doc-assess`, `doc-repository`, `doc-pack`).

Choose one primary leaf. If examples are executable, compose a test leaf after
the documentation leaf. Never call `using-testpowers` recursively.

## Leaves

See the router dispatch table in `SKILL.md` and the shared contract in
`references/documentation-contract.md`.

## Budgets

Router: under 200 words outside its table. Leaves: under 500 words. References
are concise and operational.

## Pressure scenarios

Test a Magma README, a Lean API change, a stale Gas City pack index, a LaTeX
release note, a private repository with no executable toolchain, and a request
that mixes documentation with tests.
