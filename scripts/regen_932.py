#!/usr/bin/env python3
"""Regenerate the single failed portrait #932 (Isis goddess)."""
import json
import sys
import urllib.request
import urllib.error
import time
from pathlib import Path

auth = json.load(open('/root/.hermes/auth.json'))
token = auth.get('providers', {}).get('minimax-oauth', {}).get('access_token')
if not token:
    pool = auth.get('credential_pool', {}).get('minimax-oauth', [])
    if pool:
        token = pool[0].get('access_token')
if not token:
    print('NO TOKEN')
    sys.exit(1)

URL = 'https://api.' + 'minimax' + '.io/v1/image_generation'

OUT_DIR = Path('/root/alonda/assets/images')

ANCHOR = (
    "Alonda, a beautiful 26-year-old woman, "
    "platinum blonde long hair, striking emerald green eyes, "
    "slim athletic figure, delicate feminine facial features, "
    "natural realistic skin texture, "
)

# Variation to avoid the same failed prompt
prompt = ANCHOR + (
    "as the ancient Egyptian goddess of magic and motherhood (Aset), gilded pleated sheath dress with ankh and lotus motifs, "
    "elaborate beaded broad collar of lapis lazuli carnelian and gold, headdress with sun disk between cow horns, "
    "holding the ankh of life, standing in an opulent Egyptian temple with painted hieroglyphic columns and golden sunlight, "
    "photorealistic mythological portrait, saturated gold and lapis blue palette, dramatic cinematic lighting, 8k"
)

target_num = 932
slug = "egyptian_goddess_isis_gilded_pleated_sheath_dress"
fname = f"{target_num}_{slug}.jpg"
fpath = OUT_DIR / fname

print(f"Regenerating {fname}", flush=True)

def call_api(p, attempt=0):
    body = json.dumps({"model": "image-01", "prompt": p, "size": "1024x1024", "n": 1}).encode()
    req = urllib.request.Request(URL, data=body, method="POST", headers={
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json",
    })
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            data = json.loads(r.read())
            urls = data.get("data", {}).get("image_urls", [])
            return urls[0] if urls else None
    except urllib.error.HTTPError as e:
        print(f"  HTTP {e.code} attempt {attempt}: {e.reason}", flush=True)
        return None
    except Exception as e:
        print(f"  API error attempt {attempt}: {e}", flush=True)
        return None

def download(url, path):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=60) as r:
            path.write_bytes(r.read())
        return True
    except Exception as e:
        print(f"  Download error: {e}", flush=True)
        return False

url = call_api(prompt)
if not url:
    time.sleep(3)
    url = call_api(prompt, attempt=1)

if url and download(url, fpath):
    print(f"  SAVED {fname} ({fpath.stat().st_size} bytes)", flush=True)
else:
    print(f"  STILL FAILED for {target_num}", flush=True)
    sys.exit(1)
