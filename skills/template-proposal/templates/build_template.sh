#!/usr/bin/env bash
# Build every proposal document into proposal/final-pdfs/ with the file names
# the format checker expects. description.pdf is trimmed at the page labelled
# S:bibstart (the bibliography is a separate document).
set -euo pipefail
cd "$(dirname "$0")/proposal/tex"
out=../final-pdfs; mkdir -p "$out"
build(){ latexmk -pdf -interaction=nonstopmode -halt-on-error "$1.tex" >/dev/null; cp "$1.pdf" "$out/$2.pdf"; }
build summary summary
build data data-management
build facilities facilities
build budget-justification budget-justification
[ -f mentoring.tex ] && build mentoring mentoring
latexmk -pdf -interaction=nonstopmode -halt-on-error description.tex >/dev/null
bib=$(grep -o 'newlabel{S:bibstart}{{[^}]*}{[0-9]*}' description.aux | grep -o '{[0-9]*}$' | tr -d '{}')
if [ -n "$bib" ] && [ "$bib" -gt 1 ]; then
  last=$((bib-1))
  if command -v qpdf >/dev/null; then qpdf description.pdf --pages . 1-$last -- "$out/description.pdf";
  else rm -rf .pages && mkdir .pages && pdfseparate -l $last description.pdf .pages/p-%03d.pdf && pdfunite .pages/p-*.pdf "$out/description.pdf" && rm -rf .pages; fi
else cp description.pdf "$out/description.pdf"; fi
latexmk -pdf -interaction=nonstopmode -halt-on-error references.tex >/dev/null && cp references.pdf "$out/references.pdf"
ls -l "$out"
