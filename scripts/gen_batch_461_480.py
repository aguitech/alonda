#!/usr/bin/env python3
"""Generate Alonda portraits batch 461-480 - completely new themes."""
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
_prov = auth.get("providers") or {}
_pool = auth.get("credential_pool") or {}
TOKEN = (_prov.get("minimax-oauth") or {}).get("access_token") or (_pool.get("minimax-oauth") or [{}])[0].get("access_token")
if not TOKEN:
    print("FATAL: no token", file=sys.stderr); sys.exit(2)
print(f"[token] len={len(TOKEN)}", flush=True)

ALONDA = (
    "Alonda, a beautiful 26-year-old woman, platinum blonde long hair, "
    "striking emerald green eyes, slim athletic figure, "
    "delicate feminine facial features, natural realistic skin texture, "
)

# Batch 461-480: Mythology + Extreme Sports + Sci-Fi
PROMPTS = [
    ALONDA + "as the Greek goddess Athena in gleaming bronze armor and crested helmet, holding a spear and shield with Medusa's head, standing in a marble temple with olive trees, dramatic god rays, classical Greek painting style, ultra detailed, vibrant gold and ivory palette",
    ALONDA + "as a wingsuit BASE jumper mid-flight over snowy Dolomite peaks, alpine helmet and mirrored goggles, dramatic valley below, cinematic blue sky, action photography, motion frozen, vibrant contrast",
    ALONDA + "as a cyberpunk hacker in a neon-lit back alley of Neo-Tokyo 2087, glowing holographic code in glasses, reflective trench coat, chrome drips and rain puddles, electric blue and magenta neon, ultra detailed, sharp focus",
    ALONDA + "as a Peruvian textile artist weaving a colorful Andean tapestry on a backstrap loom, surrounded by bales of alpaca wool in vibrant reds and yellows, Andean mountain backdrop, soft afternoon light, portrait photography",
    ALONDA + "as the Norse goddess Freyja riding a chariot pulled by two giant cats through a golden Asgard sky, amber necklace Brísingamen, flowing cloak, valkyrie armor, mythic Norse painting, ultra detailed, dramatic aurora overhead",
    ALONDA + "as a wingsuit pilot diving through a narrow slot canyon at sunset, sandstone walls glowing orange, dust particles in golden light, extreme adventure photography, ultra sharp, vibrant color grading",
    ALONDA + "as a quantum physicist in a futuristic particle accelerator control room, holographic atom models floating around her, white lab coat with circuit patterns, glowing teal and copper light, sci-fi realism, ultra detailed",
    ALONDA + "as a Himalayan yak herder crossing a high mountain pass in Ladakh, traditional turquoise jewelry and heavy wool robes, prayer flags fluttering, snow-capped peaks, golden evening light, documentary portrait",
    ALONDA + "as a Bigfoot researcher in the Pacific Northwest old-growth forest, khaki vest with field gear, binoculars and camera, mysterious misty mossy woods, dramatic volumetric light rays, adventure photography",
    ALONDA + "as a Venetian glassblower shaping molten orange glass at the furnace on Murano island, fiery glow on face, traditional tools, glass sculptures in workshop, dramatic chiaroscuro lighting, vibrant amber",
    ALONDA + "as a French Foreign Legion soldier on desert patrol in the Sahara, blue and white kepi cap, sand-covered boots, vast dunes at sunset, golden orange light, cinematic military photography, sharp details",
    ALONDA + "as a street magician performing a card flourish with floating cards in a Paris plaza, dramatic magenta cape, golden autumn leaves, Eiffel Tower silhouette in mist, magic hour lighting, vivid colors",
    ALONDA + "as an Amazonian shipibo shaman with geometric red and black face paint, ceremonial ayahuasca ceremony at night, surrounded by glowing jungle, firelight on skin, mystical ethno-photography, ultra detailed",
    ALONDA + "as a Formula 1 test driver in cockpit of a race car, helmet visor reflecting the track, pit crew in background, dramatic motion blur, vibrant red and chrome, motorsport photography, ultra sharp",
    ALONDA + "as a Japanese kintsugi artist carefully repairing a cracked ceramic bowl with molten gold lacquer, traditional workshop, soft golden light, kintsugi philosophy aesthetic, intimate portrait, warm tones",
    ALONDA + "as a Mongolian throat singer in traditional deel dress, vast open grassland behind, a horse nearby, dramatic golden sunset, throat singing posture, ethnographic photography, vivid sky",
    ALONDA + "as a marine biologist diving in a kelp forest with a giant sea otter beside her, sunlight filtering through emerald water, dive mask and wetsuit, vivid aquatic photography, ultra detailed, vibrant",
    ALONDA + "as a Spanish flamenco dancer in a blood-red ruffled bata de cola dress, dramatic arched back pose, golden spotlight on dark stage, motion blur in dress, sweat on brow, passionate performance photography",
    ALONDA + "as a Victorian-era ghost hunter in 1890s London fog, brass goggles and leather satchel of gadgets, gas street lamps, spectral mist, gothic steampunk aesthetic, cinematic moody lighting",
    ALONDA + "as a Thai fruit carver sculpting an intricate watermelon rose in a Bangkok market, surrounded by exotic tropical fruits, vivid dragonfruit and mangoes, warm tungsten light, food portrait photography, ultra saturated colors",
]

START = 461

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

results = []
for i, prompt in enumerate(PROMPTS):
    n = START + i
    fname = f"{n}_" + prompt[170:215].strip().replace(",", "").replace(".", "").replace(" ", "_").replace("'", "").replace('"', '').lower()[:60] + ".jpg"
    out_path = OUT / fname
    print(f"\n=== [{n}] {fname} ===", flush=True)
    attempts = 0
    while attempts < 3:
        url, err = call_api(prompt)
        if not url:
            print(f"  [err] {err}", flush=True); break
        try:
            with urllib.request.urlopen(url, context=ctx, timeout=120) as r:
                data = r.read()
            tmp = OUT / f".tmp_{n}_{int(time.time())}.jpg"
            tmp.write_bytes(data)
            if is_gray(tmp):
                tmp.unlink()
                print(f"  [gray] regenerating...", flush=True)
                attempts += 1
                continue
            tmp.rename(out_path)
            print(f"  [ok] {len(data)} bytes", flush=True)
            results.append({"num": n, "file": fname, "url": url})
            break
        except Exception as e:
            print(f"  [dl-err] {e}", flush=True); attempts += 1
    else:
        print(f"  [fail] too gray or too many errors", flush=True)
    time.sleep(2)

Path("/root/alonda/scripts/batch_461_480_results.json").write_text(json.dumps(results, indent=2))
print(f"\n[DONE] {len(results)}/{len(PROMPTS)} generated", flush=True)
