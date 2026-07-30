#!/usr/bin/env python3
"""Regenerate 468 and 469 with more vibrant prompts."""
import json, ssl, urllib.request, urllib.error, time, sys
from pathlib import Path
from PIL import Image
from io import BytesIO

OUT = Path("/root/alonda/assets/images")
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

auth = json.loads(Path("/root/.hermes/auth.json").read_text())
_prov = auth.get("providers") or {}
_pool = auth.get("credential_pool") or {}
TOKEN=(_prov.get("minimax-oauth") or {}).get("access_token") or (_pool.get("minimax-oauth") or [{}])[0].get("access_token")

ALONDA = (
    "Alonda, a beautiful 26-year-old woman, platinum blonde long hair, "
    "striking emerald green eyes, slim athletic figure, "
    "delicate feminine facial features, natural realistic skin texture, "
)

# More vibrant re-prompts for 468 and 469
PROMPTS = {
    468: ALONDA + "as a colorful Himalayan yak herder crossing a high mountain pass in Ladakh, wearing bright turquoise coral and magenta traditional jewelry, holding a vivid rainbow prayer flag pole, snow-capped peaks glowing pink at sunset, golden evening light, saturated vivid colors, documentary portrait photography, ultra detailed",
    469: ALONDA + "as a Bigfoot researcher in the Pacific Northwest rainforest celebrating a discovery, khaki vest with neon orange patches, surrounded by bright red fly agaric mushrooms and emerald moss, golden volumetric sunbeams piercing the canopy, adventure photography, vibrant saturated colors, ultra detailed",
}

def call_api(prompt, retries=2):
    url = "https://api." + "minimax" + ".io/v1/image_generation"
    body = json.dumps({"model": "image-01", "prompt": prompt, "size": "1024x1024", "n": 1}).encode()
    req = urllib.request.Request(url, data=body, headers={
        "Authorization": "Bearer " + TOKEN,
        "Content-Type": "application/json",
    })
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, context=ctx, timeout=180) as r:
                d = json.loads(r.read().decode())
            urls = d.get("data", {}).get("image_urls") or []
            return urls[0], None
        except urllib.error.HTTPError as e:
            err = f"HTTP {e.code}"
            if e.code == 429: time.sleep(15); continue
            if e.code in (500, 502, 503): time.sleep(5); continue
            return None, err
        except Exception as e:
            time.sleep(3)
    return None, "retries"

def is_gray(path, threshold=0.55):
    try:
        im = Image.open(path).convert("RGB").resize((128, 128))
        gray = 0; total = 0
        for px in im.getdata():
            r, g, b = px
            mx = max(r, g, b); mn = min(r, g, b)
            sat = (mx - mn) / 255.0 if mx else 0
            if sat < 0.10: gray += 1
            total += 1
        return (gray / total) > threshold
    except Exception:
        return False

for n, prompt in PROMPTS.items():
    # keep existing filename pattern
    files = list(OUT.glob(f"{n}_*.jpg"))
    if files:
        out_path = files[0]
        print(f"=== regenerating {n} -> {out_path.name} ===", flush=True)
    else:
        out_path = OUT / f"{n}_regenerated.jpg"
        print(f"=== generating {n} -> {out_path.name} ===", flush=True)

    for attempt in range(4):
        url, err = call_api(prompt)
        if not url:
            print(f"  [err] {err}", flush=True); continue
        try:
            with urllib.request.urlopen(url, context=ctx, timeout=120) as r:
                data = r.read()
            tmp = OUT / f".tmp_{n}_{int(time.time())}.jpg"
            tmp.write_bytes(data)
            if is_gray(tmp):
                tmp.unlink()
                print(f"  [gray] attempt {attempt+1}", flush=True)
                continue
            tmp.rename(out_path)
            print(f"  [ok] {len(data)} bytes", flush=True)
            break
        except Exception as e:
            print(f"  [dl-err] {e}", flush=True)
    else:
        print(f"  [fail] all attempts", flush=True)
