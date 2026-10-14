#!/usr/bin/env python3
"""Render a note body as real typeset LaTeX, transparent, at a target pixel width.

    latex_body(text, width_px, pt=12) -> RGBA Image

The notes are mathematics, so uncompiled source on screen ("$\\cap$") is a
legibility cost that grows with the font size. A full TeX is available here, so
the body is typeset: dvipng writes a transparent bitmap that composites onto
the frame like any other panel art.

The paper's own macros are predefined, so note text can be written the way the
manuscript writes it. A note that fails to compile raises rather than silently
rendering its own source.
"""
import os, re, shutil, subprocess, tempfile
from PIL import Image

PREAMBLE = r"""
\providecommand{\branch}{\operatorname{Branch}}
\providecommand{\Sing}{\operatorname{Sing}}
\providecommand{\Crit}{\operatorname{Crit}}
\providecommand{\crit}{\operatorname{Crit}}
\providecommand{\Spec}{\operatorname{Spec}}
\providecommand{\cO}{\mathcal{O}}
\providecommand{\PP}{\mathbb{P}}
\renewcommand{\AA}{\mathbb{A}}
\providecommand{\FF}{\mathbb{F}}
\providecommand{\restr}[2]{#1|_{#2}}
"""

def latex_body(text, width_px, pt=12):
    # dpi is chosen so that `pt`-sized type lands at the body size we want on a
    # 1920-wide frame; the measure in points then follows from the target width.
    dpi = int(round(pt * 22.0))                    # 12pt -> 264 dpi
    width_pt = width_px * 72.0 / dpi
    doc = (r"\documentclass[preview,border=2pt," + f"{pt}pt" + r"]{standalone}" "\n"
           r"\usepackage{amsmath,amssymb,varwidth}" "\n" + PREAMBLE +
           r"\begin{document}" "\n"
           r"\begin{varwidth}{" + f"{width_pt:.1f}pt" + r"}\raggedright " + "\n"
           + text + "\n" r"\end{varwidth}" "\n" r"\end{document}" "\n")
    with tempfile.TemporaryDirectory() as d:
        tex = os.path.join(d, "n.tex")
        open(tex, "w").write(doc)
        r = subprocess.run(["latex", "-interaction=nonstopmode", "-halt-on-error",
                            "-output-directory", d, tex],
                           capture_output=True, text=True, stdin=subprocess.DEVNULL)
        if r.returncode != 0:
            msg = "\n".join(l for l in r.stdout.splitlines() if l.startswith("!"))
            raise ValueError(f"note did not compile: {msg or r.stdout[-400:]}\n{text[:90]!r}")
        png = os.path.join(d, "n.png")
        r = subprocess.run(["dvipng", "-D", str(dpi), "-T", "tight", "-bg", "Transparent",
                            "-q", "-o", png, os.path.join(d, "n.dvi")],
                           capture_output=True, text=True, stdin=subprocess.DEVNULL)
        if r.returncode != 0 or not os.path.exists(png):
            raise ValueError(f"dvipng failed: {r.stderr[-300:]}")
        return Image.open(png).convert("RGBA")

if __name__ == "__main__":
    im = latex_body(r"Should be $B \cap \Sing(Y)$, not $B \cup \Sing(Y)$.", 700)
    im.save("/tmp/latexbody.png"); print("rendered", im.size)
