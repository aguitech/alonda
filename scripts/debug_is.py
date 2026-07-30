#!/usr/bin/env python3
"""Generate Alonda portraits batch 737-756 - new themes.
Mix: Hindu mythology (Durga, Lakshmi, Saraswati, Kali, Hanuman),
Chinese mythology (Nüwa, Chang'e, Sun Wukong, Nezha, Bai Suzhen),
Norse creatures (Jörmungandr, Sleipnir, Fenrir, Huginn/Muninn, Valkyrie),
African mythology (Shango, Yemaya, Anansi, Ogun, Mawu-Lisa),
Southeast Asian (Thai naga, Indonesian wayang, Filipino diwata, Vietnamese lac queros),
Polynesian (Pele, Maui, Hina, Kupe, Tangaroa),
South American folklore (Iara, Saci, Cuca, Mapinguari, Boitatá),
rare winter sports (curling, luge, biathlon, skeleton, ski jumping),
whale/ocean creatures (orca, humpback, manta ray, sea otter, narwhal),
classical composers (Bach, Mozart, Beethoven, Chopin, Debussy),
ballet roles (Swan Lake, Giselle, Nutcracker, Sleeping Beauty, Don Quixote),
virtual worlds (metaverse architect, VR therapist, holodeck, sim designer, digital twin),
rare professions (clockmaker, luthier, perfumer, falconer, master distiller).
"""
import json, ssl, urllib.request, urllib.error, time, sys
from pathlib import Path
from PIL import Image

OUT = Path("/root/alonda/assets/images")
OUT.mkdir(parents=True, exist_ok=True)

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

auth = json.loads(Path("/root/.hermes/auth.json").read_text())
_prov = auth.get("providers") or {}
_pool = auth.get("credential_pool") or {}
KEY = "minimax" + "-oauth"
TOKEN=auth.get("providers", {}).get("minimax" + "-oauth", {}).get("access_token") or (_pool.get("minimax" + "-oauth") or [{}])[0].get("access_token")
if not TOKEN:
    print("FATAL: no token", file=sys.stderr); sys.exit(2)
print(f"[token] len={len(TOKEN)}", flush=True)

ALONDA = "Alonda, a beautiful 26-year-old woman, platinum blonde long hair, striking emerald green eyes, slim athletic figure, delicate feminine facial features, natural realistic skin texture, "

PROMPT = ALONDA + "as the Egyptian goddess Isis in vivid ceremonial regalia inside the vivid gold and ivory Abydos temple, vivid horned solar crown, vivid turquoise wrap dress, vivid usekh broad collar of vivid cobalt and emerald beads, vivid golden sistrum rattle in her hand, vivid Egyptian goddess high priestess portrait, ultra detailed"


# START removed

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
            if e.code in (500, 502, 503):
                time.sleep(5); continue
            return None, last_err
        except Exception as e:
            last_err = repr(e)
            time.sleep(3)
    return None, last_err

def is_gray(path, threshold=0.55):
    try:
        im = Image.open(path).convert("RGB").resize((128, 128))
        gray = 0
        total = 0
        for px in im.getdata():
            r, g, b = px
            mn, mx = min(r, g, b), max(r, g, b)
            sat = (mx - mn) / 255.0 if mx else 0
            if sat < 0.10:
                gray += 1
            total += 1
        return (gray / total) > threshold
    except Exception:
        return False

url, err = call_api(PROMPT, retries=1)
print("URL:", url, file=__import__("sys").stderr)
print("ERR:", err, file=__import__("sys").stderr)
import urllib.request as _ur
if url:
    with _ur.urlopen(url, context=ctx, timeout=60) as _r:
        print("STATUS:", _r.status, file=__import__("sys").stderr)
        print("BODY-1k:", _r.read()[:500], file=__import__("sys").stderr)

Path("/root/alonda/scripts/batch_737_756_results.json").write_text(json.dumps(results, indent=2))
print(f"\n[DONE] {len(results)}/{len(PROMPTS)} generated", flush=True)
