#!/usr/bin/env python3
"""Tier 18 (281-300): unique blend of mythology, sci-fi worlds, offbeat
professions, seasonal weather, and classic stage arts."""
import io, json, ssl, time, urllib.request
from pathlib import Path
from PIL import Image

AUTH_PATH = Path("/root/.hermes/auth.json")
OUT_DIR = Path("/root/alonda/assets/images")
API_URL = "https://api." + "minimax" + ".io/v1/image_generation"
ALONDA = (
    "Alonda, a beautiful 26-year-old woman, platinum blonde long hair, "
    "striking emerald green eyes, slim athletic figure, delicate feminine "
    "facial features, natural realistic skin texture, "
)

SHOTS = [
    ("281_thunder_god", "Norse thunder goddess wielding lightning bolts atop a stormy fjord cliff, vermilion storm cloak, cobalt hammer, turquoise crackling lightning, saffron sunset through rain, emerald pine forest and ruby runic armor, mythic portrait"),
    ("282_persephone", "Greek queen of the underworld holding a pomegranate in a twilight asphodel meadow, vermilion chiton, cobalt diadem, turquoise glowing horizon, saffron autumn leaves, emerald ivy and ruby pomegranate seeds, mythic portrait"),
    ("283_anubis_priestess", "Egyptian priestess of Anubis conducting a moonlit ritual beside the Nile, vermilion linen gown, cobalt ankh, turquoise moonlight, saffron pyramids in distance, emerald papyrus reeds and ruby scarab amulet, mythic portrait"),
    ("284_android_engineer", "cybernetic android technician calibrating a translucent humanoid in a neon laboratory, vermilion techwear suit, cobalt holographic interface, turquoise fiber optic cables, saffron dawn through skylight, emerald circuit board and ruby diagnostics panel, sci-fi portrait"),
    ("285_qubit_scientist", "quantum physicist observing entangled particles inside a cryogenic chamber, vermilion lab coat, cobalt dilution refrigerator, turquoise glowing qubits, saffron data visualizations, emerald laser grid and ruby cryostat, science portrait"),
    ("286_volcanic_chief", "volcano chief scientist sampling lava beside an active crater at dusk, vermilion heat suit, cobalt gas mask, turquoise molten flow, saffron smoke plume, emerald basalt field and ruby thermal camera, geology portrait"),
    ("287_ice_meteor", "aurora meteorologist tracking a luminous meteor streak over Iceland, vermilion parka, cobalt notebook, turquoise aurora curtain, saffron night sky, emerald glacier and ruby telescope, atmospheric portrait"),
    ("288_petals_storm", "tropical storm chaser standing amid a magenta rain of jacaranda petals, vermilion raincoat, cobalt anemometer, turquoise petals swirling, saffron lightning, emerald rainforest canopy and ruby umbrella, weather portrait"),
    ("289_rainbow_kite", "double rainbow double kite flyer on a hillside meadow after the rain, vermilion kite silk, cobalt second kite, turquoise rainbow arc, saffron wet grass, emerald hills and ruby wildflowers, joyful weather portrait"),
    ("290_ballet_swan", "classical ballet prima ballerina performing the white swan adagio in a gilded theater, vermilion tutu with silver embroidery, cobalt tights, turquoise spotlight, saffron spotlight halo, emerald proscenium and ruby bouquet, ballet portrait"),
    ("291_flamenco_dancer", "flamenco dancer mid-zapateado inside a whitewashed Andalusian courtyard, vermilion bata de cola ruffled dress, cobalt castanets, turquoise azulejo tiles, saffron geranium pots, emerald palm fronds and ruby roses, flamenco portrait"),
    ("292_hula_kauai", "hula dancer performing under a hala tree beside a Kauai beach at sunset, vermilion ti leaf skirt, cobalt shell lei, turquoise ocean, saffron golden sun, emerald volcanic cliffs and ruby plumeria blossoms, pacific island portrait"),
    ("293_kpop_stage", "K-pop idol striking a choreographed pose on a neon mega stage, vermilion sequined jacket, cobalt in-ear monitor, turquoise pyrotechnics, saffron spotlights, emerald confetti and ruby lightstick, pop performance portrait"),
    ("294_tango_milonga", "tango dancer leaning into a dramatic pose inside a Buenos Aires milonga, vermilion satin gown, cobalt bandoneon case, turquoise spotlight, saffron wood floor, emerald velvet curtain and ruby rose in hair, argentine portrait"),
    ("295_underwater_cave", "technical cave diver exploring a luminous cenote cavern, vermilion drysuit, cobalt dive light, turquoise halocline shimmer, saffron surface glow above, emerald stalactites and ruby dive computer, underwater portrait"),
    ("296_sailmaker_loft", "traditional sailmaker stitching a crimson canvas sail inside a wooden boat loft, vermilion canvas apron, cobalt sail hook, turquoise hull timbers, saffron rope coils, emerald kelp and ruby ship wheel, maritime craft portrait"),
    ("297_taxi_classic", "vintage 1960s London taxi driver polishing a black cab outside Buckingham Palace, vermilion scarf, cobalt classic taxi, turquoise Big Ben clock, saffron lamplight, emerald park bench and ruby phone box, city portrait"),
    ("298_bonsai_master", "ancient bonsai master pruning a centuries-old juniper in a Kyoto courtyard, vermilion kimono, cobalt shears, turquoise glazed pot, saffron maple, emerald moss garden and ruby bridge, meditative craft portrait"),
    ("299_permaculture_farm", "permaculture farmer harvesting rainbow chard on a terraced hillside at sunrise, vermilion linen apron, cobalt harvest basket, turquoise drip irrigation, saffron golden light, emerald cover crops and ruby tomatoes, sustainable agriculture portrait"),
    ("300_centenarian_sage", "wise centenarian storyteller seated by a stone hearth in a candlelit cottage, vermilion knitted shawl, cobalt rocking chair, turquoise cat companion, saffron fire glow, emerald herbs drying and ruby photo album, life-stage portrait"),
]


