#!/usr/bin/env python3
"""Verify colorfulness of new portraits 875-894.
A grayscale-heavy image is bad (>55% gray pixels)."""
from PIL import Image
from pathlib import Path
import sys

OUT = Path('/root/alonda/assets/images')
files = sorted(OUT.glob('89[0-4]_alonda_*.jpg')) + sorted(OUT.glob('88[5-9]_alonda_*.jpg'))
files = sorted(set(files), key=lambda p: int(p.name.split('_')[0]))

gray_count = 0
total = 0
for f in files:
    try:
        img = Image.open(f).convert('RGB').resize((128, 128))
        pixels = list(img.tobytes())  # raw RGB bytes
        pixels = [pixels[i:i+3] for i in range(0, len(pixels), 3)]
        n = len(pixels)
        # pixel is "gray-ish" if max(rgb)-min(rgb) < 15
        gray_like = sum(1 for r,g,b in pixels if max(r,g,b) - min(r,g,b) < 15)
        pct = 100 * gray_like / n
        verdict = 'GRAY' if pct > 55 else 'OK'
        print(f"{f.name}: {pct:.1f}% gray-like  -> {verdict}")
        total += 1
        if pct > 55:
            gray_count += 1
    except Exception as e:
        print(f"{f.name}: ERROR {e}")

print(f"\nTotal: {total}, gray-flagged: {gray_count}")
sys.exit(0 if gray_count == 0 else 1)