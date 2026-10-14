---
name: doc-examples
description: Use when writing, repairing, or auditing realistic worked examples, tutorials, doctests, or examples embedded in API documentation.
---

Read the documentation and testing contracts. Start from a user task, not an
isolated method call. Make the smallest example useful, copyable, and honest:
state prerequisites, inputs, expected observation, failure behavior where
relevant, and the next step. Put a representative example near the beginning
of the document and link advanced variants.

Use the local executable-example convention. If the example is code, route its
verification to the appropriate test leaf after documentation ownership is
settled. Prefer several small examples over one opaque script. Avoid output
that depends on timestamps, paths, randomness, or private data unless it is
normalized and explained.

Return the example inventory, changed paths, command/result evidence, and any
example that remains illustrative rather than executable.
