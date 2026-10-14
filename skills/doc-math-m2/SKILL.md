---
name: doc-math-m2
description: Use when documenting Macaulay2 packages, methods, examples, package metadata, or M2 repositories.
---

Read the documentation contract and inspect `newPackage` metadata, `document`
blocks, package examples, citations, and `check` conventions. Keep package
name/version/date/authors/keywords consistent with source. Explain installation
or `installPackage`, first use, expected output, error/edge behavior, and the
package's mathematical references.

Use the repository's example and test files as the source of executable truth.
Run the narrowest `check` or documentation build available. Record an absent
Macaulay2 binary instead of simulating output. Link package docs to the
repository README and generated reference pages without duplicating them.
