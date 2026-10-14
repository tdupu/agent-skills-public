---
name: gp-coa
description: Fill NSF's Collaborators and Other Affiliations (COA) Excel template so Research.gov's validator accepts it. Use for "fill the COA", "collaborators spreadsheet", "COA has errors", "add collaborators", or before touching the COA .xlsx with any tool.
---

# gp-coa

The COA template's tables are Excel ListObjects (`TableA`, `TableD23`,
`TableC`, `TableD`, `TableD5`). Research.gov's validator reads each
table's range. openpyxl writes cells but does not extend a table's
range, so rows written below a table are invisible to the validator. In
the 2026 proposal the validator read 5 rows of 12. **Grow tables only
by inserting rows natively in Excel.**

## Procedure

1. **Template.** Download the current template from NSF's COA page
   (the PI approves the download). Never reuse last year's file. Copy it
   to `proposal/submission-docs/COA-<PI>-<year>.xlsx`.
2. **Inventory with openpyxl, read-only.** For each table, record its
   name, its `ref`, and its sample rows:
   `ws.tables.items()`. Nothing is saved.
3. **Collect the people.**
   - Table 1: the PI's name and current organization.
   - Table 2: the PI's other affiliations in the last 12 months.
   - Table 3: PhD advisors (code G) and advisees (code T).
   - Table 4: co-authors (code A) and collaborators (code C) in the last 48
     months. Build the list from the PI's papers and preprints (arXiv,
     MathSciNet, the PI's repos) and the PI's own additions.
   - Table 5: editorial boards and co-editors (codes B and E).
   Confirm the numbering against the template's own headings.
   One row per person: "Last, First", organization, last-active year
   when the column exists. Show the PI the list before writing.
4. **Write in Excel by AppleScript** (`osascript`, wrapped in
   `with timeout of 120 seconds`):
   - `clear contents range "<sample rows>"` for every table;
   - `insert into range range "<r1>:<r2>" of ws shift shift down`.
     The rows must lie strictly inside the table, between its first and
     last data rows, so the ListObject grows;
   - `set value of range "B<r>" of ws to "<name>"`, and the same for the
     other columns;
   - `save active workbook`, then `close … saving no`.
   If Excel shows a dialog, the script times out. Close the dialog and
   rerun.
5. **Verify.** Reopen with openpyxl. Each table's `ref` must now span
   every written row, there must be no sample text left, and the names
   must match the list.
6. **Upload** with `gp-researchgov` (Senior Personnel Documents → COA).
   The page must say "No issue(s) found". If it lists errors, fix them
   in Excel and re-upload.

## Red flags

| Thought | Reality |
|---|---|
| "Let the validator confirm" | The validator does not see rows outside the table range. Verify `ref` yourself (step 5). |
| "Copy styles to rows 6–12 with openpyxl" | Styled rows are still outside the ListObject. Insert in Excel. |
| "Edit `table.ref` by hand" | Untested against the validator. Insert in Excel. |
