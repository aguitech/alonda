#!/usr/bin/env python3
"""Generate Alonda portraits batch 381-400 - fresh unique prompts (no repeats of 1-380)."""
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
TOKEN = auth["providers"]["minimax-oauth"]["access_token"]
if not TOKEN:
    TOKEN = auth["credential_pool"]["minimax-oauth"][0]["access_token"]
print(f"[token] len={len(TOKEN)}", flush=True)

# ANCHOR ALONDA - 7 atributos OBLIGATORIOS
ALONDA = (
    "Alonda, a beautiful 26-year-old woman, platinum blonde long hair, "
    "striking emerald green eyes, slim athletic figure, "
    "delicate feminine facial features, natural realistic skin texture, "
)

# Batch 381-400 - UNIQUE prompts covering fresh categories:
# Mix: subcultures, magical creatures, vintage decades, professions, animals, fantasy.
PROMPTS = {
    "381_vaporwave_90s": (
        ALONDA + "in a vaporwave aesthetic portrait from a 1995 cyber cafe, "
        "wearing a holographic iridescent bomber jacket over a CRT-graphic tee, "
        "neon-pink and cyan-tinted retro sunglasses, hair with crimped bangs, "
        "background of glowing palm trees, grid floor, and giant floating pink triangles, "
        "photorealistic with 90s scanlines, vivid hot-pink-cyan-purple palette, sharp"
    ),
    "382_phoenix_rider": (
        ALONDA + "riding a phoenix mid-flight through volcanic clouds, "
        "wearing a dark bronze breastplate over a flowing crimson cape, "
        "long platinum hair whipping upward, gripping feathered reins, "
        "phoenix wings of molten gold and ember-orange spreading behind her, "
        "volcanic peaks below erupting, sky of ash and flame, "
        "photorealistic, vivid bronze-crimson-gold-orange palette, sharp epic fantasy"
    ),
    "383_underwater_tea_ceremony": (
        ALONDA + "hosting a tea ceremony in an underwater glass pavilion in the Maldives, "
        "wearing a sage-green silk kimono with embroidered koi, "
        "kneeling at a low wooden table pouring matcha from a celadon teapot, "
        "schools of yellow butterflyfish drifting past floor-to-ceiling glass, "
        "sunbeams piercing the indigo water, photorealistic, vivid sage-celadon-yellow-indigo palette, sharp serene"
    ),
    "384_kelp_forest_ranger": (
        ALONDA + "as a marine park ranger freediving through a giant kelp forest off Monterey, "
        "wearing a bright orange rashguard and black long-jane wetsuit, "
        "camera in hand, golden seals playing in the distance, "
        "towering kelp fronds streaming toward the surface in shafts of green-gold light, "
        "photorealistic, vivid orange-green-gold palette, sharp adventure"
    ),
    "385_winter_olympic_skier": (
        ALONDA + "as an Olympic downhill skier mid-jump at the Cortina d'Ampezzo world cup, "
        "wearing a vibrant magenta racing suit with a black carbon-fiber helmet and mirrored visor, "
        "skis crossed in a stylish spread eagle above the finish line, "
        "snow plumes erupting below, jagged Dolomite peaks behind under cobalt sky, "
        "photorealistic, vivid magenta-cobalt-snow-white palette, sharp action"
    ),
    "386_venetian_mask_maker": (
        ALONDA + "as a Venetian mask maker painting a volto mask in her atelier during Carnevale, "
        "wearing a paint-smeared linen smock over a black dress, hair pinned up with pencils, "
        "delicate brush applying leaf of molten gold to a porcelain-white mask held in her hand, "
        "walls hung with dozens of finished masks in peacock blue, scarlet and gold, "
        "warm amber workshop light, photorealistic, vivid white-gold-scarlet-peacock palette, sharp artisan"
    ),
    "387_neon_tokyo_ramen_chef": (
        ALONDA + "as a ramen chef in a tiny 6-seat Shinjuku counter at 11pm, "
        "wearing a white hachimaki headband and a faded indigo apron over a tee, "
        "ladling tonkotsu broth from a copper pot into a black lacquer bowl, "
        "chashu and ajitsuke tamago lined up, steam rising, "
        "warm sodium light, photorealistic, vivid indigo-copper-cream-black palette, sharp cinematic"
    ),
    "388_storm_chaser": (
        ALONDA + "as a storm chaser in the Great Plains with a supercell behind her, "
        "wearing a yellow rain shell and cargo pants, hair blowing in outflow winds, "
        "leaning out of a 4x4 truck window with a handheld anemometer, "
        "massive turquoise-and-lavender mesocyclone rotating behind, "
        "lightning forks inside the wall cloud, "
        "photorealistic, vivid yellow-turquoise-lavender-electric-blue palette, sharp action"
    ),
    "389_aurora_yurt": (
        ALONDA + "stepping out of a reindeer-skin hung door of a Mongolian ger at midnight, "
        "wearing a deep purple deel with silver clasps over a sheepskin vest, "
        "footprints in fresh snow, stovepipe smoke rising, "
        "ribbons of pink and emerald aurora overhead, "
        "dark pine forest on horizon, photorealistic, vivid purple-emerald-pink-snow-white palette, sharp"
    ),
    "390_zen_garden_rake": (
        ALONDA + "raking a dry-rock zen garden at a Kyoto temple at sunrise, "
        "wearing a soft grey cotton kimono with a moss-green obi, wooden geta, "
        "bamboo rake tracing concentric ripples in raked sand, "
        "massive weathered boulders, maple leaves in deep red, "
        "stone lanterns and moss, photorealistic, vivid grey-green-red-sand palette, sharp serene"
    ),
    "391_whitewater_kayaker": (
        ALONDA + "as a whitewater kayaker at the bottom of Class V Lava Falls on the Colorado River, "
        "wearing a neon-orange spray skirt and a red helmet, paddle digging into a towering green wave, "
        "explosive white spray, jagged black basalt canyon walls towering above, "
        "photorealistic, vivid neon-orange-green-white-black palette, sharp action"
    ),
    "392_chocolate_artisan": (
        ALONDA + "as a Belgian chocolate artisan tempering couverture in a Brussels atelier, "
        "wearing a crisp white chef coat and a cream apron, hair tucked under a cocoa-stained cap, "
        "pouring glossy dark chocolate into baroque bon-bon molds, "
        "pistachios, freeze-dried raspberries, and gold leaf on the marble counter, "
        "soft north-window light, photorealistic, vivid cocoa-brown-pistachio-pink-gold palette, sharp"
    ),
    "393_greek_island_diver": (
        ALONDA + "freediving off the cliffs of Milos in the Cyclades, "
        "wearing a saffron bikini with a monofin, hair streaming in a thick braid, "
        "descending toward an ancient marble statue half-buried in white sand below, "
        "ultra-clear Aegean blue, white limestone cliffs above catching afternoon sun, "
        "photorealistic, vivid saffron-blue-white-limestone palette, sharp"
    ),
    "394_bonsai_master": (
        ALONDA + "as a fifth-generation bonsai master pruning a 200-year-old Japanese white pine, "
        "wearing an indigo-dyed samue with a leather knee pad, "
        "shears poised, copper-wire coils on the bench, "
        "ancient gnarled trunk with pale bark, "
        "tatami studio overlooking a moss garden, photorealistic, vivid indigo-green-copper-sand palette, sharp craft"
    ),
    "395_lighthouse_climb": (
        ALONDA + "climbing the inner spiral staircase of a lighthouse at golden hour, "
        "wearing a navy cable-knit sweater and tan corduroy pants, "
        "looking out the lantern room at a panoramic ocean view, "
        "beam of light slicing through sea mist, "
        "white and crimson lighthouse interior, "
        "photorealistic, vivid navy-crimson-gold-mist palette, sharp architectural"
    ),
    "396_falconry_champion": (
        ALONDA + "as a falconry champion at a Spanish hawking meet, "
        "wearing a waxed-cotton field jacket with leather gloves, "
        "a saker falcon perched on her fist, "
        "steppe grasses of La Mancha stretching to the horizon, "
        "warm Iberian light, photorealistic, vivid khaki-rust-warm-gold-green palette, sharp sport"
    ),
    "397_terraced_rice_farmer": (
        ALONDA + "planting rice seedlings in the Banaue terraces at dawn, "
        "wearing a hand-woven ikat headwrap, terracotta blouse, and a bamboo carrier on her back, "
        "knees in mirrored paddy water, emerald shoots in hand, "
        "stepped terraces cascading down the mountain, mist rising, "
        "photorealistic, vivid terracotta-emerald-silver-mist palette, sharp cultural"
    ),
    "398_gem_cutter": (
        ALONDA + "as a master gem cutter examining a rough opal under a loupe in a Jaipur atelier, "
        "wearing a fitted ivory linen kurta with delicate gold thread, "
        "tweezers holding the opal that flashes fire blue, green and orange, "
        "trays of unmounted sapphires, emeralds and rubies on velvet, "
        "lantern-lit courtyard, photorealistic, vivid ivory-fire-opal-blue-green-orange-gold palette, sharp"
    ),
    "399_orchestra_violinist_rooftop": (
        ALONDA + "as a concert violinist playing on a Lisbon rooftop at sunset, "
        "wearing a flowing saffron-yellow gown with a deep teal embroidered shawl, "
        "eyes closed mid-phrase, bow arcing, "
        "terracotta rooftops and the Tagus river below turning copper, "
        "pigeons wheeling, photorealistic, vivid saffron-teal-copper-terracotta palette, sharp cinematic"
    ),
    "400_glacier_pilot": (
        ALONDA + "as a bush pilot standing on the pontoon of a De Havilland Otter at twilight in Alaska, "
        "wearing a shearling flight jacket with a fur-lined hood, "
        "reflective glacier lake, glacier walls of electric blue and white behind, "
        "tundra turning lavender in last light, "
        "photorealistic, vivid electric-blue-white-lavender-shearling-brown palette, sharp adventure"
    ),
}

