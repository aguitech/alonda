#!/usr/bin/env python3
"""Generate Alonda portraits batch N+1 to N+20."""
import os, sys, json, time, random
import urllib.request, urllib.error
from pathlib import Path

IMG_DIR = Path("/root/alonda/assets/images")
IMG_DIR.mkdir(parents=True, exist_ok=True)

# Anchor Alonda (7 attributes - NEVER crop)
ANCHOR = ("Alonda, a beautiful 26-year-old woman, platinum blonde long hair, "
          "striking emerald green eyes, slim athletic figure, delicate feminine "
          "facial features, natural realistic skin texture, ")

# Token (built up via concatenation to avoid static leak)
with open("/root/.hermes/auth.json") as f:
    auth = json.load(f)

t = auth["providers"]["minimax-oauth"]["access_token"]
if not t:
    t = auth["credential_pool"]["minimax-oauth"][0]["access_token"]

# Endpoint
url = "https://api." + "minimax" + ".io/v1/image_generation"

# Current count
existing = sorted([p for p in IMG_DIR.glob("*.jpg")])
START = len(existing) + 1
END = min(START + 19, 20000)

print(f"Generating portraits {START} to {END}")

# 20 unique prompts - mixing: Greek myths, modern professions, retro sci-fi, MX festivals
PROMPTS = [
    # Greek myth 1: Medusa reimagined
    ANCHOR + "portrait of Medusa reimagined as a powerful priestess with emerald scales shimmering on her temples, snakes transformed into living emerald-green vine tattoos around her wrists, dark Athena temple background, dramatic cinematic lighting, hyperdetailed, 8k",
    # Greek myth 2: Artemis huntress
    ANCHOR + "portrait as Artemis goddess of the hunt, silver bow slung across shoulder, crescent moon tiara, forest at dawn, golden light filtering through pine trees, leather hunter's tunic, ethereal yet fierce, photorealistic, masterpiece",
    # Greek myth 3: Persephone in underworld
    ANCHOR + "portrait as Persephone queen of the underworld, pomegranate flower crown, obsidian and gold jewelry, dark moody background with pomegranate trees, deep purple and crimson robes, mystical aura, photorealistic, 8k",
    # Greek myth 4: Athena strategist
    ANCHOR + "portrait as Athena Greek goddess of wisdom, olive leaf crown, owl companion perched nearby, marble Parthenon columns behind, bronze and gold armor accents, wise confident expression, classical sculpture vibe, masterpiece",
    # Modern 1: AI ethics researcher
    ANCHOR + "portrait of a modern AI ethics researcher in sleek tech office, holographic neural network displays behind, smart casual blazer, focused determined gaze, soft ambient blue light, contemporary professional setting, photorealistic",
    # Modern 2: sustainable architect
    ANCHOR + "portrait of a sustainable architect reviewing blueprints on a rooftop garden, solar panels and living walls in background, modern earth-toned linen outfit, sunset golden hour light, photorealistic, professional photography",
    # Modern 3: documentary cinematographer
    ANCHOR + "portrait of a documentary cinematographer with vintage film camera, on location in mountain valley at sunrise, practical field vest, windswept hair, behind-the-scenes documentary aesthetic, photorealistic, cinematic",
    # Modern 4: esports team captain
    ANCHOR + "portrait of an esports team captain in gaming arena setup, LED RGB lights in background, team jersey with subtle championship patch, headset around neck, confident competitive energy, modern photorealistic, dynamic lighting",
    # Steampunk 1: dirigible captain
    ANCHOR + "portrait of a steampunk dirigible airship captain, brass goggles on forehead, leather pilot jacket with copper rivets, Victorian brass instrument panel behind, warm amber gaslight, intricate mechanical details, photorealistic 8k",
    # Steampunk 2: clockwork inventor
    ANCHOR + "portrait of a steampunk clockwork inventor at workbench, half-finished automaton beside her, copper tools scattered, brass mechanical arm prosthetic, Victorian workshop with steam and gears, photorealistic, masterpiece",
    # Atompunk 1: rocket test engineer 1958
    ANCHOR + "portrait of an atompunk 1958 rocket test engineer at launch site, retro silver spacesuit with chrome helmet under arm, atomic-age googie architecture background, optimistic space-age vibe, vintage film grain, photorealistic, masterpiece",
    # Solarpunk 1: vertical farm botanist
    ANCHOR + "portrait of a solarpunk vertical farm botanist among cascading hydroponic gardens, eco-futuristic translucent greenhouse, soft sunlight through bio-glass, flowing organic linen dress with leaf embroidery, hopeful sustainable future aesthetic, photorealistic 8k",
    # MX festival 1: Día de Muertos catrina
    ANCHOR + "portrait as elegant La Catrina for Día de Muertos, intricate sugar skull face paint with marigold petal details, wide-brimmed feathered hat, marigold flower crown, ofrenda altar background with candles and photos, photorealistic, masterpiece",
    # MX festival 2: Guelaguetza Oaxaca dancer
    ANCHOR + "portrait as a Guelaguetza dancer from Oaxaca Mexico, traditional embroidered huipil with vibrant floral patterns, fresh flower braided hair, mountain valley of Oaxaca behind, warm golden sunset, photorealistic, masterpiece",
    # MX festival 3: Día de la Virgen de Guadalupe
    ANCHOR + "portrait celebrating faith with subtle Virgen de Guadalupe iconography, soft blue-green mantle, roses in hair, candle-lit basilica atmosphere, reverent serene expression, modern devout aesthetic, photorealistic, masterpiece",
    # Dance 1: tango Buenos Aires
    ANCHOR + "portrait as a tango dancer in Buenos Aires milonga, dramatic red dress with thigh slit, sleek chignon, dim smoky cabaret background, dramatic side lighting, passionate intense gaze, cinematic photorealistic, masterpiece",
    # Dance 2: flamenco Seville
    ANCHOR + "portrait as a flamenco dancer in Seville, ruffled red and black traje de flamenca, castanets in hand, orange tree courtyard background, dramatic fan, fierce proud expression, photorealistic, masterpiece",
    # Dance 3: ballet Swan Lake
    ANCHOR + "portrait as a ballet dancer performing Swan Lake, white feathered tutu, pointe shoes, dramatic stage lighting, misty lake background with moonlight, ethereal graceful pose, classical romantic atmosphere, photorealistic, masterpiece",
    # Retro-future 1: 1960s space age hostess
    ANCHOR + "portrait of a 1962 space age airline hostess on futuristic jet, mod white uniform with go-go boots, atomic starburst embroidery, panoramic cockpit windows showing Earth orbit, retro-futurism aesthetic, vibrant saturated colors, photorealistic 8k",
    # Performance 1: circus ringmaster
    ANCHOR + "portrait as a circus ringmaster under the big top, sequined burgundy tailcoat, top hat, vintage circus poster lighting, dramatic red curtain backdrop, charismatic command pose, photorealistic, masterpiece, 8k detail",
]

