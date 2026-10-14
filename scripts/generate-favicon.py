#!/usr/bin/env python3
"""Generate the site favicon set from the DH-AI-eye brand mark.

Outputs (relative to repo root):
  png/favicon-master.png      1024x1024 source mark
  png/apple-touch-icon.png    180x180 (iOS home screen)
  png/favicon-32.png          32x32   (browser tab)
  png/favicon-16.png          16x16   (browser tab, small)

The mark uses the site palette from css/style.css:
  Deep Slate  #1a2332  (background)
  Pale Blue   #E8F4F8  (lettering, eye outline)
  Bright Cyan #A8D5E2  (iris)

Requires Pillow. ImageMagick is not needed.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

BG = (26, 35, 50)       # Deep Slate  #1a2332
PALE = (232, 244, 248)  # Pale Blue   #E8F4F8
CYAN = (168, 213, 226)  # Bright Cyan #A8D5E2

S = 1024
EYE_W, EYE_H, STROKE = 470, 290, 16
FONT_SIZE = 250
FONT_PATHS = [
    '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf',
    '/usr/share/fonts/dejavu/DejaVuSerif-Bold.ttf',
]


def load_font():
    for p in FONT_PATHS:
        if Path(p).exists():
            return ImageFont.truetype(p, FONT_SIZE)
    raise SystemExit(f'serif bold font not found in: {FONT_PATHS}')


def draw_master():
    im = Image.new('RGB', (S, S), BG)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, S - 1, S - 1], radius=192, fill=BG)
    font = load_font()
    cx, cy = S // 2, S // 2

    # Eye: almond outline with cyan iris and dark pupil
    top, bot = [], []
    for i in range(201):
        t = -1 + 2 * i / 200
        top.append((cx + t * EYE_W / 2, cy - EYE_H / 2 * (1 - t * t)))
        bot.append((cx + t * EYE_W / 2, cy + EYE_H / 2 * (1 - t * t)))
    d.polygon(top + bot[::-1], outline=PALE, width=STROKE)

    ir = 132
    d.ellipse([cx - ir, cy - ir, cx + ir, cy + ir], fill=CYAN)
    pr = 64
    d.ellipse([cx - pr, cy - pr, cx + pr, cy + pr], fill=BG)

    # DH above the eye, AI below it
    for text, ymid in (('DH', cy - EYE_H / 2 - 130), ('AI', cy + EYE_H / 2 + 130)):
        b = d.textbbox((0, 0), text, font=font)
        gw, gh = b[2] - b[0], b[3] - b[1]
        d.text((cx - gw / 2 - b[0], ymid - gh / 2 - b[1]), text, font=font, fill=PALE)

    return im


def main():
    root = Path(__file__).resolve().parent.parent
    png = root / 'png'
    master = draw_master()
    master.save(png / 'favicon-master.png')
    for name, size in (
        ('apple-touch-icon.png', 180),
        ('favicon-32.png', 32),
        ('favicon-16.png', 16),
    ):
        im = master.resize((size, size), Image.LANCZOS)
        im.save(png / name)
        print(f'{png / name}  {size}x{size}')


if __name__ == '__main__':
    main()
