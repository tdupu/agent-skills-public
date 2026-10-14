---
name: test-coverage
description: Use when measuring, interpreting, or improving test coverage and identifying meaningful untested behavior.
---

Read the testing contract. Run the repository's coverage command and inspect
uncovered branches, error paths, boundaries, public entrypoints, and historical
bugs. Treat the percentage as a navigation signal, not a quality verdict.

Prioritize gaps by user risk and add the smallest meaningful test at the right
layer. Check that coverage excludes generated/vendor code intentionally and
that the command is reproducible. Report baseline, changed result, command,
scope, and remaining blind spots; never inflate coverage with tautological
assertions.
