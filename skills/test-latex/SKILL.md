---
name: test-latex
description: Use when adding or reviewing LaTeX, expl3, l3build, typesetting, package, or golden-output tests.
---

Read the testing contract and local `l3build` configuration. Use focused test
files and expectation/reference outputs for stable behavior. Normalize only
intentional engine/version noise. Test compilation, errors, labels/citations,
and rendered or serialized output at the layer the change affects.

Record engine/format/version, command, expected result, and diff-review rule.
For historical failures keep a minimal test and bug reference. Report absent
TeX engines or fonts instead of inventing a pass. Pair changed public usage
with `doc-math-latex`.
