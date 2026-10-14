---
name: test-sage
description: Use when adding or reviewing SageMath doctests, package tests, optional-feature tests, or Sage regressions.
---

Read the testing contract and Sage conventions. Prefer concise doctests for
public examples and `sage -t`-compatible tests; mark optional, slow, random,
or platform-dependent cases using local syntax. Assert mathematical results,
not formatting accidents, and include edge/error behavior plus a durable bug
reference for regressions.

Run the narrowest relevant `sage -t` command and record version, output, and
unavailable optional components. Do not turn every integration or external
dependency test into a unit test.
