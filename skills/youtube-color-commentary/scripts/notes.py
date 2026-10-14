#!/usr/bin/env python3
"""Placement, timing and rendering for burned-in commentary notes.

Imported by burn-notes.py; usable directly. Requires Pillow (which requires
FreeType for scalable text) and, for ink_mask, ffmpeg on PATH.

The hard part is placement, and the hard part of placement is knowing when it
failed. A panel dropped because ffmpeg could not decode a frame and a panel
dropped because the page is full are different problems with different fixes,
so they are reported as different reasons.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import re
import textwrap

WORDS_PER_SEC = 2.6
MIN_SECS = 4.5
MAX_SECS = 14.0
LEAD_IN_SECS = 0.8
DEFAULT_SCALE = 3
DEFAULT_TOLERANCE = 0.001
# A MaxFilter(5) dilated mark is at least 25 mask pixels. The fractional
# tolerance is meant to absorb a stray pixel, not a mark: 0.1% of a large 4K
# panel is ~90 mask pixels, which would hide three real marks. Whichever bound
# is smaller wins.
MAX_INK_PIXELS = 12
TYPESET = True   # render note bodies through LaTeX when a TeX is present
ALPHA = 165   # translucent: the lecture keeps showing through the note
STYLES = {
    "gloss": ((40, 70, 150), "What the speaker means"),
    "aside": ((150, 90, 10), "Margin note"),
}


class NoFontError(RuntimeError):
    """No scalable font is available, so text cannot be laid out."""


class MaskError(RuntimeError):
    """Frames could not be sampled, so nothing is known about the picture."""


def reading_units(text):
    """Word-equivalents in a note, counting typeset maths by what it renders to.

    `reading_seconds` used to count `text.split()`, which charges one word for
    `$\\sum_{i=1}^{n}\\binom{n}{i}x^i$` and lands a dense formula on the floor.
    Symbols are read slower than prose, not faster, so each maths span is
    charged by the symbols it contains, with a floor of two.
    """
    spans = re.findall(r"\$[^$]*\$", text)
    prose = re.sub(r"\$[^$]*\$", " ", text)
    units = len(prose.split())
    for sp in spans:
        inner = re.sub(r"[\\{}$^_]", " ", sp)
        units += max(2, len(re.findall(r"[A-Za-z0-9]+|[=+\-<>/|]", inner)))
    return units


def reading_seconds(text, rate=WORDS_PER_SEC):
    """Display seconds for this text.

    reading_units/rate + LEAD_IN_SECS, clamped to [MIN_SECS, MAX_SECS]. At the
    default rate anything under 9 units gets the floor and anything over 35
    gets the cap -- and 35 is where validate() refuses the note outright, so
    the cap is reached only by notes that will not ship. A maths span is
    charged by its symbols: counting its source as one word put dense formulas
    on the floor.
    """
    return max(MIN_SECS, min(MAX_SECS, reading_units(text) / rate + LEAD_IN_SECS))


def _font(size, bold=False):
    """A scalable font at this size.

    No absolute paths: font locations differ per platform, and hardcoding them
    makes the skill unportable. Pillow resolves a bare family name against the
    system font path. COMMENTARY_FONT / COMMENTARY_FONT_BOLD override.

    Raises NoFontError rather than returning the bitmap default. Pillow's
    load_default() returns a non-scalable ImageFont without a .size attribute
    when FreeType is unavailable, and every caller here reads .size; returning
    it produced an AttributeError deep inside layout instead of a usable
    message at the point of failure.
    """
    from PIL import ImageFont
    env = os.environ.get("COMMENTARY_FONT_BOLD" if bold else "COMMENTARY_FONT")
    names = [env] if env else []
    names += (["DejaVuSans-Bold.ttf", "LiberationSans-Bold.ttf", "Arial Bold.ttf"]
              if bold else
              ["DejaVuSans.ttf", "LiberationSans.ttf", "Arial.ttf"])
    for name in names:
        try:
            return ImageFont.truetype(name, size)
        except (OSError, ImportError):
            # ImportError, not just OSError: on a Pillow built without
            # FreeType, FreeTypeFont.__init__ re-raises the deferred
            # ImportError for the _imagingft C module. Catching only OSError
            # let that escape as a bare traceback -- the exact outcome this
            # function exists to replace.
            continue
    try:
        fallback = ImageFont.load_default(size=size)
        if hasattr(fallback, "size"):
            return fallback
    except (TypeError, AttributeError, ImportError):
        pass
    raise NoFontError(
        "no scalable font found. Pillow needs FreeType for sizeable text; "
        "install a TrueType font (DejaVu or Liberation) or set COMMENTARY_FONT "
        "to a font name or path.")



def _typeset_panel(kind, text, model, width, colour, latex_body):
    """Panel whose body is real typeset LaTeX rather than its own source.

    The notes are mathematics and the body type is large, so uncompiled source
    on screen is a legibility cost that scales with the font. A note that does
    not compile raises: silently rendering the source is the failure this
    exists to prevent.
    """
    from PIL import Image, ImageDraw
    pad = max(16, width // 30)
    body = latex_body(text, width - 2 * pad)
    foot_f = _font(max(14, width // 44))
    height = pad * 2 + body.height + int(foot_f.size * 1.8)
    img = Image.new("RGBA", (width, height), (255, 255, 255, ALPHA))
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, width - 1, height - 1], outline=colour + (235,), width=3)
    draw.rectangle([0, 0, 9, height - 1], fill=colour + (235,))
    img.paste(body, (pad, pad), body)
    draw.text((pad, pad + body.height + int(foot_f.size * 0.4)), model,
              font=foot_f, fill=(105, 105, 105))
    return img


def panel(kind, text, author, model, date, width):
    """An RGBA panel: heading, body, attribution footer.

    Refuses non-ASCII: a common sans face has no U+208A, so Unicode subscripts
    render as empty boxes. Uncompiled LaTeX is the intended notation and is
    ASCII by construction.
    """
    from PIL import Image, ImageDraw
    if kind not in STYLES:
        raise ValueError(f"unknown note kind {kind!r}; expected one of "
                         f"{sorted(STYLES)}")
    if not isinstance(text, str) or not text.strip():
        raise ValueError("note text is empty")
    if not text.isascii():
        offenders = sorted({c for c in text if not c.isascii()})
        raise ValueError(f"note text must be ASCII, would render as tofu: "
                         f"{offenders} in {text[:40]!r}")
    if not author or not model:
        raise ValueError("author and model are required: a note must say who "
                         "added it and on whose instruction")
    colour, _heading = STYLES[kind]
    if TYPESET and shutil.which("latex") and shutil.which("dvipng"):
        try:
            from mathrender import latex_body
            return _typeset_panel(kind, text, model, width, colour, latex_body)
        except ImportError:
            pass
    body_f = _font(max(30, width // 17))
    foot_f = _font(max(14, width // 44))
    pad = max(16, width // 30)
    body = textwrap.wrap(text, max(14, int(width / (body_f.size * 0.52))))
    foot = [model]
    body_h, foot_h = int(body_f.size * 1.26), int(foot_f.size * 1.25)
    height = (pad * 2 + body_h * len(body) + int(foot_f.size * 0.5)
              + foot_h * len(foot))
    img = Image.new("RGBA", (width, height), (255, 255, 255, ALPHA))
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, width - 1, height - 1], outline=colour + (235,), width=3)
    draw.rectangle([0, 0, 9, height - 1], fill=colour + (235,))
    y = pad
    for line in body:
        draw.text((pad, y), line, font=body_f, fill=(10, 10, 10))
        y += body_h
    y += int(foot_f.size * 0.5)
    for line in foot:
        draw.text((pad, y), line, font=foot_f, fill=(105, 105, 105))
        y += foot_h
    return img


def classify_ink(image, max_value=165, max_saturation=70):
    """Content pixels in one frame: dark AND desaturated, then dilated.

    Split out so the rule itself is testable without decoding a video.
    """
    from PIL import ImageChops, ImageFilter
    _h, sat, val = image.convert("HSV").split()
    dark = val.point(lambda v: 255 if v < max_value else 0)
    neutral = sat.point(lambda v: 255 if v < max_saturation else 0)
    return ImageChops.darker(dark, neutral).filter(ImageFilter.MaxFilter(5))


def union(masks):
    """Content anywhere in any frame. A page is written progressively, so a
    spot blank when a note appears can be covered before it leaves."""
    from PIL import ImageChops
    acc = None
    for m in masks:
        acc = m if acc is None else ImageChops.lighter(acc, m)
    return acc


def ink_mask(video, start, end, width, height, samples=6, scale=DEFAULT_SCALE,
             vf_pre="", max_value=165, max_saturation=70):
    """Pixels carrying content at ANY moment in [start, end].

    Ink is selected as dark AND desaturated. On a lit page filmed over a wooden
    desk that separates three classes without tuning a grey threshold: the desk
    is dark but strongly coloured, the page is bright, strokes are dark and
    neutral. It is a heuristic about *that* setup, not a law:

      * a neutral grey or black desk, letterbox bars, and deep shadow are also
        dark and desaturated, so they read as content and reduce the space
        offered -- safe, but it can leave nowhere to place anything;
      * hands are excluded because they are bright, not because they are
        coloured; a hand in shadow may read as content.

    Raises MaskError when no frame could be sampled, so the caller can say
    "could not read the video here" instead of "nowhere was clear".
    """
    from PIL import Image
    if shutil.which("ffmpeg") is None:
        raise MaskError("ffmpeg is not on PATH")
    chain = [c for c in (vf_pre, f"scale={width // scale}:{height // scale}") if c]
    acc, used, errors = None, 0, []
    with tempfile.TemporaryDirectory() as tmp:
        for i in range(samples):
            at = start + (end - start) * i / max(1, samples - 1)
            frame = os.path.join(tmp, f"{i}.png")
            proc = subprocess.run(
                ["ffmpeg", "-nostdin", "-hide_banner", "-loglevel", "error", "-y",
                 "-ss", f"{at:.2f}", "-i", video, "-frames:v", "1",
                 "-vf", ",".join(chain), frame],
                capture_output=True, text=True, stdin=subprocess.DEVNULL,
                check=False)
            if not os.path.exists(frame) or os.path.getsize(frame) == 0:
                err = (proc.stderr or "").strip().splitlines()
                errors.append(err[-1] if err else f"no frame at {at:.2f}s")
                continue
            used += 1
            mask = classify_ink(Image.open(frame), max_value, max_saturation)
            acc = union([acc, mask]) if acc is not None else mask
    if acc is None:
        raise MaskError(f"no frame could be sampled between {start:.1f}s and "
                        f"{end:.1f}s: {errors[0] if errors else 'unknown'}")
    return acc, used


def place(mask, panel_w, panel_h, scale=DEFAULT_SCALE, margin=0.02,
          tolerance=DEFAULT_TOLERANCE, blocked=()):
    """Top-left corner where the panel covers no content, or None.

    `blocked` is a sequence of (x0, y0, x1, y1) in full-resolution coordinates
    that must also be avoided -- panels already placed whose display windows
    overlap this one. Without it two notes a few seconds apart both land on the
    first clear corner and the second hides the first, and both are reported
    placed.

    `tolerance` is a fraction of the panel's area that may be content. It
    absorbs anti-aliasing at stroke edges; it is not zero, so "covers no
    content" means "covers less than that fraction".
    """
    from PIL import ImageDraw
    if mask is None:
        return None
    mw, mh = mask.size
    bw, bh = max(1, panel_w // scale), max(1, panel_h // scale)
    if bw > mw or bh > mh:
        return None
    if blocked:
        mask = mask.copy()
        draw = ImageDraw.Draw(mask)
        for x0, y0, x1, y1 in blocked:
            draw.rectangle([x0 // scale, y0 // scale, x1 // scale, y1 // scale],
                           fill=255)
    px = mask.load()
    integral = [[0] * (mw + 1) for _ in range(mh + 1)]
    for y in range(mh):
        row = 0
        for x in range(mw):
            row += 1 if px[x, y] else 0
            integral[y + 1][x + 1] = integral[y][x + 1] + row
    best, best_pos = None, None
    edge = int(min(mw, mh) * margin)
    step = max(1, min(mw, mh) // 44)
    for y in range(edge, mh - bh - edge + 1, step):
        for x in range(edge, mw - bw - edge + 1, step):
            total = (integral[y + bh][x + bw] - integral[y][x + bw]
                     - integral[y + bh][x] + integral[y][x])
            if best is None or total < best:
                best, best_pos = total, (x, y)
                if total == 0:
                    break
        if best == 0:
            break
    budget = min(tolerance * bw * bh, MAX_INK_PIXELS)
    if best_pos is None or best > budget:
        return None
    return best_pos[0] * scale, best_pos[1] * scale
