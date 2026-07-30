#!/usr/bin/env python3
"""Generate Alonda portraits 797-816 — 20 unique looks."""
import json, ssl, urllib.request, urllib.error, time, sys
from pathlib import Path

OUT = Path("/root/alonda/assets/images")
OUT.mkdir(parents=True, exist_ok=True)

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

auth = json.loads(Path("/root/.hermes/auth.json").read_text())
TOKEN = auth["providers"]["minimax-oauth"]["access_token"]
print(f"[token] len={len(TOKEN)}")

# ANCHOR — 7 atributos obligatorios
ALONDA = (
    "Alonda, a beautiful 26-year-old woman, "
    "platinum blonde long hair, striking emerald green eyes, "
    "slim athletic figure, delicate feminine facial features, "
    "natural realistic skin texture, "
)

START = 797
END = 816

LOOKS = {
    797: ("kawaii_jpop_idol", ALONDA + "as a Japanese kawaii J-pop idol wearing a fluffy pastel pink tutu dress with candy-colored accessories, oversized hair bow, sparkling eyeshadow, holding a giant lollipop, in a Tokyo Harajuku street with vivid pink and mint green storefronts, photorealistic, sharp, vivid saturated colors, professional portrait photography"),
    798: ("gothic_victorian_crypt", ALONDA + "in gothic Victorian mourning attire — black velvet Victorian gown with lace cuffs, jet bead choker, pale powdered makeup with deep burgundy lips, holding a black mourning rose, in an ornate candlelit mausoleum with carved marble angels and crimson drapery, photorealistic, sharp, vivid dramatic colors"),
    799: ("punk_rebellion_1977", ALONDA + "as a 1977 London punk rocker with a vibrant magenta mohawk, torn fishnet stockings, leather jacket covered in safety pins and anarchist patches, ripped band tee, in a gritty Camden alley with neon graffiti, photorealistic, sharp, vivid electric colors, editorial portrait"),
    800: ("preppy_ivy_league_campus", ALONDA + "as an Ivy League preppy collegiate on an autumn New England campus — crisp oxford shirt, cable-knit cashmere sweater vest in burnt orange, pleated plaid wool skirt in hunter green, knee-high riding boots, holding leather-bound books, golden maple leaves falling, photorealistic, sharp, vivid warm autumn colors"),
    801: ("steampunk_inventor_workshop", ALONDA + "as a Victorian steampunk inventor in a brass-and-copper workshop, wearing a deep burgundy leather corset with brass gears, copper goggles pushed up on forehead, holding a glowing cobalt-blue arcane device, surrounded by intricate clockwork contraptions and amber gas lamps, photorealistic, sharp, vivid sepia and electric blue tones"),
    802: ("dieselpunk_mechanic_hangar", ALONDA + "as a 1940s dieselpunk female aircraft mechanic in a massive hangar, wearing oil-stained khaki coveralls rolled up at sleeves, leather aviator cap, goggles around neck, working on a polished aluminum fuselage of a propeller fighter plane with vivid red and gold livery, dramatic cinematic lighting, photorealistic, sharp, vivid colors"),
    803: ("carnaval_rio_samba", ALONDA + "as a Rio Carnival samba dancer in the Sambadrome, wearing an enormous feathered carnival costume in vivid hot pink, electric turquoise, and sunshine yellow with sequined bodice and towering headdress with ostrich plumes, mid-dance pose, confetti raining, photorealistic, sharp, vivid explosive colors, professional photography"),
    804: ("oktoberfest_bavarian", ALONDA + "as a Bavarian Oktoberfest beer maid in a traditional dirndl in deep emerald green with white lace blouse, braided hair with white ribbon, holding two massive overflowing steins of golden beer, in a festive Bavarian beer hall with vivid wood paneling and string lights, photorealistic, sharp, vivid warm golden colors"),
    805: ("holi_india_color_festival", ALONDA + "as a participant in the Holi color festival in Mathura India, wearing a simple white cotton sari now saturated with vivid magenta, saffron yellow, electric blue, and vermilion powder, joyful mid-throw pose with arms raised, surrounded by clouds of colored powder, photorealistic, sharp, vivid explosive rainbow colors"),
    806: ("machu_picchu_sunrise", ALONDA + "standing atop Machu Picchu at golden sunrise, wearing warm earth-toned alpaca wool poncho in rust and ochre with woven patterns, wind-tousled hair, dramatic Andes mountains behind with vivid golden mist and emerald terraces, photorealistic, sharp, vivid warm cinematic colors"),
    807: ("patagonia_torres_del_paine", ALONDA + "as a Patagonia mountaineer at the base of Torres del Paine granite spires, wearing a vivid cobalt-blue hardshell jacket and rust-orange backpack, holding ice axe, dramatic glacial landscape with vivid turquoise ice and emerald lakes, photorealistic, sharp, vivid dramatic cinematic colors"),
    808: ("antelope_canyon_lightbeams", ALONDA + "inside Antelope Canyon Arizona, wearing a flowing burnt-orange silk scarf dress, standing among vivid orange swirling sandstone walls, dramatic shafts of golden sunlight beaming down from above, photorealistic, sharp, vivid warm orange and gold tones, professional landscape portrait"),
    809: ("salar_uyuni_mirror", ALONDA + "standing on the mirror-flat Salar de Uyuni salt flats at sunset, wearing a vivid flowing fuchsia silk dress that trails across the reflective surface, perfect mirror reflection of vivid pink and gold sky, photorealistic, sharp, vivid saturated colors, surreal dreamlike portrait"),
    810: ("zhangjiajie_pillars_floating", ALONDA + "as a martial arts wanderer standing on the edge of a Zhangjiajie sandstone pillar above the clouds, wearing flowing crimson silk hanfu with gold embroidery, hair flowing in the wind, dramatic sea of clouds and vivid emerald forest below, golden sunrise lighting, photorealistic, sharp, vivid colors"),
    811: ("ux_designer_modern_office", ALONDA + "as a modern UX designer at a creative tech office, wearing a crisp coral-pink turtleneck and tailored navy trousers, dual ultrawide monitors with vivid gradient app mockups, contemporary Scandinavian furniture in white and warm oak, photorealistic, sharp, vivid clean colors, professional editorial portrait"),
    812: ("data_scientist_ai_lab", ALONDA + "as a data scientist in a cutting-edge AI research lab, wearing a structured cobalt-blue lab coat over a black top, holographic data visualizations floating in vivid neon green and magenta behind her, futuristic glass-walled lab, photorealistic, sharp, vivid electric colors, professional portrait"),
    813: ("firefighter_rescue_scene", ALONDA + "as an urban firefighter at a dramatic night rescue scene, wearing full turnout gear with reflective yellow-trim coat, helmet, and breathing apparatus on chest, vivid red fire engine lights and orange flames reflecting off her determined face, smoke billowing, photorealistic, sharp, vivid cinematic dramatic colors"),
    814: ("electricista_de_altura_high_voltage", ALONDA + "as a high-voltage power-line electrician working atop a steel transmission tower, wearing vivid orange hi-vis coveralls, climbing harness, white hard hat, dramatic cobalt-blue sky with bright white clouds behind, vivid green pastoral countryside below, photorealistic, sharp, vivid colors, documentary photography"),
    815: ("piloto_de_rally_dust", ALONDA + "as a rally race driver in a vivid red-and-yellow racing suit, sitting in the cockpit of a rally car mid-race on a dusty dirt track, helmet visor raised showing vivid emerald green eyes, dust clouds and eucalyptus trees behind, golden late-afternoon light, photorealistic, sharp, vivid dynamic colors"),
    816: ("guardia_costera_helicopter", ALONDA + "as a coast guard rescue swimmer beside a vivid orange-and-white MH-65 helicopter on the deck of a patrol cutter at sunset, wearing a vivid international-orange rescue suit and float coat, dramatic vivid golden sunset over deep cobalt ocean, photorealistic, sharp, vivid cinematic colors"),
}

