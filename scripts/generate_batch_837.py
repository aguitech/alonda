#!/usr/bin/env python3
"""Generate Alonda portraits batch 837-856. 20 unique prompts."""
import json
import os
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

AUTH_PATH = Path('/root/.hermes/auth.json')
OUT_DIR = Path('/root/alonda/assets/images')

def get_token():
    d = json.loads(AUTH_PATH.read_text())
    t = d.get('providers', {}).get('minimax-oauth', {}).get('access_token')
    if not t:
        pool = d.get('credential_pool', {}).get('minimax-oauth', [])
        if pool:
            t = pool[0].get('access_token')
    if not t:
        raise RuntimeError('No token found')
    return t

ENDPOINT = 'https://api.' + 'minimax' + '.io/v1/image_generation'

ANCHOR = ("Alonda, a beautiful 26-year-old woman, platinum blonde long hair, "
          "striking emerald green eyes, slim athletic figure, delicate feminine "
          "facial features, natural realistic skin texture, ")

PROMPTS = [
    f"{ANCHOR}Poseidon goddess of the sea with trident and coral crown, deep underwater ruins, bioluminescent jellyfish, turquoise water, Greek mythology",
    f"{ANCHOR}Iris messenger goddess with rainbow wings and flowing golden robes, sky with clouds, divine light, Greek mythology",
    f"{ANCHOR}Nemesis goddess of retribution in dark obsidian armor and crimson cloak, moonlit temple ruins, dramatic shadows, Greek mythology",
    f"{ANCHOR}Hypnos god of sleep in soft lavender silk pajamas, surrounded by poppies and dream clouds, moonlit bedroom, Greek mythology",
    f"{ANCHOR}Morpheus god of dreams in a surreal dreamscape with melting clocks and floating doors, vibrant surrealist colors, Greek mythology",
    f"{ANCHOR}professional kitesurfer riding huge wave in tropical ocean, bright sunset, action shot, water spray",
    f"{ANCHOR}BMX rider mid-air doing a backflip in urban skate park, graffiti walls, dramatic angle, dynamic motion",
    f"{ANCHOR}wakeboarder doing spin behind speedboat on lake, summer sky, water droplets frozen in motion",
    f"{ANCHOR}parkour athlete leaping between rooftops in Tokyo at golden hour, urban skyline, dramatic silhouette",
    f"{ANCHOR}base jumper in wingsuit flying through mountain valley, blue sky, dramatic landscape below",
    f"{ANCHOR}kind midwife in cozy birthing center, soft natural light, holding newborn baby, warm atmosphere",
    f"{ANCHOR}caring veterinarian examining golden retriever puppy in modern clinic, stethoscope, soft light",
    f"{ANCHOR}marine biologist diving with manta rays in tropical reef, wetsuit, underwater photography",
    f"{ANCHOR}museum curator in elegant gallery examining ancient artifact, marble halls, soft museum lighting",
    f"{ANCHOR}librarian in beautiful old library with green banker lamps and leather books, golden warm light",
    f"{ANCHOR}Wonder Woman on Themyscira beach with golden lasso and tiara, dramatic DC superhero portrait, golden armor",
    f"{ANCHOR}Lara Croft adventurer in jungle tomb with dual pistols, action pose, video game character portrait",
    f"{ANCHOR}Black Widow in sleek tactical suit in spy hideout, red highlights, Marvel cinematic portrait",
    f"{ANCHOR}Daenerys Targaryen with platinum silver hair and three dragons, throne room, Game of Thrones style",
    f"{ANCHOR}Rey Skywalker holding lightsaber on desert planet Jakku, Star Wars cinematic portrait, sand and sky",
]

def call_api(prompt, token, max_retries=3):
    body = json.dumps({
        'model': 'image-01',
        'prompt': prompt,
        'size': '1024x1024',
        'n': 1,
    }).encode('utf-8')
    last_err = None
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(
                ENDPOINT,
                data=body,
                headers={
                    'Authorization': 'Bearer ' + token,
                    'Content-Type': 'application/json',
                },
                method='POST',
            )
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = json.loads(resp.read())
            urls = data.get('data', {}).get('image_urls') or data.get('image_urls') or []
            if not urls:
                raise RuntimeError(f'No URLs in response: {data}')
            return urls[0]
        except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError, RuntimeError) as e:
            last_err = e
            print(f'  attempt {attempt+1} failed: {e}', file=sys.stderr)
            time.sleep(2 + attempt * 2)
    raise RuntimeError(f'All retries failed: {last_err}')

def download(url, dest):
    for attempt in range(3):
        try:
            with urllib.request.urlopen(url, timeout=120) as resp:
                dest.write_bytes(resp.read())
            return True
        except Exception as e:
            print(f'  download attempt {attempt+1} failed: {e}', file=sys.stderr)
            time.sleep(2)
    return False

def is_grayscale(path, threshold=0.55):
    try:
        from PIL import Image
        img = Image.open(path).convert('RGB')
        w, h = img.size
        step = 4
        samples = []
        for y in range(0, h, step):
            for x in range(0, w, step):
                samples.append(img.getpixel((x, y)))
        total = len(samples)
        gray = 0
        for r, g, b in samples:
            if (max(r, g, b) - min(r, g, b)) < 15:
                gray += 1
        return (gray / total) > threshold
    except ImportError:
        return False
    except Exception as e:
        print(f'  grayscale check error: {e}', file=sys.stderr)
        return False

def main():
    token = get_token()
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    start = 837
    results = []

    for i, prompt in enumerate(PROMPTS):
        num = start + i
        # Extract short slug from prompt after ANCHOR
        body = prompt[len(ANCHOR):]
        slug_words = body.split()[:6]
        slug = '_'.join(slug_words).replace(',', '').replace('.', '').lower()
        slug = ''.join(c for c in slug if c.isalnum() or c == '_')[:50]
        fname = f'{num}_{slug}.jpg'
        dest = OUT_DIR / fname

        print(f'[{i+1}/20] generating #{num} ...', flush=True)
        try:
            url = call_api(prompt, token)
        except Exception as e:
            print(f'  SKIP {num}: {e}', file=sys.stderr)
            continue

        tmp = dest.with_suffix('.tmp.jpg')
        if not download(url, tmp):
            print(f'  SKIP {num}: download failed', file=sys.stderr)
            continue

        if is_grayscale(tmp):
            print(f'  #{num} grayscale, regenerating with vibrant suffix ...', flush=True)
            vibrant = prompt + ', vivid saturated colors, vibrant rainbow palette, hypercolorful'
            try:
                url2 = call_api(vibrant, token)
                if download(url2, tmp):
                    if is_grayscale(tmp):
                        print(f'  #{num} still grayscale, accepting', file=sys.stderr)
            except Exception as e:
                print(f'  vibrant retry failed: {e}', file=sys.stderr)

        tmp.replace(dest)
        results.append((num, fname, str(dest)))
        print(f'  OK {fname}', flush=True)
        time.sleep(1)

    print('---SUMMARY---')
    print(json.dumps({'generated': len(results), 'files': [r[1] for r in results]}))

if __name__ == '__main__':
    main()
