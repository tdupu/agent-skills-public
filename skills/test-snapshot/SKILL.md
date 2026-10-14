---
name: test-snapshot
description: Use when serialized output, generated documentation, rendered text, reports, or golden files are the behavior being protected.
---

Read the testing contract. Define the stable contract and normalize only
intentional nondeterminism such as timestamps, paths, or ordering. Keep the
fixture small and reviewable. A snapshot must fail for a meaningful user-visible
change; do not approve a wholesale update without understanding the diff.

Record the generator/update command, expected output location, review rule,
and tool/version assumptions. Add focused assertions for critical semantics so
the snapshot is not the only signal. Use `test-regression` for a bug-specific
golden case and `doc-navigation` when generated links are involved.
