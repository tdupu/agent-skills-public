---
name: doc-math-sage
description: Use when documenting SageMath code, packages, tutorials, doctests, or a Sage repository.
---

Read `../using-docpowers/references/documentation-contract.md` and preserve
Sage's source-level docstring/reStructuredText and doctest conventions. Locate
the package README, module/class/function docstrings, tutorial/reference
structure, optional-feature markers, and `sage -t` commands. Put copyable Sage
examples early and include representative edge/error behavior where useful.

Prefer examples that serve as both user documentation and doctests. Keep
heavy, optional, or platform-dependent cases marked according to local
conventions. State Sage/Python version assumptions and cite mathematical
sources. Run the narrowest relevant doctest; if Sage is unavailable, report
the exact unavailable command. Existing `improve-documentation` or
`improve-package-README` owns matching Mathcity workflows.
