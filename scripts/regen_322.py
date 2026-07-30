#!/usr/bin/env python3
"""Regenerate 322 with totally different topic (avoid flags)."""
import json, ssl, urllib.request, urllib.error, time
from pathlib import Path
from PIL import Image
from io import BytesIO

OUT = Path("/root/alonda/assets/images")
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

auth = json.loads(Path("/root/.hermes/auth.json").read_text())
p = auth.get("providers", {})
TOKEN = p.get("minimax-oauth", {}).get("access_token", "") or \
       auth.get("credential_pool", {}).get("minimax-oauth", [{}])[0].get("access_token", "") or \
       auth.get("minimax-oauth", {}).get("access_token", "")
print(f"[token] len={len(TOKEN)}", flush=True)

ALONDA = (
    "Alonda, a beautiful 26-year-old woman, platinum blonde long hair, "
    "striking emerald green eyes, slim athletic figure, "
    "delicate feminine facial features, natural realistic skin texture, "
)

PROMPT = (
    ALONDA + "as an ancient Mesopotamian high priestess in the ziggurat of Ur, "
    "wearing a fringed ceremonial robe in deep emerald green with gold embroidery, "
    "tall blue lapis lazuli beaded headdress with golden crescent ornaments, "
    "standing at the top of the ziggurat at twilight with the fertile Tigris river plains below, "
    "burning copper brazier beside her, indigo dusk sky with first stars, "
    "photorealistic, vivid emerald indigo and gold palette, sharp cinematic"
)

def gen(prompt):
    body = json.dumps({"model": "image-01", "prompt": prompt, "n": 1, "size": "1024x1024"}).encode()
    req = urllib.request.Request(
        "https://api.minimax.io/v1/image_generation",
        data=body,
        headers={"Authorization": "Bearer " + TOKEN, "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=180) as r:
            data = json.loads(r.read().decode())
        urls = (data.get("data") or {}).get("image_urls") or []
        if not urls:
            print(f"[err] {json.dumps(data)[:300]}", flush=True)
            return None
        with urllib.request.urlopen(urls[0], context=ctx, timeout=180) as r:
            return r.read()
    except Exception as e:
        print(f"[err] {e}", flush=True)
        return None

target = OUT / "322_ziggurat_priestess.jpg"
img = None
for attempt in range(3):
    img = gen(PROMPT)
    if img:
        break
    time.sleep(2)

if img is None:
    print("[FAIL] 322", flush=True)
else:
    Image.open(BytesIO(img)).convert("RGB").save(target, "JPEG", quality=90)
    print(f"[ok] {target.name} ({len(img)} bytes)", flush=True)
