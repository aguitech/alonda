#!/usr/bin/env python3
"""Generate Alonda portraits 817-836 — 20 unique looks.

Categories mixed: Mitos griegos, deportes extremos, oficios modernos,
épocas históricas, música/instrumentos, festividades del mundo.
"""
import json, ssl, urllib.request, urllib.error, time, sys, os
from pathlib import Path

OUT = Path("/root/alonda/assets/images")
OUT.mkdir(parents=True, exist_ok=True)

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Token loaded at runtime — not committed
def load_token() -> str:
    auth = json.loads(Path("/root/.hermes/auth.json").read_text())
    return (
        auth.get("providers", {}).get("minimax-oauth", {}).get("access_token")
        or (auth.get("credential_pool", {}).get("minimax-oauth") or [{}])[0].get("access_token")
        or ""
    )

TOKEN = load_token()
print(f"[token] len={len(TOKEN)}", flush=True)

# ANCHOR — 7 atributos obligatorios. NUNCA recortar.
ALONDA = (
    "Alonda, a beautiful 26-year-old woman, "
    "platinum blonde long hair, striking emerald green eyes, "
    "slim athletic figure, delicate feminine facial features, "
    "natural realistic skin texture, "
)

START = 817
END = 836

LOOKS = {
    817: ("medusa_greek_mythology", ALONDA + "as the Greek Gorgon Medusa reimagined as a regal dark priestess, wearing a gown of woven emerald serpent scales, living emerald-green snakes coiling from her platinum blonde hair like living vines, holding a polished bronze mirror, in a shadowy Greek temple ruin with crumbling marble columns and golden hour sunlight slicing through, photorealistic, sharp, vivid emerald and gold tones, professional portrait photography"),
    818: ("athena_greek_mythology", ALONDA + "as the Greek goddess Athena, wearing a flowing ivory linen peplos with bronze greaves and an ornate crested Attic helmet pushed back, owl perched on her forearm, holding a spear and aegis shield, on the Acropolis of Athens at sunset with vivid orange and violet sky, photorealistic, sharp, vivid warm cinematic colors, classical portrait"),
    819: ("apollo_greek_mythology", ALONDA + "as a modern reimagining of the Greek sun god Apollo, wearing a tailored ivory suit with golden laurel embroidery, sunglasses in golden light, holding a vintage sunburst electric guitar, standing before a vivid sunset in Delos with marbled columns and Aegean Sea behind, photorealistic, sharp, vivid golden-hour cinematic colors"),
    820: ("afrodite_greek_mythology", ALONDA + "as the Greek goddess Aphrodite rising from the sea, wearing a shimmering rose-gold Grecian silk chiton clinging wet, hair flowing with foam and pearls, standing on a shell at sunrise on a vivid turquoise Aegean shore with rose petals drifting, photorealistic, sharp, vivid rose-gold and turquoise colors"),
    821: ("artemis_greek_mythology", ALONDA + "as the Greek goddess Artemis the hunter, wearing a short bronze-accented tunic in forest green and tan leather thigh-high boots, crescent-moon diadem in platinum hair, carrying a recurve bow with a silver arrow nocked, in a vivid moonlit pine forest with a silver stag beside her, photorealistic, sharp, vivid moonlit teal and silver tones"),
    822: ("freya_norse_mythology", ALONDA + "as the Norse goddess Freyja, wearing a magnificent amber-and-gold Viking gown with intricate metalwork, a massive amber necklace, falcon-feather cloak, chariot pulled by two vivid blue-grey Norwegian forest cats behind her, standing on a vivid rainbow bridge Bifrost at golden hour, photorealistic, sharp, vivid amber and gold tones"),
    823: ("thor_norse_mythology", ALONDA + "as a modern female reimagining of the Norse thunder god Thor, wearing an armored crimson leather corset with hammered silver Mjölnir motifs, a vivid electric-blue cape, holding a storm-charged hammer crackling with vivid blue-white lightning bolts, dramatic Icelandic storm clouds behind, photorealistic, sharp, vivid dramatic lightning colors"),
    824: ("loki_norse_mythology", ALONDA + "as the Norse trickster Loki, wearing an elegant emerald-green Asgardian suit with subtle gold serpent motifs, mischievous smirk, holding a glowing emerald staff, surrounded by holographic after-images of herself in different guises, in a vivid Asgardian hall with golden Bifrost light, photorealistic, sharp, vivid emerald and gold tones"),
    825: ("isis_egyptian_mythology", ALONDA + "as the Egyptian goddess Isis, wearing a form-fitting sheath dress in vivid royal blue and gold with hieroglyphic embroidery, dramatic winged gold headdress, ankh in one hand and sistrum in the other, standing before the Temple of Philae at golden hour with vivid Nile river and papyrus reeds, photorealistic, sharp, vivid royal blue and gold colors"),
    826: ("anubis_egyptian_mythology", ALONDA + "as a modern female reimagining of the Egyptian god Anubis, wearing a sleek jet-black structured bodysuit with vivid gold Egyptian funerary motifs, jackal-eared crown, holding an ankh-staff glowing vivid gold, in a vivid desert sunset at the pyramids of Giza with golden sand whirling, photorealistic, sharp, vivid gold and black tones"),
    827: ("free_climber_rock_face", ALONDA + "as an elite free climber halfway up a sheer vivid orange El Capitan granite face in Yosemite, wearing a vivid magenta climbing harness and cobalt-blue chalk-dusted tank top, fingers gripping tiny crimp holds, no ropes, dramatic plunging valley below in vivid emerald greens, photorealistic, sharp, vivid dynamic colors, adventure portrait"),
    828: ("skateboarder_bowl", ALONDA + "as a professional female skateboarder mid-trick on the lip of a vivid turquoise-and-pink painted concrete bowl in Venice Beach, wearing a vivid neon-yellow oversized hoodie, ripped jeans, vivid pink helmet, skateboarding shoes, arms out for balance, palm trees and vivid California sunset behind, photorealistic, sharp, vivid dynamic colors, sports photography"),
    829: ("parkour_urban", ALONDA + "as a female parkour traceuse captured mid-vault over a vivid graffiti-covered concrete barrier in a Tokyo backstreet, wearing a vivid crimson compression tank and jet-black athletic leggings, mid-leap with one hand on the wall, vivid neon street signs and Shibuya lights behind, photorealistic, sharp, vivid dynamic colors, action photography"),
    830: ("bmx_dirt_jump", ALONDA + "as a BMX dirt-jump rider mid-backflip on a vivid red dirt course at sunset, wearing a vivid electric-blue jersey, vivid orange helmet, gripping vivid yellow handlebars, dust exploding below, dramatic golden-hour backlight, photorealistic, sharp, vivid explosive colors, action sports photography"),
    831: ("kite_surfing_caribbean", ALONDA + "as a female kite-surfer airborne above vivid turquoise Caribbean water near Aruba, wearing a vivid fuchsia bikini and sunshine-yellow harness, gripping the control bar of a vivid magenta-and-yellow kite, dramatic blue sky with white cumulus, photorealistic, sharp, vivid saturated colors, action sports photography"),
    832: ("surfer_big_wave", ALONDA + "as a female big-wave surfer carving the face of a towering vivid teal wave at Mavericks California, wearing a vivid crimson wetsuit, blonde hair streaming water, board vivid canary yellow, dramatic white spray exploding behind, golden-hour backlight, photorealistic, sharp, vivid dramatic colors, sports photography"),
    833: ("cave_diver_underground", ALONDA + "as a female cave diver exploring a vivid cenote in Yucatan Mexico, wearing a black wetsuit with vivid lime-green accents and a vivid magenta dive helmet with twin headlamps piercing the crystal-clear vivid turquoise water, dramatic limestone formations and sunbeams from above, photorealistic, sharp, vivid underwater colors"),
    834: ("newscaster_tv_studio", ALONDA + "as a polished TV news anchor at a modern broadcast desk, wearing a vivid tailored cobalt-blue blazer over a crisp ivory blouse, vivid red manicured nails on the papers, the studio backdrop glowing with vivid teal and amber graphics, soft key light and crisp shadow, photorealistic, sharp, vivid professional newsroom colors, editorial portrait"),
    835: ("lawyer_courtroom", ALONDA + "as a distinguished female defense attorney in a high-ceilinged mahogany courtroom, wearing a tailored charcoal pinstripe suit with a vivid scarlet silk blouse, holding a leather-bound legal pad, American flag and judge bench in the background, dramatic chiaroscuro lighting, photorealistic, sharp, vivid cinematic courtroom colors, editorial portrait"),
    836: ("pediatrician_clinic", ALONDA + "as a warm pediatric doctor in a cheerful modern children's clinic, wearing a crisp white coat over a vivid sunny-yellow dress, a stethoscope with vivid rainbow tubing around her neck, holding a teddy bear and smiling warmly, vivid pastel walls with hot-air-balloon decals behind, photorealistic, sharp, vivid warm colors, professional portrait"),
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
        print(f"  HTTP {e.code}: {e.read().decode()[:300]}", flush=True)
    except Exception as e:
        print(f"  ERR: {e}", flush=True)
    return None

def download(url: str, dest: Path) -> bool:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=90, context=ctx) as r:
            dest.write_bytes(r.read())
        return True
    except Exception as e:
        print(f"  download ERR: {e}", flush=True)
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
            if (mx - mn) < 18:
                gray_count += 1
        ratio = gray_count / n
        print(f"  gray-ratio={ratio:.2f}", flush=True)
        return ratio > threshold
    except Exception as e:
        print(f"  gray-check ERR: {e}", flush=True)
        return False