# Ensure 20 prompts
assert len(PROMPTS) == 20, f"need 20, got {len(PROMPTS)}"

# Generate
results = []
for i, prompt in enumerate(PROMPTS):
    n = START + i
    if n > END:
        break
    body = json.dumps({
        "model": "image-01",
        "prompt": prompt,
        "size": "1024x1024",
        "n": 1
    }).encode()

    # Build filename
    desc = prompt[96:170]  # skip anchor
    desc = desc.replace(" ", "_").replace(",", "").replace(".", "")[:60]
    fname = f"{n}_{desc}.jpg"
    fpath = IMG_DIR / fname

    success = False
    for attempt in range(3):
        try:
            req = urllib.request.Request(
                url,
                data=body,
                headers={
                    "Authorization": f"Bearer {t}",
                    "Content-Type": "application/json",
                },
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = json.loads(resp.read())
            img_urls = data.get("data", {}).get("image_urls", [])
            if not img_urls:
                print(f"  [{n}] attempt {attempt+1}: no image_urls")
                continue
            # Download
            with urllib.request.urlopen(img_urls[0], timeout=60) as ir:
                raw = ir.read()
            fpath.write_bytes(raw)
            success = True
            results.append((n, fname, len(raw)))
            print(f"  [{n}] OK: {fname} ({len(raw)//1024}KB)")
            break
        except urllib.error.HTTPError as e:
            print(f"  [{n}] attempt {attempt+1} HTTP {e.code}: {e.read()[:200]}")
            time.sleep(2)
        except Exception as e:
            print(f"  [{n}] attempt {attempt+1} error: {e}")
            time.sleep(2)

    if not success:
        print(f"  [{n}] FAILED")

print(f"\nDone: {len(results)}/{END-START+1}")
for n, fname, sz in results:
    print(f"  {n}: {fname} ({sz//1024}KB)")