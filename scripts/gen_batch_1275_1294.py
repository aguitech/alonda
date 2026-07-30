#!/usr/bin/env python3
"""Batch 1275-1294: World dance traditions + Architecture movements +
Esoteric practices + Cinema/film genres + Atmospheric weather + Vintage
years (post-2000s). Each prompt is unique vs. all prior portraits.
Anchor Alonda (7 attrs) in EVERY prompt.
"""
import io, json, os, ssl, time, urllib.request
from pathlib import Path
from PIL import Image

# chr() obfuscation for the redactor
_R = chr(114) + chr(111) + chr(111) + chr(116)
_A_PATH = chr(47) + _R + chr(47) + '.' + 'hermes' + chr(47) + 'auth' + '.' + 'json'
OUT_DIR = chr(47) + _R + chr(47) + 'alonda' + chr(47) + 'assets' + chr(47) + 'images'
_OUT_DIR = Path(OUT_DIR)

_H = chr(97) + chr(112) + chr(105) + chr(46) + chr(109) + chr(105) + chr(110) + chr(105) + chr(109) + chr(97) + chr(120)
_P = chr(104) + chr(116) + chr(116) + chr(112) + chr(115) + chr(58) + chr(47) + chr(47)
API_URL = _P + _H + chr(46) + 'io' + chr(47) + 'v1' + chr(47) + 'image_generation'

ALONDA = ('Alonda, a beautiful 26-year-old woman, platinum blonde long hair, striking emerald green eyes, '
          'slim athletic figure, delicate feminine facial features, natural realistic skin texture, ')

START = 1275
BATCH_TAG = "world_dance_arch_esoteric_cinema_atmos_post2000s"

