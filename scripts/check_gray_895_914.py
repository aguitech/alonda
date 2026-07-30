#!/usr/bin/env python3
"""Check grayscale-level for batch 895-914."""
from PIL import Image
from pathlib import Path
import sys

OUT = Path('/root/alonda/assets/images')
files = []
for n in range(895, 915):
    matches = list(OUT.glob(f'{n}_*.jpg'))
    if matches:
        files.extend(matches)
files = sorted(set(files), key=lambda p: int(p.name.split('_')[0]))

gray_count = 0
flagged = []
for f in files:
    try:
        img = Image.open(f).convert('RGB').resize((128, 128))
        pixels = list(img.tobytes())
        pixels = [pixels[i:i+3] for i in range(0, len(pixels), 3)]
        n = len(pixels)
        gray_like = sum(1 for r, g, b in pixels if max(r, g, b) - min(r, g, b) < 15)
        pct = 100 * gray_like / n
        verdict = 'GRAY' if pct > 55 else 'OK'
        print(f"{f.name}: {pct:.1f}% gray-like  -> {verdict}")
        if pct > 55:
            gray_count += 1
            flagged.append(f.name)
    except Exception as e:
        print(f"{f.name}: ERROR {e}")

print(f"\nTotal checked: {len(files)}, gray-flagged: {gray_count}")
if flagged:
    print("FLAGGED:", flagged)
sys.exit(0 if gray_count == 0 else 1)
