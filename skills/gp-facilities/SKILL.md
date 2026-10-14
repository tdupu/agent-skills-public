---
name: gp-facilities
description: Write the NSF Facilities, Equipment and Other Resources document (facilities.tex) — office, computing, library, software, collaborators' resources — as narrative with no dollar figures. Use for "facilities", "equipment and other resources".
---

# gp-facilities

Narrative only, with no dollar figures (GRANT-FORMAT F14). It describes
what exists for the project without NSF funds. Anything the budget pays
for belongs in the budget justification instead.

## Procedure

1. Collect the facts and confirm any you are unsure of with the PI:
   - department office and seminar space;
   - university computing (the cluster's name, e.g. VACC, and access);
   - the PI's own servers or storage, with capacity from the machine,
     not from memory;
   - library and MathSciNet access;
   - software licenses UVM provides (Magma, Mathematica, etc.);
   - external resources the project uses (LMFDB servers, collaborators'
     institutions).
2. Write short paragraphs headed **Facilities**, **Computing**,
   **Library and software** and **Other resources**. Name each resource
   and what the project uses it for.
3. Run `grep '\$' facilities.tex`. It must return nothing.
4. Build it and upload it with `gp-researchgov`.
