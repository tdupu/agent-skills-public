---
name: pd-project
description: Write one proposed-research project of an NSF Project Description — the PI result it builds on, the objective (the new theorem, object, database or tool), preliminary results at their true strength, a plan whose steps name their technique, feasibility, status lines that name obstructions, and what the project yields if its central question resolves either way. Use for "write project X", "rewrite this subsection", "the plan is unconvincing", "add feasibility".
---

# pd-project

A project subsection answers, in order: what does this build on, what will
exist afterwards that does not exist now, what is already in hand, how will
it be done, why is it feasible, and what if it fails.

## Parts, in prose (no casual run-in labels like "Built on:" or "What is in hand")

1. **Foundation** — first paragraph cites the PI's result(s) the project
   builds on, and the external theorems it uses.
2. **Objective** — one sentence naming the new theorem, object, database or
   tool. "Extend", "study", "investigate" alone fail.
3. **Preliminary results** — at their verified strength: "we proved",
   "computed", "agents report", "there is evidence". A compact table of real
   records (`pd-data-table`) when data is the evidence.
4. **Plan** — prose, or `\subsubsection`s when the project has distinct
   parts; a numbered list only for one proof program's lemmas (PD-POLICY P5).
5. **Feasibility** — what has already run and at what size, where the cost
   sits, what removes the bottleneck. Do not promise limits the PI has not
   chosen.
6. **Status and obstructions** — one sentence per partial result naming what
   is missing.
7. **Outcomes either way** — optional per project; or one section-level
   "expected outcomes and risks" subsection.

## Rules

- Title the subsection by the object or theorem, never by an activity.
- Name prior constructions and computations of the same kind, and say what
  is new relative to them.
- Predictions from a theory are cited to it ("Arthur's classification
  predicts …"), with scope; never stated as facts about the data.
- No bugs, stale data, or repair campaigns in proposal prose.
