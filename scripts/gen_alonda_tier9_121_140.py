#!/usr/bin/env python3
"""Generate Alonda Tier 10 portraits 141-160, check gray percentage, regenerate if needed."""
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


# 20 prompts UNIQUE vs portraits 1-140. Myth, extreme sports, science fiction, crafts, dance.
SHOTS = [
    ('141_athena_owl', 'Greek goddess Athena in a marble Acropolis library at dawn, wearing sapphire armor and a crimson peplos, golden owl on her shoulder, olive branches and turquoise Aegean light, vivid mythological portrait'),
    ('142_medusa_mosaic', 'Mythic Medusa reimagined as a powerful emerald-eyed heroine in a jewel-toned temple, jeweled serpents woven through platinum hair, cobalt mosaic walls, ruby roses and golden torchlight, vibrant fantasy portrait'),
    ('143_snowboarder_alps', 'Snowboard champion carving through powder on a sunlit alpine ridge, wearing electric magenta and turquoise technical gear, saffron goggles, cobalt peaks and colorful powder spray, dynamic sports portrait'),
    ('144_motocross_desert', 'Motocross racer beside a scarlet dirt bike in a desert canyon, wearing a cobalt helmet and vermilion racing suit, turquoise dust haze, saffron cliffs and dramatic sunset, cinematic action portrait'),
    ('145_kitesurfer_lagoon', 'Kite surfer launching over a crystalline tropical lagoon, wearing coral-and-teal wetsuit, bright turquoise kite, emerald palms and saffron sunlight, vivid athletic travel portrait'),
    ('146_cyberpunk_hacker', 'Cyberpunk hacker in a rain-washed neon megacity, wearing a luminous violet jacket with turquoise circuitry, holographic code and crimson reflections, cinematic science-fiction portrait'),
    ('147_space_station_botanist', 'Space-station botanist tending a floating garden beneath panoramic stars, wearing a white-and-cobalt jumpsuit with coral accents, glowing orchids, emerald Earth and golden nebula, colorful sci-fi portrait'),
    ('148_time_traveler', 'Retro-futurist time traveler beside a polished brass chronometer portal, wearing a teal velvet coat and magenta scarf, swirling aurora, ruby gears and saffron sparks, imaginative portrait'),
    ('149_robotics_engineer', 'Robotics engineer in a bright innovation lab presenting a friendly humanoid robot, wearing an emerald blazer and orange safety glasses, turquoise screens, magenta tools and warm studio light, professional portrait'),
    ('150_quantum_scientist', 'Quantum scientist in a glass observatory surrounded by luminous particle trails, wearing a cobalt lab coat with saffron trim, coral equations and emerald laser light, vibrant high-tech portrait'),
    ('151_stained_glass_artist', 'Stained-glass artisan in a sunlit workshop, wearing turquoise overalls and ruby earrings, holding a colorful glass panel of hummingbirds, magenta shards and golden light, detailed craft portrait'),
    ('152_bookbinder', 'Master bookbinder in a cozy jewel-toned studio, wearing a plum apron, arranging emerald leather and saffron-gold tooling beside an antique press, rich textures and warm light, artisan portrait'),
    ('153_blacksmith', 'Contemporary blacksmith forging a glowing blade in a colorful mountain forge, wearing protective cobalt leather and crimson gloves, orange sparks, turquoise tools and emerald firelight, powerful craft portrait'),
    ('154_flamenco_dancer', 'Flamenco dancer spinning in a Seville courtyard, wearing a dramatic crimson ruffled dress with turquoise embroidery, saffron fan, cobalt tiles and bougainvillea, elegant motion portrait'),
    ('155_tango_dancer', 'Tango dancer performing on a Buenos Aires theater stage, wearing a magenta satin dress and cobalt gloves, scarlet roses, golden spotlight and deep turquoise curtains, glamorous dance portrait'),
    ('156_kpop_dancer', 'K-pop dancer in a futuristic Seoul studio, wearing coordinated electric turquoise and pink streetwear, holographic panels, cobalt floor lights and saffron accents, energetic performance portrait'),
    ('157_hula_dancer', 'Hula dancer on a moonlit Hawaiian beach, wearing a vivid tropical lei and emerald grass skirt with coral accents, turquoise ocean, saffron torches and starry sky, joyful cultural portrait'),
    ('158_orchid_hybridizer', 'Botanical hybridizer in a luminous orchid conservatory, wearing a coral blouse and emerald gardening apron, rare violet blooms, turquoise glasshouse and golden mist, vivid nature portrait'),
    ('159_solarpunk_architect', 'Solarpunk architect on a rooftop garden designing a vertical city, wearing a saffron jumpsuit and turquoise scarf, emerald plants, colorful solar panels and magenta sunset, optimistic future portrait'),
    ('160_aurora_rescue', 'Alpine rescue specialist at a glowing aurora base camp, wearing a crimson expedition parka with cobalt and saffron gear, emerald northern lights, turquoise snow and warm lanterns, cinematic adventure portrait'),
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
                'User-Agent': 'alonda-tier10/1.0',
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

manifest = Path('/root/alonda/scripts/tier10_141_160_results.json')
manifest.write_text(json.dumps(summary, indent=2) + '\n')
print('\nCOMPLETE ' + json.dumps(summary), flush=True)
