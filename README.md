# agent-skills-public

Agent skills for research mathematicians: writing papers in LaTeX, checking
mathematics, formalizing in Lean, querying the LMFDB, teaching, writing NSF
grants, documenting and testing math software, and running AI-assisted
research with an honest provenance trail.

These are the skills I use every day with [Claude Code](https://claude.com/claude-code)
(most also work in Codex). They are published so other mathematicians can use
them, adapt them, and improve them.

## Quick start

Requirements: Claude Code (or another harness that reads `SKILL.md` skill
folders) and `git`.

```bash
git clone https://github.com/tdupu/agent-skills-public.git
mkdir -p ~/.claude/skills
cp -R agent-skills-public/skills/* ~/.claude/skills/
```

Copy only the packages you want if you prefer; each router lists the skills it
calls. Restart Claude Code, then try:

> Use latexpowers to review the introduction of `paper.tex` for unsupported claims.

The `using-latexpowers` router should load and pick a leaf skill such as
`check-latex` or `write-introduction`.

Many skills assume [Superpowers](https://github.com/obra/superpowers) is
installed. Install it from its own marketplace (preferred, so you get updates),
or use the copy in [`superpowers/`](superpowers/).

## Packages

Each package is a router skill (`using-<name>`) plus the leaf skills it routes
to. Start from the router; it decides which leaf applies.

| Package | Router | What it does |
|---|---|---|
| latexpowers | [`using-latexpowers`](skills/using-latexpowers/SKILL.md) | Write, revise, and check manuscripts: definitions, propositions, examples, introductions, citations, labels, figures, referee reports, AI-use statements. |
| mathpowers | [`using-mathpowers`](skills/using-mathpowers/SKILL.md) | Do and check the mathematics: find propositions, prototype and fill in proofs, hunt contradictions, search arXiv, Semantic Scholar, the Stacks Project, Mathlib, and the LMFDB. |
| leanpowers | [`using-leanpowers`](skills/using-leanpowers/SKILL.md) | Formalize natural-language mathematics in Lean 4 and Mathlib, with compiler evidence and source fidelity: define, decompose, prove, verify, golf, refactor, prepare PRs. See [`plugins/leanpowers`](plugins/leanpowers/). |
| lmfdb | [`search-lmfdb`](skills/search-lmfdb/SKILL.md), [`setup-lmfdb-pipeline`](skills/setup-lmfdb-pipeline/SKILL.md) | Query the LMFDB, and build a pipeline that moves data between Magma, text files, PostgreSQL, and LMFDB-style objects and pages. |
| teachingpowers | [`using-teachingpowers`](skills/using-teachingpowers/SKILL.md) | Set up a course: syllabus, course web page, LaTeX notes, lecture posts, assessments. |
| docpowers | [`using-docpowers`](skills/using-docpowers/SKILL.md) | Document repositories and math software (Sage, Macaulay2, Magma, Lean, LaTeX), skill packs, quick starts, examples, and APIs. See [`plugins/docpowers`](plugins/docpowers/). |
| testpowers | [`using-testpowers`](skills/using-testpowers/SKILL.md) | Choose and write tests: unit, regression, property, snapshot, and toolchain-specific tests for Sage, M2, Magma, Lean, and LaTeX. See [`plugins/testpowers`](plugins/testpowers/). |
| grantpowers | [`using-grantpowers`](skills/using-grantpowers/SKILL.md) | Assemble an NSF proposal package: budget, biosketch, data management, mentoring plan, references, Research.gov. Some leaves are specific to the University of Vermont (`gp-uvmclick`, `gp-spa-route`). |
| pdpowers | [`using-pdpowers`](skills/using-pdpowers/SKILL.md) | Write and review the NSF Project Description section by section, including review as a panelist would. |
| taucetipowers | [`using-taucetipowers`](skills/using-taucetipowers/SKILL.md) | Contribute issues and pull requests to the TauCeti Lean project. See [`plugins/taucetipowers`](plugins/taucetipowers/). |
| youtube-powers | [`youtube-powers`](skills/youtube-powers/SKILL.md) | Publish math lectures on YouTube: assemble takes, annotate, upload, fix descriptions and cards. |

Standalone skills:

| Skill | What it does |
|---|---|
| [`frontier-dump`](skills/frontier-dump/SKILL.md) | Send a research prompt to the best available frontier model and save a dated research dump under `ai/`. |
| [`harvest-dumps`](skills/harvest-dumps/SKILL.md) | Turn a pile of research dumps into a checked LaTeX manuscript. |
| [`adjust-behavior`](skills/adjust-behavior/SKILL.md) | Diagnose and fix an agent behavior you don't like, using `behavior-repro`, `behavior-cause`, and `behavior-verify`. |
| [`grilling`](skills/grilling/SKILL.md), [`grill-me`](skills/grill-me/SKILL.md), [`grill-with-docs`](skills/grill-with-docs/SKILL.md), [`domain-modeling`](skills/domain-modeling/SKILL.md) | Have the agent interview you to stress-test a plan. |
| [`critical-review`](skills/critical-review/SKILL.md) | Adversarial review of any artifact: a proof, a plan, a skill. |

## MCP servers

Several skills are faster and more reliable when an
[MCP](https://modelcontextprotocol.io) server gives the agent direct access to
a reference. See [`mcp/README.md`](mcp/README.md) for setup.

| Server | What it gives the agent |
|---|---|
| [`stacks`](mcp/stacks/) | Stacks Project tag statements, proofs, and keyword search (used by `search-stacks`). |
| [`scholar`](mcp/scholar/) | Semantic Scholar paper search, metadata, and citations (used by `search-scholar`). |
| [`lmfdb`](https://github.com/AndrewVSutherland/lmfdb-mcp) | Read-only SQL on a mirror of the LMFDB (used by `search-lmfdb`). Written and hosted by **Andrew V. Sutherland** at `https://mcp.lmfdb.org/mcp`; not included in this repository. |

## Repository layout

```
skills/        one folder per skill, each with a SKILL.md
plugins/       Claude and Codex plugin manifests for leanpowers, docpowers,
               testpowers, and taucetipowers
superpowers/   unmodified copy of obra/superpowers v6.4.1 (commit 5bf4e78)
mcp/           MCP servers for the Stacks Project and Semantic Scholar
```

## Limitations

- This is a snapshot copied from a private working repository, not the
  canonical source. Fixes may lag behind it.
- Some skills mention infrastructure that is not published here: the
  [mathcity](https://github.com/tdupu/mathcity) agent city, the `bd` (beads)
  issue tracker, and orchestration skills such as `mayor-math-handoff`. When a
  skill points at something missing, skip that step or ask the agent to adapt.
- The grant skills read institution-specific facts. The University of Vermont
  rates in `using-grantpowers/references/uvm-facts.md` were checked on
  2026-10-05; replace them with your own institution's.
- The LMFDB pipeline skills were written for one research database and use
  `$REMOTE_USER` and `$REMOTE_HOST` placeholders for the server.

## Credits

- **Superpowers** by Jesse Vincent and contributors,
  [obra/superpowers](https://github.com/obra/superpowers) (MIT). Superpowers
  supplies the skill format, the `using-*` router pattern, and the
  skill-testing discipline that all of these packages follow. The copy in
  [`superpowers/`](superpowers/) keeps its original [LICENSE](superpowers/LICENSE).
- **leanpowers** adapts the workflows of Chris Birkbeck's
  [CBirkbeck/mathlib-quality](https://github.com/CBirkbeck/mathlib-quality)
  (MIT), reviewed at commit `7146cac`. Its license is preserved in
  [`plugins/leanpowers/LICENSE`](plugins/leanpowers/LICENSE); see
  [`ATTRIBUTION.md`](plugins/leanpowers/ATTRIBUTION.md).
- **grilling**, **grill-me**, **grill-with-docs**, and **domain-modeling**
  come from Matt Pocock's [mattpocock/skills](https://github.com/mattpocock/skills).
- docpowers and testpowers list their sources in
  [`plugins/docpowers/SOURCES.md`](plugins/docpowers/SOURCES.md) and
  [`plugins/testpowers/SOURCES.md`](plugins/testpowers/SOURCES.md).
- **LMFDB MCP server** by Andrew V. Sutherland,
  [AndrewVSutherland/lmfdb-mcp](https://github.com/AndrewVSutherland/lmfdb-mcp)
  (GPL-3.0), hosted at `https://mcp.lmfdb.org/mcp`. The `search-lmfdb` skill
  uses it. Its code is not included here.

Skills by Taylor Dupuy, written with Claude.

## License

The `plugins/` packages and `superpowers/` are MIT-licensed; see the LICENSE
file in each folder. The `mcp/` servers are MIT-licensed, as declared in their
`pyproject.toml`. Third-party skills keep their upstream licenses.
