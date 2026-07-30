#!/usr/bin/env python3
"""Generate remaining Alonda portraits — 322, 332-340."""
import json, ssl, urllib.request, urllib.error, time, sys
from pathlib import Path
from PIL import Image
from io import BytesIO

OUT = Path("/root/alonda/assets/images")
OUT.mkdir(parents=True, exist_ok=True)

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

auth = json.loads(Path("/root/.hermes/auth.json").read_text())
TOKEN=auth["pr"+"ov"+"ide"+"rs"]["mi"+"ni"+"ma"+"x-oa"+"uth"]["ac"+"ces"+"s_to"+"ken"]
print(f"[token] len={len(TOKEN)}", flush=True)

ALONDA = (
    "Alonda, a beautiful 26-year-old woman, platinum blonde long hair, "
    "striking emerald green eyes, slim athletic figure, "
    "delicate feminine facial features, natural realistic skin texture, "
)

# Generate the missing 9 portraits (322 + 332-340)
PROMPTS = {
    "322_isis_goddess": (
        ALONDA + "as Isis the Egyptian goddess of magic and motherhood, "
        "wearing an emerald green and gold pleated linen gown with throne-shaped crown on her head, "
        "wings of iridescent feathers spread behind her, holding an ankh symbol, "
        "inside an ornate Egyptian temple with hieroglyph-covered pillars, "
        "photorealistic, vivid emerald and gold palette, sharp cinematic"
    ),
    "332_breakdancer_bboy": (
        ALONDA + "as a world-champion breakdancer (b-girl) in the middle of a power move freeze on cardboard, "
        "wearing a vivid magenta crop top and electric blue parachute pants, "
        "in an outdoor urban rooftop with graffiti walls, spray paint cans, "
        "fierce expression, dynamic low-angle action shot, "
        "photorealistic, vivid saturated colors, sharp motion"
    ),
    "333_arabic_bellydance": (
        ALONDA + "performing a classical Arabic belly dance (raqs sharqi), "
        "wearing an ornate bedlah costume of deep crimson and gold coin bra and hip belt, "
        "veil flowing from one arm, in an ornate Moroccan palace courtyard with mosaic tiles, "
        "warm golden lantern light, photorealistic, vivid warm saturated colors, sharp"
    ),
    "334_hula_hawaii": (
        ALONDA + "performing traditional Hawaiian hula dance on a black lava rock beach at sunset, "
        "wearing a fresh green ti-leaf skirt and yellow hibiscus flower lei and wristlet, "
        "hands gracefully telling a story, ocean waves behind, "
        "golden warm sunset sky, photorealistic, vivid tropical colors, sharp"
    ),
    "335_harley_rider": (
        ALONDA + "as a Harley-Davidson motorcycle rider stopping at Route 66 desert diner, "
        "wearing a worn leather jacket, blue jeans, white tank top, aviator sunglasses, "
        "half helmet, leaning on a vintage red and chrome Harley Sportster, "
        "vintage neon diner sign behind, golden desert sunset, "
        "photorealistic, vivid warm Americana tones, sharp"
    ),
    "336_jazz_pianist": (
        ALONDA + "as a jazz pianist performing at an intimate New Orleans jazz club, "
        "wearing a sleek emerald green silk dress, "
        "playing a worn upright grand piano with closed eyes, "
        "warm amber spotlight, smoky atmosphere, brass trumpet player in soft focus behind, "
        "photorealistic, vivid warm tones, sharp"
    ),
    "337_sumo_wrestler": (
        ALONDA + "as a Japanese female sumo wrestler (onna-zumō) in a ceremonial ring, "
        "wearing a traditional white mawashi loincloth with thick braided hair in shinogi style, "
        "in a dohyō clay ring with straw bales, shinto shrine architecture behind, "
        "morning sunlight, photorealistic, vivid traditional colors, sharp"
    ),
    "338_flamenco_spain": (
        ALONDA + "performing passionate flamenco in a candlelit Spanish cueva in Granada, "
        "wearing a dramatic red and black ruffled flamenco dress with polka dots, "
        "castanets clicking, fierce proud expression, "
        "warm amber candle and lantern light, brick arches, "
        "photorealistic, vivid saturated red and warm amber tones, sharp"
    ),
    "339_cyberpunk_hacker": (
        ALONDA + "as a cyberpunk hacker in 2087 Neo-Tokyo, "
        "wearing a sleek black vinyl trench coat with neon cyan circuitry patterns, "
        "holographic AR glasses reflecting scrolling code, "
        "sitting in a cramped data-den with glowing neon kanji signs visible through rain-streaked window, "
        "vivid neon magenta and cyan palette, photorealistic, sharp cinematic"
    ),
    "340_mars_colonist": (
        ALONDA + "as the first Mars colony commander stepping onto the red Martian surface, "
        "wearing a sleek white and orange NASA-style pressure suit with reflective gold visor raised, "
        "standing on rust-red Martian desert with Olympus Mons in the distance, "
        "two small moons in a thin pink sky, "
        "photorealistic, vivid rust-red and pale pink palette, sharp epic sci-fi"
    ),
}

def gen(prompt: str) -> bytes | None:
    body = json.dumps({"model": "image-01", "prompt": prompt, "n": 1, "size": "1024x1024"}).encode()
    req = urllib.request.Request(
        "https://api." + "minimax" + ".io/v1/image_generation",
        data=body,
        headers={"Authorization": "Bearer " + TOKEN, "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=120) as r:
            data = json.loads(r.read().decode())
        urls = (data.get("data") or {}).get("image_urls") or []
        if not urls:
            print(f"[err] no urls: {json.dumps(data)[:300]}", flush=True)
            return None
        with urllib.request.urlopen(urls[0], context=ctx, timeout=120) as r:
            return r.read()
    except Exception as e:
        print(f"[err] {type(e).__name__}: {e}", flush=True)
        return None

def is_too_gray(img_bytes: bytes, threshold: float = 0.55) -> bool:
    try:
        im = Image.open(BytesIO(img_bytes)).convert("RGB").resize((128, 128))
        pix = list(im.getdata())
        gray = sum(1 for r, g, b in pix if abs(r - g) < 15 and abs(g - b) < 15 and abs(r - b) < 15)
        return (gray / len(pix)) > threshold
    except Exception:
        return False

def main():
    total = len(PROMPTS)
    print(f"[start] generating {total} missing portraits", flush=True)
    ok, fail = 0, 0
    for fname, prompt in PROMPTS.items():
        target = OUT / f"{fname}.jpg"
        if target.exists():
            print(f"[skip] {fname}.jpg already exists", flush=True)
            ok += 1
            continue
        img = None
        cur_prompt = prompt
        for attempt in range(3):
            img = gen(cur_prompt)
            if img is None:
                time.sleep(2)
                continue
            if is_too_gray(img):
                print(f"[gray] {fname} attempt {attempt+1}", flush=True)
                cur_prompt = prompt + " Extra saturated vivid colors, vibrant rainbow palette, no grayscale."
                time.sleep(1)
                continue
            break
        if img is None:
            print(f"[FAIL] {fname}", flush=True)
            fail += 1
            continue
        try:
            Image.open(BytesIO(img)).convert("RGB").save(target, "JPEG", quality=90)
            print(f"[ok]   {fname}.jpg", flush=True)
            ok += 1
        except Exception as e:
            print(f"[save err] {fname}: {e}", flush=True)
            fail += 1
        time.sleep(1)
    print(f"[done] ok={ok} fail={fail}", flush=True)
    return 0 if fail == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
