# Tau Ceti contribution contract

Read this with the target checkout's current policy files; live instructions win.
Last checked against TauCeti `fcfb0af` and TauCetiRoadmap `350e970` (2026-10-17).

## Scope and attribution

- Read `AGENTS.md`, `README.md`, `COORDINATION.md`, and the PR template. `TauCeti/`
  is AI-authored mathematics. `scripts/`, `.github/`, and the lakefile are
  human-owned; `lake-manifest.json` and `lean-toolchain` are exceptions only for
  validated forward bumps.
- One topic per PR, never stacked (drafts included): open a dependent only after
  its prerequisite lands on `main`. New declarations, definitions, instances,
  notation, or files need an exact `TauCetiRoadmap` target or a demonstrable
  prerequisite. Refactors, proof simplifications, modest generalizations,
  relocations, and documentation improvements need no new target but name the
  motivating area.
- Use one standalone `Roadmap: CanonicalAreaName` or `Roadmap: none`. `none` is
  only for genuinely general, cross-cutting, infrastructure, or dependency work;
  do not infer an area from a `TauCeti/` path. New math cites the exact roadmap
  file and target in the body.

## Coordination and branch safety

- Before authoring a roadmap target, find a live claim: an unexpired intention
  the requesting human filed and holds, or our worker lease key
  `author/<focus>/<target-id>`; another owner's live claim stops. The PR
  marker is:

  ```text
  <!--tauceti-target:v1 {"focus":"<area>","id":"<canonical-target-id>"}-->
  ```

  The id is deterministic, not a nickname. If the claim cannot be verified,
  report a blocker; never invent success.
- Record the observed head before writing. New branch (create-only):

  ```sh
  git push --force-with-lease=<branch>: <remote> HEAD:<branch>
  ```

  Existing branch (exact ref and observed oid):

  ```sh
  git push --force-with-lease=<headRefName>:<observed_oid> \
    <remote-url> HEAD:<headRefName>
  ```

  A stale lease is a safe failure: re-observe, never plain or force push.

## Review and merge

- A review applies only to the current `head_sha` in the newest canonical comment
  marked `tauceti-scoreboard` with its `tauceti-meta:v1` block. Missing or stale
  marker means unreviewed. New commits require fresh review.
- `tauceti-review PR` is read-only by default; `--post` publishes and needs
  explicit authorization. The agent's job ends at green CI and every blocking
  rubric green for the current head; merge, close and dedup belong to the repo's
  CI and bors. Never `--admin`.

## Mechanical quality floor

Check path scope, reuse, truthful statements, placement, naming, docs, and each
rule in `AGENTS.md` §The rules of the repo at the observed commit. Run pinned
Lean checks, applicable linter, `lake build`, and axiom/full-type inspection.
Record exact commands and revisions. A passing build is not formalization,
roadmap, or review approval.