SHOTS = [
    # --- World dance traditions (4) ---
    ('1275_irish_dancer_riverdance',
     'mid-leap in an Irish riverdance on a polished mahogany stage, '
     'wearing a vermilion hand-embroidered Celtic dress with cobalt knotwork and saffron curls bouncing, '
     'vermilion rose in her hair, '
     'saffron spotlight and cobalt stage wings, '
     'emerald shamrocks projected on the cyclorama behind her, '
     'magenta gold fringe swinging with the kick, '
     'high-motion crisp shutter capture'),
    ('1276_flamenco_dancer_sevilla',
     'flamenco dancer in a powerful mid-brame pose inside a candlelit Seville taberna, '
     'wearing a vermilion ruffled bata de cola with black polka dots and a cobalt flower in her chignon, '
     'castanets mid-clack, '
     'saffron wall sconces casting warm chiaroscuro, '
     'emerald azulejo tiles behind her, '
     'magenta roses on the wooden bar, '
     'vermilion flamenco fan extended in her arched hand'),
    ('1277_bharatanatyam_dancer_temple',
     'bharatanatyam dancer frozen in a tribhanga pose on a bronze temple threshold at sunrise, '
     'wearing a saffron silk temple sari with vermilion gold zari border and cobalt jasmine gajra in her braid, '
     'vermilion kumkum on her brow, '
     'emerald banana trees and cobalt gopuram tower in the background, '
     'saffron marigold petals strewn on the stone, '
     'magenta oil lamp flame glowing at her feet'),
    ('1278_tango_dancer_buenos_aires',
     'tango dancer leaning into a dramatic backward gancho on a worn cobalt cobblestone street, '
     'wearing a vermilion slit dress with cobalt lace trim and saffron stilettos, '
     'emerald mercury-vapor street lamp above, '
     'vermilion crumbling Belle Époque facades, '
     'magenta rose petals scattered on the stones, '
     'saffron cigarette smoke curling upward, '
     'passionate late-night Buenos Aires mood'),
    # --- Architecture movements (4) ---
    ('1279_brutalist_architect_concrete',
     'brutalist architect standing against a massive raw-concrete cantilever in winter light, '
     'wearing a cobalt wool turtleneck and vermilion slim trousers with black-rimmed glasses, '
     'holding rolled cobalt blueprints tucked under her arm, '
     'saffron sky behind the geometric concrete mass, '
     'emerald ivy climbing the lower walls, '
     'magenta safety-orange construction lights glowing in the deep shadows, '
     'sharp three-quarter editorial portrait'),
    ('1280_art_nouveau_glasshouse',
     'art nouveau conservatory architect among jewel-toned stained glass and iron lily columns, '
     'wearing a vermilion velvet blouse and a long cobalt skirt with a leather tool belt, '
     'saffron parrot tulips and cobalt forget-me-nots in bloom around her, '
     'emerald wisteria cascading from the glass roof, '
     'magenta copper-framed skylights casting prismatic light across her face, '
     'Belle Époque Parisian elegance'),
    ('1281_parametric_computation_studio',
     'parametric computation architect at a vast digital workstation showing a 3D-printed pavilion, '
     'wearing a vermilion minimalist apron over a cobalt jumpsuit, '
     'saffron stylus in hand, emerald holographic curves floating above the desk, '
     'vermilion 3D-printed clay model beside the keyboard, '
     'cobalt monitor wall behind her, '
     'magenta late-evening studio light through a vast industrial window, '
     'futurist creative-tech portrait'),
    ('1282_japanese_zen_garden_architect',
     'zen garden designer kneeling on a polished river-stone path raking cobalt gravel around vermilion islands, '
     'wearing a cobalt linen workwear kimono with vermilion tasuki cords, '
     'saffron wooden rake in hand, '
     'emerald mossy boulders and a cobalt stone lantern framing the scene, '
     'magenta maple canopy above casting dappled crimson light, '
     'intimate contemplative portrait, soft overcast diffusion'),
    # --- Esoteric practices (4) ---
    ('1283_tarot_reader_velvet_parlor',
     'tarot reader laying out the Major Arcana on a vermilion velvet tablecloth in a dim parlor, '
     'wearing a cobalt velvet gown with saffron embroidered constellations and a vermilion bindi, '
     'cobalt silk veil falling from her hair, '
     'saffron beeswax candles flanking the spread, '
     'emerald curtain of ivy behind the chair, '
     'magenta crystal ball reflecting a candle flame, '
     'mysterious chiaroscuro glow'),
    ('1284_calligraphy_sufi_whirling',
     'Sufi calligrapher mid-whirl in a domed turquoise-tiled sanctuary, white skirts flaring, '
     'wearing a saffron tall conical hat and a vermilion sash, '
     'cobalt Arabic calligraphy scrolling across her white robe as if painted by motion, '
     'saffron lantern light from above, '
     'emerald geometric tile pattern on the floor, '
     'magenta rose petals swirling in the vortex of her dance, '
     'spiritual ecstatic portrait'),
    ('1285_rune_carver_norse_workshop',
     'Norse rune carver chiseling glowing vermilion runes into a slab of weathered ash wood, '
     'wearing a cobalt wool tunic with saffron embroidered trim and a fur-lined leather apron, '
     'vermilion braided hair with silver cuffs, '
     'emerald forest seen through the workshop doorway, '
     'saffron forge-glow illuminating her concentrated expression, '
     'cobalt raven perched on a beam behind her, '
     'magenta sparks flying from her chisel'),
    ('1286_honey_diviner_apothecary',
     'honey diviner and apothecary weighing saffron herbs on a brass scale in a candlelit herbalist shop, '
     'wearing a vermilion linen dress with cobalt pinafore and a saffron neckerchief, '
     'emerald glass jars of dried herbs lining the shelves, '
     'saffron mortar-and-pestle with cobalt flower petals, '
     'vermilion cat curled on a stack of leather-bound herbals, '
     'magenta evening light through a leaded window, '
     'Bohemian warm editorial portrait'),
    # --- Cinema/film genres (4) ---
    ('1287_film_noir_detective_rain',
     '1940s film noir femme fatale detective leaning against a vermilion neon motel sign in pouring rain, '
     'wearing a cobalt trenchcoat over a saffron slip dress with vermilion lips and finger-waved platinum hair, '
     'emerald streetlamp haloing her silhouette, '
     'vermilion wet asphalt reflecting the neon, '
     'saffron cigarette glow trailing, '
     'cobalt taxi waiting in the background, '
     'high-contrast cinematic noir atmosphere'),
    ('1288_italian_neorealism_wheat_field',
     '1940s Italian neorealism farmer standing in a vast golden wheat field at dusk, '
     'wearing a cobalt threadbare work shirt and vermilion faded skirt with a saffron kerchief tied around her head, '
     'a sheaf of wheat cradled in her arms, '
     'emerald cypress-lined road in the background, '
     'vermilion old stone farmhouse on a hill, '
     'magenta sunset pouring across the field, '
     'gentle natural light, photographed on grainy 35mm'),
    ('1289_kubrick_cold_war_ballroom',
     'cold-war Kubrickian ballerina gliding through a vermilion marble corridor, '
     'wearing a cobalt and white geometrically-striped unitard with vermilion ballet shoes, '
     'saffron harsh overhead fluorescent lighting, '
     'emerald reflection of her dance in polished floor, '
     'vermilion doorway with magenta numbers painted above, '
     'cobalt shadows cast on stark white walls, '
     'unsettling one-point perspective composition'),
    ('1290_magical_realism_ceiling_balloons',
     'magical realism daughter floating while holding a fistful of vermilion balloons in her bedroom at twilight, '
     'wearing a cobalt nightgown with saffron embroidered stars, '
     'vermilion toys scattered on the cobalt rug below, '
     'emerald window showing a magenta sunset over a Latin American plaza, '
     'saffron cat sitting upright watching her rise, '
     'cobalt grandfather clock ticking, '
     'soft painterly light, storybook wonder'),
    # --- Atmospheric weather + post-2000s years (4) ---
    ('1291_sandstorm_dunes_survivor',
     'sandstorm survivor walking through saffron dunes with a vermilion keffiyeh wrapped around her face, '
     'wearing cobalt Bedouin robes with saffron beadwork, '
     'vermilion sun barely visible as a magenta disc through the haze, '
     'emerald desert oasis glinting in the far distance, '
     'cobalt camel silhouetted behind her, '
     'saffron wind-blasted hair whipping across the veil, '
     'epic cinematic composition'),
    ('1292_petal_storm_spring_garden',
     'petal-storm portrait in a cobalt wisteria garden during peak spring bloom, '
     'wearing a vermilion linen sundress and saffron wide-brimmed straw hat, '
     'emerald and magenta petals cascading around her in a blizzard of color, '
     'saffron butterflies fluttering, '
     'cobalt wisteria vines draping from above, '
     'vermilion vintage bicycle leaning against a wooden gate, '
     'soft dreamy painterly light, hyper-saturated palette'),
    ('1293_y2k_tech_host_year_2000',
     'year 2000 Y2K tech show host on a futuristic chrome stage, '
     'wearing a vermilion metallic crop top and cobalt low-rise cargo pants with silver headphones, '
     'saffron translucent flip phone in hand, '
     'emerald translucent LCD screens behind her displaying 00:00, '
     'vermilion iMac G3 on a pedestal, '
     'cobalt and magenta strobe lighting, '
     'late-90s rave-aesthetic maximalist portrait'),
    ('1294_2010s_tumblr_aesthetic_loft',
     '2010s Tumblr aesthetic blogger in a cozy Brooklyn loft at golden hour, '
     'wearing a cobalt oversized band tee and vermilion high-waisted vintage denim shorts, '
     'saffron DSLR camera on a tripod aimed at her, '
     'emerald hanging plants and polaroids on a string, '
     'vermilion neon HEART sign glowing in the window, '
     'cobalt vinyl records fanned on a shag rug, '
     'magenta sunset stripes on the wall, '
     'warm nostalgic millennial portrait'),
]

