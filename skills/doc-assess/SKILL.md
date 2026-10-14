---
name: doc-assess
description: Use when auditing documentation quality, completeness, freshness, audience fit, or discoverability before editing files.
---

Read `../using-docpowers/references/documentation-contract.md`. Inspect the
repository layout, policies, package metadata, source-of-truth files, links,
examples, version/date/license/citation claims, planned-work references, and
the documented verification command.

Do not edit. Produce a severity-ranked report with:

1. audience and task being served;
2. missing or misleading acquisition/install/use steps;
3. example coverage and whether examples are executable;
4. wrong-level, duplicated, stale, private, or bloated content;
5. broken or orphaned navigation;
6. provenance, license, version/date, support, limitations, and roadmap gaps;
7. exact evidence paths and the smallest useful follow-up route.

Prefer repository evidence over generic style advice. If a toolchain is absent,
record that as unavailable instead of guessing. A documentation audit is
complete only when another agent can choose an edit and a verification command
from the report.
