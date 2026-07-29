#!/usr/bin/env python3
"""Generate Alonda Tier 8 portraits 101-120, check gray percentage, regenerate if needed."""
import io
import json
import ssl
import time
import urllib.error
import urllib.request
from pathlib import Path

from PIL import Image

AUTH_PATH = Path('/root/.hermes/auth.json')
OUT_DIR = Path('/root/alonda/assets/images')
API_URL = 'https://api.minimax.io/v1/image_generation'


def get_token():
    auth = json.loads(AUTH_PATH.read_text())
    value = auth.get('providers', {}).get('minimax-oauth')
    if isinstance(value, dict):
        value = value.get('access_token')
    if value:
        return value
    pool = auth.get('credential_pool', {}).get('minimax-oauth', [])
    if pool:
        value = pool[0]
        if isinstance(value, dict):
            value = value.get('access_token')
    if not value:
        raise RuntimeError('MiniMax token not found')
    return value


ALONDA = (
    'Alonda, a beautiful 26-year-old woman, platinum blonde hair, striking emerald green eyes, '
    'slim athletic figure, delicate feminine facial features, natural realistic skin texture, '
)


# 20 promts UNIQUE vs portraits 1-80. All distinct categories.
SHOTS = [
    ('101_bmx_rider',
     'BMX rider mid-air doing a tailwhip over a vivid graffiti-covered skatepark, wearing a fluorescent orange helmet and electric teal jersey, chromoly bike spinning in golden-hour light, magenta sunset sky, dynamic action sports portrait'),
    ('102_motocross_dunes',
     'Motocross racer launching off a Saharan dune on a candy-red KTM bike, wearing vermilion-and-cyan gear and mirrored goggles, ochre sand plume behind, cobalt sky, vivid motorsport portrait'),
    ('103_kite_surfer',
     'Kite surfer carving on a turquoise tropical sea, holding a saffron-and-magenta kite, wearing a cobalt wetsuit and tropical-print rashguard, palm-fringed island behind, vivid ocean action portrait'),
    ('104_mma_fighter',
     'MMA fighter in an Octagon cage under cobalt spotlights, wearing saffron-and-crimson fight shorts and MMA gloves, fierce determination, sponsor banners behind, vivid combat sport portrait'),
    ('105_skateboarder_bowl',
     'Skateboarder dropping into a vivid graffiti-tiled pool bowl at sunset, wearing a magenta bucket hat and turquoise cargo pants, neon-orange skateboard mid-grind, magenta sky, vivid urban action portrait'),
    ('106_jeweler_goldsmith',
     'Master jeweler at a sun-drenched goldsmith atelier, wearing a saffron silk blouse, examining a vivid ruby-and-emerald tiara under a brass loupe, shelves of polished gemstones and gold filigree tools, vivid artisan portrait'),
    ('107_calligrapher_ink',
     'Master calligrapher at a low vermilion-lacquered desk, wearing a sage-green kimono, dipping a sumi brush into cobalt inkstone, paper glowing with vivid emerald kanji, plum branch in ceramic vase, vivid Japanese craft portrait'),
    ('108_bookbinder_leather',
     'Artisan bookbinder at a mahogany workbench, wearing a charcoal apron over a saffron shirt, hand-tooling a magenta-and-emerald leather book cover, gold foil blocks and marbled endpapers, vivid craft portrait'),
    ('109_perfumer_lab',
     'Master perfumer at a sunlit French lab, wearing a crisp white lab coat with a vermilion silk scarf, surrounded by cobalt glass apothecary bottles and rose petals, holding an emerald crystal flacon, vivid artisan portrait'),
    ('110_space_station_engineer',
     'Aerospace engineer floating inside a vivid cobalt-and-vermilion space station module, wearing a turquoise flight suit with mission patches, working on a glowing holographic console, Earth visible through porthole, vivid sci-fi portrait'),
    ('111_mecha_pilot',
     'Mecha pilot in a vivid sunset-lit hangar, wearing a chrome-and-magenta power-suit cockpit armor, the towering humanoid mech glowing behind, holographic HUD overlay, vivid giant-robot anime-style portrait'),
    ('112_postapoc_gardener',
     'Post-apocalyptic gardener in a verdant rooftop oasis reclaimed from ruins, wearing patched denim and a crimson bandana, holding a basket of glowing tomatoes and herbs, turquoise sky and solar panels, vivid solarpunk portrait'),
    ('113_retrofuture_astronaut',
     'Retrofuture 1960s astronaut in a chrome-and-coral rocket ship, wearing a bubble-helmet silver space suit with vermilion trim, starfield of saturated retro planets through the porthole, vivid space-age nostalgia portrait'),
    ('114_ice_cream_maker',
     'Master gelato maker in a pastel Italian piazza shop, wearing a turquoise apron over a magenta striped shirt, scooping rose-and-pistachio gelato, gelato display in vivid coral-and-mint stripes, vivid confectionery portrait'),
    ('115_chocolatier_belgium',
     'Belgian chocolatier in a vivid copper-and-cobalt atelier, wearing a white chef coat with a saffron neckerchief, tempering ruby-red couverture in a copper bowl, chocolate sculptures and gold leaf, vivid artisan portrait'),
    ('116_pastry_chef_paris',
     'Pastry chef in a vivid Parisian patisserie kitchen, wearing a cobalt chef coat with rose piping, holding a layered raspberry-and-pistachio entremet, copper pots and macaron tower, vivid culinary portrait'),
    ('117_bastet_cat_goddess',
     'Egyptian goddess Bastet in a vivid sunlit temple, wearing a saffron sheath gown with lapis-blue broad collar, holding a sistrum and surrounded by gleaming golden cats, sacred grove of persea trees, vivid mythological portrait'),
    ('118_sekhmet_warrior',
     'Egyptian lion goddess Sekhmet on a vivid sandstone throne, wearing a vivid crimson sheath gown with a solar disk crown, golden lionesses prowling, ankh and scepter, sun-drenched Karnak temple, vivid goddess portrait'),
    ('119_circe_enchantress',
     'Greek enchantress Circe in a vivid Aegean island glade at twilight, wearing a saffron-and-violet draped gown, golden chalice and wand, magical cobalt-and-magenta potion swirling, white lions and leopards, vivid mythological portrait'),
    ('120_selene_moon_goddess',
     'Greek moon goddess Selene riding a vivid silver chariot across a cobalt-and-violet night sky, wearing a flowing opal-white gown and crescent-diadem, stars and lavender nebulae, glowing full moon, vivid celestial goddess portrait'),
]

