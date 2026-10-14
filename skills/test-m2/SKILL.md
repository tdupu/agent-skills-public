---
name: test-m2
description: Use when adding or reviewing Macaulay2 package checks, examples, method tests, or mathematical regressions.
---

Read the testing contract and inspect package `document` examples, `newPackage`
metadata, and existing `check` files. Use the package's real install/load path
when testing integration. Assert concrete algebraic results and important
error/edge behavior; preserve citations and a short bug reference for
regressions.

Run the narrowest `check` or package test command available. Record M2 version,
command, result, and unavailable dependencies. Keep generated/reference output
reviewable and do not claim an example works merely because the package loads.
