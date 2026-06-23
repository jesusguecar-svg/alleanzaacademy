#!/usr/bin/env python3
"""Deriva las variantes del logo a partir del oficial `assets/alleanza_logo.png`.

Genera:
  - alleanza_logo_white.png : wordmark "ALLEANZA" en blanco (para fondos oscuros).
  - alleanza_mark.png       : solo el escudo (recortado).

Uso:  python3 scripts/make_logo_variants.py
"""
import os
from PIL import Image

ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
src = os.path.join(ASSETS, "alleanza_logo.png")

im = Image.open(src).convert("RGBA")
W, H = im.size
px = im.load()

# --- variante wordmark blanco (recolorea el navy a la derecha del escudo) ---
xcut = int(W * 0.255)
white = im.copy(); wp = white.load()
for y in range(H):
    for x in range(xcut, W):
        r, g, b, a = px[x, y]
        if a > 0 and max(r, g, b) < 95:        # texto navy (incl. bordes AA)
            wp[x, y] = (255, 255, 255, a)
white.save(os.path.join(ASSETS, "alleanza_logo_white.png"))

# --- variante solo escudo ---
mark = im.crop((0, 0, int(W * 0.245), H))
mark = mark.crop(mark.getbbox())
mark.save(os.path.join(ASSETS, "alleanza_mark.png"))

print("Variantes generadas en", ASSETS)
