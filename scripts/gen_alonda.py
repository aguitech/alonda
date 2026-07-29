#!/usr/bin/env python3
"""Generate 10 hyper-realistic images of Alonda — different looks, anchored persona."""
import json, ssl, urllib.request, urllib.error, time
from pathlib import Path

OUT = Path("/root/alonda/assets/images")
OUT.mkdir(parents=True, exist_ok=True)

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

auth = json.loads(Path("/root/.hermes/auth.json").read_text())
TOKEN = auth["providers"]["minimax-oauth"]["access_token"]
print(f"[token] len={len(TOKEN)}")

# Anchored persona — kept short & vivid (avoid over-constraining)
ALONDA = (
    "beautiful 26-year-old woman named Alonda, "
    "platinum blonde long hair, slim athletic hourglass figure, "
    "striking emerald green eyes, delicate refined features, "
    "soft skin, high cheekbones, "
)

# 10 distinct looks — each: simple, vivid, hyperrealism cue, no over-spec
LOOKS = {
    "01_beach_bikini": (
        ALONDA +
        "wearing a white triangle bikini, standing on a tropical sandy beach, "
        "turquoise water behind, golden hour sunlight, "
        "photorealistic, sharp, vivid natural colors, professional photography"
    ),
    "02_black_dress": (
        ALONDA +
        "wearing an elegant fitted little black dress, standing in a luxury hotel lobby, "
        "marble floors, warm chandelier lighting, "
        "photorealistic, sharp focus, vivid colors, professional photography"
    ),
    "03_red_evening": (
        ALONDA +
        "wearing a flowing red satin evening gown, walking on a city street at night, "
        "neon reflections on wet pavement, "
        "photorealistic, vivid saturated colors, cinematic, sharp"
    ),
    "04_gym_sporty": (
        ALONDA +
        "wearing a black sports bra and high-waisted leggings, in a modern gym, "
        "doing a confident pose, natural athletic lighting, "
        "photorealistic, sharp, vivid, professional photography"
    ),
    "05_casual_denim": (
        ALONDA +
        "wearing a white crop top and high-waisted blue jeans, sitting on a cafe chair, "
        "Parisian sidewalk cafe background, soft daylight, "
        "photorealistic, sharp, vivid natural colors"
    ),
    "06_loungewear_home": (
        ALONDA +
        "wearing a soft cream silk robe, sitting on a luxury sofa, "
        "cozy modern living room, warm lamp lighting, "
        "photorealistic, sharp, vivid, natural skin tones"
    ),
    "07_pool_party": (
        ALONDA +
        "wearing a colorful tropical print swimsuit, sitting on a pool edge, "
        "blue swimming pool water, summer sunlight, palm trees in background, "
        "photorealistic, sharp, vivid bright colors"
    ),
    "08_office_pro": (
        ALONDA +
        "wearing a fitted navy blue blazer and white silk blouse, "
        "standing in a modern office with skyline view, "
        "professional confident pose, natural window lighting, "
        "photorealistic, sharp, vivid, professional photography"
    ),
    "09_beach_coverup": (
        ALONDA +
        "wearing a sheer white beach coverup over a swimsuit, "
        "standing at the shoreline with waves washing her feet, "
        "sunset golden light, wind blowing her hair, "
        "photorealistic, sharp, vivid colors, golden hour glow"
    ),
    "10_casual_selfie": (
        ALONDA +
        "wearing a casual oversized beige sweater, "
        "close-up portrait selfie style, soft natural window light, "
        "slight playful smile, modern apartment background, "
        "photorealistic, sharp, vivid natural skin, intimate portrait"
    ),
}

def gen(prompt: str, size: str = "1024x1024") -> str | None:
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
        print(f"  HTTP {e.code}: {e.read().decode()[:200]}")
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

results = []
for i, (key, prompt) in enumerate(LOOKS.items(), 1):
    print(f"\n[{i}/10] {key}")
    print(f"  prompt: {prompt[:90]}...")
    url = gen(prompt)
    if not url:
        print(f"  ❌ no URL")
        continue
    dest = OUT / f"{key}.jpeg"
    if download(url, dest):
        print(f"  ✅ {dest.name} ({dest.stat().st_size:,} bytes)")
        results.append(key)
    time.sleep(2)  # politeness

print(f"\n=== Summary: {len(results)}/10 ===")
for k in results:
    print(f"  ✅ {k}")
print(f"\nSaved to {OUT}")