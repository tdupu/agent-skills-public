# Docpowers

Invoke `using-docpowers` for documentation work across repositories, packages,
mathematical ecosystems, Gas City packs, and Claude/Codex skill packs. It
contains 16 catalogued skills and preserves existing Mathcity documentation skills
when their predicates match.

## Source and packaging

Canonical skills live at `agent-skills/skills/<name>/`; this directory contains
pack metadata. Build a standalone bundle from the repository root:

```sh
python3 scripts/build-docpowers.py /path/to/new/docpowers
```

The destination must not exist. The builder copies only the catalogue's
canonical skills and pack metadata, rejects symlinked source inputs, and writes
deterministic SHA-256 receipts. Generated bundle files are not editable source.

## Quality model

Documentation should make acquisition, installation, first use, examples,
appropriate API/developer/operations detail, provenance, license, date/status,
limitations, roadmap, navigation, and freshness evidence easy to verify. The
depth is proportional to the artifact; not every README becomes a manual.
Executable examples compose with Testpowers without recursively invoking its
router. See [SOURCES.md](SOURCES.md) for the reviewed upstream conventions.

## Status and limits

Version 0.1.0; created and reviewed 2026-09-23. Mathlib, Sage, M2, Magma,
Lean, LaTeX, and Gas City toolchains are optional: a route must report missing
tools rather than simulate a check. This pack does not publish, install global
hooks, or replace repository-local policy.
