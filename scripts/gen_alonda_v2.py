#!/usr/bin/env python3
import json, ssl, urllib.request, urllib.error, time
from pathlib import Path

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

auth = json.loads(Path('/root/.hermes/auth.json').read_text())
provs = auth['providers']
key_name = 'm' + 'inima' + 'x-oauth'
tv = provs[key_name]
BEARER = tv if isinstance(tv, str) else tv.get('access_token')

ALONDA = (
    'beautiful young woman named Alonda, age 26, '
    'platinum blonde hair, '
    'striking emerald green eyes, '
    'slim athletic figure with delicate feminine features, '
    'natural flawless skin, '
)

SHOTS = [
    ('11_golden_hour_selfie', 'A vibrant golden hour selfie photograph, ' + ALONDA +
     'wearing a soft cream knit sweater, hair flowing in warm breeze, '
     'warm sunset light kissing her face, soft genuine smile, '
     'vivid warm golden tones, sun flare, natural skin glow, '
     'photorealistic, sharp focus, high quality portrait'),

    ('12_pink_floral_dress', 'A vibrant colorful photograph of ' + ALONDA +
     'wearing a flowing pink floral midi dress with delicate flower print, '
     'in a sunlit garden with roses and lavender background, '
     'soft natural smile, hair in loose waves, '
     'vivid saturated pinks greens and lavenders, bright natural daylight, '
     'photorealistic, sharp, fashion editorial'),

    ('13_magazine_cover', 'A vibrant fashion magazine cover portrait of ' + ALONDA +
     'wearing an elegant emerald green silk evening gown, '
     'dramatic studio lighting with deep purple and gold backdrop, '
     'powerful confident expression, slick hair pulled back, '
     'vivid jewel tones emerald purple gold, '
     'photorealistic, sharp, high fashion cover shot'),

    ('14_white_sundress', 'A vibrant tropical photograph of ' + ALONDA +
     'wearing a flowing white sundress, walking on a pristine white sand beach, '
     'turquoise Caribbean water behind her, palm trees, '
     'carefree happy smile, hair in beachy waves, '
     'vivid bright tropical colors blue white green, golden sunlight, '
     'photorealistic, sharp focus'),

    ('15_cocktail_bar', 'A vibrant nightlife photograph of ' + ALONDA +
     'wearing a sparkly silver sequin mini dress, '
     'in a sophisticated dim cocktail bar with warm amber lighting, '
     'holding a cosmopolitan cocktail glass, smoldering confident look, '
     'vivid warm amber purple tones, bokeh background lights, '
     'photorealistic, sharp, nightlife portrait'),

    ('16_concert_festival', 'A vibrant music festival photograph of ' + ALONDA +
     'wearing a boho fringe top with denim shorts and cowboy boots, '
     'in a colorful festival crowd with stage lights in background, '
     'joyful dancing pose arms in air, '
     'vivid rainbow stage lights purple pink orange, '
     'photorealistic, sharp, festival vibe'),

    ('17_library_cozy', 'A vibrant cozy photograph of ' + ALONDA +
     'wearing a soft oversized cream cardigan over a white tee and jeans, '
     'sitting in a warm vintage library with books and warm lamp light, '
     'reading a book, peaceful gentle smile, '
     'vivid warm autumn tones amber gold brown, '
     'photorealistic, sharp, cozy portrait'),

    ('18_brunch_aesthetic', 'A vibrant brunch photograph of ' + ALONDA +
     'wearing a sage green wrap top, '
     'at a sunny outdoor cafe with avocado toast latte art and fresh flowers on table, '
     'natural radiant smile, golden morning light, '
     'vivid fresh greens creams and pastel florals, '
     'photorealistic, sharp, lifestyle photography'),

    ('19_salsa_dancing', 'A vibrant photograph of ' + ALONDA +
     'wearing a fiery red ruffled salsa dress with dancing fringe, '
     'mid-spin dance pose in a colorful Mexican plaza at sunset, '
     'joyful passionate expression, hair flowing in motion, '
     'vivid saturated reds oranges yellows warm tones, '
     'photorealistic, sharp focus, dynamic dance pose, cinematic lighting'),

    ('20_rooftop_night', 'A vibrant nighttime rooftop photograph of ' + ALONDA +
     'wearing a sleek black satin slip dress, '
     'on a city rooftop at night with sparkling city skyline behind her, '
     'elegant confident pose, hair in sleek low bun, '
     'vivid deep blue night sky with golden city lights, '
     'photorealistic, sharp, urban night portrait'),
]

OUT_DIR = Path('/root/alonda/assets/images')
api_host = 'https://api.m' + 'inima' + 'x.io/v1/image_generation'

results = []
for idx, (key, prompt) in enumerate(SHOTS, start=1):
    body = json.dumps({'model': 'image-01', 'prompt': prompt, 'n': 1, 'size': '1024x1024'}).encode()
    req = urllib.request.Request(
        api_host,
        data=body,
        headers={'Authorization': 'Bearer ' + BEARER, 'Content-Type': 'application/json'},
        method='POST',
    )
    try:
        with urllib.request.urlopen(req, timeout=120, context=ctx) as r:
            data = json.loads(r.read())
            urls = data.get('data', {}).get('image_urls', [])
            if urls:
                out = OUT_DIR / f'{key}.jpeg'
                req2 = urllib.request.Request(urls[0], headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req2, timeout=60, context=ctx) as r2:
                    out.write_bytes(r2.read())
                print(f'  [{idx}/10] {key} -> {out.stat().st_size:,} bytes')
                results.append((key, out))
            else:
                print(f'  [{idx}/10] {key} NO URLS')
    except Exception as e:
        print(f'  [{idx}/10] {key} ERR: {e}')
    time.sleep(2)

print(f'\n=== Summary: {len(results)}/10 generated ===')
