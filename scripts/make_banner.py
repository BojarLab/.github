"""Composes the BojarLab org README banner: title on the left, a collage of GlycoDraw glycan stickers on the right.

Usage: python scripts/make_banner.py build/glycans profile/assets/banner.png
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import glycorender

glycan_dir, out = Path(sys.argv[1]), sys.argv[2]
fonts = Path(glycorender.__file__).parent / 'fonts'
W, H = 2560, 800

# Deep blue gradient, so the white sticker cuts read well in light and dark GitHub themes alike
top, bottom = (10, 30, 52), (20, 66, 98)
bg = Image.new('RGB', (W, H))
px = bg.load()
for y in range(H):
    for x in range(W):
        t = 0.65 * y / H + 0.35 * x / W
        px[x, y] = tuple(round(a + (b - a) * t) for a, b in zip(top, bottom))
bg = bg.convert('RGBA')

# Faint oversized SNFG shapes in the background
deco = Image.new('RGBA', (W, H), (0, 0, 0, 0))
dd = ImageDraw.Draw(deco)
snfg = {'blue': (0, 144, 188), 'green': (0, 166, 81), 'yellow': (255, 212, 0), 'red': (237, 28, 36), 'purple': (165, 67, 153)}
dd.ellipse((-120, 520, 260, 900), fill = snfg['green'] + (28,))
dd.rectangle((980, -90, 1220, 150), fill = snfg['blue'] + (24,))
dd.polygon([(1080, 860), (1240, 600), (1400, 860)], fill = snfg['red'] + (22,))
dd.polygon([(2440, -60), (2620, 120), (2440, 300), (2260, 120)], fill = snfg['purple'] + (26,))
dd.ellipse((2330, 600, 2620, 890), fill = snfg['yellow'] + (22,))
bg = Image.alpha_composite(bg, deco.filter(ImageFilter.GaussianBlur(2)))

# Sticker collage: (name, height in px, center x, center y, rotation in degrees)
layout = [
    ('n_glycan', 330, 1965, 250, -4),
    ('hmo', 190, 1280, 200, 6),
    ('gm1', 255, 1400, 580, 5),
    ('o_glycan', 230, 1890, 610, -3),
    ('slex', 225, 2345, 585, -8),
]
for name, h, cx, cy, rot in layout:
    im = Image.open(glycan_dir / f'{name}.png').convert('RGBA')
    im = im.resize((round(im.width * h / im.height), h), Image.LANCZOS)
    im = im.rotate(rot, resample = Image.BICUBIC, expand = True)
    bg.alpha_composite(im, (cx - im.width // 2, cy - im.height // 2))

d = ImageDraw.Draw(bg)
title = ImageFont.truetype(str(fonts / 'Montserrat-Bold.ttf'), 150)
sub = ImageFont.truetype(str(fonts / 'Montserrat-Regular.ttf'), 50)
small = ImageFont.truetype(str(fonts / 'Montserrat-Bold.ttf'), 34)
x0 = 120
d.text((x0, 220), 'Bojar Lab', font = title, fill = (255, 255, 255))
d.text((x0, 410), 'Machine learning in glycobiology', font = sub, fill = (214, 228, 240))
d.text((x0, 475), 'and systems biology', font = sub, fill = (214, 228, 240))
# SNFG-colored rule under the title
for i, c in enumerate(['blue', 'green', 'yellow', 'red', 'purple']):
    d.rounded_rectangle((x0 + i * 78, 580, x0 + i * 78 + 64, 592), radius = 6, fill = snfg[c])
d.text((x0, 625), 'UNIVERSITY OF GOTHENBURG  ·  SWEDEN', font = small, fill = (140, 176, 204))

bg.convert('RGB').save(out, optimize = True)
