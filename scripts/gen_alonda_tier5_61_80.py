#!/usr/bin/env python3
"""Generate Alonda Tier 5 portraits 61-80, check gray percentage, regenerate if needed."""
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

# All are distinct from the prior studio/urban/lifestyle/Mexico/sports/fantasy looks.
SHOTS = [
    ('61_volcanologist_lava', 'Volcanologist beside a glowing lava field in Iceland, wearing a vivid cobalt technical expedition suit and orange safety helmet, geological tools, dramatic red-orange lava reflections, documentary adventure portrait'),
    ('62_falconer_steppe', 'Falconer on a windswept Central Asian steppe at sunrise, wearing an ornate turquoise and crimson embroidered coat, a golden eagle perched on her leather glove, mountain panorama, cinematic cultural portrait'),
    ('63_glassblower_venice', 'Master glassblower inside a colorful Murano workshop, shaping molten glass with a blowpipe, wearing a sapphire apron, shelves filled with jewel-toned glass sculptures, warm furnace glow, artisan portrait'),
    ('64_deep_sea_diver', 'Deep-sea scientific diver in a modern transparent diving helmet beneath a coral reef, surrounded by tropical fish and luminous blue water, bright yellow-red technical suit, underwater portrait'),
    ('65_hot_air_balloonist', 'Hot-air balloon pilot high above Cappadocia at sunrise, wearing a rich burgundy leather flight jacket and patterned silk scarf, dozens of multicolored balloons behind her, joyful windswept portrait'),
    ('66_archaeologist_petra', 'Archaeologist at Petra uncovering an ancient mosaic, wearing a sunlit teal field shirt, sand-colored utility trousers and wide hat, rose-red temple cliffs behind, adventurous historical portrait'),
    ('67_orchestra_conductor', 'Symphony orchestra conductor mid-performance in an opulent concert hall, wearing a dramatic emerald velvet tailcoat, baton raised, musicians and golden chandeliers behind, energetic fine-art portrait'),
    ('68_beekeeper_lavender', 'Beekeeper in a vast Provence lavender field, wearing a white protective veil over a bright sunflower-yellow linen outfit, holding a honeycomb alive with bees, violet rows at golden hour, pastoral portrait'),
    ('69_northern_lights_guide', 'Aurora expedition guide on a frozen lake in Lapland, wearing a vivid magenta insulated parka with fur hood, emerald and violet northern lights swirling overhead, colorful night adventure portrait'),
    ('70_ceramic_artist', 'Contemporary ceramic artist in a sun-filled workshop painting an enormous cobalt-and-coral vase, wearing a terracotta linen jumpsuit splashed with pigments, walls of colorful pottery, tactile artisan portrait'),
    ('71_renaissance_court', 'Italian Renaissance court portrait in a Florentine palazzo, wearing a sumptuous ruby velvet gown with pearl embroidery and gold brocade sleeves, frescoes and arched garden view, luminous historical realism'),
    ('72_rococo_masquerade', 'Rococo masquerade at Versailles, wearing an extravagant powder-blue and blush silk gown with embroidered flowers, holding an ornate gold mask, candlelit mirrored ballroom, playful pastel historical portrait'),
    ('73_art_deco_aviatrix', '1930s Art Deco aviatrix beside a polished crimson biplane, wearing a caramel leather flight suit, cream scarf and goggles, geometric hangar graphics, saturated retro travel-poster colors, cinematic portrait'),
    ('74_viking_shieldmaiden', 'Viking shieldmaiden on a Norwegian fjord shore, wearing blue wool, red leather armor and silver knotwork, round painted shield in hand, braided platinum hair, dramatic colorful saga portrait'),
    ('75_mongol_horse_archer', 'Mongol horse archer riding across a flowered highland valley, wearing turquoise lamellar armor and a crimson deel, ornate bow, fluttering prayer flags and snow mountains, dynamic epic portrait'),
    ('76_aztec_astronomer', 'Aztec astronomer-priestess atop a ceremonial observatory at twilight, wearing richly woven jade, scarlet and gold regalia with feathered celestial headdress, studying constellations, vivid historical-fantasy portrait'),
    ('77_fire_elemental', 'Personification of the fire element in a surreal volcanic palace, wearing a flowing vermilion and molten-gold gown whose fabric becomes flames, glowing amber atmosphere, majestic fantasy fashion portrait'),
    ('78_air_elemental', 'Personification of the air element above cloud islands, wearing an iridescent sky-blue and lilac chiffon gown billowing like wind, ribbons and white birds spiraling around her, bright ethereal fantasy portrait'),
    ('79_lunar_empress', 'Lunar empress in a moonlit silver-blue palace on an alien landscape, wearing an opalescent indigo gown and crescent crown, enormous colorful planets and stars behind, vibrant celestial portrait'),
    ('80_solar_oracle', 'Solar oracle inside a radiant golden observatory, wearing a saffron, coral and turquoise ceremonial robe with sunburst jewelry, prisms casting rainbow light across the scene, vivid cosmic portrait'),
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
                'User-Agent': 'alonda-tier5/1.0',
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

manifest = Path('/root/alonda/scripts/tier5_61_80_results.json')
manifest.write_text(json.dumps(summary, indent=2) + '\n')
print('\nCOMPLETE ' + json.dumps(summary), flush=True)
