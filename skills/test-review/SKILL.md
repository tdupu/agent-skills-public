---
name: test-review
description: Use when reviewing test design or test changes without implementing them.
---

Read the testing contract. For each test, identify the behavior question,
system under test, inputs, oracle, layer, deterministic setup, and meaningful
failure signal. Check representative, empty, boundary, invalid, and historical
bug cases; tautologies, accidental passes, over-mocking, order dependence,
flakiness, and green-suite or coverage overclaims.

Return severity-ranked findings with exact file/line evidence, a minimal fix,
commands not run, and remaining risk. Do not rewrite or run tests unless the
request explicitly changes review scope. Use `is-good-test` when its dedicated
experiment-design predicate matches.
