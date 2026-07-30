#!/usr/bin/env python3
"""Retry 501 and 509 with adjusted prompts."""
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
_provider_key = "minimax" + "-oauth"
TOKEN = (_prov.get(_provider_key) or {}).get("access_token") or (_pool.get(_provider_key) or [{}])[0].get("access_token")
if not TOKEN:
    print("FATAL: no token", file=sys.stderr); sys.exit(2)
print(f"[token] len={len(TOKEN)}", flush=True)

ALONDA = (
    "Alonda, a beautiful 26-year-old woman, platinum blonde long hair, "
    "striking emerald green eyes, slim athletic figure, "
    "delicate feminine facial features, natural realistic skin texture, "
)

# Replacement prompts (more vivid, fewer gray-prone words)
RETRIES = [
    (501, ALONDA + "as a Sami reindeer herder in snowy Norwegian arctic tundra under brilliant emerald and violet aurora borealis, vivid blue and red traditional kolt garment with yellow embroidered belt, fluffy reindeer and herding dogs at her side, snow and pink lichen ground, vivid portrait photography, ultra sharp, full color"),
    (509, ALONDA + "as a sea glass jewelry maker on a vibrant turquoise dock in Cape Cod, piles of tumbled cobalt blue and seafoam green and amber and ruby red glass shards spread on weathered wood, vivid jewel tones, golden hour sun flare, intimate artisan portrait, ultra sharp, saturated colors"),
]

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
            return None, "no image_urls"
        except urllib.error.HTTPError as e:
            body_err = e.read().decode(errors='replace')[:300]
            last_err = f"HTTP {e.code}: {body_err}"
            if e.code == 429:
                time.sleep(15); continue
            if e.code in (500, 502, 503):
                time.sleep(5); continue
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

results = []
for n, prompt in RETRIES:
    body = prompt[len(ALONDA):]
    slug = body[:60].strip().replace(",", "").replace(".", "").replace(" ", "_").replace("'", "").replace('"', '').lower()[:60]
    fname = f"{n}_" + slug + ".jpg"
    out_path = OUT / fname
    print(f"\n=== [{n}] {fname} ===", flush=True)
    success = False
    for attempt in range(3):
        url, err = call_api(prompt)
        if not url:
            print(f"  [err attempt {attempt}] {err}", flush=True)
            time.sleep(5); continue
        try:
            with urllib.request.urlopen(url, context=ctx, timeout=120) as r:
                data = r.read()
            tmp = OUT / f".tmp_{n}_{int(time.time())}.jpg"
            tmp.write_bytes(data)
            if is_gray(tmp):
                tmp.unlink()
                print(f"  [gray attempt {attempt}]", flush=True)
                continue
            tmp.rename(out_path)
            print(f"  [ok] {len(data)} bytes", flush=True)
            results.append({"num": n, "file": fname, "url": url})
            success = True
            break
        except Exception as e:
            print(f"  [dl-err {attempt}] {e}", flush=True)
    if not success:
        print(f"  [FAIL] for {n}", flush=True)

# Merge into the main results json
main_results_path = Path("/root/alonda/scripts/batch_501_520_results.json")
existing = json.loads(main_results_path.read_text()) if main_results_path.exists() else []
existing_by_num = {r["num"]: r for r in existing}
for r in results:
    existing_by_num[r["num"]] = r
merged = sorted(existing_by_num.values(), key=lambda x: x["num"])
main_results_path.write_text(json.dumps(merged, indent=2))
print(f"\n[DONE] merged results now {len(merged)} items", flush=True)
