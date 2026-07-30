#!/usr/bin/env python3
"""Generate Alonda portraits batch 441-460 - fresh unique themes (no repeats with 1-440)."""
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
_prov = auth.get("providers") or {}
_pool = auth.get("credential_pool") or {}
TOKEN=(_prov.get("minimax-oauth") or {}).get("access_token") or (_pool.get("minimax-oauth") or [{}])[0].get("access_token")
if not TOKEN:
    print("FATAL: no token", file=sys.stderr); sys.exit(2)
print(f"[token] len={len(TOKEN)}", flush=True)

ALONDA = (
    "Alonda, a beautiful 26-year-old woman, platinum blonde long hair, "
    "striking emerald green eyes, slim athletic figure, "
    "delicate feminine facial features, natural realistic skin texture, "
)

# Batch 441-460 - Completely new themes: engineering, deep ocean, time periods,
# food artisans, languages, music genres, transport, festivals, weather, etc.
PROMPTS = [
    ALONDA + "as a structural engineer inspecting a suspension bridge during sunset, hard hat and reflective vest, blueprint in hand, steel cables and concrete pylons behind, golden hour light, industrial photography, sharp details",
    ALONDA + "as a deep-sea submersible pilot in a cramped titanium cockpit, porthole showing bioluminescent jellyfish outside, pressure gauges glowing green, ultra-detailed sci-fi illustration, moody blue and teal lighting",
    ALONDA + "as a 1920s flapper in a beaded fringe dress and feathered headband, Charleston dance pose, art deco jazz club background with golden geometric patterns, warm amber spotlight, vintage photograph aesthetic, sepia tint",
    ALONDA + "as an Italian pizzaiola tossing dough in a wood-fired Naples pizzeria, flour dust in golden light, traditional oven flames behind, tomato and basil on marble counter, warm Mediterranean palette, candid photography",
    ALONDA + "as a Mexican lucha libre wrestler in a vibrant blue and gold mask with sequined cape, mid-pose in the ring, stadium lights, dramatic action shot, motion blur on cape, vivid colors, ultra-detailed",
    ALONDA + "as a Venetian gondoliera in striped shirt rowing through narrow canals, sunset reflecting on turquoise water, ancient palazzo walls, romantic golden light, cinematic travel photography",
    ALONDA + "as a Maasai warrior woman in traditional red shuka and beaded collar jewelry, vast African savanna at golden hour, acacia trees, dramatic sky with orange and pink, ethnographic portrait, sharp details",
    ALONDA + "as a geisha apprentice in Kyoto during cherry blossom season, white tabi socks, holding a wagasa paper umbrella, pink petals swirling, traditional wooden machiya street, soft pastel light, ultra-detailed",
    ALONDA + "as an Icelandic viking shield-maiden in fur cloak and chainmail, standing on a black sand beach with basalt cliffs, dramatic stormy sky, ravens flying, cinematic nordic photography, muted colors with red accents",
    ALONDA + "as a French patissier decorating an elaborate croquembouche in a Parisian bakery, gold leaf and spun sugar, soft bokeh of croissants in background, warm cream lighting, food photography, ultra detailed",
    ALONDA + "as a Swiss alpine mountaineer summiting the Matterhorn at dawn, ice axe in hand, oxygen mask on helmet, pink alpenglow on peaks, vast glacier valley below, dramatic mountain photography, vibrant sunrise",
    ALONDA + "as a Brazilian capoeira dancer mid-flip in a Salvador roda, white cordao de contas around neck, blue and white abada, motion blur, fellow capoeiristas clapping in circle, vibrant Afro-Brazilian backdrop",
    ALONDA + "as a Tibetan Buddhist nun in maroon robes holding a prayer wheel, spinning colorful prayer flags fluttering behind, snow-capped Himalayan peaks, golden morning light, spiritual portrait photography",
    ALONDA + "as a Norwegian cod fisher on a North Sea trawler deck at dawn, yellow oilskins and rubber boots, ropes and nets around, dramatic steel-gray sky, seabirds, harsh cold light, documentary photography",
    ALONDA + "as a Mexican taqueria owner flipping carnitas on a vertical trompo, flame and orange sparks flying, fresh cilantro and limes, vibrant Mercado background, warm tungsten light, street food photography",
    ALONDA + "as a Cuban salsa dancer in flowing red ruffled dress mid-spin, Havana street with crumbling colonial architecture, vintage car in background, golden hour light, motion blur on dress, vibrant colors",
    ALONDA + "as an Indian classical Bharatanatyam dancer in red and gold silk costume, temple gopuram background with carved deities, hands in mudra gesture, jasmine flowers in hair, golden warm light, ultra detailed",
    ALONDA + "as a Hawaiian hula dancer in traditional ti-leaf skirt and flower crown, volcanic black sand beach, ocean waves and palm trees, soft sunset, lei of orchids around neck, tropical photography, vibrant",
    ALONDA + "as a Mongolian eagle hunter on horseback across vast Altai steppe, golden eagle perched on gloved arm, dramatic winter sky, snow-dusted mountains, cold blue light, documentary photography, ultra detailed",
    ALONDA + "as a Moroccan spice merchant in a Marrakech medina, surrounded by colorful pyramids of saffron, paprika, and turmeric, fez hat, brass scales in hand, warm amber bazaar light, vibrant saturated colors, ultra detailed",
]

