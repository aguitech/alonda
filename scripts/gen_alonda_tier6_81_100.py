#!/usr/bin/env python3
"""Generate Alonda Tier 6 portraits 81-100, check gray percentage, regenerate if needed."""
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
    ('81_medusa_goddess',
     'Greek myth Medusa reimagined as an avant-garde goddess in a temple of mirrors and snakes, wearing a serpentine emerald-and-gold corset gown, living emerald serpents woven into her platinum hair, jewel-toned snakeskin mosaic floor, crystalline green-eyed reflections, vibrant cinematic mythological portrait'),
    ('82_athena_warrior',
     'Greek goddess Athena in a glowing Parthenon at sunset, wearing a crested gold helmet, polished bronze-and-white peplos with crimson sash, holding an ornate spear and a glowing olive-branch shield, owls and laurels, vividly colored marble, bold goddess portrait'),
    ('83_aphrodite_shells',
     'Greek goddess Aphrodite rising from a turquoise sea on a giant iridescent shell, wearing a flowing rose-pearl chiffon gown dripping with seafoam, surrounded by pink coral reef, golden sunset, doves and dolphins, vivid romantic mythological portrait'),
    ('84_rock_climber',
     'Sport climber on a sunlit limestone cliff over a turquoise Mediterranean cove, wearing a magenta-and-lime harness, bright cobalt chalk bag, helmet camera, dynamic three-quarter pose, vivid outdoorsy adventure portrait'),
    ('85_snowboard_alps',
     'Snowboarder mid-trick in a vivid Japanese powder park, wearing a saffron puffer jacket, electric-blue pants and mirrored goggles, exploding pink-blue sunset over Mount Fuji, neon spray of powder, vibrant action sports portrait'),
    ('86_skydiver',
     'Skydiver in freefall over a patchwork of vivid green and turquoise coastlines, wearing a hot-pink and electric-orange wingsuit, white helmet, altimeter visible, dramatic blue sky, thrilling vivid adventure portrait'),
    ('87_architect_studio',
     'Architect at a sunlit drafting table in a brutalist studio filled with magenta and saffron furniture, wearing a tailored charcoal blazer with cobalt silk scarf, hand holding a luminous blueprint model of a futuristic tower, modern editorial portrait'),
    ('88_coder_neon',
     'Software engineer at a triple-monitor workstation in a dusk-purple hacker loft, wearing a black-and-magenta hoodie, glasses reflecting scrolling neon code, holographic UI elements floating, glowing teal and magenta ambient lighting, vivid cyber professional portrait'),
    ('89_surgeon_or',
     'Cardiothoracic surgeon in a modern operating room, wearing a teal-and-navy sterile gown and cap, focused expression under bright rose-white surgical lights, robotic da Vinci arms in vivid green, gleaming instruments, cinematic medical portrait'),
    ('90_matrix_chooser',
     'The One in a vivid Matrix scene, wearing a glossy black trench coat with electric-green digital rain cascading in the air, mirrored aviator sunglasses, neon green-tinged highlights, walls of green code, saturated cyberpunk tribute portrait'),
    ('91_blade_runner_neon',
     'Blade Runner replicant in neon-drenched 2049 Los Angeles, wearing a vivid amber-and-magenta translucent raincoat, glittering holographic geisha ads and cyan spinners behind, rain-soaked glossy portrait, cinematic saturated cyberpunk noir'),
    ('92_jedi_temple',
     'Jedi Knight in a sunlit stone temple on a moss-green jungle planet, wearing cream-and-cinnamon robes with a vivid green lightsaber, ornate silver hilt, jungle waterfalls behind, epic luminous sci-fi fantasy portrait'),
    ('93_eduardian_garden',
     'Edwardian lady at a 1900s English country garden party, wearing a pale-mint and ivory lace tea gown with a wide-brimmed rose-trimmed hat, holding a pink parasol, topiary maze and foxglove borders, soft pastel historical portrait'),
    ('94_hatshepsut_egypt',
     'Queen Hatshepsut in a vivid sunlit Egyptian throne room, wearing a striped lapis-and-gold nemes headdress, kohl-lined eyes, beaded broad collar, terracotta columns and painted deities, majestic saturated historical portrait'),
    ('95_geisha_kyoto',
     'Geiko in a Kyoto teahouse at twilight, wearing a vermilion-and-cobalt silk kimono with embroidered plum blossoms, vivid crimson obi, holding a gold folding fan, paper lanterns and cherry petals, elegant vivid cultural portrait'),
    ('96_earth_elemental',
     'Personification of the earth element in a crystal forest of giant gemstones, wearing a terracotta-and-moss embroidered gown with living vines and wildflowers, butterflies and falling leaves, vivid natural fantasy portrait'),
    ('97_cosmos_nebula',
     'Cosmic goddess floating in a vibrant nebula of magenta, cyan and gold, wearing a star-patterned midnight-and-violet bodysuit with glowing constellation tattoos, distant galaxies and nebulae, vivid celestial fantasy portrait'),
    ('98_photographer_film',
     'Film photographer in a sunlit film-darkroom studio, wearing a denim jacket with magenta scarf, holding a vintage chrome Leica, rolls of saturated color film, red darkroom safelight, vivid creative professional portrait'),
    ('99_lucha_libre',
     'Mexican luchadora in a vibrant arena, wearing a custom tiger-print magenta-and-gold mask and leotard, sequin cape, ropes and crowd lights behind, dynamic victorious pose, vivid cultural sports portrait'),
    ('100_maharaja_silk',
     'Indian maharani in a Udaipur palace at golden hour, wearing a jewel-toned turquoise-and-emerald silk lehenga with heavy gold zari embroidery, ruby-and-emerald jewelry, marble jharokas and lake view, regal vivid finale portrait'),
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
                'User-Agent': 'alonda-tier6/1.0',
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

manifest = Path('/root/alonda/scripts/tier6_81_100_results.json')
manifest.write_text(json.dumps(summary, indent=2) + '\n')
print('\nCOMPLETE ' + json.dumps(summary), flush=True)
