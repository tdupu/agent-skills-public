---
name: test-magma
description: Use when adding or reviewing Magma package, intrinsic, README-example, or regression tests.
---

Read the testing contract and existing Magma package policy. Preserve package
spec/dependency order, test-file naming, numbered README-test correspondence,
concrete assertions, and explicit `OK` output. Every README example that is
claimed executable should have a matching test or a recorded reason it cannot.

For a fixed bug, keep a minimal MRE and durable reference. Cover empty,
boundary, invalid, and representative algebraic cases without hiding slow or
data-dependent work. Run the narrowest Magma command available; report
proprietary/unavailable Magma rather than faking success. Existing
`improve-package-README` remains the documentation owner for README changes.
