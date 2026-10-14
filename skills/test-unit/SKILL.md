---
name: test-unit
description: Use when adding or repairing fast isolated tests for local functions, classes, transformations, intrinsics, or small modules.
---

Read the testing contract. State the falsifiable behavior question and choose
inputs that distinguish the implementation from a tautology. Cover a normal
case plus plausible empty, boundary, invalid, and error cases; keep the test
isolated from network, clock, filesystem, and global state unless those are the
behavior under test.

Assert externally meaningful values, errors, or state transitions. Avoid
asserting implementation call counts as the sole signal. Follow local naming,
fixtures, and runner conventions. Record the exact command, expected signal,
scope, cost, and limitation. If the failure crosses a component seam, hand off
to `test-integration` rather than forcing a unit test.
