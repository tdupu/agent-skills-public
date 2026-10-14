---
name: doc-quickstart
description: Use when adding or repairing acquisition, installation, configuration, first-use, or quickstart documentation.
---

Read the documentation contract. Identify the intended audience, supported
versions, prerequisites, source checkout or package-install path, configuration
inputs, and the first useful command. Inspect existing README, release, and
install conventions before editing.

Put a copyable worked example early. State expected output or an observable
result, and distinguish optional features from the happy path. Use the
repository's real runner or package manager; do not invent commands. Link to
the canonical API/developer/operations pages instead of duplicating them.

When the example is executable, pair it with `test-entrypoint`, `test-smoke`,
or the ecosystem test leaf. Preserve read-only scope for audit requests.

Return changed paths, the exact verification command and result, supported
environment, unresolved prerequisites, and links to deeper documentation.
