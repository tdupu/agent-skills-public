---
name: break-up-proposition
description: Break an existing proposition, theorem, or corollary into a labelled enumerate with separately signposted proofs while preserving its mathematics. Use for a style-driven decomposition; adding new items is optional and must be evidence-backed.
---

# break-up-proposition

Use this leaf after `using-latexpowers` has resolved the canonical manuscript
and target region. It rewrites one existing theorem-class statement into an
enumerated interface and keeps the proof readable and traceable. It is a
refactoring skill: it does not turn an unproved idea into a result and does
not require new items when the existing statement already contains the right
claims.

## Scope and stop conditions

- Work on one proposition at a time in the declared canonical `.tex` file.
- Preserve the proposition's hypotheses, conclusions, theorem label, proof,
  citations, human markers, and surrounding order unless the user explicitly
  changes them.
- Add an item only when the user requests it or the evidence and surrounding
  manuscript establish a genuinely separate conclusion. Record its source and
  proof obligation before editing.
- Stop and route to `using-mathpowers` or `write-proposition` if a proposed
  item needs a new proof, changes the quantifiers, or is not supported by the
  existing argument. Do not silently strengthen or weaken the result.
- Stop if the statement's parts are actually separate named theorems. Split
  those into separate theorem-class environments instead of manufacturing an
  enumeration.

## Before editing

1. Read the repository's `WRITERS.md`, `STYLE.md`, `LATEX.md`, and any local
   powers policy through `using-latexpowers`. Resolve the canonical file and
   the exact proposition region; do not edit a generated or sibling variant.
2. Read the complete proposition and proof, then search the manuscript for
   its theorem label, every existing part reference, and nearby labels. Run
   the repository's label/reference checker before the edit when available.
3. Make an item map: one semantic conclusion per item, the evidence or proof
   paragraph that establishes it, and every site that will cite it. Preserve
   the original order unless there is a stated reason to reorder it.
4. Choose stable semantic item labels such as
   `item:pc-invariance` or `item:branch-control`; never use labels whose only
   meaning is an ordinal. Check that every new label is unique.

## Statement transformation

Keep the theorem-class environment limited to the hypotheses and the
conclusion. When the proposition has multiple conclusions, use an explicit
enumerate:

```tex
\begin{proposition}\label{prop:example}
Assume ... . Then:
\begin{enumerate}
  \item ... .\label{item:first-conclusion}
  \item ... .\label{item:second-conclusion}
\end{enumerate}
\end{proposition}
```

Each item must be independently meaningful and must state a conclusion, not
motivation, unpacking, or a proof step. Keep explanatory consequences outside
the theorem-class environment unless they are themselves part of the claimed
result. If there is only one conclusion after the refactor, do not enumerate
merely to create an item number.

Item labels are an interface. Update every consumer in the same change to use
`\eqref{item:<slug>}`. Never cite a part by a literal `(1)`, `(2)`, or by an
unstable ordinal. Preserve the proposition's top-level label and update any
old part labels deliberately; do not leave aliases or duplicate labels behind.

## Proof transformation

Use one `proof` environment for the proposition unless the repository's style
contract requires another form. Inside it, give a signpost and proof for each
enumerated item, in item order:

```tex
\begin{proof}
\noindent\emph{Proof of \eqref{item:first-conclusion}.}
...

\noindent\emph{Proof of \eqref{item:second-conclusion}.}
...
\end{proof}
```

The `\eqref` renders the current item number while keeping the proof tied to
the stable label. Each signposted block must discharge exactly its item. A
later block may cite an earlier item with `\eqref{item:<slug>}`; state that
dependency rather than repeating an unproved assertion. Give a short proof
for an immediate item or move it out of the proposition; never leave an
enumerated item without a corresponding proof signpost.

## After editing

Review the diff item by item: the enumerated statement is mathematically
equivalent to the original unless an explicitly authorized, evidence-backed
item was added; every item has a proof block; no proof paragraph or negative
result was dropped; and all part references use the new labels. Re-run the
label/reference checker, the repository's LaTeX/style checks, and the
canonical build. Inspect the source as well as the PDF because compilation
cannot detect an omitted conclusion or a proof attached to the wrong item.

Report the target file, the item-to-proof map, any added items and their
evidence, references updated, and the validation results. Do not commit or
sync as part of this leaf unless the user separately authorizes that action.