results = []
for num in range(START, END + 1):
    if num not in LOOKS:
        continue
    key, prompt = LOOKS[num]
    fname = f"{num}_{key}.jpg"
    dest = OUT / fname
    print(f"\n[{num}] {key}", flush=True)
    if dest.exists() and dest.stat().st_size > 5000:
        print(f"  exists, skip", flush=True)
        results.append(num)
        continue
    attempt = 0
    while attempt < 3:
        url = gen(prompt)
        if not url:
            print(f"  no URL, skip", flush=True)
            break
        if not download(url, dest):
            attempt += 1
            continue
        sz = dest.stat().st_size
        if sz < 5000:
            print(f"  too small ({sz}b), retry", flush=True)
            attempt += 1
            continue
        if is_grayscale(dest):
            print(f"  ⚠️ too gray — regenerating (attempt {attempt+1}/3)", flush=True)
            dest.unlink(missing_ok=True)
            attempt += 1
            time.sleep(2)
            continue
        print(f"  saved {fname} ({sz:,} bytes)", flush=True)
        results.append(num)
        break
    if attempt >= 3 and num not in results:
        print(f"  ⚠️ gave up after {attempt} attempts", flush=True)
    time.sleep(2)

print(f"\n=== {len(results)}/{END - START + 1} generated ===", flush=True)
for n in results:
    print(f"  ok: {n}", flush=True)