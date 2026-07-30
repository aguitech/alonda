#!/usr/bin/env python3
import io, json, ssl, time, urllib.request
from pathlib import Path
from PIL import Image

AUTH_PATH = Path('/') / 'root' / '.hermes' / 'auth.json'
OUT_DIR = Path('/root/alonda/assets/images')
API_URL = 'https://api.' + 'minimax' + '.io/v1/image_generation'
ALONDA = ('Alonda, a beautiful 26-year-old woman, platinum blonde long hair, striking emerald green eyes, '
          'slim athletic figure, delicate feminine facial features, natural realistic skin texture, ')
SHOTS = [
    ('581_dark_academia', 'dark academia scholar in a candlelit Oxford reading room at dusk, ink-black turtleneck, oxblood tweed blazer, forest-green book stack, brass reading lamp, copper fountain pen, gothic-arched window, chiaroscuro literary portrait'),
    ('582_cottagecore', 'cottagecore baker in a wildflower-filled English countryside kitchen, sage linen apron over butter-yellow sundress, cobalt ceramic mixing bowl, terracotta sourdough loaves, ruby strawberries and emerald herbs, sunlit pastoral portrait'),
    ('583_regencycore', 'regencycore debutante in an English drawing room of a Bath townhouse, pearl-white empire-waist gown with powder-blue sash, ivory lace gloves, turquoise tiarra, ruby velvet curtains and emerald parquet, Bridgerton-era portrait'),
    ('584_coastal_grandmother', 'coastal grandmother aesthetic in a weathered Nantucket beach cottage, ivory cashmere wrap over washed-linen shirt, ocean-blue wide-leg trousers, sage jute basket, turquoise hydrangeas, magenta beach roses and emerald sea, serene coastal portrait'),
    ('585_old_money', 'old money heiress at a Lake Como villa breakfast table, pristine ivory poplin shirt, pearl studs, ruby silk headband, emerald lake, terracotta citrus, cobalt glassware and saffron morning light, refined old-money portrait'),
    ('586_fairycore', 'fairycore wood-nymph in a mossy Pacific Northwest cedar grove at twilight, saffron mushroom-cap dress with emerald leaf embroidery, turquoise moth-wing shawl, ruby foxglove, cobalt fairy-lights, magical forest portrait'),
    ('587_goblincore', 'goblincore forager in a foggy autumn New England forest, mottled moss-green oversized sweater, terracotta corduroys, cobalt mushroom-print tote, turquoise beetle jewelry, ruby maple leaves and emerald ferns, earthy whimsical portrait'),
    ('588_royalcore', 'royalcore portrait at a Versailles-style gilded ballroom, sapphire velvet gown with ermine white stole, ruby tiara, emerald parquet floor, turquoise ormolu chandelier, saffron candlelight and ivory marble, regal portrait'),
    ('589_indie_sleaze', 'indie sleaze 2008 Tumblr fashion muse in a gritty downtown Brooklyn loft, cherry-red mini dress over black band tee, cobalt glitter eyeliner, magenta digital camera, turquoise exposed brick, saffron strobe lights, Y2K nostalgia portrait'),
    ('590_vsco_girl', 'vsco girl at a Malibu beach boardwalk at golden hour, sage scrunchie in hair, pearly shell necklaces, terracotta oversized tee, cobalt hydro flask, turquoise roller skates, ruby puka shell anklet and emerald surf, casual beach portrait'),
    ('591_diwali_festival', 'Diwali festival celebrant lighting diyas on a Mumbai rooftop terrace at dusk, saffron silk lehenga with magenta dupatta, turquoise jhumka earrings, emerald rangoli patterns, ruby sparkler glow and cobalt night sky, festive Indian portrait'),
    ('592_loy_krathong', 'Loy Krathong festival in Chiang Mai floating a banana-leaf krathong at twilight, cobalt Thai silk dress with saffron sash, ruby lotus offering, turquoise candlelit river, emerald sky-lanterns rising and magenta reflections, Thai festival portrait'),
    ('593_boryeong_mud', 'Boryeong mud festival reveler mid-laugh at the South Korean coastline, electric coral bikini under translucent cobalt raincoat, turquoise mud splatter on cheek, saffron beach umbrellas, emerald sea and magenta sun, joyful summer portrait'),
    ('594_diwali_dance', 'Kathak classical dancer mid-spin at a Jaipur palace courtyard during Diwali, crimson and gold ghagra with mirror work, turquoise anklet ghungroo, emerald marble arches, saffron marigold garlands and ruby diya flames, Indian dance portrait'),
    ('595_queen_bee_orchard', 'queen bee orchard keeper in a Provence cherry orchard in late spring, sage linen beekeeper suit with vermilion bandana, turquoise frame hives, saffron cherry blossoms, emerald foliage and ruby cherries, apiarist portrait'),
    ('596_falconer_steppe', 'Kazakh eagle huntress on horseback across an Altai steppe at dawn, crimson wool chapan coat, turquoise silk headscarf, golden eagle perched on leather-gloved hand, saffron grassland and cobalt mountains, nomadic hunting portrait'),
    ('597_amazona_showjumping', 'international showjumping rider mid-jump over an emerald oxer in a Spanish sunshine tour arena, navy tailcoat with saffron stock tie, vermilion saddle pad, turquoise stadium banners, ruby jump rails and cobalt sky, equestrian portrait'),
    ('598_ethologist_jaguar', 'Amazonian ethologist tracking a melanistic jaguar at dusk in a tropical river bend, olive field uniform with saffron bandana, turquoise telemetry antenna, emerald lianas, ruby macaws and cobalt twilight, wildlife research portrait'),
    ('599_orangutan_caretaker', 'Bornean orangutan caretaker at a Sepilok rehabilitation centre, sage ranger shirt with cobalt patches, terracotta rubber boots, turquoise palm-leaf shelter, a young ginger orangutan on her shoulder, emerald rainforest and ruby flowers, conservation portrait'),
    ('600_kyoto_tea_master', 'Kyoto tea master preparing matcha in a golden autumn tea garden, charcoal-grey kimono with persimmon-orange obi, emerald bamboo whisk, saffron momiji maples overhead, cobalt stone lantern and ruby lacquer tea caddy, refined Japanese portrait'),
]

