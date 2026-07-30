#!/usr/bin/env python3
"""Regenerate portrait 777 (Morrigan) with more vibrant prompt."""
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
_access = (_prov.get(KEY) or {}).get("access_token")
if not _access:
    _first = (_pool.get(KEY) or [{}])[0]
    _access = _first.get("access_token")
TOKEN = str(_access) if _access else ""

ALONDA = (
    "Alonda, a beautiful 26-year-old woman, platinum blonde long hair, "
    "striking emerald green eyes, slim athletic figure, "
    "delicate feminine facial features, natural realistic skin texture, "
)

# More vibrant Morrigan prompt with strong colors
prompt = ALONDA + (
    "as the Celtic goddess Morrigan in vivid crimson and jet-black feathered "
    "battle armor with vivid metallic emerald pauldrons, standing on a vivid "
    "vermilion hilltop at twilight with two vivid jet-black ravens on her "
    "shoulders and a vivid glowing emerald war spear, vivid crimson war cloak "
    "billowing, vivid silver Celtic torc, vivid gold crow mask pushed up on her "
    "head, vivid orange and magenta sunset sky, vivid Irish war fate "
    "sovereignty goddess portrait, ultra sharp"
)

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
            if e.code == 429:
                time.sleep(15); continue
            return None, last_err
        except Exception as e:
            last_err = repr(e)
            time.sleep(3)
    return None, last_err

def is_gray(path, threshold=0.55):
    try:
        im = Image.open(path).convert("RGB").resize((128, 128))
        gray = 0; total = 0
        for px in list(im.getdata()):
            r, g, b = px
            mn, mx = min(r, g, b), max(r, g, b)
            sat = (mx - mn) / 255.0 if mx else 0
            if sat < 0.10: gray += 1
            total += 1
        return (gray / total) > threshold
    except: return False

n = 777
fname = f"{n}_celtic_morrigan_vivid_vermilion_crimson_battle_armor.jpg"
out_path = OUT / fname
for attempt in range(3):
    print(f"=== [{n}] attempt {attempt+1} ===", flush=True)
    url, err = call_api(prompt)
    if not url:
        print(f"[err] {err}", flush=True); break
    try:
        with urllib.request.urlopen(url, context=ctx, timeout=120) as r:
            data = r.read()
        tmp = OUT / f".tmp_{n}_{int(time.time())}.jpg"
        tmp.write_bytes(data)
        if is_gray(tmp):
            tmp.unlink()
            print(f"  [gray] retrying...", flush=True)
            continue
        tmp.rename(out_path)
        print(f"  [ok] {len(data)} bytes -> {fname}", flush=True)
        break
    except Exception as e:
        print(f"  [dl-err] {e}", flush=True)