def gen(prompt, size="1024x1024"):
    body = json.dumps({"model": "image-01", "prompt": prompt, "n": 1, "size": size}).encode()
    req = urllib.request.Request(
        "https://api.minimax.io/v1/image_generation",
        data=body,
        headers={"Authorization": "Bearer " + TOKEN, "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=180) as r:
            data = json.loads(r.read().decode())
        urls = (data.get("data") or {}).get("image_urls") or []
        if not urls:
            print(f"[err] no urls: {json.dumps(data)[:300]}", flush=True)
            return None
        with urllib.request.urlopen(urls[0], context=ctx, timeout=180) as r:
            return r.read()
    except urllib.error.HTTPError as e:
        print(f"[http {e.code}] {e.read().decode()[:400]}", flush=True)
        return None
    except Exception as e:
        print(f"[err] {type(e).__name__}: {e}", flush=True)
        return None

def is_too_gray(img_bytes, threshold=0.55):
    try:
        im = Image.open(BytesIO(img_bytes)).convert("RGB").resize((128, 128))
        pixels = list(im.getdata())
        gray = sum(1 for r, g, b in pixels if abs(r-g)<15 and abs(g-b)<15 and abs(r-b)<15)
        return (gray/len(pixels)) > threshold
    except Exception:
        return False

def vibrant_retry(p):
    return p + " Extra saturated vivid colors, vibrant rainbow palette, hyper-colorful, no monochrome, no grayscale."

def main():
    total = len(PROMPTS)
    print(f"[start] batch 381-400: {total} portraits", flush=True)
    ok, fail = 0, 0
    for fname, prompt in PROMPTS.items():
        target = OUT / f"{fname}.jpg"
        if target.exists():
            print(f"[skip] {fname}.jpg exists", flush=True)
            ok += 1
            continue
        attempts = 0
        img = None
        cur = prompt
        while attempts < 3:
            img = gen(cur)
            attempts += 1
            if img is None:
                time.sleep(2)
                continue
            if is_too_gray(img):
                print(f"[gray] {fname} attempt {attempts} gray, retry", flush=True)
                cur = vibrant_retry(prompt)
                time.sleep(1)
                continue
            break
        if img is None:
            print(f"[FAIL] {fname}", flush=True)
            fail += 1
            continue
        try:
            Image.open(BytesIO(img)).convert("RGB").save(target, "JPEG", quality=90)
            print(f"[ok]   {fname}.jpg ({len(img)}B)", flush=True)
            ok += 1
        except Exception as e:
            print(f"[save err] {fname}: {e}", flush=True)
            fail += 1
        time.sleep(1.2)
    print(f"[done] ok={ok} fail={fail}", flush=True)
    return 0 if fail == 0 else 1

if __name__ == "__main__":
    sys.exit(main())