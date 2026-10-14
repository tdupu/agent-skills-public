---
name: doc-math-latex
description: Use when documenting LaTeX packages, classes, expl3 code, l3doc sources, release metadata, or TeX repositories.
---

Read the documentation contract and inspect the repository's `l3doc`, README,
CHANGELOG, labels/citations, and `l3build` conventions. Put a minimal
copyable TeX example early, state engine/package prerequisites, and separate
user, implementation, and release documentation. Keep version/date and
license metadata synchronized with tags and build files.

Use `l3build` documentation/test targets when present. Check labels, links,
expected outputs, and generated artifacts without committing generated files
unless local policy says to. Report unavailable TeX engines honestly.
