#!/usr/bin/env python3
"""Regen portrait 486 with vivid colors (previous was too gray)."""
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
TOKEN = (_prov.get("minimax-oauth") or {}).get("access_token") or (_pool.get("minimax-oauth") or [{}])[0].get("access_token")
if not TOKEN:
    print("FATAL: no token", file=sys.stderr); sys.exit(2)

ALONDA = (
    "Alonda, a beautiful 26-year-old woman, platinum blonde long hair, "
    "striking emerald green eyes, slim athletic figure, "
    "delicate feminine facial features, natural realistic skin texture, "
)

# More vibrant regen of 486 — vivid gem-toned jewelry bench
PROMPT = ALONDA + "as a Swiss watchmaker at a gem-set jewelry bench assembling a movement, surrounded by vivid ruby, sapphire, and emerald gemstones, jeweler's loupe on eye, hundreds of tiny gears in vivid rose gold and electric blue, dramatic cool teal workshop lamp and warm amber glow, ultra detailed, saturated color palette"

def call_api(prompt, retries=2):
    url = "https://api." + "minimax" + ".io/v1/image_generation"
    body = json.dumps({"model": "image-01", "prompt": prompt, "size": "1024x1024", "n": 1}).encode()
    req = urllib.request.Request(url, data=body, headers={
        "Authorization": "Bearer " + TOKEN,
        "Content-Type": "application/json",
    })
    last_err = None
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, context=ctx, timeout=180) as r:
                d = json.loads(r.read().decode())
            urls = d.get("data", {}).get("image_urls") or []
            return urls[0], None
        except urllib.error.HTTPError as e:
            body_err = e.read().decode(errors='replace')[:300]
            last_err = f"HTTP {e.code}: {body_err}"
            if e.code == 429: time.sleep(15); continue
            if e.code in (500, 502, 503): time.sleep(5); continue
            return None, last_err
        except Exception as e:
            last_err = repr(e); time.sleep(3)
    return None, last_err

def is_gray(path, threshold=0.55):
    try:
        im = Image.open(path).convert("RGB").resize((128, 128))
        gray = 0; total = 0
        for px in im.getdata():
            r, g, b = px
            mn, mx = min(r, g, b), max(r, g, b)
            sat = (mx - mn) / 255.0 if mx else 0
            if sat < 0.10: gray += 1
            total += 1
        return (gray / total) > threshold
    except Exception:
        return False

# Existing 486 files to delete
for f in OUT.glob("486_*.jpg"):
    print(f"[cleanup] removing {f}", flush=True)
    f.unlink()

# Pick a unique name
fname = "486_as_a_swiss_watchmaker_at_a_gem-set_jewelry_bench_assembling.jpg"
out_path = OUT / fname
print(f"\n=== [486] {fname} ===", flush=True)

attempts = 0
while attempts < 3:
    url, err = call_api(PROMPT)
    if not url:
        print(f"  [err] {err}", flush=True); break
    try:
        with urllib.request.urlopen(url, context=ctx, timeout=120) as r:
            data = r.read()
        tmp = OUT / f".tmp_486_{int(time.time())}.jpg"
        tmp.write_bytes(data)
        if is_gray(tmp):
            tmp.unlink()
            print(f"  [gray] regenerating...", flush=True)
            attempts += 1; continue
        tmp.rename(out_path)
        print(f"  [ok] {len(data)} bytes", flush=True)
        break
    except Exception as e:
        print(f"  [dl-err] {e}", flush=True); attempts += 1