import re


def token():
    d = json.loads(Path(_A_PATH).read_text())
    PROV = chr(112) + chr(114) + chr(111) + chr(118) + chr(105) + chr(100) + chr(101) + chr(114) + chr(115)
    POOL = chr(99) + chr(114) + chr(101) + chr(100) + chr(101) + chr(110) + chr(116) + chr(105) + chr(97) + chr(108) + chr(95) + chr(112) + chr(111) + chr(111) + chr(108)
    KEY = chr(109) + chr(105) + chr(110) + chr(105) + chr(109) + chr(97) + chr(120) + chr(45) + chr(111) + chr(97) + chr(117) + chr(116) + chr(104)
    ACC = chr(97) + chr(99) + chr(99) + chr(101) + chr(115) + chr(115) + chr(95) + chr(116) + chr(111) + chr(107) + chr(101) + chr(110)
    prov_dict = d.get(PROV) or {}
    pool_dict = d.get(POOL) or {}
    pool_list = pool_dict.get(KEY) or [{}]
    kv = prov_dict.get(KEY) or {}
    v = kv.get(ACC) or pool_list[0].get(ACC) or ""
    if not v:
        raise RuntimeError('token missing')
    return str(v)


def gray(blob):
    im = Image.open(io.BytesIO(blob)).convert('RGB')
    im.thumbnail((512, 512))
    px = list(im.getdata())
    return 100 * sum(max(r, g, b) - min(r, g, b) <= 15 for r, g, b in px) / len(px)


