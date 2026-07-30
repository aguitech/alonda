#!/usr/bin/env python3
"""Generate Alonda portraits batch 481-500 - completely new themes."""
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
TOKEN = (_prov.get("minimax-oauth") or {}).get("access_token") or (_pool.get("minimax-oauth") or [{}])[0].get("access_token")
if not TOKEN:
    print("FATAL: no token", file=sys.stderr); sys.exit(2)
print(f"[token] len={len(TOKEN)}", flush=True)

ALONDA = (
    "Alonda, a beautiful 26-year-old woman, platinum blonde long hair, "
    "striking emerald green eyes, slim athletic figure, "
    "delicate feminine facial features, natural realistic skin texture, "
)

# Batch 481-500: Mythology cont. + Renaissance crafts + Underwater worlds + Decades
PROMPTS = [
    ALONDA + "as the Greek goddess Persephone in an eternal spring meadow, pomegranate in hand, flowing chiton of deep crimson and gold, wildflowers at her feet, soft golden hour light, classical Greek painting style, ultra detailed, vivid floral palette",
    ALONDA + "as a master luthier hand-carving a violin in a Cremona workshop, curls of maple wood on the bench, varnish pot open, soft amber window light, intimate artisan portrait, warm wood tones, ultra detailed",
    ALONDA + "as a free diver descending into a crystal blue cenote in the Yucatan, sunlight shafts piercing turquoise water, limestone cave formations, single breath dive mask, vivid aquamarine tones, underwater photography, ultra sharp",
    ALONDA + "as a 1940s WWII-era riveter on an aircraft assembly line, red polka-dot bandana rolled hair, denim work overalls, sleeves rolled, determination on face, propaganda poster aesthetic, sepia with pops of red and navy, sharp focus",
    ALONDA + "as the Japanese goddess Amaterasu stepping from a cave, brilliant solar disc halo behind her, sacred mirror in hand, shrine maiden robes of crimson and white, cherry blossoms swirling, dramatic golden hour, mythic painting, vibrant",
    ALONDA + "as a Swiss watchmaker assembling a tourbillon movement under a loupe, hair pinned back, hundreds of tiny gears on velvet mat, soft cool workbench lamp, microscopic precision world, ultra detailed, muted golds and steel blues",
    ALONDA + "as a synchronized swimmer mid-routine in an Olympic pool, nose plug and floral cap, underwater camera angle, sunlight refracting through surface, vivid aqua water, droplets sparkling, ultra sharp, sports photography",
    ALONDA + "as a 1920s Parisian cabaret performer in a beaded flapper dress with feathered headband, cigarette holder pose, art deco backdrop, jazz age sparkle, glamorous studio lighting, vivid emerald and silver sequins, ultra detailed",
    ALONDA + "as an Egyptian pharaoh's architect surveying the half-built pyramid at Giza, white linen robes with gold collar usekh, papyrus scroll in hand, dramatic desert sunset, workers in distance, golden sand tones, epic historical painting",
    ALONDA + "as a deep sea submarine pilot inside a yellow submersible porthole, glowing bioluminescent creatures outside the window, control panel of analog dials, dramatic teal and amber light, retro sci-fi realism, ultra detailed",
    ALONDA + "as a Mexican alebrijes artisan painting an intricate fantastical creature sculpture in a Oaxaca workshop, dozens of vivid magenta, turquoise, and orange brushstrokes, vibrant folk art aesthetic, intimate craft portrait, warm light",
    ALONDA + "as a competitive rock climber mid-route on El Capitan, chalk bag at waist, crimp grip on a granite edge, Yosemite valley far below, dramatic afternoon light, vivid green pine and grey stone, action sports photography, ultra sharp",
    ALONDA + "as the Slavic goddess Mokosh weaving the threads of fate at a golden loom, white Slavic embroidered blouse, rivers of light flowing from the threads, enchanted forest clearing, ethereal warm glow, mythic painting, vivid",
    ALONDA + "as a 1960s mod go-go dancer on a swinging London stage in a white vinyl miniskirt and go-go boots, geometric op-art backdrop, vivid orange and magenta lighting, dynamic pose mid-kick, retro pop photography, ultra saturated",
    ALONDA + "as a kelp farmer harvesting giant kelp blades from a boat in Monterey Bay, wetsuit and rubber boots, Pacific sunset behind, vivid orange sun and emerald fronds, sustainable ocean farming portrait, golden hour, ultra detailed",
    ALONDA + "as a celestial cartographer mapping constellations in a Victorian observatory, brass telescope and star charts, ink-stained fingers, candle and moonlight, deep navy and gold palette, steampunk realism, intimate portrait",
    ALONDA + "as a Brazilian capoeira mestre in white abadá pants and cordão cord, low ginga stance, berimbau in hands, vibrant Bahian sunset, motion blur in sweep, vivid yellow and earth red, dynamic action portrait, sharp focus",
    ALONDA + "as a Japanese tea ceremony master in a Kyoto tatami room, kneeled before a rustic chawan bowl, soft late afternoon light through paper shoji, vivid matcha green, wabi-sabi aesthetic, intimate portrait, warm muted palette",
    ALONDA + "as a Polynesian wayfinder navigator on a double-hulled voyaging canoe at dawn, traditional tattoos, braided hair with flowers, vast Pacific Ocean, crimson sunrise, ancient seafaring tradition, ethnographic photography, vivid",
    ALONDA + "as a 1980s synthwave aerobics instructor on a sunlit Miami beach, neon pink leotard and leg warmers, cassette player on towel, palm trees and art deco skyline, vivid magenta and cyan, retro film photography aesthetic, ultra saturated",
]

START = 481

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
    # Extract a stable slug from the prompt body (after ALONDA anchor)
    body = prompt[len(ALONDA):] if prompt.startswith(ALONDA) else prompt
    # Take first 60 chars of body, clean
    slug = body[:60].strip().replace(",", "").replace(".", "").replace(" ", "_").replace("'", "").replace('"', '').lower()[:60]
    fname = f"{n}_" + slug + ".jpg"
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

Path("/root/alonda/scripts/batch_481_500_results.json").write_text(json.dumps(results, indent=2))
print(f"\n[DONE] {len(results)}/{len(PROMPTS)} generated", flush=True)
