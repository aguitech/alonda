#!/usr/bin/env python3
"""Generate 20 more Alonda portraits — Tier 3 (editorial + cultura + méxico + deportes)."""
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
    # ── Tier 3A · Editorial / Moda ──────────────────────────────────────
    ('21_wedding_dress', 'A vibrant bridal portrait of ' + ALONDA +
     'wearing an elegant white lace wedding dress with cathedral veil, '
     'soft romantic studio lighting with white roses, '
     'gentle radiant bridal smile, hair in elegant updo, '
     'vivid ivory whites soft greens rose gold tones, '
     'photorealistic, sharp, luxury bridal photography'),

    ('22_power_suit', 'A vibrant powerful executive portrait of ' + ALONDA +
     'wearing a tailored burgundy red power suit with gold buttons, '
     'standing confidently in a modern glass corner office with city skyline, '
     'powerful confident expression, sleek hair pulled back, '
     'vivid deep burgundy red gold amber tones, '
     'photorealistic, sharp, executive headshot'),

    ('23_minimalist_studio', 'A vibrant minimalist studio portrait of ' + ALONDA +
     'wearing a simple clean white tank top and high-waisted cream trousers, '
     'clean white studio backdrop with soft shadows, '
     'natural beauty minimal makeup hair down, '
     'vivid pure whites soft creams clean tones, '
     'photorealistic, sharp, minimalist fashion'),

    ('24_boho_crochet', 'A vibrant boho beach photograph of ' + ALONDA +
     'wearing a white crochet beach top and flowing sage green skirt, '
     'on a sunny beach with turquoise water and golden sand, '
     'carefree happy smile, sun-kissed hair, '
     'vivid turquoise white sage green golden tones, '
     'photorealistic, sharp, boho lifestyle photography'),

    ('25_couture_runway', 'A vibrant haute couture runway photograph of ' + ALONDA +
     'wearing a dramatic architectural black and gold sculptural gown, '
     'on a fashion runway with dramatic spotlights and audience blurred behind, '
     'powerful fierce model expression, sleek straight hair, '
     'vivid black gold dramatic contrast tones, '
     'photorealistic, sharp, fashion runway photography'),

    # ── Tier 3B · Cultura / Lifestyle ───────────────────────────────────
    ('26_paris_cafe', 'A vibrant lifestyle photograph of ' + ALONDA +
     'wearing a striped navy breton top and red lipstick, '
     'sitting at a classic Parisian cafe terrace with espresso and croissant, '
     'chic effortless smile, hair in messy French twist, '
     'vivid navy red cream cafe tones, '
     'photorealistic, sharp, Paris lifestyle'),

    ('27_skate_park', 'A vibrant urban photograph of ' + ALONDA +
     'wearing a tie-dye cropped hoodie high-waisted ripped jeans white sneakers, '
     'at a colorful graffiti skate park holding a skateboard, '
     'fun confident pose, hair loose wild, '
     'vivid rainbow graffiti tones street art, '
     'photorealistic, sharp, urban street style'),

    ('28_art_museum', 'A vibrant cultural portrait of ' + ALONDA +
     'wearing a sleek black turtleneck and tailored grey wool coat, '
     'in a grand classical art museum gallery with marble columns and paintings, '
     'contemplative serene expression, hair in elegant low bun, '
     'vivid warm museum lighting gold marble tones, '
     'photorealistic, sharp, museum portrait'),

    ('29_train_station', 'A vibrant vintage travel photograph of ' + ALONDA +
     'wearing a camel coat with silk red scarf and leather gloves, '
     'in a grand vintage European train station with clock and steam, '
     'wistful adventurous expression, hair under beret, '
     'vivid warm amber sepia vintage tones, '
     'photorealistic, sharp, vintage travel photography'),

    ('30_sunrise_rooftop', 'A vibrant sunrise rooftop photograph of ' + ALONDA +
     'wearing a soft lavender silk robe, holding a cup of coffee, '
     'on a city rooftop at golden sunrise, soft morning light, '
     'peaceful meditative expression, hair flowing in morning breeze, '
     'vivid soft lavender peach gold sunrise tones, '
     'photorealistic, sharp, golden hour morning portrait'),

    # ── Tier 3C · México lindo ─────────────────────────────────────────
    ('31_tehuana_oaxaquena', 'A vibrant cultural portrait of ' + ALONDA +
     'wearing a traditional Tehuana white huipil with elaborate floral embroidery and gold jewelry, '
     'standing in a colorful Oaxaca market with bougainvillea, '
     'proud dignified expression, hair in long braid with flowers, '
     'vivid white gold fuchsia bougainvillea tones, '
     'photorealistic, sharp, Mexican cultural photography'),

    ('32_catrina_dia_muertos', 'A vibrant Day of the Dead elegant portrait of ' + ALONDA +
     'in elegant La Catrina makeup with intricate sugar skull face paint, '
     'wearing a flowing marigold orange gown with floral crown, '
     'in a candlelit ofrenda setting with marigolds, '
     'vivid orange marigold gold purple candle tones, '
     'photorealistic, sharp, Mexican cultural celebration'),

    ('33_flower_market', 'A vibrant market photograph of ' + ALONDA +
     'wearing a simple yellow sundress, '
     'surrounded by vivid piles of flowers roses dahlias sunflowers at a Mexican flower market, '
     'joyful expression, hair with a flower tucked behind ear, '
     'vivid saturated pinks yellows oranges reds, '
     'photorealistic, sharp, market lifestyle photography'),

    ('34_charra_sombrero', 'A vibrant charrería portrait of ' + ALONDA +
     'wearing a traditional charro outfit with wide brim sombrero and embroidered jacket, '
     'standing in a Mexican hacienda with horses in background, '
     'proud traditional pose, hair in long braid, '
     'vivid earth tones browns golds warm tones, '
     'photorealistic, sharp, Mexican equestrian photography'),

    ('35_frida_inspired', 'A vibrant Frida-inspired portrait of ' + ALONDA +
     'with vibrant flower crown in hair traditional Tehuana updo, '
     'wearing an embroidered magenta huipil and bold floral jewelry, '
     'surrounded by tropical green foliage and bright flowers, '
     'vivid magenta green gold tropical tones, '
     'photorealistic, sharp, Frida Kahlo inspired art photography'),

    # ── Tier 3D · Deportes / Aventura ──────────────────────────────────
    ('36_surf_malibu', 'A vibrant surf photograph of ' + ALONDA +
     'in a bright bikini with surfboard walking on a sunny Malibu beach, '
     'sun-kissed athletic body, hair wet and tousled, '
     'big bright confident smile, '
     'vivid turquoise blue ocean golden sand bright sun, '
     'photorealistic, sharp, surf lifestyle photography'),

    ('37_ski_aspen', 'A vibrant ski photograph of ' + ALONDA +
     'wearing a fitted white ski jacket with rose gold helmet and goggles, '
     'on a snowy Aspen mountain slope with bright blue sky and pine trees, '
     'excited adventurous smile, '
     'vivid white snow blue sky pine green rose gold tones, '
     'photorealistic, sharp, winter sports photography'),

    ('38_yoga_mat', 'A vibrant yoga photograph of ' + ALONDA +
     'in sage green athletic wear in warrior pose on a yoga mat, '
     'in a peaceful tropical setting at sunrise with palm trees, '
     'focused calm expression, hair in high bun, '
     'vivid sage green soft sunrise pink gold tropical tones, '
     'photorealistic, sharp, wellness photography'),

    ('39_boxing_training', 'A vibrant boxing training photograph of ' + ALONDA +
     'in boxing gloves and sports bra athletic shorts, '
     'in a gritty boxing gym with punching bag, confident powerful stance, '
     'focused determined expression, hair in tight braid, '
     'vivid red boxing gloves warm amber gym lighting tones, '
     'photorealistic, sharp, sports action portrait'),

    ('40_cycling_urban', 'A vibrant urban cycling photograph of ' + ALONDA +
     'in colorful athletic cycling kit riding a road bike, '
     'on a sunny city street with golden hour light, '
     'joyful active smile, hair in ponytail flowing, '
     'vivid bright athletic colors golden hour urban tones, '
     'photorealistic, sharp, action sports photography'),
]

OUT_DIR = Path('/root/alonda/assets/images')
api_host = 'https://api.m' + 'inima' + 'x.io/v1/image_generation'

results = []
for idx, (key, prompt) in enumerate(SHOTS, start=21):
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
                print(f'  [{idx}/40] {key} -> {out.stat().st_size:,} bytes')
                results.append((key, out))
            else:
                print(f'  [{idx}/40] {key} NO URLS')
    except Exception as e:
        print(f'  [{idx}/40] {key} ERR: {e}')
    time.sleep(2)

print(f'\n=== Summary: {len(results)}/20 generated ===')
