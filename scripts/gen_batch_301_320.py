#!/usr/bin/env python3
"""Generate Alonda portraits batch 301-320 — fresh unique prompts (no repeats of 1-300)."""
import json, ssl, urllib.request, urllib.error, time, sys, re
from pathlib import Path
from PIL import Image
from io import BytesIO

OUT = Path("/root/alonda/assets/images")
OUT.mkdir(parents=True, exist_ok=True)

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

auth = json.loads(Path("/root/.hermes/auth.json").read_text())
TOKEN = auth["providers"]["minimax-oauth"]["access_token"]
print(f"[token] len={len(TOKEN)}", flush=True)

# ANCHOR ALONDA — 7 atributos OBLIGATORIOS
ALONDA = (
    "Alonda, a beautiful 26-year-old woman, platinum blonde long hair, "
    "striking emerald green eyes, slim athletic figure, "
    "delicate feminine facial features, natural realistic skin texture, "
)

# Batch 301-320 — UNIQUE prompts (no overlap with prior batches 1-300)
# Mix: mythology, sci-fi retro, dance, foods, extreme sports, professions, music,
# historical, vehicles, weather, festivals, fantasy.
PROMPTS = {
    "301_medusa_goddess": (
        ALONDA + "as Medusa the Greek goddess, with hair transformed into living emerald serpents, "
        "wearing an emerald silk gown with golden Greek meander pattern, "
        "standing in an ancient marble temple with shafts of golden sunlight, "
        "mystical green glowing eyes, photorealistic, vivid saturated colors, sharp focus"
    ),
    "302_athena_warrior": (
        ALONDA + "as Athena the Greek goddess of wisdom and war, "
        "wearing a flowing white and gold peplos with bronze armor breastplate, "
        "holding a spear and aegis shield, standing on the Acropolis of Athens at sunrise, "
        "olive wreath crown in hair, photorealistic, vivid colors, epic cinematic"
    ),
    "303_steampunk_inventor": (
        ALONDA + "as a steampunk Victorian inventor in 1885 London, "
        "wearing a leather corset with brass gears and clockwork goggles on forehead, "
        "standing in her steam-powered workshop with copper pipes and gauges, "
        "warm gaslight illumination, photorealistic, vivid sepia-bronze tones, sharp"
    ),
    "304_kuchipudi_indian": (
        ALONDA + "performing Kuchipudi classical Indian dance, "
        "wearing a vibrant red and gold traditional temple sari with temple jewelry, "
        "ankle bells, on a stone temple stage with marigold flowers, "
        "expression of devotional bhakti, photorealistic, vivid saturated colors, sharp"
    ),
    "305_violinist_concert": (
        ALONDA + "as a world-class concert violinist on stage at Carnegie Hall, "
        "wearing a midnight blue velvet floor-length gown, "
        "playing a Stradivarius violin with closed eyes in deep concentration, "
        "warm spotlight, blurred orchestra behind, photorealistic, vivid warm tones"
    ),
    "306_jazz_singer_nyc": (
        ALONDA + "as a sultry jazz singer performing at a smoky New York jazz club, "
        "wearing a sequined champagne flapper dress, "
        "standing at a vintage microphone, red curtain backdrop, "
        "saxophone player in soft focus behind, warm amber stage lights, photorealistic, vivid"
    ),
    "307_dune_sandworm": (
        ALONDA + "as a Fremen warrior of Arrakis from Dune, "
        "wearing a desert stillsuit with aqua blue eyes (from spice), "
        "standing on a vast orange sand dune with a sandworm emerging in the far distance, "
        "harsh twin suns of Arrakis, photorealistic, vivid orange-amber palette, epic cinematic"
    ),
    "308_arctic_researcher": (
        ALONDA + "as an Arctic climate researcher at the North Pole research station, "
        "wearing a heavy red parka with fur-lined hood and insulated gloves, "
        "standing on sea ice with the aurora borealis in green and purple above, "
        "research equipment nearby, cold blue ice tones contrasted with aurora, photorealistic, vivid"
    ),
    "309_oktoberfest_munich": (
        ALONDA + "celebrating Oktoberfest in Munich, wearing a traditional dirndl in deep emerald green with white lace blouse, "
        "sitting at a long wooden beer hall table holding a large Maßkrug stein, "
        "pretzels and brass band in background, warm festive amber lighting, "
        "photorealistic, vivid warm Bavarian colors, sharp"
    ),
    "310_holi_festival_india": (
        ALONDA + "celebrating Holi festival in Mathura India, "
        "wearing a simple white cotton kurta now completely splattered with vivid magenta, yellow, turquoise, and saffron powder, "
        "laughing joyfully throwing pink gulal powder, "
        "crowd of similarly colorful figures behind, golden afternoon light, "
        "photorealistic, explosive vivid colors, sharp"
    ),
    "311_iron_welder": (
        ALONDA + "as a professional industrial welder in a steel fabrication workshop, "
        "wearing a leather welding apron, heavy gloves, auto-darkening helmet pushed up on head, "
        "bright blue-white welding arc sparks flying, molten metal glowing orange, "
        "dramatic chiaroscuro lighting, photorealistic, vivid orange-blue contrast, sharp"
    ),
    "312_electrician_tower": (
        ALONDA + "as a high-voltage power line electrician climbing a steel transmission tower, "
        "wearing orange hi-vis coveralls and white safety helmet, "
        "climbing harness and tool belt, dramatic view from above the clouds at sunset, "
        "photorealistic, vivid orange-blue sky, sharp, industrial realism"
    ),
    "313_f1_racer_podium": (
        ALONDA + "as a Formula 1 champion driver celebrating on the podium at Monaco Grand Prix, "
        "wearing a sleek red and black racing suit with sponsor logos, "
        "holding up a champagne bottle spraying celebration spray, "
        "crowd cheering behind, confetti falling, Mediterranean harbor in background, "
        "photorealistic, vivid saturated colors, sharp dynamic action"
    ),
    "314_yacht_captain": (
        ALONDA + "as the captain of a luxury sailing yacht in the Mediterranean, "
        "wearing a crisp white nautical captain's uniform with gold epaulettes and peaked cap, "
        "steering the helm at the stern of a sleek teak deck yacht, "
        "turquoise Caribbean-blue water, white sails billowing, brilliant noon sun, "
        "photorealistic, vivid blue-white palette, sharp"
    ),
    "315_machu_picchu_sunrise": (
        ALONDA + "standing at the ancient Inca citadel of Machu Picchu at golden sunrise, "
        "wearing a traditional Andean alpaca wool poncho in earthy red and ochre with intricate geometric patterns, "
        "stone terraces and Huayna Picchu mountain behind, "
        "soft golden hour light, morning mist in the valleys, "
        "photorealistic, vivid warm gold-amber tones, sharp epic landscape"
    ),
    "316_petra_treasury": (
        ALONDA + "standing in front of the carved rose-red Treasury (Al-Khazneh) in Petra Jordan, "
        "wearing a flowing desert Bedouin-style dress in deep saffron gold with silver Bedouin jewelry, "
        "ancient sandstone cliffs glowing in late afternoon sun, "
        "photorealistic, vivid rose-gold-orange palette, sharp"
    ),
    "317_zhangjiajie_pillars": (
        ALONDA + "standing among the towering sandstone pillars of Zhangjiajie National Forest China, "
        "wearing a flowing scarlet red qipao-inspired silk dress, "
        "lush green moss and mist swirling between pillars, "
        "luminous golden sunlight filtering through, "
        "photorealistic, vivid emerald and scarlet palette, sharp epic fantasy"
    ),
    "318_kite_surfer": (
        ALONDA + "kite surfing on bright turquoise tropical ocean waves, "
        "wearing a vivid sunset orange bikini and yellow life vest, "
        "mid-jump airborne above the wave with the colorful kite trailing above, "
        "salt spray, brilliant Caribbean sun, "
        "photorealistic, vivid tropical colors, sharp action shot"
    ),
    "319_paraglider_alps": (
        ALONDA + "paragliding above the snow-capped Swiss Alps, "
        "wearing a brightly colored red and yellow paragliding harness with helmet and goggles, "
        "suspended from the canopy of a vivid orange paraglider wing, "
        "glacial valleys and alpine lakes thousands of feet below, "
        "photorealistic, vivid saturated colors, sharp epic aerial"
    ),
    "320_centenarian_sage": (
        ALONDA + "as a wise centenarian sage with flowing silver-white hair, "
        "wearing layered cream linen robes with subtle Celtic knot embroidery, "
        "sitting peacefully in a lush cottage garden surrounded by lavender, rosemary, and climbing roses, "
        "soft dappled golden afternoon light, "
        "photorealistic, vivid natural colors, sharp, peaceful portrait"
    ),
}

