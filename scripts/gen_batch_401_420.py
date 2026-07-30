#!/usr/bin/env python3
"""Generate Alonda portraits batch 401-420 - fresh unique prompts."""
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

# Batch 401-420 - Fresh unexplored themes: cartography, botany, extreme weather,
# mythology, instrument-making, festival, retro-tech, deep sea, observatory,
# rare crafts, and more.
PROMPTS = {
    "401_cartographer_atelier": (
        ALONDA + "as a master cartographer in a Dutch map atelier of the 1640s, "
        "wearing a deep teal velvet gown with pearl buttons, hair in a low chignon, "
        "inking a detailed map of an imagined coastline with a crow-quill pen, "
        "rolling compasses, brass sextant, jars of cochineal and indigo pigments, "
        "parchment scrolls and a globe on a claw-foot desk, "
        "photorealistic, vivid teal-pearl-cochineal-indigo-gold palette, sharp painterly"
    ),
    "402_meadow_orchid_botanist": (
        ALONDA + "kneeling in a Pyrenees alpine meadow as a field botanist, "
        "wearing a sage canvas field vest and rolled-up linen shirt, "
        "examining a rare lady's slipper orchid with a hand lens, "
        "wildflower tapestry of indigo gentian, magenta clover, yellow arnica, "
        "jagged limestone peaks behind, golden morning light, "
        "photorealistic, vivid sage-indigo-magenta-yellow-amber palette, sharp naturalist"
    ),
    "403_underwater_cathedral_diver": (
        ALONDA + "freediving inside a submerged limestone cathedral cave in Mexico's cenotes, "
        "wearing a minimal teal bikini and a single long fin, hair fanning in the water, "
        "shafts of white sunlight piercing turquoise water from above, "
        "exposed tree roots and stalactites draped in cave pearls, "
        "ancient Maya offerings resting on a stone altar below, "
        "photorealistic, vivid teal-turquoise-white-amber palette, sharp sacred"
    ),
    "404_lightning_sculptor": (
        ALONDA + "as a Tesla-inspired artist sculpting arcs of plasma in a darkened lab, "
        "wearing a graphite Faraday-suit with copper-thread embroidery, "
        "operating a massive coil behind her throwing blue-white forks of electricity, "
        "aluminum plates and glass sculptures charging nearby, "
        "long-exposure arcing tendrils, deep navy void background, "
        "photorealistic, vivid navy-electric-blue-copper-graphite-white palette, sharp sci-art"
    ),
    "405_lunar_base_commander": (
        ALONDA + "as a lunar-base commander inside a glass-walled habitat at Shackleton crater, "
        "wearing a charcoal flight suit with mission patches and a transparent helmet under her arm, "
        "Earth a thin blue crescent above the gray regolith horizon, "
        "hydroponic green lettuce and red tomatoes in trays, "
        "pressurized rover parked in adjacent bay, photorealistic, vivid charcoal-blue-gray-green-red palette, sharp sci-fi"
    ),
    "406_volcano_lava_surfer": (
        ALONDA + "as an extreme lava-surfer riding a heat-shield board over an active pahoehoe flow in Hawaii, "
        "wearing an aluminum-reflective silver suit with an obsidian visor, "
        "standing crouched, board skimming molten orange rivers, "
        "black basalt field with steam plumes, glowing red horizon, "
        "photorealistic, vivid silver-molten-orange-red-black-steam palette, sharp action"
    ),
    "407_persian_carpet_weaver": (
        ALONDA + "as a Persian carpet weaver in a Kashan workshop at midday, "
        "wearing a saffron headscarf and a navy chapan with paisley motifs, "
        "tying silk knots on a vertical loom, "
        "half-finished crimson and indigo medallion rug, "
        "sun streaming through lattice windows casting geometric shadows, "
        "photorealistic, vivid saffron-navy-crimson-indigo-lattice-shadow palette, sharp craft"
    ),
    "408_bioluminescent_forest_walk": (
        ALONDA + "walking barefoot through a New Zealand Waitomo forest at night, "
        "wearing an ivory linen slip dress, hair loose and slightly damp, "
        "thousands of blue-green glowworm strands lighting the limestone ceiling above, "
        "mossy trunks, dark velvet-black pool reflections, "
        "photorealistic, vivid ivory-blue-green-moss-black palette, sharp magical"
    ),
    "409_dune_silence_sahara": (
        ALONDA + "as a Tuareg caravanner pausing at the lip of the Erg Chebbi dunes at dawn, "
        "wearing an indigo tagelmust turban and a deep saffron robe, "
        "blue-veiled face half turned to camera, "
        "single dromedary beside her, "
        "rose-pink dunes fading to apricot and gold under the rising sun, "
        "photorealistic, vivid indigo-saffron-rose-apricot-gold palette, sharp cultural"
    ),
    "410_instrument_maker_cremona": (
        ALONDA + "as a violin maker in a Cremona workshop gilding the purfling of a maple instrument, "
        "wearing a burgundy leather apron over a cream henley, hair tied back, "
        "curved chisels, hide glue pot, and hand-split spruce laid on bench, "
        "varnish bottles of amber and deep red, "
        "sawdust on the floor, warm afternoon window light, "
        "photorealistic, vivid burgundy-cream-amber-deep-red-sawdust palette, sharp artisan"
    ),
    "411_polar_dog_sled_race": (
        ALONDA + "as a sled-dog racer mushing a team of huskies across the Yukon at the Iditarod, "
        "wearing a canary-yellow parka with fur ruff and reflective goggles pushed up, "
        "breath clouding in the cobalt air, "
        "pups in pink booties galloping through powder, "
        "northern lights shimmering green overhead, "
        "photorealistic, vivid canary-cobalt-pink-green-snow palette, sharp adventure"
    ),
    "412_celestial_observatory_1880": (
        ALONDA + "as an Edwardian astronomer at the Royal Observatory Greenwich, "
        "wearing a high-collared midnight blue wool gown with brass buttons, "
        "peering through a great equatorial refractor, "
        "ivory astronomical charts and brass orrery on a side table, "
        "rotating dome open to a star-flooded night sky, "
        "photorealistic, vivid midnight-blue-brass-ivory-star-white palette, sharp vintage sci"
    ),
    "413_glassblower_murano": (
        ALONDA + "as a Murano glassblower gathering molten glass on a blowpipe in the furnace room, "
        "wearing a soot-streaked linen tunic and leather forearm guard, "
        "a glowing orange gather elongating as she rotates, "
        "shelves of finished cobalt goblets, emerald vases, ruby tazze, "
        "embers floating in the dark workshop, photorealistic, vivid cobalt-emerald-ruby-orange-ember palette, sharp"
    ),
    "414_bellydancer_cairo_modern": (
        ALONDA + "as a modern Cairo cabaret dancer mid-spin in a renovated Ottoman theater, "
        "wearing a fuchsia bedlah set with crystal fringe and a coin hip belt, "
        "veil cascading in motion, kohl-lined emerald eyes glowing, "
        "geometric mashrabiya screens, hanging brass lanterns, amber spotlight, "
        "photorealistic, vivid fuchsia-crystal-amber-brass-kohl palette, sharp performance"
    ),
    "415_orchid_vivarium_curator": (
        ALONDA + "as a curator misting a rare Phragmipedium orchid inside a Victorian glass vivarium, "
        "wearing a moss-green velvet waistcoat and lace cuffs, "
        "tweezers steadying the bloom, brass mister held aloft, "
        "ferns and jewel-toned amphibians in the background case, "
        "damp greenhouse light filtering through rippled glass, "
        "photorealistic, vivid moss-emerald-ferns-amber-glass palette, sharp"
    ),
    "416_storm_ship_helmsman": (
        ALONDA + "as a tall-ship helmsman wrestling the wheel of a three-masted schooner in a Force-10 gale, "
        "wearing a yellow oilskin jacket and a sou'wester hat, "
        "massive teal waves crashing over the bow, "
        "canvas sails reefed tight, gulls wheeling through spray, "
        "steely horizon lit by a single shaft of sun, "
        "photorealistic, vivid yellow-teal-white-steel palette, sharp maritime"
    ),
    "417_japanese_calligrapher": (
        ALONDA + "as a Japanese shodō master executing a bold kanji with a fude brush, "
        "wearing a charcoal kimono with a deep vermillion obi, "
        "kneeling on a tatami at a low desk, sumi ink grinding on a slate, "
        "white hanshi paper unfurling, red seal stamp to one side, "
        "soft window light on bamboo grove outside, "
        "photorealistic, vivid charcoal-vermillion-black-white-bamboo-green palette, sharp zen"
    ),
    "418_midnight_bookbinder": (
        ALONDA + "as a London bookbinder stitching a volume in gold-tooled leather at midnight, "
        "wearing a tweed waistcoat and brass loupes perched on her forehead, "
        "bone folder creasing endpapers, linen thread pulled taut, "
        "towering shelves of leather-bound spines receding into shadow, "
        "single banker lamp casting amber pool, "
        "photorealistic, vivid tweed-amber-gold-bone-leather palette, sharp artisan"
    ),
    "419_sahara_rain_dancer": (
        ALONDA + "as a Wodaabe beauty contestant at the Gerewol festival dancing in the Sahel dust, "
        "wearing amber-beaded braids, white face-paint stripes, indigo robe with cowrie trim, "
        "arms raised overhead in the yaake dance, "
        "ring of male suitors clapping in concentric circles, "
        "late golden sun, photorealistic, vivid amber-ink-white-indigo-cowrie-cream palette, sharp cultural"
    ),
    "420_glass_diver_aquarium": (
        ALONDA + "as the lead diver inside the cylindrical shark-tank of an Osaka aquarium, "
        "wearing a black neoprene wetsuit with pink trim, hair inside a black neoprene hood, "
        "feeding a sand tiger shark by hand, "
        "cobalt water, sunbeams slicing from the surface, "
        "school of trevally swirling, photorealistic, vivid cobalt-pink-black-trevally-silver palette, sharp"
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
    print(f"[start] batch 401-420: {total} portraits", flush=True)
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
