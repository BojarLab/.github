"""Draws the showcase glycans for the BojarLab org README with GlycoDraw, as die-cut stickers.

Usage: python scripts/draw_glycans.py build/glycans
"""
import sys
from pathlib import Path
from glycowork.motif.draw import GlycoDraw

out = sys.argv[1]
Path(out).mkdir(parents = True, exist_ok = True)
glycans = {
    'n_glycan': 'Neu5Ac(a2-6)Gal(b1-4)GlcNAc(b1-2)Man(a1-3)[Neu5Ac(a2-6)Gal(b1-4)GlcNAc(b1-2)Man(a1-6)]Man(b1-4)GlcNAc(b1-4)[Fuc(a1-6)]GlcNAc',
    'o_glycan': 'Neu5Ac(a2-3)Gal(b1-3)[Gal(b1-4)GlcNAc(b1-6)]GalNAc',
    'hmo': 'Fuc(a1-2)Gal(b1-3)GlcNAc(b1-3)Gal(b1-4)Glc',
    'slex': 'Neu5Ac(a2-3)Gal(b1-4)[Fuc(a1-3)]GlcNAc',
    'gm1': 'Gal(b1-3)GalNAc(b1-4)[Neu5Ac(a2-3)]Gal(b1-4)Glc1Cer',
}
for name, seq in glycans.items():
    d = GlycoDraw(seq, sticker = True, suppress = True, show_linkage = True)
    d.save(f'{out}/{name}.png')
    print(name, d.drawing_obj.width, d.drawing_obj.height)
