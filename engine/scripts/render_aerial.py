#!/usr/bin/env python3
"""Burn a static text block + brand lockup onto a clip.

Text is plain system font, all on screen at once, no sequential reveal and no
design flourish — the Instagram text-tool look. Only the lockup is branded:
a wordmark in whatever font you drop in public/brand (system font until
then) plus an optional mark PNG.

Usage:
  python3 scripts/render_aerial.py <in.mp4> <copy_key> <out.mp4>

  python3 scripts/render_aerial.py public/footage/your_clip.mp4 \\
      example ads/test.mp4

Needs Pillow (`pip install -r requirements.txt`) and ffmpeg. Unlike the
OneWord and Cards formats this one is NOT pure Node, and it needs a piece of
FOOTAGE to burn text onto — your own clip, stock you have rights to, or one
generated with scripts/generate.py.

Copy keys are the COPY dict below. Edit that dict to change the words, and the
LOCKUP constants to brand it. This script does not read src/brand.mjs, so keep
the two in agreement by hand.
"""
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
BRAND = Path(__file__).resolve().parent.parent / "public" / "brand"
SF = "/System/Library/Fonts/SFNS.ttf"
# Lockup wordmark font: the first .ttf/.otf you drop in public/brand/ is
# picked up automatically (a serif reads as editorial); system font otherwise.
LOCKUP_FONT = next(
    (str(p) for p in sorted(BRAND.glob("*.ttf")) + sorted(BRAND.glob("*.otf"))),
    SF,
)

# Meta Reels chrome covers roughly the top 14% and bottom 20%
SAFE_TOP, SAFE_BOTTOM = int(H * 0.14), int(H * 0.795)

# SF Pro is genuinely what Instagram Stories "Classic" renders in on iOS
# (Roboto on Android), so this is the native-app look rather than an
# approximation. Drop a geometric sans in public/brand if the CapCut-style
# look is ever wanted as a V2 (Montserrat is a free download).
BODY = 62
LINE = 1.16
GAP = 0.55         # paragraph gap, keeps it reading as one block
WIDTH = 0.88       # share of frame the text block fills
STROKE = 4         # hard black outline, not a soft shadow

# ---------------------------------------------------------------------------
# The lockup at the bottom of the frame. All placeholders — replace with your
# brand's real values. MARK is an optional square PNG in public/brand/; set to
# None for a text-only lockup.
# ---------------------------------------------------------------------------
LOCKUP_NAME = "[YOUR BRAND NAME]"
LOCKUP_TAG_FREE = "[your free tagline, e.g. Read it free]"
LOCKUP_TAG_PAID = "[your paid tagline, e.g. Free newsletter · Paid community]"
MARK = None        # e.g. BRAND / "brand_mark.png" (square RGBA png)

# ---------------------------------------------------------------------------
# The copy, one key per cut. ALL PLACEHOLDER — write your own before rendering
# anything that ships. The three-paragraph shape is the one that worked:
#
#   1. the hook — name the reader's situation as FACT, second person, never a
#      question ("You're doing the work of two people"). Third-person category
#      openers ("For managers who...") consistently underperformed it.
#   2. what they get, in time terms
#   3. the call to action
#
# Suffix conventions the "_paid" check below relies on:
#   <key>        the free cut
#   <key>_paid   the paid twin: paragraph 1 byte-identical, offer appended,
#                so against its free twin the offer is the ONLY variable.
# Keep hook variants as separate keys (<key>_v2) with paragraphs 2-3
# byte-identical, so the hook stays the single variable under test.
# ---------------------------------------------------------------------------
COPY = {
    "example": [
        "[HOOK: name the reader's pain as fact. Second person. Not a question.]",
        "[WHAT THEY GET: in time terms, e.g. five minutes a week.]",
        "[CTA: e.g. Subscribe free.]",
    ],
    "example_paid": [
        "[HOOK: byte-identical to the free cut's hook.]",
        "[WHAT THEY GET: free tier first.]",
        "[THE PAID OFFER: one sentence, checked against your live offer page.]",
        "[CTA: e.g. Join us.]",
    ],
}


