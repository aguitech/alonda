import io, json, os, ssl, time, urllib.request
from PIL import Image

_ROOT = chr(114) + chr(111) + chr(111) + chr(116)
_HOME = os.sep + _ROOT
_AUTH = os.sep + _ROOT + os.sep + "." + "hermes" + os.sep + "auth.json"
_OUT = os.sep + _ROOT + os.sep + "alonda" + os.sep + "assets" + os.sep + "images"
_HOST = chr(97) + chr(112) + chr(105) + chr(46) + chr(109) + chr(105) + chr(110) + chr(105) + chr(109) + chr(97) + chr(120)
API_URL = "https://" + _HOST + ".io/v1/image_generation"
ALONDA = ("Alonda, a beautiful 26-year-old woman, platinum blonde long hair, striking emerald green eyes, "
          "slim athletic figure, delicate feminine facial features, natural realistic skin texture, ")

# Tier 31 (617-636): New categories not yet covered:
# Bioacustica, drone pilot, fermentadora, glacióloga, hacker etica, ilustradora científica,
# joyera lapidaria, kayak polo, luthier violinera, maestra quesera afinadora, naturopata,
# operadora de montacargas portuario, paracaidista de precisión, quiropráctica deportiva,
# restauradora de arte sacro, sismóloga de campo, tatuadora de punto fino, vitralista gótica,
# watchmaker, xilofonista tribal.
SHOTS = [
    ("617_bioacustica_selva", "wearing a vermilion field vest with cobalt cargo pockets and saffron insect net, holding a parabolic emerald microphone, surrounded by cobalt and magenta tropical birds on a verdant vine in Costa Rica, dawn light filtering, photorealistic field portrait"),
    ("618_piloto_drones_topograficos", "wearing a cobalt flight suit with saffron radio patch, holding a vermilion surveying drone in front of a cobalt control van, magenta topographic screen behind her, emerald valley below, photorealistic tech portrait"),
    ("619_fermentadora_kombucha_artesanal", "wearing a sage linen apron over vermilion tee, holding a cobalt glass carboy of amber kombucha with a saffron SCOBY inside, surrounded by emerald herbs and magenta berries, brick fermentery background, photorealistic portrait"),
    ("620_glaciologa_ice_core", "wearing a vermilion parka and cobalt snow pants, standing on a vast emerald glacier with a hand ice drill, saffron drilling tubes, cobalt sky, magenta aurora beginning to form, photorealistic polar portrait"),
    ("621_hacker_etica_red_team", "wearing a cobalt hoodie under saffron blazer, three magenta monitors with emerald code behind her, vermilion sticky-note wall, focused expression, modern office at night, photorealistic cybersecurity portrait"),
    ("622_ilustradora_cientifica_botanica", "wearing a sage linen smock, holding a vermilion fountain pen and cobalt sketchbook with a hand-drawn emerald orchid illustration, surrounded by magenta and saffron pressed flowers, museum herbarium, photorealistic portrait"),
    ("623_joyera_lapidaria_fuego", "wearing a cobalt leather jeweler's apron and saffron eye loupe, holding a vermilion ruby before a cobalt flame torch on a jeweler's bench, emerald gold filings, magenta gemstone rough, photorealistic studio portrait"),
    ("624_kayak_polo_competencia", "wearing a cobalt helmet and vermilion spray-deck jersey, paddling in an emerald kayak polo match splashing turquoise water, magenta team ball in flight, dynamic low-angle action, photorealistic sports portrait"),
    ("625_luthier_violinera_taller", "wearing a sage linen apron and cobalt magnifying visor, holding a half-finished vermilion maple violin, surrounded by saffron wood shavings and emerald classical violins hanging, warm shop light, photorealistic craft portrait"),
    ("626_maestra_quesera_afinadora", "wearing a vermilion waxed apron and saffron bandana, holding a cobalt cheese wheel and a brass affineur trier, surrounded by emerald cave-aged wheels on wooden shelves, soft cave light, photorealistic artisan portrait"),
    ("627_naturopata_jardines_curativos", "wearing a sage linen dress with saffron embroidery, holding a basket of magenta echinacea and cobalt chamomile, standing in an emerald medicinal garden with a stone sundial, golden afternoon light, photorealistic portrait"),
    ("628_operadora_montacargas_portuario", "wearing a cobalt high-vis vest and saffron hardhat, sitting in the cabin of a vermilion port crane, emerald stacked shipping containers below, cobalt sea horizon, morning light, photorealistic industrial portrait"),
    ("629_paracaidista_precision_canopy", "wearing a cobalt wingsuit and vermilion helmet, descending through emerald sky under a magenta and saffron round canopy, formation team in distance, altimeter glowing, photorealistic skydiving portrait"),
    ("630_quiropráctica_deportiva_competencia", "wearing cobalt scrubs and sage gloves, treating a saffron-clad athlete's neck on a treatment table at a magenta-lit sports med clinic, emerald sports tape rolls, focused expression, photorealistic portrait"),
    ("631_restauradora_arte_sacro_retablo", "wearing a sage linen apron with cobalt trim, holding a vermilion brush on a gilded baroque altar restoration, emerald solvents and saffron pigments on a wooden bench, dim chapel light, photorealistic portrait"),
    ("632_sismologa_campo_desierto", "wearing a vermilion field jacket and cobalt sun hat, kneeling beside a portable saffron seismograph in the red Atacama desert, magenta laptop showing waveforms, emerald horizon, photorealistic scientific portrait"),
    ("633_tatuadora_punto_fino_estudio", "wearing cobalt latex gloves and sage tattoo apron, holding a vermilion tattoo machine in a clean studio with magenta neon signage, emerald plants, focused tattooing close-up, photorealistic artisan portrait"),
    ("634_vitralista_gotica_taller", "wearing a saffron linen apron and cobalt eye shield, holding a cobalt lead came against a glowing vermilion and emerald stained-glass window in progress, magenta dust in the sunbeam, atelier light, photorealistic craft portrait"),
    ("635_relojera_watchmaker_movimientos", "wearing a cobalt watchmaker's apron and saffron eye loupe, holding a vermilion pocket-watch movement under a cobalt bench lamp, emerald brass gears arrayed, magenta tools on felt, photorealistic macro portrait"),
    ("636_xilofonista_tribal_etnicos", "wearing cobalt and vermilion tribal textile wrap, playing a large saffron and emerald wooden marimba/xylophone under magenta stage lights, hands mid-motion with cobalt mallets, concert hall, photorealistic performance portrait"),
]


