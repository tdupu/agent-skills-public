# Leanpowers

Invoke **using-leanpowers** for natural-language mathematics → Lean, Lean
maintenance, or a formalization audit. It routes to 26 smaller skills, catalogued
below. [`skills.json`](skills.json) is the machine-readable list the builder
consumes; the routing table itself lives in `skills/using-leanpowers/SKILL.md` in a
built plugin.

The workflow keeps compiler correctness and faithfulness to the source as
separate gates. It records exact statements, definitions, assumptions, target
coverage, axiom dependencies and evidence freshness. A successful build alone
does not mean a manuscript is formalized.

## Source and packaging

Canonical skills live at `agent-skills/skills/<name>/`; this directory contains
package metadata. Build a standalone plugin from the repository root:

```sh
python3 scripts/build-leanpowers.py /path/to/new/leanpowers
```

The destination must not exist. The builder copies the catalogue's canonical
skills and references, both plugin manifests, license and attribution. It rejects
symlinks and writes deterministic SHA-256 source receipts. No sibling repository
or development checkout is needed by the resulting plugin. Install that built
directory using your host's local-plugin mechanism; this source metadata folder
is not itself a complete installable bundle.

## Catalogue

The 26 routed skills, grouped by the phase they serve. One-line purposes are
condensed from each skill's own `description:` frontmatter, which is canonical —
consult the skill itself before relying on a summary here.

**Coordinate**

| Skill | Purpose |
| --- | --- |
| `lean-workflow` | Coordinate or resume a multi-step formalization, or a combined maintenance request |
| `lean-status` | Report what is formalized, what is blocked, what remains, and whether evidence is current |

**Set up**

| Skill | Purpose |
| --- | --- |
| `lean-project` | Add or locate the workspace; fix its paths, including the registry manifest |
| `lean-doctor` | Establish the build baseline before edits, maintenance or upgrades |
| `lean-upgrade` | Change a Lean or Mathlib version, and handle the resulting compatibility failures |

**Plan the formalization**

| Skill | Purpose |
| --- | --- |
| `lean-extract-claims` | Inventory what a manuscript or proof actually claims |
| `lean-design-definitions` | Choose Lean representations for the objects, structures and notation |
| `lean-decompose` | Split a multi-step proof into helper lemmas and prerequisites |

**Write**

| Skill | Purpose |
| --- | --- |
| `lean-define` | Implement agreed definitions, structures, classes and instances |
| `lean-align-statement` | Translate one assertion into a Lean type, or check a proposed statement before proving |
| `lean-search` | Find an existing library lemma, instance or equivalent formulation first |
| `lean-prove` | Prove one aligned theorem or ready obligation |
| `lean-diagnose` | Handle an actual error, a stalled tactic, a build regression or an unexpected goal |

**Check** — two separate gates; a green build settles only the first

| Skill | Purpose |
| --- | --- |
| `lean-verify` | Compiler evidence: build, target coverage, axioms — before reporting anything as checked |
| `lean-fidelity` | Source match: do the declarations represent the manuscript's claims? |
| `lean-review` | Review changes, a handoff, representation choices, or a contribution candidate |

**Improve**

| Skill | Purpose |
| --- | --- |
| `lean-style` | Formatting, naming, documentation, imports |
| `lean-golf` | Simplify a working proof without changing its statement or context |
| `lean-generalize` | Weaken assumptions or broaden types, one change at a time |
| `lean-refactor` | Rename, extract helpers, split modules, restructure dependencies |
| `lean-profile` | Slow elaboration, resource limits, explicit performance work |

**Present and contribute**

| Skill | Purpose |
| --- | --- |
| `lean-unformalize` | Render a Lean declaration back into ordinary mathematics |
| `lean-blueprint` | Create or synchronize a blueprint and its dependency presentation |
| `lean-mathlib-fit` | Assess whether a declaration belongs in Mathlib, or is already supplied |
| `lean-prepare-pr` | Assemble a contribution for review and submission readiness |
| `lean-apply-feedback` | Apply review comments and reconcile requested corrections |

### Verifying the catalogue

`skills.json` and the skills on disk are expected to agree exactly, and the
builder fails on a name it cannot resolve. To check both directions, and that the
routing table names nothing uncatalogued, from the repository root:

```sh
python3 - <<'EOF'
import json, os, re
cat = set(json.load(open('plugins/leanpowers/skills.json')))
disk = {d for d in os.listdir('skills') if d.startswith('lean-') or d == 'using-leanpowers'}
router = open('skills/using-leanpowers/SKILL.md').read()
print("on disk, uncatalogued:", sorted(disk - cat) or "none")
print("catalogued, absent from disk:", sorted(cat - disk) or "none")
print("routed but uncatalogued:",
      sorted(r for r in re.findall(r'`(lean-[a-z-]+)`', router) if r not in cat) or "none")
EOF
```

All three report `none` as of 2026-09-24, at 27 catalogue entries — the router
plus the 26 it routes to.

## Composition

Superpowers supplies process discipline, Mathpowers handles informal mathematics,
Latexpowers handles manuscript prose, and Leanpowers handles formal artifacts.
They retain one coordinator, one scope and the same claim IDs. Peer plugins are
optional for standalone Lean work; a missing peer blocks its own operation and
must be reported. Use plain or host-qualified installed skill names.

Read `AGENTS.md`, `LAYOUT.md` and the existing toolchain first. Prefer root `lean/`
beside `latex/` when adding formalization; retain an established `formal/`, Lake
workspace or other repository convention. Keep generated evidence in the
repository's scratch area. Do not overwrite a layout policy to impose a template.

## Evidence and limits

Lean and Lake are required to claim a checked proof. Mathlib is required only for
targets using it. LSP servers, hosted search, blueprint tooling and Mathcity are
optional. Search has local source and CLI fallbacks. Toolchain installation and
upgrades respect the user's scope and repository pin.

LeanSearch and Loogle MCP provide Mathlib candidate lookup; Stacks MCP supplies
tagged informal statements/proofs. The Lean search workflow also routes bounded
lookups to Palomar's versioned registry and pinned Tau Ceti source/roadmap
surfaces, while keeping their provenance and verification states separate from
Mathlib declarations. The bundled `search-tools.md` reference documents
discovery, setup and direct HTTP/CLI fallbacks. MCP servers are optional external
tools, not bundled runtimes. The tested Lean MCP 0.30.0 needs Lean >=4.24 for LSP;
older projects retain their pin and use CLI validation.

`FORMALIZED` requires both current compiler evidence and a checked source match;
`LEAN-PROVED`, `CONDITIONAL`, `REFUTED`, `BLOCKED` and `STALE` preserve distinctions.
Usual Lean logical axioms and native evaluation trust are recorded separately
from admitted proofs and unproved domain assumptions. See the bundled
`skills/lean-workflow/references/` for the evidence contract.

This is an agent workflow, not an automatic guarantee that arbitrary research
mathematics can be formalized. Development probes and review transcripts stay
under ignored `ai/leanpowers-2026-09-20/`; durable design and validation summaries
live under `docs/`.
