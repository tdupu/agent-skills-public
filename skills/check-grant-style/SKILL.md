---
name: check-grant-style
description: Audit an NSF Project Description and Summary against Grants/GRANT-STYLE.md (every project has a plan and names what is new; results in prose with citations; prior support itemized; broader impacts with a track record; banned dean-speak; "AI-assisted, human-driven"; only PI-verified claims; exact numbers). Use after drafting or revising any proposal text, before check-grant-format, or when asked "review the proposal", "is this too vague", "style check".
---

# check-grant-style

Audit of `proposal/tex/description.tex` and `summary.tex` against
`Grants/GRANT-STYLE.md` (S1–S14). Mechanical rules run by script; judgment
rules are read section by section, every violation quoted with file:line.
Never edit the proposal; report.

## Procedure

1. Read `Grants/GRANT-STYLE.md` and `Grants/GRANT-REVIEWS.md`; they are the
   authority. Register/structure rules (P1–P16) live in
   `using-pdpowers/references/PD-POLICY.md`; run its `check_pd_policy.py` first.
2. Run the mechanical pass:

```bash
python3 ~/.claude/skills/check-grant-style/check_style.py <folder>
```

   Covers S4 (prior-support fields), S5 (theorem-class environment count ≤ 2),
   S7 (gerund subsection titles), S9 (banned words), S10 (banned
   "AI-driven" strings; presence of "human-driven"/"AI-assisted"), S11 (every
   number has a row in `REVIEW.md` §3), S8 (every `\cite`-less result sentence
   "we proved/showed/established" maps to a PI-verified `REVIEW.md` §1 row).
3. Judgment pass, one `\subsection` of Proposed Research at a time:
   - S1: quote the plan; if none, FAIL with the subsection title.
   - S2: quote the "what is new" sentence; if it uses only
     extend/generalize/improve, FAIL.
   - S3: name the PI citation in the first paragraph; if absent, FAIL.
   - S12: for each result in the Overview, name the classical anchor.
   - S13: list partial results and check each names its obstruction.
   - S6: for each Broader Impacts item, quote the past-tense fact and the
     future-tense plan.
   - S14: if a sibling proposal exists in `Grants/NSF-<same year>-*`,
     diff the theorem/project/conjecture statements; any overlap FAILs.
4. Output: table `rule | PASS/FAIL | evidence (file:line, quote)`, then a
   prioritized fix list, S8 and S1 first.

## Pass criterion

No FAIL; judgment PASSes cite the quoted evidence, not assert it.