def gen(prompt: str, size: str = "1024x1024"):
    body = json.dumps({"model": "image-01", "prompt": prompt, "n": 1, "size": size}).encode()
    req = urllib.request.Request(
        "https://api.minimax.io/v1/image_generation",
        data=body,
        headers={"Authorization": "Bearer " + TOKEN, "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=180, context=ctx) as r:
            data = json.loads(r.read())
            urls = data.get("data", {}).get("image_urls", [])
            return urls[0] if urls else None
    except urllib.error.HTTPError as e:
        print(f"  HTTP {e.code}: {e.read().decode()[:300]}")
    except Exception as e:
        print(f"  ERR: {e}")
    return None

def download(url: str, dest: Path) -> bool:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=90, context=ctx) as r:
            dest.write_bytes(r.read())
        return True
    except Exception as e:
        print(f"  download ERR: {e}")
        return False

def is_grayscale(path: Path, threshold: float = 0.55) -> bool:
    """Return True if image looks too gray (saturation low)."""
    try:
        from PIL import Image
        img = Image.open(path).convert("RGB")
        small = img.resize((100, 100))
        pixels = [p for p in small.getdata()]
        n = len(pixels)
        gray_count = 0
        for r, g, b in pixels:
            mx, mn = max(r, g, b), min(r, g, b)
            # "Gray" = low saturation: spread < 15 OR overall brightness in flat mid-tone
            if (mx - mn) < 18:
                gray_count += 1
        ratio = gray_count / n
        print(f"  gray-ratio={ratio:.2f}")
        return ratio > threshold
    except Exception as e:
        print(f"  gray-check ERR: {e}")
        return False

results = []
for num in range(START, END + 1):
    if num not in LOOKS:
        continue
    key, prompt = LOOKS[num]
    fname = f"{num}_{key}.jpg"
    dest = OUT / fname
    print(f"\n[{num}] {key}")
    if dest.exists() and dest.stat().st_size > 5000:
        print(f"  exists, skip")
        results.append(num)
        continue
    url = gen(prompt)
    if not url:
        print(f"  no URL, skip")
        continue
    if not download(url, dest):
        continue
    sz = dest.stat().st_size
    print(f"  saved {fname} ({sz:,} bytes)")
    # gray check (PIL may not be installed; tolerate)
    if is_grayscale(dest):
        print(f"  ⚠️ too gray — but keeping (no regen attempt this batch)")
    results.append(num)
    time.sleep(2)

print(f"\n=== {len(results)}/{END - START + 1} generated ===")
for n in results:
    print(f"  ok: {n}")