# Documentation contract

Use this contract for every documentation route. Scale the depth to audience,
risk, and artifact size; do not turn every README into a manual.

## Minimum questions

- Who is the reader and what decision or task should become easy?
- Where is the source of truth, and what is deliberately out of scope?
- Can a new user acquire, install, configure, and perform a first useful action?
- Is a realistic worked example near the beginning? Can it execute, or is the
  reason it cannot be executable explicit?
- Are API, developer, and operational details at the appropriate level?
- Are version/date, license, citation/provenance, support status, limitations,
  and planned work visible when relevant?
- Does navigation have one canonical home per topic and checked links?
- What evidence establishes freshness, and what is the shortest update path?

## Quality gates

Prefer one canonical explanation linked from smaller pages. Remove duplicated,
private, stale, and ornamental prose. Keep commands copyable and outputs
truthful. Examples must state prerequisites and expected observations. If an
example changes behavior, pair it with the repository’s appropriate test leaf.

## Handoff

Report changed paths, commands and results, unresolved gaps, unavailable
toolchains, and the next specialized route. For audits, report findings only;
do not silently mutate the repository.
