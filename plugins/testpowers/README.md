# Testpowers

Invoke `using-testpowers` for thoughtful test design across software, packages,
skills, packs, and mathematical ecosystems. It contains 17 catalogued skills
and routes by risk rather than assuming every request needs a unit test.

## Source and packaging

Canonical skills live at `agent-skills/skills/<name>/`; this directory contains
pack metadata. Build a standalone bundle from the repository root:

```sh
python3 scripts/build-testpowers.py /path/to/new/testpowers
```

The destination must not exist. The builder copies only the catalogue's
canonical skills and pack metadata, rejects symlinked source inputs, and writes
deterministic SHA-256 receipts. Generated bundle files are not editable source.

## Quality model

Every test states a falsifiable question, risk-matched layer, meaningful
oracle, boundary/error coverage, repeatability, command, scope, and limitation.
Fixed bugs retain durable regression tests. Coverage and green suites are
signals, not proof. Public behavior changes can compose with Docpowers after
test ownership is settled. See [SOURCES.md](SOURCES.md) for the reviewed
upstream conventions.

## Status and limits

Version 0.1.0; created and reviewed 2026-09-23. Sage, M2, Magma, Lean, LaTeX,
and other toolchains are optional: a route must report unavailable commands
and environments honestly. This pack does not install global hooks or promise
universal branch coverage.