START = 441

def call_api(prompt, retries=2):
    url = "https://api." + "minimax" + ".io/v1/image_generation"
    body = json.dumps({"model": "image-01", "prompt": prompt, "size": "1024x1024", "n": 1}).encode()
    req = urllib.request.Request(url, data=body, headers={
        "Authorization": "Bearer " + TOKEN,
        "Content-Type": "application/json",
    })
    last_err = None
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, context=ctx, timeout=180) as r:
                d = json.loads(r.read().decode())
            urls = d.get("data", {}).get("image_urls") or []
            return urls[0], None
        except urllib.error.HTTPError as e:
            body_err = e.read().decode(errors='replace')[:300]
            last_err = f"HTTP {e.code}: {body_err}"
            if e.code == 429:
                time.sleep(15)
                continue
            if e.code in (500, 502, 503):
                time.sleep(5)
                continue
            return None, last_err
        except Exception as e:
            last_err = f"EXC: {e}"
            time.sleep(3)
    return None, last_err

def download(url, dest, retries=3):
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'curl/7.81'})
            with urllib.request.urlopen(req, context=ctx, timeout=180) as r:
                data = r.read()
            with open(dest, 'wb') as f:
                f.write(data)
            return True, None
        except Exception as e:
            if i == retries - 1:
                return False, str(e)
            time.sleep(2)
    return False, "max retries"

def is_gray(path, threshold=55.0):
    try:
        img = Image.open(path).convert('RGB')
        img.thumbnail((128, 128))
        px = list(img.getdata())
        if not px:
            return False, 0.0
        gc = sum(1 for p in px if max(p[0], p[1], p[2]) - min(p[0], p[1], p[2]) < 12)
        return 100.0 * gc / len(px) > threshold, 100.0 * gc / len(px)
    except Exception as e:
        return False, 0.0

def slug(s):
    keep = []
    for ch in s.lower():
        if ch.isalnum():
            keep.append(ch)
        elif ch in ' _-':
            keep.append('_')
    out = ''.join(keep)
    while '__' in out:
        out = out.replace('__', '_')
    return out.strip('_')[:50]

results = []
for i, prompt in enumerate(PROMPTS):
    num = START + i
    base_slug = slug(prompt[len(ALONDA):].strip(' ,').split(',')[0])
    fname = f"{num:03d}_{base_slug}.jpg"
    dest = OUT / fname

    print(f"[{i+1}/20] {fname}...", flush=True)

    # First attempt
    url, err = call_api(prompt)
    if not url:
        print(f"  ERR: {err}", flush=True)
        results.append({"num": num, "file": fname, "error": err})
        time.sleep(2)
        continue

    ok, derr = download(url, dest)
    if not ok:
        print(f"  DL ERR: {derr}", flush=True)
        results.append({"num": num, "file": fname, "error": f"dl: {derr}", "url": url})
        time.sleep(2)
        continue

    # grayscale check
    gray, pct = is_gray(dest)
    size_kb = dest.stat().st_size // 1024

    # If gray, retry once with a vibrant prompt
    if gray:
        print(f"  GRAY {pct:.1f}% — regenerating with vibrant prompt...", flush=True)
        vibrant = prompt + " vivid saturated colors, bright vibrant palette, rich tones, no grayscale, high chroma"
        url2, err2 = call_api(vibrant)
        if url2:
            ok2, derr2 = download(url2, dest)
            if ok2:
                gray2, pct2 = is_gray(dest)
                size_kb = dest.stat().st_size // 1024
                print(f"  REGEN ok {size_kb}KB gray={pct2:.1f}%", flush=True)
                results.append({"num": num, "file": fname, "url": url2, "size_kb": size_kb, "gray_pct": pct2})
                time.sleep(1.5)
                continue
        # fallback: keep original
        print(f"  REGEN failed, keeping original gray={pct:.1f}%", flush=True)
        results.append({"num": num, "file": fname, "url": url, "size_kb": size_kb, "gray_pct": pct, "still_gray": True})
    else:
        print(f"  ok {size_kb}KB gray={pct:.1f}%", flush=True)
        results.append({"num": num, "file": fname, "url": url, "size_kb": size_kb, "gray_pct": pct})

    time.sleep(1.5)

# Write summary
ok_count = sum(1 for r in results if "url" in r and not r.get("error"))
print(f"\n=== SUMMARY ===\nGenerated: {ok_count}/20")
out_json = OUT.parent / "scripts" / f"batch_{START}_{START+19}_results.json"
out_json.write_text(json.dumps(results, indent=2))
print(f"Wrote {out_json}")
