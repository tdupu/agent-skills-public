---
name: test-regression
description: Use when fixing a reported bug, preserving a historical failure, or recording a behavior that must never regress.
---

Read the testing contract. Preserve a durable bug reference: issue/commit,
short historical symptom, affected input/state, and the expected corrected
behavior. Reproduce the old failure with a minimal case before or alongside the
fix when practical, then assert the externally visible result and the relevant
negative/error behavior.

Do not delete the regression when the implementation changes. Keep the test
close to the owning component and make it deterministic. Record the runner
command, result, and any unavailable environment. If the bug exposed a public
usage/documentation mistake, hand off to `doc-examples` or `doc-api`.
