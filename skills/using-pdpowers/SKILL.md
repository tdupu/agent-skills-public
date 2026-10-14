---
name: using-pdpowers
description: Routing skill for writing, revising, walking, fact-checking and checking an NSF Project Description (and its Project Summary). Use for "write the project description", "revise the proposal", "walk the description with me", "fact-check the proposal", "write the prior support / broader impacts / AI statement", "fill the remaining pages", or any request about NSF proposal prose. Routes each request to one pd-* leaf skill or to the grant checkers; the leaves encode how proposal writing differs from manuscript writing.
---

# using-pdpowers

A Project Description is read once, fast, by a panel mostly outside the subject,
and judged on what it will produce, whether the PI can do it, and whether every
claim can be trusted. Announce the route, then follow the leaf; leaves do not re-route.

## Contracts and precedence

Before any edit, locate the proposal folder and read, in order:
1. The PI's current instructions in the conversation.
2. The grants workspace's decision records and contracts when they exist
   (`CONTEXT.md`, `docs/adr/`, `GRANT-STYLE.md`, `GRANT-FORMAT.md`).
3. The proposal folder's `REVIEW.md`, `COMMENTS.md` and `reviews/`.
4. The solicitation and the PAPPG chapter it defers to. Check page limits
   there; do not take them from memory.

The PI's instructions win; then the contracts; then these skills. No leaf
states a result the evidence does not support, whatever the instruction.

## Dispatch

| Situation | Route |
|---|---|
| New proposal folder from a template | `create-nsf-grant` (scaffold), then the leaves below per section |
| "Walk the description with me", "show me the next section", PI annotations | `pd-section-walk` |
| "Is this true?", claim/number/citation/pinpoint checks, "check the dates" | `pd-fact-check` — run it before asking the PI anything a file or paper can answer |
| Decisions the draft depends on (headline, scope, what to cut) | `grill-with-docs`, recording ADRs and glossary terms; then return here |
| Overview / headline / solicitation framing | `pd-overview` |
| Background, definitions for the panel, prior literature, classical anchor | `pd-background` |
| Worked example, table of real records | `pd-data-table` (inside the section that needs it) |
| Software and AI assistance statement for the proposal itself | `pd-ai-statement` |
| Results from Prior NSF Support | `pd-prior-support` |
| One proposed project (foundation, objective, preliminary results, plan, feasibility, risks) | `pd-project` |
| Method, tools, orchestration, records, due diligence | `pd-method` |
| Broader Impacts | `pd-broader-impacts` |
| Project Summary | write last, from the finished description: `pd-overview` rules, one page, three headed parts, third person |
| Reviewer-perspective pass (one subagent per role or named reviewer) | `pd-review-as`; reviewers from `gp-potential-reviewers` |
| Apply a comment log or review tables to the draft | `pd-apply-feedback` |
| “Is this paragraph good?” / paragraph-by-paragraph pass over the description | `check-paragraph` — one subagent per paragraph via its `split_paragraphs.py`, reader = NSF panelist outside the subject; verdicts to `reviews/paragraphs-<file>-<date>.md`, no edits |
| Policy audit (`references/PD-POLICY.md`, P1–P17) | `python3 scripts/check_pd_policy.py <description.tex>` (mechanical rules), then the [J] rules by hand |
| Style / format audit (pages, fonts, headings, URLs, build) | `check-grant-style` / `check-grant-format` |
| "Sounds like AI", "too many claudeisms", de-slop (P17) | `purge-claudisms` — scan, rewrite hits in place, rescan to zero; before the style audit |
| Mathematics that needs proving or a research gap | `using-mathpowers`, then return here |
| Any other proposal document (references, data plan, facilities, budget and justification, COA, biosketch, current and pending, mentoring), Research.gov, UVMClick, SPA routing, package review | `using-grantpowers` |
| A manuscript, not a proposal | `using-latexpowers` |

## Floors every leaf enforces

- **Only verified claims are results.** Published, submitted with the
  statement untouched by referees, or checked by the PI. Agent output the PI
  has not checked is "agents report …" or is held in `REVIEW.md`.
- **Prose for the PI's results; environments for the panel's anchors.** Main
  definitions in `definition`, main conjectures in `conjecture`, at most two
  `theorem`s; the PI's own results in prose with citations (PD-POLICY P2–P3).
- **Exact, sourced numbers.** Every number has a `REVIEW.md` row with its
  source and date.
- **Register.** Third person ("the PI", "this proposal"); direct, plain; no
  hype, no sentence whose only content is importance, no run-in labels or
  step lists (P1, P4, P5, P12). "AI-assisted, human-driven".
- **Define for the panel.** Every term a non-specialist panelist would not
  know is defined once, where first used, in one sentence.
- **Show the data.** Prefer a small table of real, verified records over a
  description of a schema.
- **No process in the mathematics.** "We initially believed", earlier drafts,
  and model chatter belong only in the AI statement.

## Finish

After each batch of edits: build; run `purge-claudisms`, `check_pd_policy.py`,
`check-grant-style` and `check-grant-format`; confirm the page limits from the
solicitation; update `REVIEW.md`; report what changed, what is unverified, and
what the PI must decide. Never commit, push, or submit unless the PI asks.
