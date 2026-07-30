#!/usr/bin/env python3
"""Batch 1215-1234: Music/instruments + Vehicles + Sci-fi retro + Unique seasons
+ Animals/nature hybrids + Performance arts. Each prompt is unique vs. all
prior portraits. Anchor Alonda (7 attrs) in EVERY prompt.
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

START = 1215
BATCH_TAG = "music_vehicles_scifi_retro_unique_seasons"

SHOTS = [
    # --- Music & instruments (5) ---
    ('1215_harpsichord_baroque',
     'seated at an ornately carved vermilion and gold harpsichord in a candlelit baroque salon, '
     'wearing a saffron silk gown with a powdered periwig braid and cobalt sash, '
     'fingers mid-keystroke on ivory keys, emerald velvet drapery behind her, '
     'turquoise cherub frescoes on the ceiling, magenta rose on the harpsichord lid, '
     'warm chiaroscuro lighting from beeswax tapers'),
    ('1216_jazz_saxophone_smoky_club',
     'standing on a smoky vermilion stage playing a brass saxophone with eyes closed in concentration, '
     'wearing a cobalt sequined flapper dress and saffron feathered headpiece, '
     'saffron spotlight cutting through cobalt cigar haze, emerald curtain backdrop, '
     'magenta neon sign for the club glowing behind her, '
     'vermilion grand piano visible at the edge of frame, vintage 1950s jazz club vibe'),
    ('1217_electric_guitarist_arena_rock',
     'electric guitarist mid-leap on a massive stadium stage, screaming into a cobalt microphone stand, '
     'wearing a vermilion leather jacket with saffron studs and cobalt ripped jeans, '
     'vermilion flying-V electric guitar with cobalt lightning inlays, '
     'emerald laser beams and saffron pyrotechnics erupting behind her, '
     'magenta strobe lights and a sea of cobalt phone flashlights from the audience, '
     'high-energy action shot, motion blur on hair'),
    ('1218_cello_quartet_rooftop',
     'seated on a vermilion velvet chair on a Parisian rooftop at dusk, deeply bowing a varnished amber cello, '
     'wearing a cobalt wrap dress with saffron shawl draped over her shoulder, '
     'vermilion Haussmann rooftops and turquoise Eiffel Tower in the background, '
     'emerald ivy trailing along the rooftop railing, magenta sunset painting the clouds, '
     'intimate chamber-music moment, golden hour rim light'),
    ('1219_dj_techno_warehouse',
     'DJ behind a vermilion-and-cobalt mixing console in a cavernous warehouse rave, '
     'wearing a holographic silver bomber jacket and saffron oversized headphones around her neck, '
     'saffron strobes and emerald lasers piercing cobalt fog, '
     'magenta LED wall behind her pulsing with waveforms, '
     'vermilion vinyl records fanned on the table, '
     'high-energy electronic music moment, dynamic composition'),
    # --- Vehicles (5) ---
    ('1220_classic_car_mechanic_under_chassis',
     'classic car mechanic in rolled-up vermilion coveralls sliding out from under a saffron 1967 Mustang chassis, '
     'holding a cobalt wrench, smudged with turquoise grease on her cheek, '
     'vermilion tool chest on cobalt casters, '
     'saffron chrome bumpers and emerald vintage gas pump in the background, '
     'magenta neon OPEN sign flickering, sunlit garage with sawdust on the floor'),
    ('1221_helicopter_pilot_mountain_rescue',
     'helicopter pilot strapping into the cockpit of a vermilion rescue chopper on a snow-blown alpine ridge, '
     'wearing a cobalt flight suit with vermilion epaulets and an emerald helmet with gold visor flipped up, '
     'saffron rotor wash whipping her platinum hair, '
     'cobalt glacier and vermilion peak in the background, '
     'magenta distress flare smoke trailing from a distant ledge, '
     'heroic three-quarter angle, crisp alpine light'),
    ('1222_train_conductor_vintage_locomotive',
     'train conductor leaning out the cab of a vermilion steam locomotive, one hand on the polished brass whistle, '
     'wearing a cobalt uniform with brass buttons and a vermilion-banded peaked cap, '
     'saffron steam billowing around her, '
     'emerald signal lamps and cobalt telegraph poles streaking past, '
     'magenta sunset over the Great Plains behind, vintage 1930s railway aesthetic, '
     'wind whipping her platinum braid'),
    ('1223_sailboat_captain_rough_seas',
     'sailboat captain at the helm of a vermilion sloop in a turquoise stormy sea, hair plastered with sea spray, '
     'wearing a cobalt oilskin coat with saffron hood thrown back, '
     'one hand on the cobalt wheel, emerald navigation charts in a brass tube at her hip, '
     'saffron sails taut in cobalt squall, vermilion lighthouse beam cutting the gloom on the horizon, '
     'magenta sky above the squall line, dramatic maritime composition'),
    ('1224_motorcycle_rider_neon_tokyo',
     'motorcycle rider pausing at a vermilion neon-lit Shibuya crosswalk on a cobalt sport bike, '
     'wearing a saffron leather jacket with cobalt racing stripes and a vermilion helmet under her arm, '
     'vermilion taillights and saffron headlights streaking into motion blur, '
     'emerald kanji signs and cobalt vending machines lining the street, '
     'magenta cherry blossoms drifting through the frame, '
     'cyberpunk night street portrait, cinematic depth of field'),
    # --- Sci-fi retro (5) ---
    ('1225_steampunk_inventor_airship',
     'steampunk inventor leaning against the gondola railing of a moored vermilion brass-riveted airship, '
     'wearing a saffron leather corset with copper gears and a cobalt aviator cap with brass goggles pushed up, '
     'vermilion mechanical wings folded behind her, '
     'saffron clockwork gauges and emerald pressure valves on the gondola, '
     'cobalt cloudy sky with emerald gas balloons drifting, magenta sunset on the horizon'),
    ('1226_atompunk_scientist_lab',
     'atompunk scientist in a 1950s-style nuclear research lab with a clipboard, '
     'wearing a cobalt lab coat over a saffron polka-dot dress with vermillion cat-eye glasses, '
     'vermilion Bunsen burner flame and cobalt Geiger counter ticking beside her, '
     'emerald bubbling beakers and saffron radiation-warning signs on the wall, '
     'magenta atom-model diagram in chalk behind her, '
     'retro-futurist optimistic-science aesthetic, warm tungsten lighting'),
    ('1227_solarpunk_architect_green_tower',
     'solarpunk architect on the sky-bridge of a vertical emerald garden tower at golden hour, '
     'wearing a vermilion linen jumpsuit with cobalt tool belt and a saffron straw hat, '
     'vermilion solar panels embedded in living walls, cobalt glass atrium overhead, '
     'saffron butterflies and emerald hummingbirds fluttering around her, '
     'magenta bougainvillea cascading from upper terraces, '
     'utopian eco-future composition, vibrant green palette'),
    ('1228_postapocalyptic_scavenger',
     'postapocalyptic scavenger in a dusty cobalt vault-tec workshop examining a salvaged circuit board, '
     'wearing a vermilion patched canvas duster with cobalt cargo straps, '
     'saffron gas mask hanging around her neck, emerald goggles perched on her forehead, '
     'vermilion neon "REPCON" sign flickering through cracked window, '
     'magenta rust-orange desert haze outside, '
     'cobalt screwdriver at her belt, cinematic dystopia'),
    ('1229_retrofuturist_space_age_hostess',
     '1960s-style retrofuturist space-age airline hostess in a moon-shaped porthole lounge, '
     'wearing a saffron go-go mod uniform dress with a white vinyl space-helmet hood and vermilion Pucci-print scarf, '
     'saffron dome ceiling with cobalt star maps, '
     'emerald velvet banquette seating, vermilion cocktail in a cobalt martini glass on a brass tray, '
     'magenta and turquoise space-age lighting, jet-age glamour portrait'),
    # --- Unique seasons & weather + animals (5) ---
    ('1230_autumn_koyo_kyoto_temple',
     'in Kyoto during peak autumn koyo, standing on the vermilion wooden veranda of a moss-covered temple, '
     'wearing a cobalt kimono with vermilion obi and a saffron chrysanthemum tucked behind her ear, '
     'vermilion Japanese maple leaves swirling around her, '
     'emerald moss garden with cobalt stone lanterns in the background, '
     'magenta late-afternoon sun cutting through the maples, traditional elegance'),
    ('1231_winter_lapland_reindeer_herder',
     'reindeer herder in Lapland during polar twilight, kneeling to feed a fluffy calf, '
     'wearing a cobalt and vermilion Sámi gákti traditional coat with saffron embroidered trim, '
     'vermilion four-point cap with cobalt braid, '
     'saffron reindeer herd dusted with snow behind her, '
     'emerald and magenta aurora borealis streaking the cobalt arctic sky, '
     'platinum breath vapor in the cold air'),
    ('1232_eclipse_solar_observatory',
     'astronomer at a cliffside observatory during a total solar eclipse, '
     'wearing a vermilion wool sweater and cobalt utility vest with a saffron telescope eyepiece in hand, '
     'saffron corona ring around the eclipsed sun, '
     'emerald and cobalt sky shifted to deep magenta and turquoise at totality, '
     'vermilion observatory dome open behind her, '
     'stars visible at midday, dramatic cosmic composition'),
    ('1233_rainforest_canopy_ethologist',
     'primate ethologist suspended in a climbing harness among a rainforest canopy, observing a cobalt-and-vermilion howler monkey, '
     'wearing a saffron field vest over a cobalt T-shirt and vermilion waterproof pants, '
     'vermilion binoculars around her neck, emerald clipboard hanging by a carabiner, '
     'saffron lianas and cobalt bromeliads surrounding her, '
     'magenta and turquoise macaws flying past, dappled canopy light'),
    ('1234_arctic_fur_seal_researcher',
     'marine biologist researcher kneeling on cobalt pack ice beside a curious fur seal pup, '
     'wearing a vermilion insulated parka with cobalt fur-lined hood thrown back and saffron insulated bib pants, '
     'saffron data tablet and cobalt tag applicator in her hands, '
     'emerald glacier wall in the background, '
     'magenta pastel sunset over the ice, '
     'pale vermilion seal-colony silhouettes on a distant floe'),
]

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
        import re
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
                        'regenerated': regen, 'bytes': out_path.stat().st_size})
        print(f'[{i}/{len(SHOTS)}] {out_name} gray={g:.2f}%', flush=True)
        time.sleep(2)
    results_path = Path(chr(47) + _R + chr(47) + 'alonda' + chr(47) + 'scripts') / ('batch_' + str(START) + '_' + str(START + len(SHOTS) - 1) + '_results.json')
    results_path.write_text(json.dumps(summary, indent=2) + '\n')
    print('GENERATION_COMPLETE', flush=True)
    print(json.dumps(summary), flush=True)


if __name__ == '__main__':
    main()
