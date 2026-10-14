---
name: test-smoke
description: Use when checking that an installed package, pack, command, service, or project starts and performs one representative useful action.
---

Read the testing contract. Choose the smallest user-visible path that proves
the artifact is installed, discoverable, configured, and minimally functional.
Use real packaging/entrypoint boundaries; keep the action fast and avoid
claiming broad correctness from it.

State prerequisites, cleanup, command, expected output/exit code, environment,
and what the smoke test does not cover. Make failures diagnostic. Pair it with
deeper unit/integration tests as needed and hand off user instructions to
`doc-quickstart` when the path is public.
