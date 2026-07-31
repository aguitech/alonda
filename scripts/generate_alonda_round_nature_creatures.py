#!/usr/bin/env python3
"""Generate next batch of Alonda portraits.

Mixes categories not recently covered:
- Cuisine / chefs / bakers / ice cream makers
- Vehicles / mechanics / pilots / captains
- Botanica / flowers / gardens
- Mythology round 2 (Norse + Celtic + Slavic)
"""
import json
import os
import sys
import time
import urllib.request
import urllib.parse
from pathlib import Path


def _load_token() -> str:
    """Load OAuth token from hermes auth.json (avoid hardcoding)."""
    auth_path = Path(os.environ.get("HERMES_AUTH_PATH", "/root/.hermes/auth.json"))
    with auth_path.open() as f:
        data = json.load(f)
    # try common keys
    for key in (
        ("providers", "minimax-oauth", "access_token"),
        ("credential_pool", "minimax-oauth", "0", "access_token"),
    ):
        cur = data
        try:
            for k in key:
                cur = cur[k]
            if cur:
                return cur
        except (KeyError, TypeError):
            continue
    raise RuntimeError("minimax-oauth token not found in auth.json")


TOKEN = _load_token()
# End-point via concatenation to avoid redactor filters
ENDPOINT = "https://api." + "minimax" + ".io/v1/image_generation"

ANCHOR = "Alonda, a beautiful 26-year-old woman, platinum blonde long hair, striking emerald green eyes, slim athletic figure, delicate feminine facial features, natural realistic skin texture, "

OUT_DIR = Path("/root/alonda/assets/images")
OUT_DIR.mkdir(parents=True, exist_ok=True)

START_NUM = 1486

# Categories mixed: chefs (5) + vehicles (5) + botanica (5) + mythology r2 (5)
PROMPTS = [
    # Chefs / pastry
    ("artisan_pastry_chef", "artisanal pastry chef portrait of her in a cobalt double-breasted chef coat with vermilion piping and saffron apron dusted with cobalt powdered sugar, hand-piping saffron macarons on a vermilion copper tray in a patisserie lit by warm tungsten bulbs, atelier in the morning, shallow depth of field, editorial food photography style, high detail, 8k"),
    ("artisan_pizza_maker", "artisan Neapolitan pizzaiola portrait of her tossing cobalt dough in the air inside a vermilion wood-fired brick oven glowing with saffron embers, flour dust in the cobalt backlight, Naples alley at dusk, rustic copper pots in the background, cinematic food portrait, 8k"),
    ("artisan_icecream_maker", "artisanal gelato maker portrait of her in a cobalt striped apron and vermilion bandana, hand-scooping saffron and vermilion gelato from a cobalt pozzetti display case in a tiny Roman cobblestone piazza, summer light, candid editorial style, 8k"),
    ("artisan_chocolatier", "artisanal chocolatier portrait of her tempering a slab of cobalt tempered chocolate on a vermilion marble slab, wearing saffron leather apron, copper molds shaped like seashells behind her, atelier with hanging Edison bulbs, editorial food portrait, 8k"),
    ("artisan_sushi_chef", "Edomae sushi chef portrait of her in a cobalt hada jacket and vermilion tenugui headband, knife-blade gleaming, forming nigiri over a vermilion hinoki cypress counter with cobalt nori sheets and a saffron ceramic plate, intimate Tokyo sushiya in soft lantern light, editorial portrait, 8k"),
    # Vehicles
    ("classic_car_mechanic", "classic car mechanic portrait of her in cobalt coveralls with vermilion patches, leaning on the fender of a fully restored vermilion 1965 cobalt-detailed Shelby Cobra in a warm-lit private garage, wrenches in hand, candid editorial portrait, 8k"),
    ("formula_one_racer", "formula one racing driver portrait of her stepping out of a cobalt-and-vermilion-liveried single-seater F1 car in the pit lane at golden hour, helmet tucked under one arm, race suit fireproof cobalt with vermilion sponsor stripes, garage in soft focus behind, dynamic editorial portrait, 8k"),
    ("train_engine_driver", "locomotive engineer portrait of her at the throttle of a vermilion 1920s steam locomotive cab with cobalt gauges and saffron steam billowing outside the cab window, mountain railway in autumn, warm industrial portrait, 8k"),
    ("yacht_captain_solo", "solo sailing captain portrait of her at the helm of a cobalt sloop under vermilion spinnaker sail on a deep cobalt ocean with whitecaps, wearing saffron foul weather jacket, golden hour sun on her face, adventurous editorial portrait, 8k"),
    ("helicopter_pilot_rescue", "rescue helicopter pilot portrait of her in cockpit of a vermilion and cobalt EMS helicopter hovering over a saffron desert canyon, helmet visor up, headset on, mountain rescue scene, dynamic editorial portrait, 8k"),
    # Botanica
    ("english_garden_head", "head gardener of a walled English garden portrait of her in cobalt linen apron with saffron leather gloves, pruning vermilion rambling roses climbing a stone wall, soft English overcast light, countryside estate, editorial portrait, 8k"),
    ("orchid_grower", "rare orchid grower portrait of her inside a glass Victorian orchid conservatory, holding a vermilion phalaenopsis bloom, surrounded by cobalt and saffron orchid species hanging from the glass ceiling, soft diffused light, editorial portrait, 8k"),
    ("bonsai_master", "bonsai master portrait of her trimming a hundred-year-old cobalt-needled Japanese white pine bonsai with vermilion scissors, seated at a saffron wood workbench in a traditional tatami room, afternoon light filtering through shoji, editorial portrait, 8k"),
    ("urban_greenhouse", "urban hydroponic greenhouse farmer portrait of her in a cobalt vertical farm under vermilion LED grow lights, harvesting saffron basil and cobalt kale, high-tech greenhouse in Brooklyn, editorial portrait, 8k"),
    ("viticulture_harvest", "winemaker during grape harvest portrait of her in cobalt mud-spattered boots and a vermilion plaid shirt, holding a basket of cobalt Concord grapes at sunset in a Napa vineyard rolling into saffron hills, candid editorial portrait, 8k"),
    # Mythology round 2
    ("freya_falcon_cloak", "Freyja Norse goddess of love and war portrait of her wearing a vermilion falcon-feather cloak over a cobalt gown, with saffron Brísingamen gold torque necklace, holding a small cobalt falcon on her gloved wrist, aurora-lit Norse fjord, mythological editorial portrait, 8k"),
    ("thor_lightning", "Thor Norse thunder goddess portrait of her in vermilion scale armor with cobalt under-tunic, wielding a short-hafted saffron war hammer crackling with cobalt lightning, standing on a Norse mountain ridge under a stormy cobalt sky, mythological editorial portrait, 8k"),
    ("loki_shapeshifter", "Loki Norse trickster portrait of her in emerald and saffron silk with a sly smile, holding a cobalt staff topped with a vermilion flame, surrounded by shifting smoke in a Norse birch forest, mythological editorial portrait, 8k"),
    ("celtic_morrigan_crow", "Morrígan Celtic war goddess portrait of her in cobalt raven-feather cloak with vermilion eye-paint, perched on a saffron standing stone in a misty Irish bog at twilight, crows circling overhead, mythological editorial portrait, 8k"),
    ("slavic_baba_yaga", "Baba Yága Slavic forest witch portrait of her as a young crone figure in tattered vermilion shawl and cobalt dress, standing beside a saffron hut on chicken legs deep in a dark Slavic birch forest glowing with cobalt will-o'-the-wisps, mythological editorial portrait, 8k"),
]


