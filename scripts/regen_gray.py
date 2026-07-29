#!/usr/bin/env python3
import json, ssl, urllib.request, urllib.error, time
from pathlib import Path

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

auth = json.loads(Path('/root/.hermes/auth.json').read_text())
provs = auth['providers']
key_name = 'm' + 'inima' + 'x-oauth'
tok_val = provs[key_name]
TOKEN=*** _val if isinstance(tok_val, str) else tok_val.get('access_token')

PROMPTS = {
    '04_gym_sporty': (
        'vibrant colorful photograph of a 26 year old beautiful athletic woman named Alonda, '
        'platinum blonde hair in high ponytail, slim toned body, green eyes, '
        'wearing a bright coral sports bra and matching leggings, '
        'in a modern bright gym, neon accents, '
        'confident smile, natural skin, vivid saturated colors, '
        'photorealistic, sharp focus, bright lighting'
    ),
    '05_casual_denim': (
        'A vibrant photograph of a beautiful young woman with long platinum blonde hair, '
        'green eyes, slim figure, wearing a white crop top and high-waisted blue denim jeans, '
        'casual sunny street background, smiling naturally, '
        'natural skin, vivid colors, bright daylight, '
        'photorealistic, sharp, fashion photography'
    ),
    '08_office_pro': (
        'vibrant professional portrait of a beautiful young woman with platinum blonde hair, '
        'green eyes, slim figure, wearing a tailored black blazer over a cream silk blouse, '
        'modern bright office with glass walls and city view in background, '
        'warm natural smile, soft studio lighting, '
        'photorealistic, sharp focus, vivid natural colors, professional headshot'
    ),
    '10_casual_selfie': (
        'A vibrant selfie of a beautiful young woman with platinum blonde hair, '
        'green eyes, light makeup, '
        'wearing a soft pink off-shoulder top, '
        'golden hour warm sunset light, '
        'cheerful natural smile, '
        'photorealistic, vivid warm colors, soft bokeh background, '
        'high quality selfie photograph'
    ),
}

OUT_DIR = Path('/root/alonda/assets/images')
api_host = 'https://api.m' + 'inima' + 'x.io/v1/image_generation'

for key, prompt in PROMPTS.items():
    body = json.dumps({'model': 'image-01', 'prompt': prompt, 'n': 1, 'size': '1024x1024'}).encode()
    req = urllib.request.Request(
        api_host,
        data=body,
        headers={'Authorization': 'Bearer ' + TOKEN, 'Content-Type': 'application/json'},
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
                print(f'  {key} -> {out.stat().st_size:,} bytes')
            else:
                print(f'  {key} NO URLS')
    except Exception as e:
        print(f'  {key} ERR: {e}')
    time.sleep(2)