def gen(prompt: str, size: str = "1024x1024") -> bytes | None:
    body = json.dumps({"model": "image-01", "prompt": prompt, "n": 1, "size": size}).encode()
    req = urllib.request.Request(
        "https://api.minimax.io/v1/image_generation",
        data=body,
        headers={"Authorization": "Bearer " + TOKEN, "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=180) as r:
            data = json.loads(r.read().decode())
        urls = (data.get("data") or {}).get("image_urls") or []
        if not urls:
            print(f"[err] no urls in response: {json.dumps(data)[:300]}", flush=True)
            return None
        with urllib.request.urlopen(urls[0], context=ctx, timeout=180) as r:
            return r.read()
    except urllib.error.HTTPError as e:
        print(f"[http {e.code}] {e.read().decode()[:400]}", flush=True)
        return None
    except Exception as e:
        print(f"[err] {type(e).__name__}: {e}", flush=True)
        return None

def is_too_gray(img_bytes: bytes, threshold: float = 0.55) -> bool:
    try:
        im = Image.open(BytesIO(img_bytes)).convert("RGB").resize((128, 128))
        pixels = list(im.getdata())
        gray = sum(1 for r, g, b in pixels if abs(r - g) < 15 and abs(g - b) < 15 and abs(r - b) < 15)
        return (gray / len(pixels)) > threshold
    except Exception:
        return False

def vibrant_retry_prompt(base: str) -> str:
    return base + " Extra saturated vivid colors, vibrant rainbow palette, hyper-colorful, no monochrome, no grayscale."

def main():
    total = len(PROMPTS)
    print(f"[start] generating {total} portraits for batch 301-320", flush=True)
    ok, fail = 0, 0
    for fname, prompt in PROMPTS.items():
        target = OUT / f"{fname}.jpg"
        if target.exists():
            print(f"[skip] {fname}.jpg already exists", flush=True)
            ok += 1
            continue

        attempts = 0
        img = None
        cur_prompt = prompt
        while attempts < 3:
            img = gen(cur_prompt)
            attempts += 1
            if img is None:
                time.sleep(2)
                continue
            if is_too_gray(img):
                print(f"[gray] {fname} attempt {attempts} too gray, retrying vibrant", flush=True)
                cur_prompt = vibrant_retry_prompt(prompt)
                time.sleep(1)
                continue
            break

        if img is None:
            print(f"[FAIL] {fname} — no image returned", flush=True)
            fail += 1
            continue

        try:
            Image.open(BytesIO(img)).convert("RGB").save(target, "JPEG", quality=90)
            print(f"[ok]   {fname}.jpg ({len(img)} bytes)", flush=True)
            ok += 1
        except Exception as e:
            print(f"[save err] {fname}: {e}", flush=True)
            fail += 1

        time.sleep(1.2)

    print(f"[done] ok={ok} fail={fail}", flush=True)
    return 0 if fail == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
