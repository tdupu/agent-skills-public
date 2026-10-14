---
name: test-integration
description: Use when testing a meaningful seam between modules, packages, filesystems, databases, services, compilers, or external tools.
---

Read the testing contract. Name the seam and the failure that a unit test
cannot detect. Use the smallest real components and controlled fixture; avoid
mocking the very boundary whose compatibility matters. Cover successful data
flow, malformed/empty input, timeout or unavailable dependency where relevant,
and cleanup/repeatability.

Record setup, teardown, environment, runner command, expected signal, cost, and
whether the test is opt-in or required. Keep credentials and private data out
of fixtures. If the test is only install/user-path confidence, hand off to
`test-entrypoint` or `test-smoke`.