def token():
    d = json.loads(AUTH_PATH.read_text())
    v = d.get('providers', {}).get('minimax-oauth')
    if isinstance(v, dict): v = v.get('access_token')
    if not v:
        v = d.get('credential_pool', {}).get('minimax-oauth', [{}])[0]
        v = v.get('access_token') if isinstance(v, dict) else v
    if not v: raise RuntimeError('token missing')
    return v

def gray(blob):
    im = Image.open(io.BytesIO(blob)).convert('RGB')
    im.thumbnail((512, 512))
    px = list(im.getdata())
    return 100 * sum(max(r, g, b) - min(r, g, b) <= 15 for r, g, b in px) / len(px)

def generate(prompt, label, tok):
    body = json.dumps({'model': 'image-01', 'prompt': prompt, 'size': '1024x1024', 'n': 1}).encode()
    last = None
    for attempt in range(1, 4):
        try:
            req = urllib.request.Request(API_URL, data=body, method='POST',
                                          headers={'Authorization': 'Bearer ' + tok,
                                                   'Content-Type': 'application/json',
                                                   'User-Agent': 'alonda-tier30/1.0'})
            with urllib.request.urlopen(req, timeout=180, context=ssl.create_default_context()) as r:
                d = json.loads(r.read())
            urls = d.get('data', {}).get('image_urls', [])
            if not urls: raise RuntimeError('no image URL: ' + json.dumps(d)[:300])
            with urllib.request.urlopen(urllib.request.Request(urls[0], headers={'User-Agent': 'Mozilla/5.0'}), timeout=120) as r:
                b = r.read()
            Image.open(io.BytesIO(b)).verify()
            print(label + ' generated', flush=True)
            return b
        except Exception as e:
            last = e
            print(label + ' attempt ' + str(attempt) + ' failed: ' + str(e), flush=True)
            if attempt < 3: time.sleep(4 * attempt)
    raise RuntimeError(str(last))

OUT_DIR.mkdir(parents=True, exist_ok=True)
tok = token()
summary = []
for i, (key, scene) in enumerate(SHOTS, 1):
    base = ('A colorful, vibrant, photorealistic editorial portrait of ' + ALONDA + scene +
            '. Waist-up or three-quarter composition with Alonda clearly visible, accurate anatomy, '
            'cinematic lighting, rich saturated colors, sharp facial detail, premium magazine photography, '
            'no text, no watermark, not monochrome.')
    b = generate(base, key, tok)
    g = gray(b)
    regen = False
    if g > 55:
        regen = True
        b = generate(base + ' REGENERATE IN BRILLIANT FULL COLOR: intensely saturated cobalt, turquoise, vermilion, magenta, saffron and emerald accents everywhere; bright colorful lighting; absolutely no grayscale, monochrome, muted, desaturated, black-and-white or sepia.',
                     key + ' vivid', tok)
        g = gray(b)
        if g > 55: raise RuntimeError(key + ' remains too gray: ' + str(g))
    out = OUT_DIR / (key + '.jpg')
    Image.open(io.BytesIO(b)).convert('RGB').save(out, 'JPEG', quality=94, optimize=True)
    summary.append({'file': out.name, 'gray_percent': round(g, 2), 'regenerated': regen, 'bytes': out.stat().st_size})
    print(f'[{i}/20] {key} gray={g:.2f}%', flush=True)
    time.sleep(2)
Path('/root/alonda/scripts/tier30_581_600_results.json').write_text(json.dumps(summary, indent=2) + '\n')
print('COMPLETE ' + json.dumps(summary), flush=True)
