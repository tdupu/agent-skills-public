---
name: doc-api
description: Use when documenting public functions, classes, intrinsics, commands, interfaces, parameters, return values, errors, or compatibility behavior.
---

Read the documentation contract and locate the source of truth for the public
interface. Document purpose and audience first, then inputs, outputs, side
effects, errors, edge cases, version/compatibility notes, and a realistic
example. Match the repository's native API form: docstrings, generated source
comments, package blocks, declarations, or reference pages.

Do not copy an API list that will drift from source. Link to canonical details,
cite external mathematics or standards, and make examples executable when the
toolchain supports it. For a public behavior change, hand off to a test leaf
and record the expected observable signal.

Return changed paths, source-of-truth evidence, example/test evidence, and
known undocumented behavior.
