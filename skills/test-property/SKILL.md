---
name: test-property
description: Use when an invariant, algebraic law, round-trip, monotonicity, idempotence, or broad input family is more important than fixed examples.
---

Read the testing contract. State the invariant and its domain, including
preconditions and excluded values. Use the repository's property-testing or
generator convention with deterministic seeds or reproducible shrinking.
Include a few named examples that make failures understandable, and test
boundary/degenerate values explicitly when generators may miss them.

Assert a property of the public result, not the generator or implementation
steps. Record seed/reproducer, command, expected signal, runtime budget, and
known blind spots. Use `test-regression` as well when the property was added
because of a specific historical bug.
