# Project Description Policy

Parent: `using-pdpowers/SKILL.md`. Companion to the grants workspace's
`GRANT-STYLE.md` (S-rules) and `GRANT-FORMAT.md` (F-rules); the P-rules
below cover what those do not. P17 is checked by `purge-claudisms`. Checker: `scripts/check_pd_policy.py
<description.tex>` runs every rule tagged [M]; [J] rules are read by the
agent, section by section, quoting file:line. Pass means no FAIL.

| Field  | Value      |
| ------ | ---------- |
| Status | Draft      |
| Date   | 2026-10-12 |
| Prefix | P          |

## Rules

**P1 — Third person [M].** The document speaks as "the PI", "this
proposal", "the project". No "we propose", "our".
- Pass: zero matches of `\bwe propose\b`, `\bour\b` outside comments and
  `\taylor{}` markers. Remaining `\bwe\b` are listed for judgment.

**P2 — Main definitions in a `definition` environment [M-heuristic, J].**
Every term a project depends on (the object in a subsection title, the
object a theorem is about) is defined in `\begin{definition}`.
- Pass: no sentence of the form "A/An \emph{X} is …" or "… is called a/an
  \emph{X}" outside a `definition` environment refers to a load-bearing
  term. The checker lists candidates as CONFIRM; the agent decides.

**P3 — Main conjectures in a `conjecture` environment [J].** A conjecture a
project attacks or a section is organized around is stated in
`\begin{conjecture}` with attribution and date; not paraphrased in prose.
- Pass: every "Conjecture" named in prose has an environment; GRANT-STYLE S5
  exempts `conjecture` from the two-environment cap.

**P4 — No scaffolding labels [M].** No run-in labels `\emph{Built on:}`,
`\emph{What is new.}`, `\emph{Plan.}`, no paragraph opening with a bold
label `\textbf{Students.}`, and no sentence announcing "what is new"; the
objective sentence says it.
- Pass: zero matches of `\emph{(Built on|Where it stands|What is new|
  Plan.|Deliverables)`, of a line-initial `\textbf{...[.:]}`, and of
  `what is new` outside comments.

**P5 — No fixed-count step lists outside a proof program [M, J].** Plans
are prose or `\subsubsection`s. A numbered list appears only when the
items are the steps of one argument (a proof program), and then has as many
items as the argument has.
- Pass [M]: zero `\item[Step`. Pass [J]: every `enumerate` inside Proposed
  Research is a proof program, not a work plan.

**P6 — Topic-sentence paragraphs [J].** Each paragraph opens with the
sentence it is about; a new topic starts a new paragraph.
- Pass: for each paragraph of Background and Proposed Research, the first
  sentence states the paragraph's claim.

**P7 — No referee comments [M].** Nothing a referee of a submitted paper
wrote appears, paraphrased or quoted.
- Pass: zero matches of `referee` outside comments and markers.

**P8 — No private notes [M, J].** No appeal to notes, drafts, or files the
panel cannot read ("in our notes", "the PI's notes show").
- Pass [M]: zero lines pairing `notes?` with `our|the PI's|private|
  unpublished|in preparation`. Pass [J]: every evidence pointer is a
  citation, a public repository named in words, or a table in the text.

**P9 — Dated events [J].** Every event and status carries a date or year
("as of September 2026", "submitted in 2025"); no "recently", "currently",
"last year", "now", "soon".
- Pass: the checker's list of relative-time words is empty or each hit is
  justified; every status line in Proposed Research has a date.

**P10 — Award numbers [M].** A prior award is named by number
(`DMS-NNNNNNN`), never "the previous grant" or "the 2024 award".
- Pass: zero lines matching `(previous|prior|last|earlier) (award|grant|
  proposal)` or `the 20\d\d award` without `DMS-\d{7}` on the same line.

**P11 — Short solicitation quotes [M].** The solicitation is quoted at most
once and briefly; its language is otherwise paraphrased or simply met.
- Pass: no quoted passage (``…'' or "…") of more than 25 words.

**P12 — State practices; do not preach [M, J].** The method section says
what is done and how it is recorded. No exhortation, no philosophy of
practice, no sentence whose content is that something matters.
- Pass [M]: zero matches of `it is (important|essential|crucial|vital|
  imperative)`, `we believe`, `best practice`. Pass [J]: every sentence of
  Method and Standards names a practice, a record, or a check.

**P13 — Items are labelled and referenced [M].** Every `\item` in an
`enumerate` that prose refers to carries `\label{item:…}`, and prose refers
to it by `\eqref{item:…}` (or `\ref`), never "item 3" or "items 3--8".
- Pass: zero prose matches of `\bitems? \d` or `\bitems? \\ref`; zero
  `\item` without `\label` inside the Results from Prior NSF Support
  enumerate.

**P14 — Senior people named fairly [J].** Every project names the people
whose results or problems it uses (including senior figures likely to sit
on the panel), with citations, and nothing in the text diminishes a named
person's work. Check against `submission-docs/potential-reviewers.md`.
- Pass: each project's foundation paragraph cites the external results it
  rests on; no comparative sentence belittles a cited author.

**P15 — Reviewer-perspective pass before the PI walk [J, process].**
Before `pd-section-walk`, `pd-review-as` has run from each perspective in
`submission-docs/potential-reviewers.md` plus the standard roles, and
`pd-apply-feedback` has applied or deferred every row.
- Pass: `reviews/review-as-*.md` exist, each dated after the current
  `description.tex`, and no row is still `open`.

**P16 — Environment inventory [M, info].** The checker reports the count of
each theorem-class environment (`theorem`, `proposition`, `lemma`,
`corollary`, `conjecture`, `definition`, `problem`, `question`) so S5 and
P2–P3 can be judged together.

**P17 — No claudisms [M, J].** No machine tells from
`purge-claudisms/references/claudisms.md` (stock LLM vocabulary, importance
and reveal frames, "not X but Y", triads, semicolon and colon chains, em-dash
splices, run-in labels, summary tails).
- Pass [M]: `purge-claudisms/scripts/scan_claudisms.py description.tex`
  exits 0 (no lexical or structural hit). Pass [J]: each remaining WARN row
  has a one-line justification in the report.
