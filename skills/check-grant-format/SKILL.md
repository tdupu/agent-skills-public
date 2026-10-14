---
name: check-grant-format
description: Audit an NSF proposal folder against Grants/GRANT-FORMAT.md (page limits, fonts, margins, required headings, no URLs in the description, prior-support items, clean build, file set). Use before any proposal PDF is sent to SPA, after every rebuild, or when asked "is this proposal compliant", "check the format", "page count", "PAPPG check".
---

# check-grant-format

Mechanical audit of one proposal folder against `Grants/GRANT-FORMAT.md`
(rules F1–F18). Reports per-rule PASS/FAIL with the measured value. Never
edits the proposal.

## Procedure

1. Resolve the folder: the argument, else the nearest ancestor containing
   `proposal/tex/`. Read `../GRANT-FORMAT.md` (the contract is the
   authority; if a rule number here disagrees with the file, the file
   wins).
2. If `proposal/final-pdfs/` is missing or older than any `.tex`, run
   `./build.sh` first and keep its log.
3. Run the script:

```bash
python3 ~/.claude/skills/check-grant-format/check_format.py <folder>
```

   It checks F1 (file set), F2 (fonts via `pdffonts`), F3 (page size and
   margins from the preamble), F4 (summary: one page, three headings in
   order), F5 (description ≤ 15 pages; prior-support span ≤ 5 from the
   `.aux`), F6/F7 (required headings and prior-support items), F8 (no
   URLs), F9 (log: undefined refs/cites, `??`, overfull > 20pt), F10
   (references PDF bibliography-only), F13 (DMP ≤ 2 pages), F14 (no `$`
   in facilities), F15 (budget justification ≤ 5 pages; summer months ≤ 2
   from the text), F16 (mentoring iff postdoc), F17 (reviewer names absent
   from description).
4. Judgment rules F11, F12, F18 are reported as `CONFIRM` with the question
   the PI must answer (SciENcv certified? COA template current? date SPA
   received the set?).
5. Output: a table `rule | result | measured | where`, then the list of
   FAILs with the fix. Exit status nonzero if any FAIL.

## Pass criterion

All mechanical rules PASS and every CONFIRM has a dated answer in the
proposal's `README.md`.