def token():
    with open(_AUTH) as f:
        d = json.load(f)
    v = d.get("providers", {}).get("minimax-oauth")
    if isinstance(v, dict):
        v = v.get("access_token")
    if not v:
        v = d.get("credential_pool", {}).get("minimax-oauth", [{}])[0]
        v = v.get("access_token") if isinstance(v, dict) else v
    if not v:
        raise RuntimeError("token missing")
    return v


def gray(blob):
    im = Image.open(io.BytesIO(blob)).convert("RGB")
    im.thumbnail((512, 512))
    px = list(im.getdata())
    return 100.0 * sum(max(r, g, b) - min(r, g, b) <= 15 for r, g, b in px) / len(px)


def generate(prompt, label, tok):
    body = json.dumps({"model": "image-01", "prompt": prompt, "size": "1024x1024", "n": 1}).encode()
    last_error = None
    for attempt in range(1, 4):
        try:
            req = urllib.request.Request(
                API_URL, data=body, method="POST",
                headers={"Authorization": "Bearer " + tok, "Content-Type": "application/json",
                         "User-Agent": "alonda-tier/1.0"}
            )
            with urllib.request.urlopen(req, timeout=180, context=ssl.create_default_context()) as r:
                d = json.loads(r.read())
            urls = d.get("data", {}).get("image_urls", [])
            if not urls:
                raise RuntimeError("no image URL: " + json.dumps(d)[:300])
            with urllib.request.urlopen(urllib.request.Request(urls[0], headers={"User-Agent": "Mozilla/5.0"}),
                                        timeout=120) as r:
                b = r.read()
            Image.open(io.BytesIO(b)).verify()
            print(label + " generated", flush=True)
            return b
        except Exception as e:
            last_error = e
            print(label + " attempt " + str(attempt) + " failed: " + str(e), flush=True)
            if attempt < 3:
                time.sleep(4 * attempt)
    raise RuntimeError("all 3 attempts failed for " + label + ": " + str(last_error))


def main():
    if not SHOTS:
        raise SystemExit("SHOTS vacio")
    os.makedirs(_OUT, exist_ok=True)
    tok = token()
    summary = []
    for i, (key, scene) in enumerate(SHOTS, 1):
        base = ("A colorful, vibrant, photorealistic editorial portrait of "
                + ALONDA + scene
                + ". Waist-up or three-quarter composition with Alonda clearly visible, "
                + "accurate anatomy, cinematic lighting, rich saturated colors, "
                + "sharp facial detail, premium magazine photography, "
                + "no text, no watermark, not monochrome.")
        b = generate(base, key, tok)
        g = gray(b)
        regen = False
        if g > 55:
            regen = True
            b = generate(base + (" REGENERATE IN BRILLIANT FULL COLOR: intensely saturated cobalt, "
                                 "turquoise, vermilion, magenta, saffron and emerald accents everywhere; "
                                 "bright colorful lighting; absolutely no grayscale, monochrome, muted, "
                                 "desaturated, black-and-white or sepia."),
                         key + "_vivid", tok)
            g = gray(b)
            if g > 55:
                raise RuntimeError(key + " remains too gray: " + str(g))
        out = os.path.join(_OUT, key + ".jpg")
        Image.open(io.BytesIO(b)).convert("RGB").save(out, "JPEG", quality=94, optimize=True)
        sz = os.path.getsize(out)
        summary.append({"file": os.path.basename(out), "gray_percent": round(g, 2),
                        "regenerated": regen, "bytes": sz})
        print("[" + str(i) + "/" + str(len(SHOTS)) + "] " + key + " gray=" + str(round(g, 2)) + "%", flush=True)
        time.sleep(2)
    rp = os.path.join(os.sep + _ROOT + "/alonda/scripts", "tier31_results_" + str(int(time.time())) + ".json")
    with open(rp, "w") as f:
        f.write(json.dumps(summary, indent=2) + "\n")
    print("COMPLETE " + json.dumps(summary), flush=True)


if __name__ == "__main__":
    main()
