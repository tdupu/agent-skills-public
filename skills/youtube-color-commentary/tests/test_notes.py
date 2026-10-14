#!/usr/bin/env python3
"""Tests for the placement, timing and attribution rules.

Run: python3 tests/test_notes.py
Requires Pillow. Does not require ffmpeg: placement is tested against
synthetic masks, which is also how the regressions below are pinned.
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                os.pardir, "scripts"))
import notes as N  # noqa: E402

FAILED = []


def _raises(exc, fn, *a, **k):
    try:
        fn(*a, **k)
    except exc:
        return True
    except Exception:
        return False
    return False

def check(name, ok, detail=""):
    print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f"  [{detail}]" if detail and not ok else ""))
    if not ok:
        FAILED.append(name)


def mask_from_rows(rows):
    """'.' clear, '#' content."""
    from PIL import Image
    h, w = len(rows), len(rows[0])
    im = Image.new("L", (w, h), 0)
    px = im.load()
    for y, row in enumerate(rows):
        for x, c in enumerate(row):
            px[x, y] = 255 if c == "#" else 0
    return im


def main():
    print("[1] reading time is derived from length, not guessed")
    short, long_ = "four words go here", " ".join(["word"] * 60)
    check("a short note still gets the floor",
          N.reading_seconds(short) == N.MIN_SECS)
    check("a long note is capped", N.reading_seconds(long_) == N.MAX_SECS)
    check("in between, longer text gets longer",
          N.reading_seconds(" ".join(["word"] * 20))
          > N.reading_seconds(" ".join(["word"] * 10)))
    check("nothing is ever shorter than the floor",
          all(N.reading_seconds(" ".join(["w"] * n)) >= N.MIN_SECS
              for n in range(1, 200)))

    print("\n[2] attribution is mandatory")
    for author, model in (("", "M"), ("A", ""), ("", "")):
        try:
            N.panel("gloss", "text", author, model, "2000-01-01", 400)
            check(f"refuses author={author!r} model={model!r}", False)
        except ValueError:
            check(f"refuses author={author!r} model={model!r}", True)
    img = N.panel("gloss", "text", "A. Person", "Some Model", "2000-01-01", 400)
    check("a complete panel renders", img.width == 400 and img.height > 0)

    print("\n[3] non-ASCII is refused, because it renders as tofu")
    try:
        N.panel("gloss", "subscript ₊ here", "A", "M", "2000-01-01", 400)
        check("refuses U+208A", False)
    except ValueError:
        check("refuses U+208A", True)
    check("uncompiled LaTeX is accepted",
          N.panel("gloss", "$\\Delta_+(e) = e \\otimes 1$", "A", "M",
                  "2000-01-01", 400).width == 400)

    print("\n[4] placement never covers content")
    clear = mask_from_rows(["." * 40 for _ in range(30)])
    pos = N.place(clear, 30, 30, scale=3)
    check("an empty surface places", pos is not None)
    full = mask_from_rows(["#" * 40 for _ in range(30)])
    check("a full surface refuses", N.place(full, 30, 30, scale=3) is None)
    # content on the left, clear on the right
    split = mask_from_rows(["#" * 20 + "." * 20 for _ in range(30)])
    pos = N.place(split, 30, 30, scale=3)
    check("places on the clear side", pos is not None and pos[0] >= 20 * 3,
          f"pos={pos}")
    # A real stroke is never one pixel: ink_mask dilates with MaxFilter(5), so
    # the smallest mark reaching place() is a 5x5 block. That is what must
    # reject a panel spanning the whole frame.
    stroke = ["." * 40 for _ in range(30)]
    for y in range(13, 18):
        stroke[y] = "." * 18 + "#" * 5 + "." * 17
    got = N.place(mask_from_rows(stroke), 120, 90, scale=3)
    check("a dilated stroke rejects a panel spanning the frame", got is None)

    # The tolerance is deliberate: it absorbs anti-aliasing at stroke edges,
    # not real content. Pinned so it cannot drift upward unnoticed.
    speck = ["." * 40 for _ in range(30)]
    speck[15] = "." * 20 + "#" + "." * 19
    got = N.place(mask_from_rows(speck), 120, 90, scale=3)
    check("a single sub-tolerance pixel is absorbed", got is not None,
          f"1/1200 = {1 / 1200:.5f} vs tolerance 0.001")
    check("tolerance is 0.1% of panel area",
          abs(N.DEFAULT_TOLERANCE - 0.001) < 1e-9)

    print("\n[5] regression: a panel larger than the surface is refused")
    check("oversized panel refused",
          N.place(clear, 6000, 6000, scale=3) is None)

    print("\n[6] the HSV rule separates pen from desk and paper")
    from PIL import Image
    img = Image.new("RGB", (60, 20), (200, 197, 194))          # paper
    for x in range(0, 20):
        for y in range(20):
            img.putpixel((x, y), (72, 42, 26))                 # wooden desk
    for x in range(40, 44):
        for y in range(8, 12):
            img.putpixel((x, y), (20, 20, 22))                 # pen
    m = N.classify_ink(img).load()
    check("a coloured desk is not content", not m[5, 10])
    check("a neutral stroke is content", bool(m[42, 10]))
    check("bright paper is not content", not m[32, 2])
    grey = Image.new("RGB", (20, 20), (60, 60, 60))
    check("a NEUTRAL dark surface IS read as content, as documented",
          bool(N.classify_ink(grey).load()[10, 10]))

    print("\n[7] the union covers every moment, not just one frame")
    early = mask_from_rows(["#" * 5 + "." * 35] + ["." * 40] * 29)
    late = mask_from_rows(["." * 40] * 29 + ["." * 35 + "#" * 5])
    u = N.union([early, late]).load()
    check("content from the first frame survives", bool(u[2, 0]))
    check("content from the last frame survives", bool(u[37, 29]))
    check("union of nothing is None", N.union([]) is None)

    print("\n[8] a panel already on screen is not free space")
    blank = mask_from_rows(["." * 40 for _ in range(30)])
    first = N.place(blank, 30, 30, scale=3)
    check("the first note places", first is not None)
    again = N.place(blank, 30, 30, scale=3,
                    blocked=[(first[0], first[1], first[0] + 30, first[1] + 30)])
    check("a second note does not land on the first",
          again is None or again != first, f"{first} vs {again}")

    print("\n[9] failure types are distinct and catchable")
    check("NoFontError", issubclass(N.NoFontError, RuntimeError))
    check("MaskError", issubclass(N.MaskError, RuntimeError))

    print("\n[10] unknown kinds and empty text are refused")
    for bad_kind in ("note", "", None):
        try:
            N.panel(bad_kind, "text", "A", "M", "2000-01-01", 400)
            check(f"refuses kind={bad_kind!r}", False)
        except (ValueError, TypeError):
            check(f"refuses kind={bad_kind!r}", True)
    try:
        N.panel("gloss", "   ", "A", "M", "2000-01-01", 400)
        check("refuses blank text", False)
    except ValueError:
        check("refuses blank text", True)

    print("\n[11] FAILURE PATHS are exercised, not just declared")
    from PIL import ImageFont
    from PIL._util import DeferredError
    saved = ImageFont.core
    ImageFont.core = DeferredError.new(ImportError("_imagingft not installed"))
    try:
        N._font(20)
        check("a FreeType-less Pillow raises NoFontError", False,
              "returned a font")
    except N.NoFontError:
        check("a FreeType-less Pillow raises NoFontError", True)
    except Exception as exc:
        check("a FreeType-less Pillow raises NoFontError", False,
              f"{type(exc).__name__}: {exc}")
    finally:
        ImageFont.core = saved

    check("ink_mask raises MaskError when ffmpeg cannot read the file",
          _raises(N.MaskError, N.ink_mask, "no-such-video.mp4", 0, 1, 640, 480,
                  samples=1))

    print("\n[12] a full picture fails the same way with or without panels")
    from PIL import Image
    solid = Image.new("L", (40, 30), 255)
    check("no placement on a full picture", N.place(solid, 30, 30, scale=3) is None)
    check("still none when panels are blocked too",
          N.place(solid, 30, 30, scale=3, blocked=[(0, 0, 30, 30)]) is None)

    print("\n[13] the tolerance cannot swallow a whole dilated mark")
    check("an absolute pixel budget caps the fractional one",
          N.MAX_INK_PIXELS < 25,
          f"MAX_INK_PIXELS={N.MAX_INK_PIXELS} vs 25 px per dilated mark")
    # The panel must be small enough that the candidate loop is non-empty,
    # otherwise the margin guard returns None and the budget is never consulted.
    big = Image.new("L", (400, 300), 0)
    for x in range(198, 203):
        for y in range(148, 153):
            big.putpixel((x, y), 255)           # one dilated mark, 25 px
    panel_px = 380 * 282                         # fractional budget = 107 px
    check("the fractional budget alone would allow this mark",
          0.001 * panel_px > 25, f"{0.001 * panel_px:.0f} px")
    check("but the absolute cap refuses it",
          N.place(big, 380 * 3, 282 * 3, scale=3) is None)
    clear_big = Image.new("L", (400, 300), 0)
    check("and the same panel places on a clear mask, so the loop is not empty",
          N.place(clear_big, 380 * 3, 282 * 3, scale=3) is not None)

    print("\n[14] placed panels do not intersect, not merely differ")
    blank2 = mask_from_rows(["." * 40 for _ in range(30)])
    p1 = N.place(blank2, 30, 30, scale=3)
    p2 = N.place(blank2, 30, 30, scale=3,
                 blocked=[(p1[0], p1[1], p1[0] + 30, p1[1] + 30)])
    if p2 is None:
        check("second placement avoided the first (dropped)", True)
    else:
        overlap = not (p2[0] + 30 <= p1[0] or p1[0] + 30 <= p2[0]
                       or p2[1] + 30 <= p1[1] or p1[1] + 30 <= p2[1])
        check("second placement does not intersect the first", not overlap,
              f"{p1} vs {p2}")

    print("\n[6] note bodies are typeset, and bad LaTeX fails loudly")
    try:
        from mathrender import latex_body  # noqa: F401
        have_tex = True
    except Exception:
        have_tex = False
    if have_tex and N.TYPESET:
        p = N.panel("gloss", r"$B \cap \Sing(Y)$", "T", "M", "2026-10-02", 700)
        check("a math note renders to a panel", p.width == 700 and p.height > 40)
        try:
            N.panel("gloss", r"$\nosuchmacro{x}$", "T", "M", "2026-10-02", 700)
            check("non-compiling LaTeX raises", False, "no exception")
        except ValueError as e:
            check("non-compiling LaTeX raises", "did not compile" in str(e), str(e)[:80])
    else:
        check("typesetting unavailable - skipped", True)

    print(f"\n{'ALL PASS' if not FAILED else str(len(FAILED)) + ' FAILED: ' + ', '.join(FAILED)}")
    return 1 if FAILED else 0


if __name__ == "__main__":
    sys.exit(main())
