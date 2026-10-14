---
name: doc-math-magma
description: Use when documenting Magma packages, specs, intrinsics, README examples, or Magma package repositories.
---

Read the documentation contract and the existing `improve-package-README`
skill. Preserve local Magma package policy: package header, dependency/spec
order, README sections, concrete examples, numbered README-test correspondence,
and explicit expected assertions. Do not impose this convention on other
ecosystems.

Trace each public example to its package/spec source and a runnable test. Keep
slow/data-dependent cases marked as local policy requires. Include acquisition,
AttachSpec/load path, first use, version/date/license/citation, limitations,
and planned work. Run the narrowest Magma command available; proprietary or
missing tools are reported as unavailable.
