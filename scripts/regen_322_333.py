#!/usr/bin/env python3
"""Regenerate 322 and 333 with neutralized prompts (were flagged sensitive)."""
import json, ssl, urllib.request, urllib.error, time, sys
from pathlib import Path
from PIL import Image
from io import BytesIO

OUT = Path("/root/alonda/assets/images")
OUT.mkdir(parents=True, exist_ok=True)

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

auth = json.loads(Path("/root/.hermes/auth.json").read_text())
TOKEN = auth.get("providers", {}).get("minimax-oauth", {}).get("access_token") or \
        auth.get("credential_pool", {}).get("minimax-oauth", [{}])[0].get("access_token") or \
        auth.get("minimax-oauth", {}).get("access_token") or ""
print(f"[token] len={len(TOKEN)}", flush=True)

ALONDA = (
    "Alonda, a beautiful 26-year-old woman, platinum blonde long hair, "
    "striking emerald green eyes, slim athletic figure, "
    "delicate feminine facial features, natural realistic skin texture, "
)

PROMPTS = {
    "322_isis_goddess": (
        ALONDA + "as the ancient Egyptian high priestess of the temple of Isis, "
        "wearing a pleated white linen sheath dress with a golden broad collar necklace and a tall golden throne-shaped ceremonial headdress, "
        "holding a golden ankh staff, standing in a sandstone temple hall with painted hieroglyphs and papyrus columns, "
        "warm golden afternoon light streaming through the doorway, photorealistic, vivid emerald white and gold palette, sharp"
    ),
    "333_arabic_bellydance": (
        ALONDA + "as a classical Arabic dancer performing at a Marrakech palace at night, "
        "wearing a richly embroidered magenta and gold bedlah costume with coin belt and hip scarf, "
        "holding small finger cymbals, dancing in a tiled courtyard with carved cedar arches, "
        "warm lantern light, mosaic walls, photorealistic, vivid magenta-gold-orange palette, sharp"
    ),
}

def gen(prompt: str) -> bytes | None:
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
        print(f"[err] {type(e).__name__}: {e}", flush=True)
        return None

def is_too_gray(img_bytes: bytes, threshold: float = 0.55) -> bool:
    try:
        im = Image.open(BytesIO(img_bytes)).convert("RGB").resize((128, 128))
        pix = list(im.getdata())
        gray = sum(1 for r, g, b in pix if abs(r - g) < 15 and abs(g - b) < 15 and abs(r - b) < 15)
        return (gray / len(pix)) > threshold
    except Exception:
        return False

for fname, prompt in PROMPTS.items():
    target = OUT / f"{fname}.jpg"
    if target.exists():
        print(f"[skip] {fname}.jpg", flush=True)
        continue
    img = None
    cur = prompt
    for attempt in range(3):
        img = gen(cur)
        if img is None:
            time.sleep(2)
            continue
        if is_too_gray(img):
            print(f"[gray] {fname} retrying", flush=True)
            cur = prompt + " Extra vivid saturated colors, vibrant palette, hyper-colorful."
            time.sleep(1)
            continue
        break
    if img is None:
        print(f"[FAIL] {fname}", flush=True)
        continue
    Image.open(BytesIO(img)).convert("RGB").save(target, "JPEG", quality=90)
    print(f"[ok]   {fname}.jpg ({len(img)} bytes)", flush=True)
    time.sleep(1.2)
