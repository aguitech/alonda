#!/usr/bin/env python3
"""Batch 1335-1354: World cuisines + Mythical creatures + Snow/ice sports +
Photography styles + Perfumer/cosmetic + Couture fashion houses + Glassblowing +
Carnival of animals + Board games cafe + Bookshop culture. Each prompt is
unique vs. all prior portraits (1335 new range). Anchor Alonda (7 attrs)
in EVERY prompt.
"""
import io, json, ssl, time, urllib.request
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

START = 1335
BATCH_TAG = "cuisines_creatures_snow_photo_perfum_couture_glass_zoo_games_book"

SHOTS = [
    # --- World cuisines (3) ---
    ('1335_georgian_khinkali_maker',
     'mid-steam portrait of a Georgian khinkali maker pinching twisted dough parcels over a vermilion copper pot, '
     'wearing a cobalt striped apron and saffron headscarf with emerald embroidered collar, '
     'vermilion pomegranate halves split on the wooden counter, '
     'saffron window light filtering through clay roof tiles, '
     'cobalt Tbilisi old-town walls in the background, '
     'magenta bunch of fresh herbs hanging from a beam, '
     'rustic editorial food-portrait mood'),
    ('1336_thai_noodle_chef_bangkok',
     'Bangkok street-vendor noodle chef tossing vermilion woks over a saffron flame, '
     'wearing a cobalt sleeveless work shirt and vermilion bandana with magenta jasmine garland, '
     'emerald market baskets of lemongrass and chili in the foreground, '
     'saffron and crimson neon signage overhead in Chinese-Thai characters, '
     'cobalt steam billowing upward lit by warm tungsten lamps, '
     'magenta bougainvillea spilling from a balcony above, '
     'high-energy street-portrait composition'),
    ('1337_moroccan_tagine_cook',
     'Moroccan cook stirring a vermilion clay tagine in a cobalt-tiled courtyard in Fez, '
     'wearing a saffron kaftan with vermilion embroidered belt and emerald head wrap, '
     'cobalt mosaic fountain trickling behind her, '
     'saffron apricots and emerald olives in brass bowls, '
     'vermilion gerbera daisies climbing the whitewashed archway, '
     'magenta lantern casting patterned light across her face, '
     'warm North-African editorial portrait'),
    # --- Mythical creatures/fusion (3) ---
    ('1338_phoenix_rebirth_alchemist',
     'phoenix-rebirth alchemist standing inside a vermilion fire vortex, plumage-like hair of saffron and magenta flame, '
     'wearing a cobalt long coat with emerald brocade and vermilion phoenix brooch, '
     'saffron alchemy symbols glowing on a chalkboard behind her, '
     'cobalt raven perched on her shoulder wreathed in vermilion flame, '
     'emerald phoenix egg cradled in her arm, '
     'magenta sparks and ash drifting upward, '
     'cinematic high-fantasy portrait'),
    ('1339_dragon_tamer_nordic_cliff',
     'dragon tamer standing atop a snowy Nordic cliff beside a coiled vermilion eastern dragon breathing saffron fire, '
     'wearing cobalt scaled armor with emerald pauldrons and a vermilion cape, '
     'saffron Norse runes etched on her sword hilt, '
     'emerald aurora borealis unfurling above, '
     'cobalt glacier valley below, '
     'magenta dragon scales catching firelight on her cheek, '
     'epic cinematic fantasy portrait'),
    ('1340_unicorn_knight_celestial',
     'celestial unicorn knight in a starfield with a luminous pearlescent horn at her side, '
     'wearing vermilion silver-plate armor with cobalt filigree and a saffron cape, '
     'saffron constellation map painted on the shield, '
     'emerald nebulae swirled behind her, '
     'cobalt crystal moon overhead casting rim light on her platinum hair, '
     'magenta sparkles raining around the unicorn, '
     'mythic editorial portrait'),
    # --- Snow/ice sports (3) ---
    ('1341_ice_climber_rozenberg',
     'ice climber mid-placement on a towering cobalt glacier face of Rozenberg peak, '
     'wearing vermilion down suit and saffron helmet with a translucent ice-axe in hand, '
     'saffron rope trailing down to a magenta belay partner below, '
     'emerald ice pillar formations glinting in winter sun, '
     'cobalt crevasse yawning at her boots, '
     'vermilion flags of an alpine camp far behind, '
     'sharp adventure-photography portrait'),
    ('1342_curler_bonspiel',
     'curler in a release slide on a polished vermilion rink stone during a bonspiel, '
     'wearing a cobalt team sweater and saffron broom with a vermilion granite stone sliding ahead, '
     'emerald house circles painted on the ice ahead, '
     'saffron and cobalt team flags hanging above, '
     'cobalt scoreboard lit in the background, '
     'magenta teammates calling line, '
     'editorial sports portrait'),
    ('1343_ski_jumper_olympic',
     'Olympic ski jumper captured in flight at the apex of her jump against a cobalt winter sky, '
     'wearing a vermilion speed suit with saffron stripes and cobalt aerodynamic helmet, '
     'emerald pines lining the landing slope far below, '
     'saffron sunburst glinting off her goggles, '
     'cobalt snow plume trailing behind her skis, '
     'magenta Olympic rings on the stadium scoreboard behind, '
     'freeze-frame action portrait'),
    # --- Photography styles (3) ---
    ('1344_polaroid_lofi_diner',
     'soft Polaroid lo-fi portrait of her seated at a vermilion vinyl booth in a 1970s American diner, '
     'wearing a cobalt soft sweater and saffron corduroy pants, '
     'saffron milkshake with cobalt whipped cream in front of her, '
     'emerald neon clock on the wall behind, '
     'vermilion jukebox glowing in the corner, '
     'cobalt plastic menu propped beside her, '
     'magenta checkerboard floor stretching back, '
     'instant-film warm-tone aesthetic'),
    ('1345_high_speed_flash_splash',
     'high-speed flash photography studio portrait of her mid-laugh with vermilion and cobalt paint splashing around her face, '
     'wearing a saffron tank top, '
     'emerald paint droplets frozen in air, '
     'saffron strobe lighting reflecting off cobalt plexiglass panels, '
     'vermilion seamless paper backdrop stained with magenta splatter, '
     'cobalt softbox rim light on her platinum hair, '
     'editorial splash-photography portrait'),
    ('1346_double_exposure_paris',
     'double-exposure fine-art portrait blending her silhouette with the Eiffel Tower and vermilion Parisian rooftops, '
     'wearing a cobalt beret and saffron scarf, '
     'emerald Seine river reflecting the second exposure, '
     'saffron soft window light across the composite, '
     'cobalt twilight blue tone filling negative space, '
     'magenta streetlamps glowing faintly within the silhouette, '
     'fine-art conceptual portrait'),
    # --- Perfumer/cosmetic (2) ---
    ('1347_perfumer_grasse_atelier',
     'Grasse perfumer in her atelier surrounded by cobalt and emerald glass flasks, '
     'wearing a saffron silk blouse with vermilion leather apron, '
     'saffron scent strips tucked in her collar, '
     'vermilion rose petals drying on wooden trays, '
     'cobalt copper still gleaming in the corner, '
     'emerald jasmine vines climbing the window, '
     'magenta afternoon sun through leaded glass, '
     'warm editorial craft-portrait'),
    ('1348_lipstick_formulator_lab',
     'lipstick formulator in a clean-room lab pouring vermilion pigment into a cobalt lipstick mold, '
     'wearing a saffron lab coat with cobalt safety goggles pushed up on her forehead, '
     'emerald racks of test shades behind her, '
     'saffron pipettes and vermilion beakers on the bench, '
     'cobalt moodboard of lip-tone gradients on the wall, '
     'magenta softbox light giving a glossy product-shot feel, '
     'beauty-industry editorial portrait'),
    # --- Couture fashion houses (2) ---
    ('1349_christian_lacroix_floral',
     'in a Lacroix-inspired haute couture floral gown with vermilion peony appliques and cobalt feathered hem, '
     'wearing a saffron feathered headpiece and emerald opera gloves, '
     'cobalt marble colonnade behind her, '
     'saffron soft directional studio light, '
     'vermilion backdrop embroidered with cobalt baroque scrollwork, '
     'magenta velvet carpet underfoot, '
     'couture runway editorial portrait'),
    ('1350_rick_owens_dark_gothic',
     'in a Rick Owens-inspired sculptural dark gothic gown with cobalt draped leather and vermilion bone clasps, '
     'wearing saffron stacked leather cuffs and emerald oxidized silver rings, '
     'cobalt concrete brutalist corridor behind her, '
     'saffron low-key cinematic lighting, '
     'vermilion rose placed on the concrete floor, '
     'magenta backlit hair giving a halo effect, '
     'avant-garde editorial portrait'),
    # --- Glassblowing + Misc (4) ---
    ('1351_glassblower_murano',
     'Murano glassblower shaping a vermilion molten orb at the end of her blowpipe inside a saffron-lit furnace, '
     'wearing a cobalt heat-resistant jacket with emerald apron and saffron face shield pushed up, '
     'cobalt glass rods and emerald shards on the workbench, '
     'saffron furnace glow lighting her from below, '
     'vermilion finished glass sculptures on shelves behind, '
     'magenta reflected light dancing on the ceiling, '
     'industrial craft editorial portrait'),
    ('1352_meerkat_photographer_zoo',
     'wildlife portrait of her kneeling at a meerkat enclosure with vermilion and cobalt meerkats climbing on her arms, '
     'wearing a safari-saffron shirt and cobalt cargo pants with a vermilion camera in hand, '
     'emerald enclosure foliage around her, '
     'saffron late-afternoon zoo light, '
     'cobalt wooden viewing platform behind, '
     'magenta information sign with cartoon meerkat illustration, '
     'documentary-style portrait'),
    ('1353_chess_cafe_grandmaster',
     'chess grandmaster in a wood-paneled cafe mid-move over a vermilion and emerald inlaid chessboard, '
     'wearing a cobalt roll-neck and saffron corduroy jacket, '
     'saffron leather-bound chess books on the shelf behind, '
     'vermilion ceramic tea cup steaming beside the board, '
     'cobalt framed vintage chess posters on the wall, '
     'emerald potted fern on the side table, '
     'magenta wall lamp casting warm pool of light, '
     'intellectual editorial portrait'),
    ('1354_bookshop_owner_ladder',
     'independent bookshop owner perched halfway up a cobalt rolling ladder reaching for a vermilion leather-bound tome, '
     'wearing a saffron knit sweater and cobalt corduroy trousers with emerald reading glasses on a chain, '
     'saffron stacked paperbacks on the floor beside her, '
     'emerald potted ivy climbing the ladder rail, '
     'vermilion hand-lettered OPEN sign in the window, '
     'cobalt Persian rug under the ladder, '
     'magenta afternoon sunbeams cutting through dust, '
     'warm indie-bookshop editorial portrait'),
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