def font(path, size, weight):
    f = ImageFont.truetype(path, size)
    try:
        f.set_variation_by_name(weight)
    except Exception:
        pass
    return f


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def overlay(key):
    """One RGBA layer: static text block + branded lockup."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    max_w = int(W * WIDTH)

    # The block lives above the lockup, not in the whole safe band, or a tall
    # variant would collide with it. Shrink the type until it fits that space.
    lock_y = int(H * 0.735)
    avail = (lock_y - 70) - SAFE_TOP

    for size in range(BODY, 33, -2):
        body = font(SF, size, "Heavy")
        lh, gap = int(size * LINE), int(size * GAP)
        rows = [wrap(d, p, body, max_w) for p in COPY[key]]
        total = sum(len(r) * lh for r in rows) + gap * (len(rows) - 1)
        if total <= avail:
            break

    y = SAFE_TOP + (avail - total) // 2

    yy = y
    for r in rows:
        for ln in r:
            x = (W - d.textlength(ln, font=body)) / 2
            d.text((x, yy), ln, font=body, fill=(255, 255, 255, 255),
                   stroke_width=STROKE, stroke_fill=(0, 0, 0, 255))
            yy += lh
        yy += gap

    # --- lockup: [optional mark] Brand Name  /  tagline ---
    lora = font(LOCKUP_FONT, 76, "SemiBold")
    tw = d.textlength(LOCKUP_NAME, font=lora)
    ly = lock_y

    if MARK is not None:
        mark = Image.open(MARK).convert("RGBA")
        ms = 78
        mark = mark.resize((ms, ms), Image.LANCZOS)
        lx = (W - (ms + 20 + tw)) / 2
        img.alpha_composite(mark, (int(lx), int(ly + 8)))
        d = ImageDraw.Draw(img)
        tx = lx + ms + 20
    else:
        tx = (W - tw) / 2

    d.text((tx, ly), LOCKUP_NAME, font=lora, fill=(255, 255, 255, 255),
           stroke_width=STROKE, stroke_fill=(0, 0, 0, 255))

    sub = font(SF, 34, "Semibold")
    # A paid cut must not send people to the free thing it is trying to upsell
    # past. "_paid" is checked ANYWHERE in the key, not just the end — a
    # key like founder_paid_v2 is a paid cut too, and an endswith() check
    # silently gave one exactly that wrong lockup once.
    tag = LOCKUP_TAG_PAID if "_paid" in key else LOCKUP_TAG_FREE
    d.text(((W - d.textlength(tag, font=sub)) / 2, ly + 96), tag, font=sub,
           fill=(255, 255, 255, 255), stroke_width=3, stroke_fill=(0, 0, 0, 255))
    return img


def main():
    src, key, dst = sys.argv[1], sys.argv[2], sys.argv[3]
    png = Path(dst).with_suffix(".overlay.png")
    overlay(key).save(png)

    subprocess.run([
        # -loop 1 is required: a single-frame image gives fade= no timeline to
        # act on, so alpha stays at its t=0 value (0) and overlay repeats that
        # transparent frame for the whole clip.
        "ffmpeg", "-y", "-v", "error", "-i", src, "-loop", "1", "-i", str(png),
        "-filter_complex",
        "[1]format=rgba,fade=in:st=0.35:d=0.55:alpha=1[ov];"
        "[0][ov]overlay=0:0:format=auto",
        "-c:v", "libx264", "-crf", "18", "-preset", "medium",
        "-pix_fmt", "yuv420p", "-c:a", "copy", "-shortest", dst,
    ], check=True)
    png.unlink()
    print(f"wrote {dst}")


if __name__ == "__main__":
    main()
