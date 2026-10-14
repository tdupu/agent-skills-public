---
name: doc-math-lean
description: Use when documenting Lean declarations, Mathlib-style APIs, Lean projects, blueprints, or generated Lean documentation.
---

Read the documentation contract and preserve source doc comments as the
canonical API source. Separate explanatory prose, generated declaration docs,
examples, contributor/build instructions, and formal fidelity claims. Use
`lake build`, `lake test`, and the repository's documentation build/check as
separate evidence gates when available.

State Lean/toolchain and dependency versions, cite mathematical sources, and
distinguish proved, assumed, and planned results. For a declaration change,
compose `test-lean` or `lean-verify` only after documentation ownership is
clear. Do not claim generated pages were rebuilt when the toolchain is absent.
