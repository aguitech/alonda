#!/usr/bin/env python3
"""Retry image 772 with safer Egyptian goddess prompt (no mummified body / Osiris)."""
import json, ssl, urllib.request, urllib.error, time, sys
from pathlib import Path
from PIL import Image

OUT = Path("/root/alonda/assets/images")
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

auth = json.loads(Path("/root/.hermes/auth.json").read_text())
_pool = auth.get("credential_pool") or {}
TOKEN=*** "").get("minimax" + "-oauth", {}).get("access_token") or (_pool.get("minimax" + "-oauth") or [{}])[0].get("access_token")

ALONDA = (
    "Alonda, a beautiful 26-year-old woman, platinum blonde long hair, "
    "striking emerald green eyes, slim athletic figure, "
    "delicate feminine facial features, natural realistic skin texture, "
)

# Safer version - no "mummified Osiris", no "winged protection"
PROMPTS = [
    ALONDA + "as the Egyptian goddess Isis with vivid gold sun disc and cow horn crown seated on a vivid gilded throne at the vivid turquoise Philae temple beside the vivid Nile at sunset, vivid turquoise and ivory pleated linen dress, vivid cobalt and gold broad collar usekh necklace, vivid emerald ankh loop-cross in her raised hand, vivid emerald and gold lotus staff, vivid warm Egyptian divine magic queen portrait, ultra detailed",
    ALONDA + "as the ancient Egyptian sky goddess Isis in a vivid lapis-blue and gold temple setting, vivid gold sun disc crown, vivid turquoise pleated linen gown, vivid silver ankh, vivid emerald lotus offering, vivid golden temple columns glowing in vivid amber sunset, vivid divine Egyptian queen portrait, ultra sharp",
    ALONDA + "as the Egyptian goddess Isis in vivid ceremonial regalia inside the vivid gold and ivory Abydos temple, vivid horned solar crown, vivid turquoise wrap dress, vivid usekh broad collar of vivid cobalt and emerald beads, vivid golden sistrum rattle in her hand, vivid Egyptian goddess high priestess portrait, ultra detailed",
]

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
            if urls: return urls[0], None
            last_err = f"no urls: {str(d)[:200]}"
            time.sleep(5)
        except urllib.error.HTTPError as e:
            body_err = e.read().decode(errors='replace')[:300]
            last_err = f"HTTP {e.code}: {body_err}"
            if e.code == 429: time.sleep(15); continue
            if e.code in (500, 502, 503): time.sleep(5); continue
            return None, last_err
        except Exception as e:
            last_err = repr(e); time.sleep(5)
    return None, last_err

def is_gray(path, threshold=0.55):
    try:
        im = Image.open(path).convert("RGB").resize((128, 128))
        gray = 0; total = 0
        for px in im.getdata():
            r, g, b = px
            mn, mx = min(r, g, b), max(r, g, b)
            if (mx - mn) / 255.0 < 0.10: gray += 1
            total += 1
        return (gray / total) > threshold
    except: return False

n = 772
slug_base = "as_the_egyptian_goddess_isis_in_vivid_egyptian_regalia"
fname = f"{n}_{slug_base}.jpg"
out_path = OUT / fname
print(f"=== [{n}] {fname} ===", flush=True)
for pi, PROMPT in enumerate(PROMPTS):
    print(f"  attempt prompt #{pi+1}", flush=True)
    for attempts in range(2):
        url, err = call_api(PROMPT)
        if not url:
            print(f"    [err] {err}", flush=True); break
        try:
            with urllib.request.urlopen(url, context=ctx, timeout=120) as r:
                data = r.read()
            tmp = OUT / f".tmp_{n}_{int(time.time())}.jpg"
            tmp.write_bytes(data)
            if is_gray(tmp):
                tmp.unlink(); print(f"    [gray] regen", flush=True); continue
            tmp.rename(out_path)
            print(f"    [ok] {len(data)} bytes", flush=True)
            rj = Path("/root/alonda/scripts/batch_757_776_results.json")
            if rj.exists():
                d = json.loads(rj.read_text())
                # remove old 772 entries if any, then add
                d = [x for x in d if x.get("num") != n]
                d.append({"num": n, "file": fname, "url": url, "prompt_variant": pi+1})
                rj.write_text(json.dumps(d, indent=2))
            sys.exit(0)
        except Exception as e:
            print(f"    [dl-err] {e}", flush=True); time.sleep(5)
print("[FAIL] all 3 prompts failed", flush=True); sys.exit(1)
