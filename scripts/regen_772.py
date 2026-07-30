#!/usr/bin/env python3
"""Retry image 772 (Isis) only."""
import json, ssl, urllib.request, urllib.error, time, sys
from pathlib import Path
from PIL import Image

OUT = Path("/root/alonda/assets/images")
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

auth = json.loads(Path("/root/.hermes/auth.json").read_text())
_pool = auth.get("credential_pool") or {}
TOKEN=auth.get("providers", {}).get("minimax" + "-oauth", {}).get("access_token") or (_pool.get("minimax" + "-oauth") or [{}])[0].get("access_token")

ALONDA = (
    "Alonda, a beautiful 26-year-old woman, platinum blonde long hair, "
    "striking emerald green eyes, slim athletic figure, "
    "delicate feminine facial features, natural realistic skin texture, "
)

PROMPT = ALONDA + "as the Egyptian goddess Isis with vivid gold sun-disc and cow horn crown kneeling at the vivid Nilebank spreading vivid silver-cyan winged protection over a vivid mummified Osiris, vivid turquoise and ivory pleated linen dress, vivid cobalt and gold broad collar usekh, vivid emerald ankh loop-cross, vivid Egyptian divine magic mother portrait, ultra detailed"

def call_api(prompt, retries=3):
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
            if urls:
                return urls[0], None
            last_err = f"no image_urls in response: {str(d)[:200]}"
            time.sleep(5)
        except urllib.error.HTTPError as e:
            body_err = e.read().decode(errors='replace')[:300]
            last_err = f"HTTP {e.code}: {body_err}"
            if e.code == 429: time.sleep(15); continue
            if e.code in (500, 502, 503): time.sleep(5); continue
            return None, last_err
        except Exception as e:
            last_err = repr(e)
            time.sleep(5)
    return None, last_err

def is_gray(path, threshold=0.55):
    try:
        im = Image.open(path).convert("RGB").resize((128, 128))
        gray = 0; total = 0
        for px in im.get_flattened_data() if hasattr(im, 'get_flattened_data') else im.getdata():
            r, g, b = (px, px, px) if isinstance(px, int) else (px[0], px[1], px[2])
            mn, mx = min(r, g, b), max(r, g, b)
            if (mx - mn) / 255.0 < 0.10: gray += 1
            total += 1
        return (gray / total) > threshold
    except Exception as e:
        print(f"[gray-check-err] {e}", flush=True)
        return False

n = 772
fname = "772_as_the_egyptian_goddess_isis_with_vivid_gold_sun-disc_and_co.jpg"
out_path = OUT / fname
print(f"=== [{n}] retry {fname} ===", flush=True)
for attempts in range(4):
    url, err = call_api(PROMPT)
    if not url:
        print(f"  [err] {err}", flush=True)
        time.sleep(5); continue
    try:
        with urllib.request.urlopen(url, context=ctx, timeout=120) as r:
            data = r.read()
        tmp = OUT / f".tmp_{n}_{int(time.time())}.jpg"
        tmp.write_bytes(data)
        if is_gray(tmp):
            tmp.unlink(); print(f"  [gray] regen", flush=True); continue
        tmp.rename(out_path)
        print(f"  [ok] {len(data)} bytes", flush=True)
        # Update results
        rj = Path("/root/alonda/scripts/batch_757_776_results.json")
        if rj.exists():
            d = json.loads(rj.read_text())
            d.append({"num": n, "file": fname, "url": url})
            rj.write_text(json.dumps(d, indent=2))
        sys.exit(0)
    except Exception as e:
        print(f"  [dl-err] {e}", flush=True)
        time.sleep(5)
print("[FAIL]", flush=True); sys.exit(1)
