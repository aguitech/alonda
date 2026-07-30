#!/usr/bin/env python3
"""Generate Alonda portraits batch 361-380 - fresh unique prompts (no repeats of 1-360)."""
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

# Batch 361-380 - UNIQUE prompts (no overlap with prior 1-360)
# Mix: ocean, sports, mythology, music, magical creatures, professions, travel.
PROMPTS = {
    "361_coral_diver": (
        ALONDA + "as a marine biologist freediving over a living coral reef in Raja Ampat, "
        "wearing a sleek cobalt wetsuit with mask and snorkel pushed up, "
        "schools of electric-blue damsels swirling around her, massive purple seafan behind, "
        "crystal-clear turquoise water, sun rays piercing the surface, "
        "photorealistic, vivid cobalt-turquoise-purple palette, sharp underwater"
    ),
    "362_archery_champion": (
        ALONDA + "as a champion archer at full draw at a Mongolian naadam archery contest, "
        "wearing a traditional deel in vermilion silk with gold brocade sash, "
        "composite recurve bow drawn, arrow nocked, focused emerald gaze along the shaft, "
        "steppe grasslands stretching behind, white gers in distance, "
        "photorealistic, vivid vermilion-gold-green palette, sharp sport"
    ),
    "363_thor_valkyrie": (
        ALONDA + "as the Norse goddess Skuld the Valkyrie on a windswept Nordic ridge, "
        "wearing burnished silver scale armor over a fur-lined cloak of storm-grey, "
        "long platinum braid whipping sideways, holding a spectral spear of crackling white lightning, "
        "storm clouds boiling, ravens wheeling, photorealistic, vivid silver-grey-lightning palette, sharp"
    ),
    "364_harpsichordist": (
        ALONDA + "as a Baroque harpsichordist in a candlelit Venetian salon in 1720, "
        "wearing a pale rose silk gown with panniers and silver lace engageantes, "
        "powdered coiffure with pearl pins, hands mid-trill on ivory keys, "
        "ornate carved and gilded harpsichord with painted lid, music scores scattered, "
        "photorealistic, vivid rose-gold-ivory palette, sharp historical"
    ),
    "365_velociraptor_paleo": (
        ALONDA + "as a paleontologist in the Gobi Desert at dawn, "
        "wearing a dusty khaki field jacket with a multi-pocket vest and leather satchel, "
        "kneeling beside an exposed velociraptor skeleton half-emerged from sandstone, "
        "holding a small brush and geological hammer, crimson desert cliffs behind, "
        "photorealistic, vivid khaki-crimson-sand palette, sharp adventure"
    ),
    "366_dragonsmith": (
        ALONDA + "as a dragonsmith forging a sword in a volcanic forge, "
        "wearing heavy black leather apron and iron-shod boots, hair tied back with a leather cord, "
        "hammering a blade of glowing orange dragonsteel on an anvil with embers flying, "
        "lava channel behind, dragon-scale cooling rack, "
        "photorealistic, vivid orange-black-iron palette, sharp fantasy crafts"
    ),
    "367_tango_buenos_aires": (
        ALONDA + "as a tango dancer in a milonga in San Telmo Buenos Aires at midnight, "
        "wearing a backless crimson satin dress with a thigh slit and stiletto heels, "
        "mid-corte with leg extended, partner's hand on her waist, "
        "wrought-iron balcony, dim amber chandelier, smoky golden light, "
        "photorealistic, vivid crimson-amber-black palette, sharp dance"
    ),
    "368_kintsugi_master": (
        ALONDA + "as a Japanese kintsugi master kneeling at a low workbench in a Kyoto townhouse, "
        "wearing an indigo-dyed samue with a tan leather apron, hair in a loose low bun, "
        "painting seams of molten gold across a broken celadon teabowl with a fine brush, "
        "tatami floor, hanging scrolls, soft window light, "
        "photorealistic, vivid indigo-gold-celadon palette, sharp craft"
    ),
    "369_jetski_racer": (
        ALONDA + "as a jetski championship racer carving a hard turn at the Pro Watercross World Finals, "
        "wearing a neon-yellow and black racing vest over a wetsuit, helmet visor up, "
        "rooster tail of white spray arcing behind, orange buoy course markers, "
        "Miami turquoise water, photorealistic, vivid neon-yellow-turquoise-orange palette, sharp action"
    ),
    "370_honey_harvest": (
        ALONDA + "as a Croatian beekeeper harvesting honey from traditional bagrem hives in late summer, "
        "wearing a white canvas bee suit with veiled hat pushed back, holding a dripping frame of amber comb, "
        "thousands of bees swarming, goldenrod flowers in the orchard behind, "
        "Adriatic stone walls, photorealistic, vivid amber-white-green palette, sharp"
    ),
    "371_cyber_neon_alley": (
        ALONDA + "in a Blade Runner 2049 cyberpunk alley in nighttime Neo-Tokyo, "
        "wearing a glossy black vinyl trenchcoat with neon-pink piping, "
        "rain-slick street reflecting kanji signs in electric blue and magenta, "
        "drones hovering, her face lit only by holo-ads, "
        "photorealistic, vivid magenta-electric-blue-black palette, sharp sci-fi noir"
    ),
    "372_balloon_pilot_rainbow": (
        ALONDA + "as a hot-air balloon pilot climbing through a flock of rainbow-colored balloons at dawn, "
        "wearing a leather flight cap and goggles, gripping the burner rope, "
        "her striped balloon envelope rising through dozens of others, "
        "Bagan temples in mist below, sky turning coral pink, "
        "photorealistic, vivid rainbow-coral-pink palette, sharp adventure"
    ),
    "373_rune_carver": (
        ALONDA + "as a Norse rune carver on a windswept Swedish island, "
        "wearing a layered wool tunic in rust and lichen-green with a heavy bronze brooch, "
        "carving a bind rune into a standing granite stone with mallet and chisel, "
        "windswept heather and grey sea behind, ravens on the stone, "
        "photorealistic, vivid rust-green-grey palette, sharp historical"
    ),
    "374_sashiko_artisan": (
        ALONDA + "as a Japanese sashiko embroidery artisan in a snowy northern townhouse, "
        "wearing a soft indigo cotton noragi over a pale grey inner layer, "
        "stitching a deep indigo and white geometric hitomezashi pattern on cotton, "
        "wooden frame hoop, charcoal irori hearth glowing, snow falling outside paper screen, "
        "photorealistic, vivid indigo-white-warm-amber palette, sharp craft"
    ),
    "375_dune_skydiver": (
        ALONDA + "as a skydiver in freefall over Namibia's Sossusvlei red dunes, "
        "wearing a sleek black and tangerine wingsuit, helmet visor mirroring dunes below, "
        "arms in delta position, parachute just deployed trailing orange and white, "
        "shadow of her parachute on the crimson sand far below, "
        "photorealistic, vivid tangerine-crimson-black palette, sharp extreme"
    ),
    "376_icecream_maker": (
        ALONDA + "as a Sicilian artisan gelato maker in her shop in Taormina, "
        "wearing a floral apron over a crisp white linen shirt, hair tucked under a bandana, "
        "scooping pistachio and raspberry swirl gelato into a crisp waffle cone, "
        "marble counter, copper pots, lemons and strawberries piled in baskets, "
        "Mediterranean blue sea visible through arched window, "
        "photorealistic, vivid pistachio-raspberry-white-blue palette, sharp"
    ),
    "377_winter_figure_skater": (
        ALONDA + "as a championship figure skater mid-axel on a frozen alpine lake at sunset, "
        "wearing a deep teal velvet skating dress with frost-white feathered hem, "
        "arms tucked, blade catching the last copper light, "
        "snow-dusted peaks behind, breath frost in cold air, "
        "photorealistic, vivid teal-copper-snow-white palette, sharp sport"
    ),
    "378_bioluminescent_kayak": (
        ALONDA + "kayaking alone at midnight in a glass kayak through bioluminescent water in Puerto Rico, "
        "wearing a sleeveless rashguard in coral, paddle dripping glowing plankton, "
        "each stroke leaving a swirl of electric-blue light, "
        "mangrove roots overhead, stars above, "
        "photorealistic, vivid electric-blue-coral-night palette, sharp nature"
    ),
    "379_japanese_neon_alley": (
        ALONDA + "walking alone through a Shinjuku alley at 2am in a midnight blue kimono with a single white crane motif, "
        "geta sandals clicking on wet asphalt, "
        "vertical neon signs in kanji glowing in pink, cyan and yellow, "
        "steam rising from a nearby ramen cart, photorealistic, vivid neon-midnight-blue palette, sharp cinematic"
    ),
    "380_aurora_hunter_dog": (
        ALONDA + "as a husky sled musher on the Yukon tundra under a sweeping aurora, "
        "wearing a heavy wolf-parka with frost on the fur ruff, face half-lit by green light, "
        "two huskies straining at the harness, breath plumes, "
        "photorealistic, vivid aurora-green-violet-snow palette, sharp arctic"
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
    print(f"[start] batch 361-380: {total} portraits", flush=True)
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
