# Taucetipowers

Invoke **using-taucetipowers** for work intended for
`TauCetiProject/TauCeti`. It routes issue drafting to `create-issue-tauceti`,
Lean contribution work to `pr-pipeline-tauceti`, read-only triage of
existing work to `tauceti-triage`, TauCetiRoadmap PR drafting and hand-off to
`roadmap-pr-tauceti`, and contributing an existing development end to end to
`contribute-to-tauceti`, while composing with Leanpowers for formalization,
verification, and feedback.

The package is policy-driven: it reads the target checkout's current rules and
live GitHub templates, requires exact roadmap attribution for new mathematics,
preserves Tau Ceti's coordination/lease contract, and treats build evidence,
review state, and remote writes as separate gates. Issue filing stops for exact
body approval. PR preparation stops at a readiness report unless the requested
remote action is explicitly authorized.

Canonical skill sources remain under `agent-skills/skills/`; this directory is
package metadata. Do not edit generated plugin copies. No Tau Ceti-specific MCP
is bundled; optional LeanSearch and Loogle remain Leanpowers capabilities, with
Palomar registry and pinned Tau Ceti source/roadmap lookup documented as
separate search channels and with direct fallbacks.
