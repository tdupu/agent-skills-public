---
name: roadmap-pr-tauceti
description: Use when a TauCetiRoadmap pull request — a new roadmap area, or an addition to an existing area — must be drafted, checked, pushed to the human's fork and handed over for the human to open, including deciding how material splits across areas and writing the PR body.
---

# TauCetiRoadmap pull request

Agents never open TauCetiRoadmap PRs or issues (Tau Ceti `AGENTS.md`); the human does.
First read TauCetiRoadmap README §Writing a roadmap, §Porting existing work, §Filing a
roadmap and `CONTRIBUTING.md` at a recorded commit. `draft-roadmap` supplies the
decomposition and the evidence rules for every library name.

**Where.** Drafts live in the source repository, one folder per PR under
`<lean-workspace>/tauceti/roadmap-prs/` (`lean-project` locates the workspace; with
none, `<repo>/tauceti/`). A new area: its `README.md`, `Suggested.lean`,
`metadata.toml`. An addition to an existing area: a patch against a recorded upstream
commit plus the changed sections, no `metadata.toml`. Both: the PR body and `NOTES.md`.
Status words, review records, authors' answers and open questions go in `NOTES.md`,
never in the text to be filed. `Suggested.lean` is not a module of the source: keep it
out of every `lean_lib` and out of public submissions. A roadmap clone or worktree is
scratch.

**Content.**
- Targets are stated primarily in library vocabulary (Mathlib and Tau Ceti at the
  roadmap repository's pins). Stacks-form restatements with proved equivalences may be
  added as accompanying targets, with `@[stacks]`, where they aid reuse: propose them,
  ask the area author, and record the answer in `NOTES.md`.
- Fetch every Stacks tag cited and compare its statement, hypotheses included. A tag
  wrong as written gets a stated correction and a Check.
- Material two new areas both need can go into a separate prerequisite area that both
  cite, or the earlier area can own it; ask the area authors. Additions to a merged
  area's sections go as separate small PRs that ask that area's author.
- Cite other roadmaps by name and section; state the merge order in each PR body.
- Put the map from targets to the source code in a provenance section, clearly
  secondary.

**Before handing over.**
1. Re-fetch upstream `main`; in a fresh worktree of it with only this PR's change
   added, run `lake exe cache get` and `lake build TauCetiRoadmap.<Area>.Suggested`:
   only `sorry` warnings. Remove the worktree.
2. Run the repository's checks (`.github/scripts/check_roadmap_topics.py` and its tests).
   `check_roadmap_areas.py` fails for a new area until the sync bot runs after merge;
   that is expected, and the generated lists stay untouched.
3. Run at least one independent adversarial mathematical review that fetches the tags
   (`critical-review`, or a fresh subagent), graded BLOCKING / SHOULD / NIT. Fix every
   BLOCKING and SHOULD; keep the review beside the draft.
4. On authorization, push a branch to the human's fork with a create-only lease
   (`pr-pipeline-tauceti` contract) and give the human the compare URL
   `https://github.com/TauCetiProject/TauCetiRoadmap/compare/main...<login>:<fork-repo>:<branch>?expand=1`,
   the title and the `awaiting-review` label (if the human cannot apply labels yet, the
   body says so, per CONTRIBUTING). The human opens the PR.

**PR body.** Top: a visible placeholder for the human's own note,
`**[HUMAN NOTE: who selected the scope, which models were used, and that you read this
text. Replace before opening.]**`. Then a :robot: line naming the model and saying an AI
agent working for the human drafted what follows. Never write in the human's voice.
Fill in sibling PR numbers once they are known.
