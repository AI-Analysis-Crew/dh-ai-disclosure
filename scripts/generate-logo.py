#!/usr/bin/env python3
"""Generate the site nav logo: the DH-eye-AI mark in a badge.

Outputs (relative to repo root):
  png/logo.png    1200x440, transparent background
                  (displayed in the nav at width=120 height=44)

Design: the horizontal DH [eye] AI lockup inside a rounded badge —
Medium Slate fill with a Muted Teal border, so it stands off the Deep
Slate nav bar. Same mark and palette as the favicon set (square
vertical lockup) from scripts/generate-favicon.py.
Colors from css/style.css:
  Deep Slate   #1a2332  (pupil)
  Medium Slate #2a3444  (badge fill)
  Pale Blue    #E8F4F8  (lettering, eye outline)
  Bright Cyan  #A8D5E2  (iris)
  Muted Teal   #5A93AC  (badge border)

Requires Pillow. ImageMagick is not needed.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

PALE = (232, 244, 248)  # Pale Blue    #E8F4F8
CYAN = (168, 213, 226)  # Bright Cyan  #A8D5E2
TEAL = (90, 147, 172)   # Muted Teal   #5A93AC
MED = (42, 52, 68)      # Medium Slate #2a3444
BG = (26, 35, 50)       # Deep Slate   #1a2332 (pupil fill)

# Supersample 2x for anti-aliased edges
W, H = 2700, 600
EYE_W, EYE_H, GAP = 620, 425, 100
PAD, BORDER, RADIUS = 150, 20, 84
FONT_PATHS = [
    '/usr/share/fonts/liberation-fonts/LiberationSerif-Regular.ttf',
    '/usr/share/fonts/truetype/liberation2/LiberationSerif-Regular.ttf',
    '/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf',
]


def load_font(size):
    for p in FONT_PATHS:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    raise SystemExit(f'serif bold font not found in: {FONT_PATHS}')


def draw_eye(d, cx, cy):
    top, bot = [], []
    for i in range(201):
        t = -1 + 2 * i / 200
        top.append((cx + t * EYE_W / 2, cy - EYE_H / 2 * (1 - t * t)))
        bot.append((cx + t * EYE_W / 2, cy + EYE_H / 2 * (1 - t * t)))
    d.polygon(top + bot[::-1], outline=PALE, width=20)
    ir = int(EYE_H * 0.44)
    d.ellipse([cx - ir, cy - ir, cx + ir, cy + ir], fill=CYAN)
    pr = int(EYE_H * 0.22)
    d.ellipse([cx - pr, cy - pr, cx + pr, cy + pr], fill=BG + (255,))


def draw_logo():
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)

    # Badge: rounded box, Medium Slate fill, Muted Teal border
    d.rounded_rectangle(
        [BORDER // 2, BORDER // 2, W - 1 - BORDER // 2, H - 1 - BORDER // 2],
        radius=RADIUS, fill=MED + (255,), outline=TEAL, width=BORDER,
    )

    # Auto-fit the lettering around the fixed-size eye
    size = 400
    while True:
        font = load_font(size)
        boxes = {t: d.textbbox((0, 0), t, font=font) for t in ('DH', 'AI')}
        total = (
            boxes['DH'][2] - boxes['DH'][0]
            + GAP + EYE_W + GAP
            + boxes['AI'][2] - boxes['AI'][0]
        )
        if total <= W - 2 * PAD:
            break
        size -= 4

    cy = H // 2
    x = (W - total) // 2

    def glyph(text, x):
        b = boxes[text]
        gw, gh = b[2] - b[0], b[3] - b[1]
        d.text((x - b[0], cy - gh / 2 - b[1]), text, font=font, fill=PALE)
        return x + gw

    x = glyph('DH', x) + GAP
    draw_eye(d, x + EYE_W / 2, cy)
    glyph('AI', x + EYE_W + GAP)

    return im.resize((W // 2, H // 2), Image.LANCZOS)


def main():
    root = Path(__file__).resolve().parent.parent
    out = root / 'png' / 'logo.png'
    draw_logo().save(out)
    print(f'{out}  {W // 2}x{H // 2}')


if __name__ == '__main__':
    main()
