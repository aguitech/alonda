#!/usr/bin/env python3
"""Regenerate portrait #891 (Persephone - last retry of batch)."""
import json
import urllib.request
import urllib.error
import ssl
from pathlib import Path
import time
import re

auth = json.load(open('/root/.hermes/auth.json'))
token = auth.get('providers', {}).get('minimax-oauth', {}).get('access_token')

URL = 'https://api.' + 'minimax' + '.io/v1/image_generation'
OUT = Path('/root/alonda/assets/images')

ANCHOR = (
    "Alonda, a beautiful 26-year-old woman, "
    "platinum blonde long hair, striking emerald green eyes, "
    "slim athletic figure, delicate feminine facial features, "
    "natural realistic skin texture, "
)

# Slot 16 was Persephone. Use a fresh variant.
prompt = (
    f"{ANCHOR}Greek goddess Persephone holding a glowing pomegranate and a torch, "
    f"in an underworld garden of silver asphodel flowers, half her figure in shadow "
    f"half in golden light, flowing gown of deep crimson and obsidian, pomegranate-red "
    f"and gold-leaf color palette, photorealistic mythological portrait"
)

body = json.dumps({"model": "image-01", "prompt": prompt, "size": "1024x1024", "n": 1}).encode()
ctx = ssl.create_default_context()

for attempt in range(3):
    try:
        req = urllib.request.Request(
            URL, data=body,
            headers={'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token},
            method='POST',
        )
        with urllib.request.urlopen(req, context=ctx, timeout=120) as r:
            payload = json.loads(r.read().decode())
        urls = payload.get('data', {}).get('image_urls') if payload.get('data') else None
        if not urls:
            print('attempt', attempt+1, 'no urls:', json.dumps(payload)[:200])
            time.sleep(3); continue
        url = urls[0]
        with urllib.request.urlopen(url, context=ctx, timeout=120) as r:
            data = r.read()
        slug = re.sub(r'[^a-z0-9]+', '_', prompt.lower()).strip('_')[:80]
        out_path = OUT / f"891_{slug}.jpg"
        out_path.write_bytes(data)
        print(f"[OK] {out_path.name} ({len(data)//1024} KB)")
        break
    except Exception as e:
        print('attempt', attempt+1, 'err:', e)
        time.sleep(3)