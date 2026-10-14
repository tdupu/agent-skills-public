---
name: pd-section-walk
description: Walk an NSF Project Description with the PI one section at a time — display the section's prose with LaTeX stripped so the PI can annotate it, record every annotation verbatim, add the agent's own checked analysis, and hold all edits until the PI calls for revision (typically a grill-with-docs pass). Use for "walk the description with me", "show me the next section", "hold the comments", or when the PI replies with quoted-and-annotated proposal text.
---

# pd-section-walk

The PI reads; the agent displays, records and checks. Nothing in the
proposal changes during a walk unless the PI says to apply a comment now.

## Each section

1. **Display** the section's prose in chat: LaTeX stripped, math in Unicode,
   paragraphs tagged with short handles (`[P1]`, `[L2]`) so the PI can point
   at them. Keep theorem names and citations as `[Author year]`.
2. **Check before showing.** Run `pd-fact-check` on the section's claims
   first. Present a short analysis after the prose: what the files and
   papers show, with evidence. Ask the PI only what the evidence cannot
   settle (what to claim, what they personally verified, judgment calls).
3. **Record** the PI's annotations verbatim in the proposal folder's comment
   log (one table per section: id, quoted draft text, PI comment, status).
   Record the agent's own notes in a separate running list in the same file.
4. **Hold.** Do not edit the draft unless told. When the PI says "next", move
   on; when the PI says to stop, summarize what is open.

## Rules

- One section per message. Long sections may be split by subsection.
- Quote the PI's words exactly; do not paraphrase a comment into a softer one.
- A comment that asks a question ("what is X?", "is this true?") is a
  request for an answer from the files or literature, not for the PI to
  answer it.
- A comment that names a missing explanation becomes a writing task for the
  relevant leaf, not a definition dump in chat.
- When the walk ends, hand off to `grill-with-docs` (decisions) and then to
  the section leaves (writing), carrying the comment log as input.
