#!/usr/bin/env python3
"""Generate Alonda Tier 4 portraits 41-60, check gray percentage, regenerate if needed.
Categories entirely new — no overlap with tiers 1-3, 5, or 6.
"""
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


# 20 promts UNIQUE — no overlap with tiers 1-3, 5, 6.
SHOTS = [
    ('41_pirate_caribbean',
     'Bold 18th-century Caribbean pirate captain on the deck of a teak galleon at golden hour, '
     'wearing a vivid vermilion silk waistcoat with brass buttons, tricorn hat with a saffron plume, '
     'leather corset belt with a jeweled dagger, parrot on her shoulder, vivid turquoise Caribbean '
     'sea and pink sunset sky behind, daring vivid adventure portrait'),
    ('42_western_cowgirl',
     'Frontier cowgirl at a vibrant Arizona rodeo at sunset, wearing a turquoise-embroidered leather '
     'bolero, fringed leather skirt, magenta bandana, brass conchos and silver spurs, holding a '
     'lasso loop, vivid orange-red desert sky and rodeo lights, vibrant western portrait'),
    ('43_flamenco_dancer',
     'Flamenco dancer mid-pose in a sunlit Andalusian patio with vivid azulejo tiles, wearing a '
     'crimson ruffled polka-dot dress with black lace mantilla, castanets clicking, roses in her '
     'hair, warm orange-warm light, vivid Spanish cultural portrait'),
    ('44_naval_officer',
     'Modern naval officer on the bridge of a sleek warship at dawn, wearing a pristine white-and-'
     'navy uniform with brass insignia and gold stripes, scanning horizon with binoculars, vivid '
     'rose-and-coral sunrise over cobalt ocean, crisp cinematic maritime portrait'),
    ('45_arctic_explorer',
     'Polar explorer on a glittering Arctic ice floe, wearing a vivid saffron parka with cobalt '
     'fur-lined hood, frost on eyelashes, sled dogs and vivid teal aurora overhead, vibrant '
     'adventure polar portrait'),
    ('46_data_scientist',
     'Data scientist in a sunlit modern lab filled with holographic data visualizations, wearing a '
     'cobalt blazer over a magenta silk blouse, holding a tablet glowing with chromatic graphs, '
     'turquoise ambient lighting, vivid tech professional portrait'),
    ('47_rally_driver',
     'Rally co-driver mid-race in a vivid red-and-yellow Peugeot cockpit, wearing a cobalt-and-'
     'white fire suit, helmet visor raised, dust swirling outside the windshield, dynamic motion '
     'blur, vivid motorsport portrait'),
    ('48_victorian_gardener',
     'Victorian head gardener at a vivid English walled rose garden, wearing a sage-green linen '
     'smock over a rose-pearl dress, leather gloves, secateurs in hand, overflowing flower borders '
     'of magenta and crimson roses, vivid horticultural portrait'),
    ('49_antique_bookseller',
     'Antique bookshop owner in a cozy wood-paneled shop stacked with leather-bound volumes, '
     'wearing a vintage emerald velvet jacket with gold brooch, reading spectacles perched on '
     'her platinum hair, warm amber lamp light, vivid literary portrait'),
    ('50_expressive_painter',
     'Expressionist painter in a vivid splattered studio, wearing paint-splattered overalls in '
     'cobalt, magenta and saffron, palette in one hand and brush in the other, canvas exploding '
     'with abstract color, vivid artistic portrait'),
    ('51_bonsai_master',
     'Bonsai master in a serene Japanese garden, wearing a cobalt kimono with sage obi, carefully '
     'shaping a miniature pink azalea bonsai with copper wire, vivid maple leaves and stone '
     'lanterns, vivid horticultural cultural portrait'),
    ('52_tap_dancer',
     'Tap dancer mid-routine on a vivid Broadway spotlight stage, wearing a sparkling cobalt '
     'sequin flapper dress with fringe, ruby lipstick, vintage microphone, magenta stage curtains, '
     'vivid jazz-age performance portrait'),
    ('53_drag_queen',
     'Drag queen in vivid full glam on a glittering nightclub stage, wearing an oversized magenta '
     'feather headdress, jewel-encrusted cobalt bodysuit, dramatic lashes and contour, spotlight '
     'in rose and gold, vibrant performance portrait'),
    ('54_kpop_idol',
     'K-pop idol on a neon-drenched Seoul stage, wearing a futuristic holographic pink-and-cyan '
     'crop top and pleated skirt, glitter makeup, glowing mic stand, vivid magenta and teal stage '
     'lights, vibrant pop performance portrait'),
    ('55_speleologist',
     'Speleologist deep in a vivid illuminated crystal cave, wearing a cobalt climbing helmet with '
     'LED light, harness and ropes, surrounded by glowing magenta and turquoise stalactites, '
     'underground river reflecting lights, vivid exploration portrait'),
    ('56_art_restorer',
     'Art restorer in a vivid sunlit Renaissance gallery, wearing a white lab coat over a saffron '
     'silk blouse, examining a vivid baroque painting with magnifying loupe, jewel-toned '
     'masterpieces behind her, vivid cultural professional portrait'),
    ('57_dragster_pilot',
     'Dragster pilot on the starting line of a vivid sunset strip, wearing a cobalt fire suit with '
     'saffron stripes and tinted visor, leaning against a candy-red top-fuel dragster, '
     'nitromethane flames in the background, vivid motorsport portrait'),
    ('58_medieval_tarot',
     'Medieval tarot reader in a candlelit Gothic tower, wearing a velvet amethyst gown with gold '
     'embroidery, laying out vivid celestial tarot cards on an aged oak table, owls and ravens '
     'perched nearby, mysterious vivid mystical portrait'),
    ('59_butoh_dancer',
     'Butoh dancer in a minimalist white studio flooded with vivid magenta and cobalt light, '
     'wearing chalk-white body paint with cobalt accents, slow-motion avant-garde pose, '
     'vivid contemporary dance portrait'),
    ('60_urban_beekeeper',
     'Urban beekeeper on a vivid Brooklyn rooftop apiary, wearing a cobalt beekeeping veil and '
     'white gloves, holding a wooden frame dripping with golden honeycomb, vivid yellow sunflowers '
     'and city skyline behind, vibrant modern apiarist portrait'),
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
                'User-Agent': 'alonda-tier4/1.0',
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

manifest = Path('/root/alonda/scripts/tier4_41_60_results.json')
manifest.write_text(json.dumps(summary, indent=2) + '\n')
print('\nCOMPLETE ' + json.dumps(summary), flush=True)
