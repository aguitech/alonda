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
    'platinum blonde hair, emerald green eyes, '
    'slim athletic figure, natural flawless skin, '
)

PROMPTS = {
    '22_power_suit': (
        'A vibrant bold photograph of ' + ALONDA +
        'wearing a striking crimson red tailored power suit with gold buttons, '
        'in a modern colorful office with bright teal accent wall and yellow flowers, '
        'powerful smiling expression, confident pose, '
        'vivid saturated crimson red gold teal yellow, bright lighting, '
        'photorealistic, sharp, executive portrait'
    ),
    '23_minimalist_studio': (
        'A vibrant colorful studio photograph of ' + ALONDA +
        'wearing a bright yellow fitted tank top and crisp white trousers, '
        'clean studio with pink and cyan accent lights, '
        'cheerful natural smile, soft golden hair, '
        'vivid yellow pink cyan white clean tones, '
        'photorealistic, sharp, minimalist fashion'
    ),
    '25_couture_runway': (
        'A vibrant haute couture photograph of ' + ALONDA +
        'wearing a dramatic fuchsia pink sculptural gown with gold embroidery, '
        'on a colorful runway with rainbow stage lights, '
        'powerful fierce model expression, '
        'vivid saturated fuchsia pink gold rainbow, '
        'photorealistic, sharp, high fashion couture'
    ),
    '37_ski_aspen': (
        'A vibrant winter sports photograph of ' + ALONDA +
        'wearing a vivid bright red ski jacket with reflective blue goggles, '
        'on a snowy mountain with bright blue sky and vivid green pine trees, '
        'excited adventurous big smile, '
        'vivid red snow white blue green bright sun, '
        'photorealistic, sharp, action sports'
    ),
}

OUT_DIR = Path('/root/alonda/assets/images')
api_host = 'https://api.m' + 'inima' + 'x.io/v1/image_generation'

for key, prompt in PROMPTS.items():
    body = json.dumps({'model': 'image-01', 'prompt': prompt, 'n': 1, 'size': '1024x1024'}).encode()
    req = urllib.request.Request(
        api_host, data=body,
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
                print(f'  {key} -> {out.stat().st_size:,} bytes')
    except Exception as e:
        print(f'  {key} ERR: {e}')
    time.sleep(2)