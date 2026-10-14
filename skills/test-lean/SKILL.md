---
name: test-lean
description: Use when adding or reviewing Lean build, theorem, example, project, Mathlib-style, or generated-documentation tests.
---

Read the testing contract and separate Lean evidence gates: `lake build` for
compilation, `lake test` for project tests, and documentation generation/checks
when applicable. Assert the intended theorem/type/behavior; do not confuse
successful elaboration with a test of the user-facing API. Include countercase
or boundary examples where the theorem permits them and record axioms or
environment assumptions when relevant.

For a formalization bug, preserve a minimal reproducer and durable reference.
Report exact toolchain and unavailable commands.
