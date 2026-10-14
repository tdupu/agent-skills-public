# Attribution

Leanpowers adapts workflow ideas and instruction material from
[CBirkbeck/mathlib-quality](https://github.com/CBirkbeck/mathlib-quality), plugin
version 0.73.3, reviewed at commit
`7146cacdeb08b44e1ce15d63a95b421a8861f28d`.

The upstream MIT license, including its original `Copyright (c) 2024` notice,
is preserved verbatim in [LICENSE](LICENSE). The upstream repository is not a
runtime dependency. This port splits its development, proof, checking and
maintenance workflows into composable skills and replaces global hooks and
mandatory cleanup loops with scoped evidence gates.

The source study in `docs/design/2026-09-20-mathlib-quality-study.md` in the
agent-skills repository maps all upstream commands to the adopted or declined
behavior. Leanpowers is maintained in agent-skills; it is not an upstream
Mathlib or mathlib-quality endorsement.
