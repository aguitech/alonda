#!/usr/bin/env python3
"""Generate Alonda portraits batch 501-520 - completely new themes."""
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

# Batch 501-520: New themes - Northern Lights cultures + Reptile handlers + Vintage aviation + Musical eras + Spice route + Glass art
PROMPTS = [
    ALONDA + "as a Sami reindeer herder in the Norwegian arctic tundra under swirling aurora borealis, traditional blue and red kolt garment with embroidered belt, herding dogs at her side, vivid emerald and violet auroras, snow and lichen ground, documentary portrait photography, ultra sharp",
    ALONDA + "as a Komodo dragon field biologist on Rinca Island, khaki field vest and pith helmet, giant monitor lizard in foreground, dry savanna backdrop, vivid ochre earth and emerald foliage, wildlife conservation photography, golden hour, sharp",
    ALONDA + "as a 1930s aviator wing-walker standing atop a bright red biplane in flight, leather flight cap and goggles pushed up, white silk scarf whipping, dramatic cumulus clouds, vivid crimson plane and azure sky, vintage Kodachrome color, ultra detailed",
    ALONDA + "as a Tuvan throat singer beside a burning juniper smoke ritual on a Central Asian steppe at dusk, white felt deel robe, traditional morin khuur horsehead fiddle beside her, violet mountains, vivid amber fire glow and teal sky, ethnographic portrait, ultra sharp",
    ALONDA + "as a Venetian glassblower shaping molten amber glass on a Murano blowpipe, sweat on brow, glowing furnace behind, vivid orange molten glass and cobalt reflections, intimate workshop portrait, fire-lit chiaroscuro, ultra detailed",
    ALONDA + "as a Byzantine icon painter in a Thessaloniki monastery studio grinding lapis lazuli pigment, gold leaf halo sketches on cedar panel, deep ultramarine and vermillion pigments, candlelit intimate portrait, classical Orthodox sacred art context, vivid",
    ALONDA + "as a Maasai beadwork elder in the Kenyan savanna creating a wedding collar, layers of red, blue, white and yellow disc beads, traditional shuka cloth, acacia trees at golden hour, vivid tribal palette, intimate craft portrait, ultra sharp",
    ALONDA + "as a 19th century hot air balloon aeronaut in a wicker basket lifting off from a French countryside, brass instruments and navigational charts, billowing red and gold striped balloon, vivid pastoral palette and warm sunrise light, romantic period painting, ultra detailed",
    ALONDA + "as a Sea glass jewelry maker sorting tumbled shards on a weathered Cape Cod dock, polished cobalt blue and seafoam green and amber glass, faded denim and linen apron, vivid jewel tones against grey wood, soft overcast light, intimate artisan portrait, ultra sharp",
    ALONDA + "as a Silk Road caravan trader at a Samarkand bazaar silk merchant stall, holding bolts of saffron yellow and indigo madder dyed silk, tiled madrasa dome behind, vivid spice market palette, ethnographic photography, sharp focus",
    ALONDA + "as an Inuit throat singer drum dancer on sea ice under polar night, vivid aurora green ribbons overhead, white caribou fur parka with crimson trim, hand drum with caribou hide, vivid cold blues and emerald sky, fine art photography, ultra sharp",
    ALONDA + "as a Bahian acarajé seller on a Salvador da Bahia street at dusk, white cotton dress and head wrap, frying golden black-eyed pea fritters in dendê palm oil, vivid saffron fritters and cobalt blue walls, street portrait, warm lighting, sharp",
    ALONDA + "as an Edo period ukiyo-e woodblock printer carving cherry wood blocks in a Tokyo atelier, cherry print key block and color blocks visible, vivid beni red and indigo inks, late afternoon light through paper screens, traditional craft portrait, ultra detailed",
    ALONDA + "as a Galápagos marine iguana researcher snorkeling in shallow turquoise water, wetsuit and research clipboard in waterproof bag, volcanic black rocks, vivid teal water and emerald seaweed, sunlit underwater scene, wildlife science photography, sharp",
    ALONDA + "as a 1960s Cuban son singer on a Havana rooftop at sunset, white guayabera and wide-brimmed straw sombrero, tres cubano guitar, faded pastel Caribbean architecture, vivid magenta bougainvillea, golden hour tropical light, vintage film photography, ultra detailed",
    ALONDA + "as a Patagonian wind surfer riding a Lago Argentino storm gust, vivid electric blue and lime green sail, snow-capped Andes in distance, fierce wind whipping platinum hair, vivid storm grey and glacier blue, action sports photography, ultra sharp",
    ALONDA + "as a Kyoto kintsugi master repairing a shattered tea bowl with urushi lacquer and gold powder, magnifying headband, simple black samue, glowing workshop, vivid gold seams against crackled celadon bowl, intimate craft portrait, ultra detailed",
    ALONDA + "as a Mongolian eagle hunter on a vast Altai steppe in winter, heavy white fox fur coat and traditional malgai headdress, golden eagle perched on her gloved fist, vivid cold blue steppe and pale dawn light, ethnographic portrait, ultra sharp",
    ALONDA + "as an Andalusian flamenco dancer mid-braceo pose in a Seville patio, vivid crimson bata de cola gown with white polka dots, castanets mid-clack, terracotta tile and bougainvillea backdrop, dramatic warm stage light, ultra detailed",
    ALONDA + "as a deep-core ice core scientist in a Greenland research station, red parka and glacier glasses, ice core samples on lab bench, vivid cobalt blue ice layers visible in core, fluorescent lab light, science documentary photography, ultra sharp",
]

START = 501

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
    body = prompt[len(ALONDA):] if prompt.startswith(ALONDA) else prompt
    slug = body[:60].strip().replace(",", "").replace(".", "").replace(" ", "_").replace("'", "").replace('"', '').lower()[:60]
    fname = f"{n}_" + slug + ".jpg"
    out_path = OUT / fname
    print(f"\n=== [{n}] {fname} ===", flush=True)
    attempts = 0
    success = False
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
            success = True
            break
        except Exception as e:
            print(f"  [dl-err] {e}", flush=True); attempts += 1
    if not success:
        print(f"  [fail] too gray or too many errors", flush=True)
    time.sleep(2)

Path("/root/alonda/scripts/batch_501_520_results.json").write_text(json.dumps(results, indent=2))
print(f"\n[DONE] {len(results)}/{len(PROMPTS)} generated", flush=True)
