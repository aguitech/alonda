#!/usr/bin/env python3
"""Generate Alonda portraits batch 321-340 — fresh unique prompts (no repeats of 1-320)."""
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
TOKEN=auth["providers"]["minimax-oauth"]["access_token"]
if not TOKEN:
    TOKEN = auth["credential_pool"]["minimax-oauth"][0]["access_token"]
print(f"[token] len={len(TOKEN)}", flush=True)

# ANCHOR ALONDA — 7 atributos OBLIGATORIOS
ALONDA = (
    "Alonda, a beautiful 26-year-old woman, platinum blonde long hair, "
    "striking emerald green eyes, slim athletic figure, "
    "delicate feminine facial features, natural realistic skin texture, "
)

# Batch 321-340 — UNIQUE prompts (no overlap with prior batches 1-320)
# Mix: mythology, sci-fi retro, dance, foods, extreme sports, professions, music,
# historical, vehicles, weather, festivals, fantasy.
PROMPTS = {
    "321_anubis_egypt": (
        ALONDA + "as an Egyptian priestess of Anubis at the banks of the Nile, "
        "wearing a sleek black sheath dress with gold Anubis-jackal headdress and broad gold collar necklace, "
        "jackal guardian statue beside her, sunset over the pyramids in the distance, "
        "papyrus reeds and golden warm light, photorealistic, vivid saturated colors, sharp"
    ),
    "322_isis_goddess": (
        ALONDA + "as Isis the Egyptian goddess of magic and motherhood, "
        "wearing an emerald green and gold pleated linen gown with throne-shaped crown on her head, "
        "wings of iridescent feathers spread behind her, holding an ankh symbol, "
        "inside an ornate Egyptian temple with hieroglyph-covered pillars, "
        "photorealistic, vivid emerald and gold palette, sharp cinematic"
    ),
    "323_apollon_oracle": (
        ALONDA + "as the Oracle of Apollo at Delphi, "
        "wearing a flowing white and saffron Grecian chiton with golden laurel wreath, "
        "standing at the mouth of the temple cleft with olive trees and Mount Parnassus behind, "
        "ethereal morning mist, golden sun rays piercing clouds, "
        "photorealistic, vivid warm tones, sharp mystical"
    ),
    "324_artemis_huntress": (
        ALONDA + "as Artemis the Greek goddess of the hunt, "
        "wearing a short bronze-leaf tunic with silver crescent moon diadem, "
        "holding a recurve bow with a silver arrow nocked, a stag beside her, "
        "in a moonlit forest clearing with silver light filtering through ancient oaks, "
        "photorealistic, vivid silver-blue moonlight palette, sharp"
    ),
    "325_dieselpunk_pilot": (
        ALONDA + "as a dieselpunk 1940s female fighter pilot ace, "
        "wearing a worn brown leather bomber jacket with fleece collar and a silk aviator scarf, "
        "goggles pushed up on her forehead, standing in front of a polished silver P-51 Mustang plane, "
        "hangar with riveted steel walls, dramatic noir lighting, "
        "photorealistic, vivid sepia-bronze tones, sharp retro-futuristic"
    ),
    "326_atompunk_scientist": (
        ALONDA + "as a 1950s atompunk atomic-age scientist in her retro-futuristic lab, "
        "wearing a fitted white lab coat over a teal polka-dot swing dress, cat-eye glasses, "
        "standing beside a bubbling glass retort with bright green glowing plasma, "
        "chrome and pastel appliances around, atomic starburst wallpaper, "
        "photorealistic, vivid pastel-teal palette, sharp retrofuturist"
    ),
    "327_solarpunk_architect": (
        ALONDA + "as a solarpunk eco-architect in her sustainable vertical garden tower, "
        "wearing a linen jumpsuit in soft sage green with copper belt, "
        "surrounded by living walls of lush plants, solar panel canopy overhead, "
        "butterflies and birds, golden sustainable future light, "
        "photorealistic, vivid emerald-sunlit palette, sharp utopian"
    ),
    "328_irish_dancer": (
        ALONDA + "performing an Irish step dance with arms straight at her sides, "
        "wearing an emerald green Celtic-embroidered dress with curly hairpieces, "
        "midair above a wooden stage with Celtic knot designs, "
        "footlights in green and gold, Irish flag behind, "
        "photorealistic, vivid emerald-green palette, sharp motion-captured"
    ),
    "329_tango_buenos_aires": (
        ALONDA + "dancing passionate Argentine tango in a Buenos Aires milonga, "
        "wearing a deep red slit tango dress with thigh-high stockings and red heels, "
        "in a dramatic dip pose with a dark-suited partner, "
        "warm amber stage lighting, polished wood floor, dramatic shadows, "
        "photorealistic, vivid red-amber palette, sharp cinematic"
    ),
    "330_salsa_cuba": (
        ALONDA + "dancing vibrant Cuban salsa in a Havana street, "
        "wearing a flowing tropical yellow and orange ruffled salsa dress, "
        "mid-twirl with skirt flaring, colorful colonial buildings behind, "
        "vintage cars in pastel pink and mint, golden Caribbean sun, "
        "photorealistic, vivid tropical palette, sharp joyful motion"
    ),
    "331_kpop_idol": (
        ALONDA + "as a K-pop idol on a neon-lit Seoul music show stage, "
        "wearing a holographic iridescent crop top and pleated mini skirt with chunky platform boots, "
        "performing a dance pose with one hand reaching toward camera, "
        "explosion of pink and cyan LED lights and confetti behind, "
        "photorealistic, vivid neon-pink-cyan palette, sharp stage glamour"
    ),
    "332_guitarista_flamenca": (
        ALONDA + "as a passionate flamenco guitarist in a Seville tablao, "
        "wearing a black off-shoulder flamenco dress with red rose in her hair, "
        "playing a Spanish classical guitar with intense focus, "
        "warm terracotta tile floor, candles and a Spanish shawl draped over a chair, "
        "photorealistic, vivid black-red-amber palette, sharp"
    ),
    "333_whisky_distiller": (
        ALONDA + "as a Scottish master whisky distiller in the Scottish Highlands, "
        "wearing a heavy dark green wool sweater and leather apron, "
        "holding a glass of amber single-malt whisky up to the light, "
        "copper pot stills and oak barrels behind her, peat smoke in the air, "
        "photorealistic, vivid amber-copper palette, sharp atmospheric"
    ),
    "334_chocolatier_paris": (
        ALONDA + "as an artisan chocolatier in her Paris boutique kitchen, "
        "wearing a white double-breasted chef coat and a red silk neckerchief, "
        "hand-tempering a tray of glossy dark chocolate truffles, "
        "copper pots, marble counters, walls of cocoa pods, "
        "photorealistic, vivid warm brown-red palette, sharp"
    ),
    "335_pizza_maker_naples": (
        ALONDA + "as a Neapolitan pizza master tossing dough in a wood-fired pizzeria in Naples, "
        "wearing a white apron over a tomato-red shirt and a flour-dusted cheek, "
        "stretching pizza dough high above her head with one hand, "
        "blazing wood-fired oven with orange flames behind, basil and San Marzano tomatoes on the counter, "
        "photorealistic, vivid warm orange-red palette, sharp action"
    ),
    "336_ice_cream_maker": (
        ALONDA + "as an artisan gelato maker in a sunny Italian piazza, "
        "wearing a crisp white apron and a pistachio-green striped shirt, "
        "scooping bright pastel gelato (pistachio, strawberry, lemon, stracciatella) into a crystal dish, "
        "gelato display case with vibrant pastel mounds, flower boxes, "
        "photorealistic, vivid pastel rainbow palette, sharp"
    ),
    "337_cheese_monger": (
        ALONDA + "as a French affineur cheese monger in a fromagerie in Lyon, "
        "wearing a navy striped Breton shirt and a cream linen apron, "
        "holding a half-wheel of aged Comté cheese, displaying its crystalline texture, "
        "aged cave walls, wheels of Gruyère, Roquefort, and Brie behind her, "
        "photorealistic, vivid warm cream-amber palette, sharp"
    ),
    "338_barista_latte_art": (
        ALONDA + "as a third-wave specialty coffee barista pouring latte art in a Tokyo cafe, "
        "wearing a sage-green apron over a black t-shirt, hair tied back, "
        "pouring steamed milk into a ceramic cup creating a rosetta pattern, "
        "minimalist wood and concrete cafe interior, copper espresso machine behind, "
        "photorealistic, vivid sage-warm palette, sharp"
    ),
    "339_tea_sommelier": (
        ALONDA + "as an Asian tea sommelier performing gongfu cha ceremony in a Kyoto tea house, "
        "wearing a refined sage green silk kimono with subtle bamboo embroidery, "
        "gracefully pouring jade-green matcha from a bamboo whisk into a rustic clay bowl, "
        "tatami floor, ikebana flower arrangement, soft shoji-filtered daylight, "
        "photorealistic, vivid muted sage-green palette, sharp"
    ),
    "340_night_tea_ceremony": (
        ALONDA + "as a sommelier of whisky and Japanese tea at a night tasting, "
        "wearing a deep charcoal velvet tuxedo blazer with a silk cravat, "
        "holding a crystal whisky nosing glass up to candlelight, examining color, "
        "dark mahogany tasting room, candles and old books, "
        "photorealistic, vivid deep amber-charcoal palette, sharp"
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
    print(f"[start] batch 321-340: {total} portraits", flush=True)
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
