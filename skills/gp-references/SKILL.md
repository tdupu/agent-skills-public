---
name: gp-references
description: Build the NSF References Cited document (references.tex + references.bib) — every key cited in the description, full bibliographic fields, amsalpha — and clear Research.gov's spacing warnings. Use for "references", "bibliography", "references cited", "missing citation", "line spacing warning on references".
---

# gp-references

A separate PDF with entries only and no prose (GRANT-FORMAT F10). The
citations must match the description exactly.

## Procedure

1. **Extract the keys** cited in `description.tex` (`\cite{…}` and
   friends), and collect every key in `references.bib`.
   - Any key cited but missing from the bib is an error.
   - Any key in the bib but never cited is removed, or kept only with
     `\nocite` if the PI wants it.
2. **Complete each entry** from MathSciNet, the arXiv or the journal
   site, never from memory:
   - all authors, the title, the journal or publisher, volume, year,
     pages, and DOI;
   - preprints as `@misc` with the arXiv number;
   - the statuses must match `REVIEW.md` (published, to appear,
     submitted, preprint).
3. **`references.tex`:** `amsart` 11pt, 1in margins, style `amsalpha`,
   `\nocite` only if needed. Add
   `\makeatletter\renewcommand{\bibliofont}{\normalsize}\makeatother`
   so amsart's small bibliography font does not trigger Research.gov's
   "line spacing" warning.
4. **Build:** `bibtex` must report no missing-field warnings for
   `article` and `book` entries, and no `??` may appear in the
   description PDF.
5. **Upload** with `gp-researchgov`, and report any warning that
   remains. A spacing warning is not an error.
