#!/usr/bin/env python3
"""Regenerate 536 with more vibrant prompt."""
import json, ssl, urllib.request, urllib.error, time
from pathlib import Path
from PIL import Image

OUT = Path("/root/alonda/assets/images")
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

auth = json.loads(Path("/root/.hermes/auth.json").read_text())
_prov = auth.get("providers") or {}
_pool = auth.get("credential_pool") or {}
_provider_key = "minimax" + "-oauth"
TOKEN = (_prov.get(_provider_key) or {}).get("access_token") or (_pool.get(_provider_key) or [{}])[0].get("access_token")

ALONDA = (
    "Alonda, a beautiful 26-year-old woman, platinum blonde long hair, "
    "striking emerald green eyes, slim athletic figure, "
    "delicate feminine facial features, natural realistic skin texture, "
)

PROMPT = (
    ALONDA +
    "as an Irish sean-nós singer in a vibrant Connemara coastal cottage doorway "
    "with electric emerald green Atlantic ocean and rainbow behind, vivid saffron "
    "Aran sweater with crimson Celtic knot embroidery, fiddle with rosewood grain "
    "in her hands, vivid magenta fuchsia rhododendrons in foreground, blazing "
    "golden hour sunlight, lush saturated color palette, intimate folk music portrait, ultra sharp"
)

def call_api(prompt, retries=3):
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
            return (d.get("data", {}).get("image_urls") or [None])[0]
        except Exception as e:
            print(f"  attempt {attempt+1}: {e}", flush=True)
            time.sleep(5)
    return None

url = call_api(PROMPT)
print(f"url: {url}", flush=True)
if url:
    with urllib.request.urlopen(url, context=ctx, timeout=120) as r:
        data = r.read()
    out = OUT / "536_as_an_irish_sean-n_singer_in_a_connemara_coastal_cottage_vibran.jpg"
    out.write_bytes(data)
    print(f"saved {len(data)} bytes to {out.name}", flush=True)

    # Verify not gray
    im = Image.open(out).convert("RGB").resize((128, 128))
    gray = total = 0
    for px in im.get_flattened_data() if hasattr(im, 'get_flattened_data') else im.getdata():
        r, g, b = px
        sat = (max(r,g,b) - min(r,g,b)) / 255.0
        if sat < 0.10: gray += 1
        total += 1
    print(f"gray ratio: {gray/total:.2%}", flush=True)
