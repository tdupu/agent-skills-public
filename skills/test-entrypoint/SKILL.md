---
name: test-entrypoint
description: Use when validating the documented install, CLI, package import, REPL, build, or other user entrypoint end to end.
---

Read the testing contract. Start from the documented quickstart and execute it
in a clean or explicitly described environment. Verify acquisition/install,
configuration, first useful action, expected output, and clean exit. Do not
silently substitute an internal API for the user path.

Keep the scenario short and deterministic. Record versions, command, exit code,
observed result, cleanup, cost, and limitations. If the documentation and
entrypoint disagree, preserve the evidence and hand off to `doc-quickstart`.
