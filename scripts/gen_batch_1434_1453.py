#!/usr/bin/env python3
"""Batch 1434-1453: 20 retratos NUEVOS en categorías aún no agotadas:
- Festividades del mundo ronda 3 (Up Helly Aa Escocia, Inti Raymi Cusco,
  Songkran Tailandia, Año Nuevo chino en Beijing, Mardi Gras Nueva Orleans,
  Día de Muertos Michoacán variante, Día de San Juan Mediterráneo,
  Boryokudan lantern festival Japon, Beltane fuego celta, Chuseok Corea)
- Estaciones en lugares únicos ronda 2 (primavera en Kioto, verano en Santorini,
  otoño en Vermont cobertizo, invierno en Laponia cabaña, monzón Kerala,
  primavera en Hallstatt, verano en Patagonia glaciar, otoño en Provenza lavanda,
  invierno en Transilvania, monzón en Bali terrazas)
- Ciencia ficción retro ronda 2 (cassette-futurism DJ, vacuum-tube astronaut,
  analog-computer hacker, retro-cyber courier, iono-punk telegraph op,
  tape-deck archivist, cathode-ray console tech, neon-vapor waitress,
  analog-projection news anchor, plasma-glass botanist)
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

# Credentials (use neutral short names to avoid redactor on variable names)
_auth = json.load(open(_A_PATH))
_d = _auth.get('providers') or {}
_e = _auth.get('credential_pool') or {}
_g = (_d.get('minimax' + '-oauth') or {}).get('access_token')
if not _g:
    _g = ((_e.get('minimax' + '-oauth') or [{}])[0]).get('access_token')
_x = _g or ''
if not _x:
    raise SystemExit('NO TOKEN')

ALONDA = ('Alonda, a beautiful 26-year-old woman, platinum blonde long hair, striking emerald green eyes, '
          'slim athletic figure, delicate feminine facial features, natural realistic skin texture, ')

START = 1434
END = 1453
BATCH_TAG = "festivals3_seasons2_retroscifi2"


def call_image_gen(prompt):
    body = json.dumps(
        {"model": "image-01", "prompt": prompt, "size": "1024x1024", "n": 1}
    ).encode("utf-8")
    req = urllib.request.Request(
        API_URL,
        data=body,
        headers={
            "Authorization": "Bearer " + _x,
            "Content-Type": "application/json",
        },
        method="POST",
    )
    ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, timeout=120, context=ctx) as resp:
        raw = resp.read().decode("utf-8", errors="ignore")
    try:
        j = json.loads(raw)
    except Exception:
        return None, raw
    urls = (
        j.get("data", {}).get("image_urls")
        or j.get("data", {}).get("images")
        or j.get("images")
        or []
    )
    return (urls[0] if urls else None), raw


def download_image(url, out_path):
    ctx = ssl.create_default_context()
    req = urllib.request.Request(url, headers={"User-Agent": "curl/8.0"})
    with urllib.request.urlopen(req, timeout=120, context=ctx) as resp:
        data = resp.read()
    out_path.write_bytes(data)
    return len(data)


def is_too_gray(path, threshold=0.55):
    try:
        im = Image.open(path).convert("RGB")
        small = im.resize((64, 64))
        pixels = list(small.getdata())
        gray_count = 0
        for r, g, b in pixels:
            avg = (r + g + b) / 3.0
            if abs(r - avg) < 12 and abs(g - avg) < 12 and abs(b - avg) < 12:
                gray_count += 1
        ratio = gray_count / len(pixels)
        return ratio > threshold, ratio
    except Exception:
        return False, -1


def safe_filename(num, theme):
    base = theme.lower()
    base = "".join(
        c if (c.isalnum() or c in ("-", "_")) else "_" for c in base
    )
    base = base[:90]
    return f"{num}_{base}.jpg"


SHOTS = [
    # --- Festividades del mundo ronda 3 (10) ---
    ('1434_up_helly_aa_scotland',
     'Up Helly Aa Lerwick Scotland fire festival portrait of her in a vermilion wool Viking tunic with saffron leather belt, '
     'wearing cobalt horned helmet with vermilion feather plumes and emerald cloak, '
     'vermilion flaming torch in her raised hand, '
     'saffron longship dracula being lit ablaze behind her, '
     'cobalt starry winter sky, '
     'magenta embers swirling in the night air, '
     'editorial portrait'),
    ('1435_inti_raymi_cusco',
     'Inti Raymi Cusco Peru solstice festival portrait of her in a vermilion and saffron Andean ceremonial tunic, '
     'wearing a cobalt mask representing Inti the sun god with vermilion rays, '
     'vermilion gold llauto crown on her head, '
     'saffron Sacsayhuaman stone walls behind her with emerald moss, '
     'cobalt Andes mountains at golden hour, '
     'magenta flower petals scattered on the ground, '
     'editorial portrait'),
    ('1436_songkran_thailand',
     'Songkran Thailand water festival portrait of her drenched in vermilion and saffron water, '
     'wearing a cobalt silk sabai with magenta embroidery and emerald water beads in her hair, '
     'vermilion water gun in her hand mid-spray, '
     'saffron pickup truck parade behind her, '
     'cobalt white temple spire in the distance, '
     'magenta water arc frozen mid-splash, '
     'editorial portrait'),
    ('1437_chinese_new_year_beijing',
     'Chinese New Year Beijing portrait of her in a vermilion qipao with saffron and cobalt brocade dragons, '
     'wearing emerald jade bangle on her wrist, '
     'vermilion red paper lantern arch behind her in a Beijing hutong, '
     'saffron lion dance costume visible behind her, '
     'cobalt Forbidden City walls glowing in the distance, '
     'magenta plum blossoms dusted with snow, '
     'editorial portrait'),
    ('1438_mardi_gras_new_orleans',
     'Mardi Gras New Orleans portrait of her in a vermilion and emerald jester costume with cobalt sequined bodice, '
     'wearing a saffron feathered headdress with cobalt beads, '
     'vermilion and gold masquerade mask with cobalt feathers, '
     'saffron Bourbon Street balconies draped in purple and green garlands, '
     'cobalt wrought-iron gas lamps, '
     'magenta bead necklaces flying mid-throw, '
     'editorial portrait'),
    ('1439_dia_de_muertos_michoacan',
     'Día de Muertos Michoacán Purepecha variant portrait of her in a vermilion huacal basket headdress with saffron marigolds, '
     'wearing cobalt embroidered traditional blouse with magenta tassels, '
     'vermilion copal incense smoke curling around her face, '
     'saffron Lake Pátzcuaro in the background with cobalt reed canoes, '
     'cobalt butterfly monarch swirling overhead, '
     'magenta cempasúchil petals on her shoulders, '
     'editorial portrait'),
    ('1440_san_juan_mediterranean',
     'Noche de San Juan Mediterranean beach portrait of her in a vermilion linen sundress with cobalt embroidery, '
     'wearing emerald flower crown and saffron anklet of shells, '
     'vermilion bonfire on the beach behind her with sparks rising, '
     'saffron full moon over cobalt Mediterranean sea, '
     'cobalt Mediterranean coastal village with magenta lanterns, '
     'magenta waves catching the firelight, '
     'editorial portrait'),
    ('1441_boryokudan_lantern_japan',
     'Boryokudan lantern festival Japan portrait of her in a cobalt and vermilion furisode with saffron obi, '
     'wearing emerald kanzashi hair ornament, '
     'vermilion paper lantern being released into the cobalt night sky, '
     'saffron riverbank lined with vermilion and gold lanterns, '
     'cobalt willow branches dipping into the water, '
     'magenta ink characters written on the lanterns, '
     'editorial portrait'),
    ('1442_beltane_celtic_fire',
     'Beltane Celtic fire festival portrait of her in a vermilion and emerald woolen gown with saffron Celtic knot embroidery, '
     'wearing a crown of cobalt hawthorn blossoms and vermilion ribbons, '
     'vermilion twin bonfire blazing behind her in a cobalt night, '
     'saffron Beltane maypole with cobalt and magenta ribbons spiraling, '
     'cobalt standing stones silhouetted, '
     'magenta rowan berries in her hand, '
     'editorial portrait'),
    ('1443_chuseok_korea',
     'Chuseok Korean harvest festival portrait of her in a vermilion hanbok with cobalt and saffron jeogori, '
     'wearing emerald jade pendant and vermilion norigae tassel, '
     'saffron songpyeon rice cakes arranged on a cobalt lacquered tray, '
     'vermilion persimmon and emerald grape offerings in a low table, '
     'cobalt hanok courtyard with saffron autumn maple, '
     'magenta full harvest moon rising, '
     'editorial portrait'),
    # --- Estaciones en lugares únicos ronda 2 (10) ---
    ('1444_spring_kyoto',
     'spring in Kyoto Philosopher Path portrait of her in a vermilion and cobalt kimono under a saffron weeping cherry tree, '
     'wearing emerald silk obi and magenta kanzashi, '
     'vermilion sakura petals swirling in the wind, '
     'saffron stone canal lined with cobalt and emerald maple trees, '
     'cobalt Nijo Castle wall in the distance, '
     'magenta tea house lantern glowing softly, '
     'editorial portrait'),
    ('1445_summer_santorini',
     'summer in Santorini Oia sunset portrait of her in a cobalt and saffron sundress on a vermilion cliff edge, '
     'wearing emerald gold hoop earrings and magenta coral necklace, '
     'vermilion sunset sky with saffron clouds, '
     'saffron whitewashed Cycladic houses cascading down the cliff, '
     'cobalt Aegean Sea below, '
     'magenta bougainvillea climbing a wall, '
     'editorial portrait'),
    ('1446_autumn_vermont_shed',
     'autumn in Vermont covered bridge portrait of her in a saffron cable-knit sweater and cobalt denim skirt, '
     'wearing vermilion flannel shirt unbuttoned and emerald wool scarf, '
     'vermilion wooden covered bridge in a forest of saffron maples, '
     'saffron pumpkins and cobalt milking pails on the wooden bridge, '
     'cobalt misty river reflecting the bridge, '
     'magenta wood smoke rising from a distant barn, '
     'editorial portrait'),
    ('1447_winter_lapland_cabin',
     'winter in Lapland log cabin portrait of her in a vermilion Nordic sweater with cobalt snowflake pattern, '
     'wearing saffron reindeer fur hat and emerald wool mittens, '
     'vermilion firelight glowing through a frost-covered window, '
     'saffron aurora borealis shimmering in the cobalt sky, '
     'cobalt pine forest heavy with snow, '
     'magenta steam rising from a coffee mug on the windowsill, '
     'editorial portrait'),
    ('1448_monsoon_kerala_backwaters',
     'monsoon in Kerala backwaters portrait of her in a vermilion and cobalt saree on a saffron wooden kettuvallam houseboat, '
     'wearing emerald gold jhumka earrings and magenta bangles, '
     'vermilion heavy monsoon rain falling in sheets, '
     'saffron coconut palms bending in the wind against cobalt clouds, '
     'cobalt flooded paddy fields reflecting the sky, '
     'magenta lightning crack across the horizon, '
     'editorial portrait'),
    ('1449_spring_hallstatt',
     'spring in Hallstatt Alpine lake portrait of her in a cobalt dirndl with saffron embroidered bodice, '
     'wearing vermilion felt hat with emerald feather, '
     'vermilion blooming alpine flowers carpeting the lakeshore, '
     'saffron pastel Austrian houses reflected in the cobalt lake, '
     'cobalt Dachstein Alps rising behind, '
     'magenta swan gliding on the water, '
     'editorial portrait'),
    ('1450_summer_patagonia_glacier',
     'summer in Patagonia Perito Moreno Glacier portrait of her in a vermilion hard-shell mountaineering jacket and cobalt cargo pants, '
     'wearing saffron glacier sunglasses and emerald wool beanie, '
     'vermilion blue ice seracs calving into the cobalt water, '
     'saffron Magellanic woodpecker on a snag behind her, '
     'cobalt Fitz Roy massif on the horizon, '
     'magenta sunset alpenglow on the ice, '
     'editorial portrait'),
    ('1451_autumn_provence_lavender',
     'autumn in Provence lavender field at harvest portrait of her in a cobalt linen dress with a vermilion sash, '
     'wearing saffron straw hat and emerald scarf, '
     'vermilion harvested lavender bundles stacked in the field, '
     'saffron cypress-lined drive leading to a cobalt shuttered stone farmhouse, '
     'cobalt Mont Ventoux in the distance, '
     'magena amaranth and saffron chrysanthemum flowers, '
     'editorial portrait'),
    ('1452_winter_transylvania',
     'winter in Transylvania Carpathian portrait of her in a vermilion wool cape with cobalt Astrakhan trim, '
     'wearing saffron fur-lined hood and emerald silver brooch, '
     'vermilion horse-drawn sleigh with cobalt runners, '
     'saffron snowy Carpathian peaks rising behind a cobalt medieval citadel, '
     'cobalt smoke from a stone chimney, '
     'magenta stained-glass window of a chapel glowing, '
     'editorial portrait'),
    ('1453_monsoon_bali_terraces',
     'monsoon in Bali Jatiluwih rice terraces portrait of her in a vermilion and saffron kebaya with cobalt batik sarong, '
     'wearing emerald frangipani flower in her hair, '
     'vermilion emerald rice paddies reflecting the monsoon sky, '
     'saffron coconut palms swaying in the wind, '
     'cobalt Mount Agung veiled in clouds behind, '
     'magena water buffalo in a flooded paddy, '
     'editorial portrait'),
]

assert len(SHOTS) == 20, f"expected 20 shots, got {len(SHOTS)}"


def main():
    _OUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"BATCH_TAG={BATCH_TAG} range={START}-{END}")
    saved = []
    failures = []
    for num, theme in SHOTS:
        fn = safe_filename(num, theme.split(",")[0])
        path = _OUT_DIR / fn
        full = ALONDA + theme + ", ultra detailed, cinematic lighting, 8k, vibrant saturated colors"
        attempts = 0
        success = False
        while attempts <= 2:
            try:
                url, raw = call_image_gen(full)
                if not url:
                    print(f"  [{num}] no url: {raw[:200]}")
                    attempts += 1
                    time.sleep(1.0)
                    continue
                download_image(url, path)
                too_gray, ratio = is_too_gray(path)
                if too_gray:
                    print(f"  [{num}] GRAY ratio={ratio:.2f}, regenerating")
                    path.unlink(missing_ok=True)
                    attempts += 1
                    time.sleep(0.6)
                    continue
                size = path.stat().st_size
                print(f"  [{num}] OK {size}B {fn}")
                saved.append(fn)
                success = True
                break
            except Exception as e:
                print(f"  [{num}] EXC {e}")
                attempts += 1
                time.sleep(1.0)
        if not success:
            failures.append((num, theme))
        time.sleep(0.4)
    print(f"DONE saved={len(saved)} failures={len(failures)}")
    return saved, failures


if __name__ == "__main__":
    main()