def load_token():
    with open(AUTH_PATH) as f:
        data = json.load(f)
    if "providers" in data and "minimax-oauth" in data["providers"]:
        t = data["providers"]["minimax-oauth"].get("access_token")
        if t:
            return t
    if "credential_pool" in data and "minimax-oauth" in data["credential_pool"]:
        arr = data["credential_pool"]["minimax-oauth"]
        if arr:
            return arr[0].get("access_token")
    raise RuntimeError("No token")


def call_api(token, prompt):
    body = json.dumps({"model": "image-01", "prompt": prompt, "size": "1024x1024", "n": 1}).encode("utf-8")
    req = urllib.request.Request(
        API_URL,
        data=body,
        method="POST",
        headers={"Content-Type": "application/json", "Authorization": "Bearer " + token},
    )
    ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, timeout=120, context=ctx) as resp:
        return json.loads(resp.read().decode("utf-8"))


def is_too_gray(path_or_bytes, threshold=0.55):
    try:
        if isinstance(path_or_bytes, (bytes, bytearray)):
            img = Image.open(io.BytesIO(path_or_bytes)).convert("RGB")
        else:
            img = Image.open(path_or_bytes).convert("RGB")
        small = img.resize((64, 64))
        px = list(small.getdata())
        gray_count = 0
        for r, g, b in px:
            d = abs(r - g) + abs(g - b) + abs(r - b)
            if d < 30:
                gray_count += 1
        return (gray_count / len(px)) > threshold
    except Exception:
        return False


def main():
    token = load_token()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    results = []
    for fname, desc in SHOTS:
        out_path = OUT_DIR / (fname + ".jpg")
        if out_path.exists() and out_path.stat().st_size > 1024:
            print("SKIP " + fname + " (exists)")
            results.append({"name": fname, "status": "exists"})
            continue
        prompt = ALONDA + desc
        attempts = 0
        ok = False
        while attempts < 3:
            attempts += 1
            try:
                resp = call_api(token, prompt)
                urls = resp.get("data", {}).get("image_urls") or resp.get("image_urls") or []
                if not urls:
                    print("NO URL for " + fname + " attempt " + str(attempts))
                    time.sleep(2)
                    continue
                url = urls[0]
                ctx = ssl.create_default_context()
                with urllib.request.urlopen(url, timeout=120, context=ctx) as r:
                    data = r.read()
                if is_too_gray(data):
                    print("GRAY " + fname + " attempt " + str(attempts) + ", regenerating")
                    prompt = ALONDA + desc + ", vibrant saturated colors, vivid rainbow palette, hyper colorful, eye-catching hues, dynamic lighting"
                    time.sleep(2)
                    continue
                out_path.write_bytes(data)
                print("OK " + fname + " " + str(len(data)) + " bytes")
                results.append({"name": fname, "bytes": len(data), "status": "ok"})
                ok = True
                break
            except Exception as e:
                print("ERR " + fname + " attempt " + str(attempts) + ": " + str(e))
                time.sleep(3)
        if not ok:
            results.append({"name": fname, "status": "failed"})
        time.sleep(1.0)
    Path("/root/alonda/scripts/tier18_281_300_results.json").write_text(json.dumps(results, indent=2))
    print("Done. Total results: " + str(len(results)))


if __name__ == "__main__":
    main()
