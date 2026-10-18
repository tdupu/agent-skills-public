---
name: contribute-to-tauceti
description: Use when an existing Lean development (a paper's formalization, a project repository) is to be contributed to Tau Ceti end to end, or such a contribution is resumed midway — triage, coordinating with roadmap authors, roadmap PRs, intentions, and the ordered series of code PRs through merge.
---

# Contribute an existing development to Tau Ceti

Input: the source repository at a pinned commit and the human's GitHub login. This skill
only orders the stages; each stage's rules live in the skill it names. Stages run per
target, so different targets can be at different stages.

0. **Consent and forks.** Confirm with the human that the source authors agree to the
   port; without agreement, verify the licence permits the copying and discuss the plan
   on the Lean Zulip first (TauCetiRoadmap README §Porting existing work). Creating the
   human's forks of TauCeti and TauCetiRoadmap, enabling issues, changing Actions and
   syncing a fork's `main` with upstream are remote writes: on authorization only.
1. **Triage** the source at the pinned commit: `tauceti-triage`.
2. **Coordinate.** Where triage finds an author who owns the text (usually an open
   roadmap PR), draft one comment to them: what the source proves and under which
   hypotheses, which targets nobody owns, and concrete options for ownership (their area
   keeps it; a separate area that theirs cites). Offer the human the options and ask what
   they want (comment rules: `using-taucetipowers`). Roadmap text that depends on the
   answer waits for it.
3. **Roadmap PRs** for targets on no merged roadmap: `roadmap-pr-tauceti`.
4. **Intentions** once a target's area has merged: `create-issue-tauceti`.
5. **Prepare code ahead** on the human's TauCeti fork, recorded in
   `<lean-workspace>/tauceti/code-prs/MANIFEST.md`, the single source for code-PR state:
   one row per topic in dependency order, with branch, head, roadmap target, intention,
   dependencies, gate result and PR, and each branch's draft body beside it. Branch
   rules: `pr-pipeline-tauceti` step 2.
6. **Open a PR** only when its roadmap target has merged, its claim is live and its
   dependencies are on `main`: `pr-pipeline-tauceti`. Improvements to merged code need
   no target or claim.
7. **Watch** CI and review, then follow-up PRs: `pr-pipeline-tauceti` step 6.
8. **After merge**, tell the human to close the intention (`create-issue-tauceti`), and
   update the manifest and tracker.

**Tracker.** Keep one public tracking issue on the human's TauCeti fork. Its code-PR
table is copied from the manifest, never edited separately; it also lists stages and
roadmap PRs. Put upstream references (`owner/repo#N`) and logins in backticks, so the
tracker pings nobody and adds no backlinks to upstream threads. Mark it :robot: with the
model. Creating it needs the human's authorization; a standing one covers later edits.

**Fork Actions.** Upstream workflows fail on the fork and email the human on each push.
Recommend disabling GitHub Actions on the fork; it is the human's call, or done on their
direct authorization.

Browser help with GitHub forms: `using-taucetipowers/references/github-forms.md`.
