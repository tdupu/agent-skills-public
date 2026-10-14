---
name: pd-data-table
description: Build a small, verified table of real records for an NSF proposal — labels, objects, computed values, and the database entries they match — so the panel sees that the data exists. Every entry is checked against the source data or a live database query. Use for "add a table", "show the data", "do this with an example", "worked example".
---

# pd-data-table

A table of ten real records persuades more than a page describing a schema.
Panels do not need field lists; they need to see actual objects, actual
numbers, and the match to something they already trust.

## Procedure

1. Choose the claim the table supports (a pattern, a match, a count, a
   diagnostic). One table, one claim.
2. Pull the rows from the source data or from the reports that produced them;
   re-derive any computed column (e.g. a residual or a bound) yourself.
3. Query external databases live for every external label and invariant you
   print (signs, coefficients, levels); record the query date.
4. Include the rows that do **not** fit, or that are missing, when they bear
   on the claim; a complete column is stronger than a selected one.
5. Caption states what to read off the table in one sentence, and the date.
6. Add a `REVIEW.md` row for every number the style checker will flag.

## Rules

- Unpack any label once in the text, field by field.
- Keep tables within the text width (paragraph columns, small font);
  overfull boxes fail the format check.
- "Not matched" is not "absent": say "does not appear in the data" unless
  the computation was exhaustive.