ctx = ssl.create_default_context()
token = get_token()
OUT_DIR.mkdir(parents=True, exist_ok=True)


def gray_percent(blob):
    image = Image.open(io.BytesIO(blob)).convert('RGB')
    image.thumbnail((512, 512))
    pixels = list(image.getdata())
    gray = sum(1 for r, g, b in pixels if max(r, g, b) - min(r, g, b) <= 15)
    return 100.0 * gray / len(pixels), image.size


def generate(prompt, label):
    body = json.dumps({'model': 'image-01', 'prompt': prompt, 'size': '1024x1024', 'n': 1}).encode()
    last = None
    for attempt in range(1, 4):
        try:
            req = urllib.request.Request(API_URL, data=body, method='POST', headers={
                'Authorization': 'Bearer ' + token,
                'Content-Type': 'application/json',
                'User-Agent': 'alonda-tier8/1.0',
            })
            with urllib.request.urlopen(req, timeout=180, context=ctx) as response:
                data = json.loads(response.read())
            urls = data.get('data', {}).get('image_urls', [])
            if not urls:
                raise RuntimeError('API response has no image URLs: ' + json.dumps(data)[:500])
            dl = urllib.request.Request(urls[0], headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(dl, timeout=120, context=ctx) as response:
                blob = response.read()
            Image.open(io.BytesIO(blob)).verify()
            print(f'{label}: generated on attempt {attempt}, {len(blob):,} bytes', flush=True)
            return blob
        except Exception as exc:
            last = exc
            print(f'{label}: attempt {attempt}/3 failed: {exc}', flush=True)
            if attempt < 3:
                time.sleep(4 * attempt)
    raise RuntimeError(f'{label}: exhausted retries: {last}')


summary = []
for position, (key, scene) in enumerate(SHOTS, start=1):
    base = (
        'A colorful, vibrant, photorealistic editorial portrait of ' + ALONDA + scene + '. '
        'Waist-up or three-quarter composition with Alonda clearly visible, accurate anatomy, cinematic lighting, '
        'rich saturated colors, sharp facial detail, premium magazine photography, no text, no watermark, not monochrome.'
    )
    blob = generate(base, key)
    gray, dimensions = gray_percent(blob)
    regenerated = False
    print(f'[{position}/20] {key}: gray={gray:.2f}% dimensions={dimensions}', flush=True)
    if gray > 55.0:
        regenerated = True
        vivid = (
            base + ' REGENERATE IN BRILLIANT FULL COLOR: use intensely saturated cobalt, turquoise, vermilion, '
            'magenta, saffron and emerald accents throughout the wardrobe, foreground and background; bright colorful '
            'lighting; absolutely no grayscale, monochrome, muted, desaturated, black-and-white or sepia treatment.'
        )
        blob = generate(vivid, key + '-vivid-regeneration')
        gray, dimensions = gray_percent(blob)
        print(f'[{position}/20] {key}: regenerated gray={gray:.2f}% dimensions={dimensions}', flush=True)
        if gray > 55.0:
            raise RuntimeError(f'{key}: regenerated image still exceeds gray threshold ({gray:.2f}%)')
    out = OUT_DIR / f'{key}.jpg'
    image = Image.open(io.BytesIO(blob)).convert('RGB')
    image.save(out, 'JPEG', quality=94, optimize=True)
    summary.append({'file': out.name, 'gray_percent': round(gray, 2), 'regenerated': regenerated, 'bytes': out.stat().st_size})
    time.sleep(2)

manifest = Path('/root/alonda/scripts/tier8_101_120_results.json')
manifest.write_text(json.dumps(summary, indent=2) + '\n')
print('\nCOMPLETE ' + json.dumps(summary), flush=True)
