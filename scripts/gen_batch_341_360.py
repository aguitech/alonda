#!/usr/bin/env python3
"""Generate Alonda portraits batch 341-360 — fresh unique prompts (no repeats of 1-340)."""
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

# ANCHOR ALONDA — 7 atributos OBLIGATORIOS
ALONDA = (
    "Alonda, a beautiful 26-year-old woman, platinum blonde long hair, "
    "striking emerald green eyes, slim athletic figure, "
    "delicate feminine facial features, natural realistic skin texture, "
)

# Batch 341-360 — UNIQUE prompts (no overlap with prior 1-340)
# Mix: dance, festivals, vehicles, science, mythology, fantasy, professions,
# animals, weather, historical.
PROMPTS = {
    "341_morris_dancer": (
        ALONDA + "as an English Morris dancer with bell-pads on shins and white skirt with red cross, "
        "waving a white handkerchief in each hand mid-leap on a village green, "
        "May morning, maypole with colored ribbons in background, vivid greens and reds, "
        "photorealistic, vivid saturated colors, sharp folk-festival"
    ),
    "342_bellydance_egypt": (
        ALONDA + "as an Egyptian raqs sharqi belly dancer in Cairo at sunset, "
        "wearing a bedlah set in deep magenta with gold coins and a beaded hip scarf, "
        "veil trailing behind her on a Nile rooftop with minarets and pyramids in the distance, "
        "warm golden hour light, photorealistic, vivid magenta-gold palette, sharp"
    ),
    "343_robot_mechanic": (
        ALONDA + "as a future robot mechanic in a giant robotics workshop, "
        "wearing a heavy canvas work jumpsuit in cobalt blue with welding goggles pushed up, "
        "holding a glowing plasma spanner while servicing a towering humanoid android chassis, "
        "neon-lit repair bay, sparks flying, photorealistic, vivid cobalt-orange palette, sharp sci-fi industrial"
    ),
    "344_queen_merlin_court": (
        ALONDA + "as Queen Guinevere at a round table in Camelot, "
        "wearing an ivory silk gown with gold thread and a delicate gold circlet with a single ruby, "
        "long embroidered tapestry walls, candles and rose petals, "
        "photorealistic, vivid ivory-gold-scarlet palette, sharp medieval fantasy"
    ),
    "345_northern_aurora": (
        ALONDA + "as an Inuit aurora hunter on the Arctic tundra at night, "
        "wearing a caribou-fur parka with embroidered trim and sealskin mukluks, "
        "dancing ribbons of green and violet aurora filling the sky, fresh snow underfoot, "
        "photorealistic, vivid green-violet-night palette, sharp cinematic"
    ),
    "346_tahitian_dancer": (
        ALONDA + "as a Tahitian 'ote'a dancer on a black sand beach in Bora Bora, "
        "wearing a coconut-bra top and a hei (grass skirt) of pandanus with a flower crown of tiare, "
        "bare midriff oiled, hips mid-shimmy, palms lifted gracefully, "
        "turquoise lagoon and overwater bungalows behind, photorealistic, vivid tropical palette, sharp"
    ),
    "347_egypt_dune": (
        ALONDA + "as a Bedouin desert guide riding a camel across the Sahara at golden hour, "
        "wearing an indigo-dyed malafa face veil flowing in the wind revealing emerald eyes, "
        "rolling orange dunes stretching to the horizon, "
        "photorealistic, vivid orange-indigo-gold palette, sharp cinematic"
    ),
    "348_hummingbird_rainforest": (
        ALONDA + "as a Costa Rican cloud-forest ornithologist tracking hummingbirds, "
        "wearing a mossy green field vest with binoculars and a wide-brim hat, "
        "hand outstretched with a tiny violet-ear hummingbird hovering at her finger, "
        "lush bromeliads and emerald moss everywhere, misty mountain light, "
        "photorealistic, vivid emerald-violet palette, sharp wildlife"
    ),
    "349_japanese_maiko_tea": (
        ALONDA + "as a young Japanese maiko apprentice geisha in Kyoto during a tea ceremony, "
        "wearing an elaborate furisode kimono in coral with golden phoenix embroidery, "
        "kanzashi hair ornaments with dangling silver bells, holding a chawan bowl gracefully, "
        "tatami room with a tokonoma alcove displaying a hanging scroll and ikebana, "
        "photorealistic, vivid coral-gold-sage palette, sharp"
    ),
    "350_festival_lantern": (
        ALONDA + "releasing a sky lantern at the Yi Peng lantern festival in Chiang Mai, "
        "wearing a traditional Lanna Thai silk dress in sapphire blue with silver thread, "
        "thousands of golden lanterns floating into the night sky, golden temple silhouettes, "
        "photorealistic, vivid sapphire-gold-night palette, sharp magical"
    ),
    "351_zookeeper_orangutan": (
        ALONDA + "as a senior orangutan keeper at a Borneo sanctuary, "
        "wearing a khaki field uniform with a Borneo Orangutan Survival Foundation patch, "
        "feeding a baby orangutan a banana, mother orangutan watching protectively, "
        "lush tropical jungle with strangler figs and morning mist, "
        "photorealistic, vivid khaki-green-warm palette, sharp wildlife conservation"
    ),
    "352_bioluminescent_cave": (
        ALONDA + "as a marine biologist exploring a bioluminescent cave in New Zealand, "
        "wearing a black neoprene wetsuit, swimming through water glowing with electric blue bio-luminescence, "
        "limestone walls dripping, glowing plankton swirling around her outstretched hand, "
        "photorealistic, vivid electric-blue-dark palette, sharp underwater fantasy"
    ),
    "353_glassblower_murano": (
        ALONDA + "as a master glassblower on the island of Murano in Venice, "
        "wearing a heavy leather apron and asbestos glove, "
        "blowing a glowing orange bubble of molten glass at the end of a blowpipe, "
        "furnace flames licking behind, colorful finished glass sculptures on shelves, "
        "photorealistic, vivid orange-amber-rainbow palette, sharp action"
    ),
    "354_astronaut_spacewalk": (
        ALONDA + "as a NASA astronaut on a spacewalk untethered at the ISS, "
        "wearing a white Extravehicular Mobility Unit spacesuit with American and Mexican flag patches, "
        "Earth glowing blue and white behind her, golden helmet visor reflecting continents, "
        "toolbox floating in zero gravity, photorealistic, vivid cobalt-gold-Earth palette, sharp cinematic"
    ),
    "355_lighthouse_keeper": (
        ALONDA + "as a lighthouse keeper on a remote Pacific Northwest cliff at dusk, "
        "wearing a heavy yellow oilskin slicker and rubber boots, "
        "trimming the wick of the great Fresnel lens, beam sweeping over a stormy sea, "
        "lighthouse interior with brass and aged wood, gulls swirling, "
        "photorealistic, vivid amber-stormy-blue palette, sharp dramatic"
    ),
    "356_polar_scientist": (
        ALONDA + "as a climate scientist drilling an ice core in Antarctica, "
        "wearing a bright red Canada Goose parka and glacier goggles pushed up, "
        "ice core cylinder held up showing thousand-year-old ice layers, "
        "vast blue-white Antarctic plateau behind her with aurora australis overhead, "
        "photorealistic, vivid red-blue-white-aurora palette, sharp scientific"
    ),
    "357_ice_princess": (
        ALONDA + "as an ice queen on a throne of frozen crystal in a glacial palace, "
        "wearing a gown of pale blue frost-lace and a crown of jagged icicles, "
        "frosty breath visible, snowflakes drifting in shafts of pale blue light, "
        "northern lights through arched ice windows, photorealistic, vivid pale-blue-white-silver palette, sharp fantasy"
    ),
    "358_renaissance_artist": (
        ALONDA + "as a Renaissance painter in her Florentine atelier in 1502, "
        "wearing an embroidered crimson velvet gown with puffed sleeves, hair braided with pearls, "
        "mixing lapis lazuli blue pigment with linseed oil on a wooden palette, "
        "frescoes of a half-finished Madonna on the wall, north-facing window light, "
        "photorealistic, vivid crimson-lapis-gold palette, sharp historical"
    ),
    "359_burlesque_singer": (
        ALONDA + "as a 1920s Parisian burlesque cabaret singer on a tiny stage, "
        "wearing a long-sleeved velvet gown in deep burgundy with feather fan, "
        "holding a vintage microphone, ostrich-feather boa cascading off the chair, "
        "red velvet curtains and art deco gilded sconces, photorealistic, vivid burgundy-gold-red palette, sharp"
    ),
    "360_dune_rider": (
        ALONDA + "as a futuristic dune rider on a hoverbike on the red dunes of Mars, "
        "wearing a sleek matte-black pressure suit with a transparent bubble helmet, "
        "racing across rust-orange dunes, twin plumes of dust behind, two pale Martian moons rising, "
        "photorealistic, vivid rust-orange-black-pale-violet palette, sharp retro sci-fi"
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
    print(f"[start] batch 341-360: {total} portraits", flush=True)
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
