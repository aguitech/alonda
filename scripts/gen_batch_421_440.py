#!/usr/bin/env python3
"""Generate Alonda portraits batch 421-440 - fresh unique prompts.
Categories: mythology (Medusa, Athena, Apollo, Artemis), extreme sports,
performance arts, subcultures, retro sci-fi, more music, fantasy creatures.
"""
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

# Batch 421-440 - 20 fresh themes
PROMPTS = {
    "421_medusa_greek_myth": (
        ALONDA + "as Medusa from Greek mythology in a temple of olive groves at twilight, "
        "wearing a saffron chiton belted with a serpent-skin sash, "
        "living emerald serpents coiling through her platinum hair instead of strands, "
        "bronze mirror shield propped on an altar nearby, marble columns with creeping vines, "
        "petrified stone garden in background, "
        "photorealistic, vivid saffron-emerald-bronze-marble-amber palette, sharp mythic"
    ),
    "422_athena_warrior_scholar": (
        ALONDA + "as Athena, Greek goddess of wisdom and strategic warfare, "
        "standing in a Parthenon study hall, "
        "wearing a flowing ivory peplos with a deep indigo himation and a polished bronze aegis, "
        "olive-branch crown in hair, an owl perched on her forearm, "
        "papyrus scrolls and a bronze compass on the lectern, "
        "photorealistic, vivid ivory-indigo-bronze-olive-amber palette, sharp classical"
    ),
    "423_apollo_lyre_sunrise": (
        ALONDA + "as Apollo, Greek god of music and the sun, "
        "on a marble terrace at Helios' first dawn, "
        "wearing a flowing tunic of saffron and gold, a laurel crown, "
        "playing a golden tortoise-shell lyre, "
        "chariot of the sun rising behind casting rose and gold beams, "
        "photorealistic, vivid saffron-gold-laurel-rose-pearl palette, sharp mythic"
    ),
    "424_artemis_huntress_forest": (
        ALONDA + "as Artemis, Greek goddess of the hunt, "
        "in a moonlit Taurus Mountain pine forest, "
        "wearing a short chestnut leather tunic and silvered greaves, "
        "silver recurve bow drawn, quiver of moonsteel arrows, a silver wolf companion beside, "
        "lunar halo casting pale blue-silver light, "
        "photorealistic, vivid chestnut-silver-moon-blue-pine palette, sharp mythic"
    ),
    "425_afrodite_cyprus_shore": (
        ALONDA + "as Aphrodite rising from a Cyprus seashore at golden hour, "
        "wearing a flowing rose-pearl chiton soaked with sea foam, "
        "crown of myrtle and tiny white shells in her hair, "
        "doves circling overhead, an oyster shell and pink coral at her feet, "
        "turquoise surf and pink-tinged clouds behind, "
        "photorealistic, vivid rose-pearl-turquoise-myrtle-pink palette, sharp mythic"
    ),
    "426_freya_norse_chariot": (
        ALONDA + "as Freyja, Norse goddess of love and war, "
        "driving a cat-drawn chariot across a fjord in autumn, "
        "wearing a bronze corselet over a deep magenta gown, "
        "amber-beaded cloak, golden torque, "
        "two large forest cats pulling her through amber foliage, "
        "Ragnarok storm clouds brewing amber and rose behind, "
        "photorealistic, vivid bronze-magenta-amber-rose-fjord palette, sharp Norse"
    ),
    "427_thor_stormcaller": (
        ALONDA + "as Thor's shieldmaiden sister in Norse saga, "
        "wielding twin short axes on a basalt cliff above a stormy North Sea, "
        "wearing a charcoal wolfskin cloak over riveted iron scale, "
        "hammer pendant around her neck, lightning forks in cobalt sky, "
        "longship with red-and-white striped sail in cove below, "
        "photorealistic, vivid charcoal-iron-cobalt-white-red palette, sharp Norse"
    ),
    "428_anubis_egypt_underworld": (
        ALONDA + "as an ancient Egyptian priestess of Anubis at the weighing-of-the-hearts ceremony, "
        "in a candlelit temple at Karnak, "
        "wearing a lapis sheath dress, gold ankh collar, and a jackal-mask pushed back on her head, "
        "holding a golden scale, "
        "papyrus scroll of the Book of the Dead on a side altar, "
        "photorealistic, vivid lapis-gold-candlelight-papyrus-cream palette, sharp Egypt"
    ),
    "429_isis_mother_magic": (
        ALONDA + "as Isis, ancient Egyptian goddess of magic and motherhood, "
        "in a Nile-side temple garden at twilight, "
        "wearing a pleated white linen gown with gold hieroglyphic sash, "
        "throne-shaped headdress with sun disk and cow horns, "
        "ankh in one hand, lotus in the other, "
        "papyrus reeds and golden ibises in background, "
        "photorealistic, vivid white-gold-sun-twilight-papyrus palette, sharp Egypt"
    ),
    "430_persephone_pomegranate_garden": (
        ALONDA + "as Persephone in the underworld pomegranate garden, "
        "wearing a flowing gown split pomegranate-red above and amber below, "
        "crown of asphodel and narcissus in hair, "
        "holding a split pomegranate dripping ruby seeds, "
        "dark cypresses and glowing amber torchlight, marble throne to one side, "
        "photorealistic, vivid pomegranate-amber-ruby-cypress-gold palette, sharp mythic"
    ),
    "431_free_climber_yosemite": (
        ALONDA + "as a free-climber halfway up El Capitan's Dawn Wall in Yosemite, "
        "wearing a coral chalk-tank and graphite climbing shorts, "
        "fingers crimping a granite razor-edge, "
        "sunrise alpenglow painting the wall rose and gold, "
        "valley of blue mist and pine far below, "
        "photorealistic, vivid coral-graphite-rose-gold-blue-mist palette, sharp extreme-sport"
    ),
    "432_skateboarder_bowl_dusk": (
        ALONDA + "as a skateboarder mid-grind on a tiled pool bowl at Venice Beach at dusk, "
        "wearing a magenta cropped hoodie, high-waist acid-wash denim shorts, "
        "neon-yellow wheel skateboard underfoot, "
        "graffiti wall of cobalt, tangerine and mint behind, "
        "boardwalk lights glowing amber, "
        "photorealistic, vivid magenta-acid-neon-yellow-cobalt-tangerine palette, sharp sport"
    ),
    "433_parkour_traceuse_rooftop": (
        ALONDA + "as a parkour traceuse mid-vault between rooftops in Lisbon at sunset, "
        "wearing a charcoal compression top and cobalt leggings, "
        "mid-air over a tiled terra-cotta parapet, "
        "Tagus river glowing rose behind, "
        "yellow trams on the cobbled street below, "
        "photorealistic, vivid charcoal-cobalt-terra-rose-yellow palette, sharp action"
    ),
    "434_bmx_ramp_neon": (
        ALONDA + "as a BMX rider inverted on a halfpipe under neon arena lights, "
        "wearing a magenta helmet and chrome-silver leathers, "
        "bike spinning turquoise-rimmed wheels above her, "
        "audience of silhouettes lit by magenta-cyan-green stage lights, "
        "concrete bowl walls glowing cobalt, "
        "photorealistic, vivid magenta-cyan-green-cobalt-chrome palette, sharp extreme"
    ),
    "435_opera_soprano_curtain": (
        ALONDA + "as a soprano moments before stepping onto a La Scala stage, "
        "wearing a vermillion silk ball gown with gold-embroidered bodice, "
        "pearl-and-ruby tiara in hair, "
        "heavy crimson velvet curtain half-drawn behind, "
        "orchestra pit lights gleaming gold on brass instruments, "
        "photorealistic, vivid vermillion-gold-pearl-ruby-crimson palette, sharp opera"
    ),
    "436_jazz_pianist_1940s": (
        ALONDA + "as a 1940s jazz pianist in a Harlem basement club, "
        "wearing a forest-green satin jumpsuit with gold cuffs, "
        "hair in victory rolls, "
        "hands mid-riff on a baby-grand piano, glass of rye whiskey on the lid, "
        "cigarette smoke curling under amber pin-spot, "
        "photorealistic, vivid forest-green-gold-amber-smoke-rye palette, sharp retro"
    ),
    "437_mime_artist_paris": (
        ALONDA + "as a mime artist frozen mid-expression against a Paris wall, "
        "wearing classic black-and-white striped long-sleeve shirt, black trousers, white gloves, "
        "painted white face with a single black tear, "
        "old stone wall of weathered cream and moss-green behind, "
        "scattered red roses at her feet, "
        "photorealistic, vivid black-white-cream-moss-red palette, sharp performance"
    ),
    "438_contortionist_burlesque": (
        ALONDA + "as a contortionist mid-fold in a vintage burlesque tent, "
        "wearing a corseted fuchsia-and-gold bodysuit, "
        "body bent backward over a brass rail, "
        "crystal chandelier above casting prismatic splinters, "
        "burgundy velvet drapery background, "
        "photorealistic, vivid fuchsia-gold-crystal-burgundy-prism palette, sharp performance"
    ),
    "439_equestrienne_showjumping": (
        ALONDA + "as an equestrienne clearing a 1.60m oxer on a dappled gray Andalusian mare, "
        "wearing a graphite hunt coat, white stock tie, canary show shirt, black velvet helmet, "
        "horse mid-leap with forelegs tucked, "
        "sunlit arena sand, navy rails, jumping standards in white and red, "
        "audience in soft pastel blur behind, "
        "photorealistic, vivid graphite-canary-white-navy-red-gray palette, sharp sport"
    ),
    "440_falconer_winter_field": (
        ALONDA + "as a falconer in a snow-dusted Hungarian puszta in winter, "
        "wearing a dark chestnut sheepskin coat and olive wool scarf, "
        "leather glove raised with a saker falcon about to launch, "
        "bare birches and a low ochre farmhouse in distance, "
        "pale gray sky with a single circling buzzard, "
        "photorealistic, vivid chestnut-olive-snow-gray-ochre palette, sharp sport"
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
    print(f"[start] batch 421-440: {total} portraits", flush=True)
    ok, fail = 0, 0
    results = {}
    for fname, prompt in PROMPTS.items():
        target = OUT / f"{fname}.jpg"
        if target.exists():
            print(f"[skip] {fname}.jpg exists", flush=True)
            ok += 1
            results[fname] = "skipped"
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
            results[fname] = "fail"
            continue
        try:
            Image.open(BytesIO(img)).convert("RGB").save(target, "JPEG", quality=90)
            print(f"[ok]   {fname}.jpg ({len(img)}B)", flush=True)
            ok += 1
            results[fname] = "ok"
        except Exception as e:
            print(f"[save err] {fname}: {e}", flush=True)
            fail += 1
            results[fname] = f"save_err: {e}"
        time.sleep(1.2)
    print(f"[done] ok={ok} fail={fail}", flush=True)
    Path("/root/alonda/scripts/batch_421_440_results.json").write_text(json.dumps(results, indent=2))
    return 0 if fail == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
