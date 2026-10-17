---
name: tauceti-triage
description: Use when existing Lean work must be checked against Tau Ceti before contributing it — which targets the roadmaps already own, what TauCeti or open mathlib4 PRs already provide, and who else is working on it. Read-only.
---

# Tau Ceti triage

Input: a Lean source at an exact commit and pin. Output: one decision per target
of the source, with evidence. Nothing is posted, pushed, filed or opened; drafts
of comments or intentions go to `using-taucetipowers` routes.

Read the current TauCeti `AGENTS.md`, `README.md`, `COORDINATION.md` and the
TauCetiRoadmap `README.md` and `CONTRIBUTING.md` first; they define what a target,
a claim and "never wait for Mathlib" mean. Record every source with a commit,
PR head SHA or fetch time:

- merged roadmap targets on TauCetiRoadmap `main`, and open roadmap PR heads
  (a target in an open PR authorizes nothing yet but shows who owns the text);
- intention issues, all states, and their claims;
- TauCeti `main` and open TauCeti PRs (`tauceti-target` markers, claim refs);
- open mathlib4 PRs, and Mathlib at TauCeti's pin.

Per target, one outcome: **adopt** an existing TauCeti/Mathlib object (ours is
deleted or bridged by an equivalence); **build in the shape of** an open mathlib4
PR (never wait for it); **coordinate** with an open TauCeti PR, intention or
roadmap PR author; **not on a merged roadmap** (route to `draft-roadmap`); or
**first-PR candidate**, with its size, prerequisites and landing order (no
stacking). Absence claims follow `draft-roadmap`'s evidence rules: a positive
control and a leaf-name search, not one keyword query.

Write the report in the source repository (`ai/<date>-tauceti-triage/` or
`<lean-workspace>/tauceti/`), marking each fact verified or unverified. Worked
example: `tdupu/pcf` `ai/2026-10-17-tauceti-triage/` (CODE, ROADMAP, MATHLIB,
PLAN) with `lean/tauceti/INTAKE.md` and `CONFLICTS.md`.
