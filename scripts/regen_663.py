#!/usr/bin/env python3
"""Regen Alonda 663 (Isis) which failed in batch 657-676."""
import json, ssl, urllib.request, urllib.error, time, sys
from pathlib import Path
from PIL import Image

OUT = Path("/root/alonda/assets/images")
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

auth = json.loads(Path("/root/.hermes/auth.json").read_text())
_prov = auth.get("providers") or {}
_pool = auth.get("credential_pool") or {}
KEY = "minimax" + "-oauth"
TOKEN = (_prov.get(KEY) or {}).get("access_token") or (_pool.get(KEY) or [{}])[0].get("access_token")
if not TOKEN:
    print("FATAL: no token", file=sys.stderr); sys.exit(2)

ALONDA = (
    "Alonda, a beautiful 26-year-old woman, platinum blonde long hair, "
    "striking emerald green eyes, slim athletic figure, "
    "delicate feminine facial features, natural realistic skin texture, "
)

PROMPT = ALONDA + "as Isis Egyptian goddess of magic with vivid gilded falcon-wing headdress, golden ankh in one hand and vivid vermilion throne symbol in the other, white linen sheath dress, vivid lapis lazuli and gold jewelry, dramatic Nile sunset behind with vermilion and saffron papyrus reeds, vivid Egyptian mythology portrait, ultra detailed"

fname = "663_as_isis_egyptian_goddess_of_magic_with_vivid_gilded_falcon.jpg"
out_path = OUT / fname

url = "https://api." + "minimax" + ".io/v1/image_generation"
body = json.dumps({"model": "image-01", "prompt": PROMPT, "size": "1024x1024", "n": 1}).encode()
req = urllib.request.Request(url, data=body, headers={
    "Authorization": "Bearer " + TOKEN,
    "Content-Type": "application/json",
})

for attempt in range(3):
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=180) as r:
            d = json.loads(r.read().decode())
        urls = d.get("data", {}).get("image_urls") or []
        if not urls:
            print(f"[err] no url returned (attempt {attempt+1})", flush=True); time.sleep(5); continue
        image_url = urls[0]
        with urllib.request.urlopen(image_url, context=ctx, timeout=120) as r:
            data = r.read()
        tmp = OUT / f".tmp_663_{int(time.time())}.jpg"
        tmp.write_bytes(data)
        # gray check
        im = Image.open(tmp).convert("RGB").resize((128, 128))
        gray = 0; total = 0
        for px in im.getdata():
            r, g, b = px
            mn, mx = min(r, g, b), max(r, g, b)
            sat = (mx - mn) / 255.0 if mx else 0
            if sat < 0.10: gray += 1
            total += 1
        if (gray/total) > 0.55:
            tmp.unlink()
            print(f"[gray] regenerating (attempt {attempt+1})...", flush=True); time.sleep(3); continue
        tmp.rename(out_path)
        print(f"[ok] {len(data)} bytes -> {fname}", flush=True)
        sys.exit(0)
    except Exception as e:
        print(f"[err] attempt {attempt+1}: {e}", flush=True); time.sleep(5)

print("FAILED all attempts", flush=True)
sys.exit(1)
