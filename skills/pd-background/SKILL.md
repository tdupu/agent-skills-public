---
name: pd-background
description: Write the background and foundations section of an NSF Project Description for a mixed panel — the objects, the classical theory being generalized, the definitions a non-specialist needs (one sentence each, at first use), the prior literature on the same objects, and one worked example with real data. Use for "write the background", "they won't know what X is", "explain X", "add an example".
---

# pd-background

The background exists so that every later section can be read by a panelist
outside the subfield. It is not a survey and not a paper's introduction.

## Contents, in order

1. **The objects**, with notation fixed once, and a sentence that heads off
   the most likely misreading (e.g. a group that looks like a familiar one
   but is not).
2. **What already exists on these objects**: cite earlier work on the same
   groups/spaces before stating what the PI's work added. Never write as if
   the objects began with the PI.
3. **The classical theory and what it predicts**, with the named theorems
   (S12-style classical anchors) and their exact scope: weight, level,
   field, hypotheses, conditional or not.
4. **Definitions for the panel**: each term the later sections rely on
   (e.g. cuspidal/Eisenstein, Hecke eigensystem, tempered, Satake parameters,
   packets, inner forms, real loci) gets one plain sentence where first used.
5. **One worked example** with real, verified data (`pd-data-table`): a label
   unpacked field by field, a small table of values, and the diagnostic it
   illustrates.
6. **The Software and AI assistance statement** at the end
   (`pd-ai-statement`), when the PI places it here.

## Rules

- Cite theorems with pinpoints only after `pd-fact-check` verified them.
- Restate at most one classical theorem in an environment; the rest is prose.
- Every definition is used later; delete definitions nothing depends on.
- Do not explain the route to results here (no "we first tried").