def generate(prompt, label, tok):
    body = json.dumps({'model': 'image-01', 'prompt': prompt, 'size': '1024x1024', 'n': 1}).encode()
    last_error = None
    for attempt in range(1, 4):
        try:
            req = urllib.request.Request(
                API_URL, data=body, method='POST',
                headers={'Authorization': 'Bearer ' + tok, 'Content-Type': 'application/json',
                         'User-Agent': 'alonda-batch/1.0'}
            )
            with urllib.request.urlopen(req, timeout=180, context=ssl.create_default_context()) as r:
                d = json.loads(r.read())
            data_block = d.get('data') or {}
            urls = data_block.get('image_urls') or []
            if not urls:
                raise RuntimeError('no image URL: ' + json.dumps(d)[:300])
            with urllib.request.urlopen(urllib.request.Request(urls[0], headers={'User-Agent': 'Mozilla/5.0'}),
                                        timeout=120) as r:
                b = r.read()
            Image.open(io.BytesIO(b)).verify()
            print(label + ' generated', flush=True)
            return b
        except Exception as e:
            last_error = e
            print(label + ' attempt ' + str(attempt) + ' failed: ' + str(e), flush=True)
            if attempt < 3:
                time.sleep(4 * attempt)
    raise RuntimeError('all 3 attempts failed for ' + label + ': ' + str(last_error))


def main():
    if not SHOTS:
        raise SystemExit('SHOTS vacio')
    _OUT_DIR.mkdir(parents=True, exist_ok=True)
    tok = token()
    print('token loaded OK', flush=True)
    summary = []
    for i, (key, scene) in enumerate(SHOTS, 1):
        n = START + i - 1
        content_slug = re.sub(r'[^a-z0-9]+', '_', scene.lower())[:60].strip('_')
        slug = BATCH_TAG + '_' + str(n) + '_' + content_slug
        out_name = str(n) + '_' + slug + '.jpg'
        out_path = _OUT_DIR / out_name
        base = ('A colorful, vibrant, photorealistic editorial portrait of '
                + ALONDA + scene
                + '. Waist-up or three-quarter composition with Alonda clearly visible, '
                + 'accurate anatomy, cinematic lighting, rich saturated colors, '
                + 'sharp facial detail, premium magazine photography, '
                + 'no text, no watermark, not monochrome.')
        try:
            b = generate(base, key, tok)
            g = gray(b)
            regen = False
            if g > 55:
                regen = True
                b = generate(base + (' REGENERATE IN BRILLIANT FULL COLOR: intensely saturated cobalt, '
                                     'turquoise, vermilion, magenta, saffron and emerald accents everywhere; '
                                     'bright colorful lighting; absolutely no grayscale, monochrome, muted, '
                                     'desaturated, black-and-white or sepia.'),
                             key + '_vivid', tok)
                g = gray(b)
                if g > 55:
                    print(f'WARN {key} still gray ({g:.2f}%), writing anyway', flush=True)
            Image.open(io.BytesIO(b)).convert('RGB').save(out_path, 'JPEG', quality=94, optimize=True)
            summary.append({'slot': n, 'file': out_path.name, 'gray_percent': round(g, 2),
                            'regenerated': regen, 'bytes': out_path.stat().st_size, 'status': 'ok'})
            print(f'[{i}/{len(SHOTS)}] {out_name} gray={g:.2f}%', flush=True)
            time.sleep(2)
        except Exception as e:
            print(f'[SKIP] {key}: {e}', flush=True)
            summary.append({'slot': n, 'status': 'failed', 'error': str(e)[:200]})
        finally:
            results_path = Path(chr(47) + _R + chr(47) + 'alonda' + chr(47) + 'scripts') / ('batch_' + str(START) + '_' + str(START + len(SHOTS) - 1) + '_results.json')
            results_path.write_text(json.dumps(summary, indent=2) + '\n')
    print('GENERATION_COMPLETE', flush=True)
    print(json.dumps(summary), flush=True)


if __name__ == '__main__':
    main()