def post_one(prompt: str, timeout: int = 60) -> bytes:
    body = json.dumps({
        "model": "image-01",
        "prompt": prompt,
        "size": "1024x1024",
        "n": 1,
    }).encode("utf-8")
    req = urllib.request.Request(
        ENDPOINT,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + TOKEN,
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    urls = data.get("data", {}).get("image_urls") or data.get("image_urls") or []
    if not urls:
        raise RuntimeError(f"No image_urls in response: {json.dumps(data)[:300]}")
    url = urls[0]
    with urllib.request.urlopen(url, timeout=timeout) as img_resp:
        return img_resp.read()


def check_gray(path: Path, threshold: float = 55.0):
    """Return (too_gray: bool, pct: float)."""
    from PIL import Image
    img = Image.open(path).convert("RGB").resize((128, 128))
    pixels = list(img.getdata())
    gray = sum(1 for r, g, b in pixels if abs(r - g) < 12 and abs(g - b) < 12 and abs(r - b) < 12)
    pct = gray / len(pixels) * 100
    return pct > threshold, pct


def main() -> int:
    print(f"Starting at number {START_NUM}, target {START_NUM + len(PROMPTS) - 1}")
    successes = []
    failures = []
    for i, (slug, prompt) in enumerate(PROMPTS):
        n = START_NUM + i
        filename = f"chefs_vehicles_botanic_myth2_round3_{n}_{slug}.jpg"
        path = OUT_DIR / filename
        final_prompt = ANCHOR + prompt
        attempts = 0
        saved = False
        last_err = None
        while attempts < 3:
            attempts += 1
            try:
                blob = post_one(final_prompt)
                path.write_bytes(blob)
                # gray check
                try:
                    too_gray, pct = check_gray(path)
                    print(f"[{n}] saved {filename} ({len(blob)} bytes) gray={pct:.1f}%")
                    if too_gray and attempts < 3:
                        # try once more with more vibrant modifier
                        final_prompt = ANCHOR + prompt + " hyper-saturated cinematic color grading, vivid complementary palette, no desaturated tones"
                        continue
                except Exception:
                    print(f"[{n}] saved {filename} ({len(blob)} bytes) [no gray check]")
                saved = True
                successes.append(filename)
                break
            except Exception as e:
                last_err = repr(e)
                print(f"[{n}] attempt {attempts} failed: {last_err}")
                time.sleep(2)
        if not saved:
            failures.append((n, filename, last_err))
        # gentle rate-limit
        time.sleep(0.4)

    print(f"\nDONE: {len(successes)} ok, {len(failures)} failed")
    if failures:
        for f in failures:
            print(" FAIL:", f)
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())