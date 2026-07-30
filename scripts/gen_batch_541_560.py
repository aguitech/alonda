#!/usr/bin/env python3
"""Generate Alonda portraits batch 541-560 - completely new themes.
Themes mix: extreme sports (BMX/parkour/kitesurf), astrophysics, steampunk,
            mythology, deep-sea exploration, body-paint festivals, herbalism,
            Bauhaus design, cave painting restoration, kabuki theater,
            renewable energy engineering, botanical illustration, arctic explorer,
            Polish szopka nativity builder, Indonesian batik tulis, Persian carpet dyer,
            Cape Malay cook, Corsican polyphony singer, Sami joik vocalist,
            Argentinian tango milonga dancer, Brazilian capoeira angola roda player
"""
import json, ssl, urllib.request, urllib.error, time, sys
from pathlib import Path
from PIL import Image

OUT = Path("/root/alonda/assets/images")
OUT.mkdir(parents=True, exist_ok=True)

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

auth = json.loads(Path("/root/.hermes/auth.json").read_text())
_prov = auth.get("providers") or {}
_pool = auth.get("credential_pool") or {}
_provider_key = "minimax" + "-oauth"
TOKEN = (_prov.get(_provider_key) or {}).get("access_token") or (_pool.get(_provider_key) or [{}])[0].get("access_token")
if not TOKEN:
    print("FATAL: no token", file=sys.stderr); sys.exit(2)
print(f"[token] len={len(TOKEN)}", flush=True)

ALONDA = (
    "Alonda, a beautiful 26-year-old woman, platinum blonde long hair, "
    "striking emerald green eyes, slim athletic figure, "
    "delicate feminine facial features, natural realistic skin texture, "
)

PROMPTS = [
    ALONDA + "as a BMX rider mid-tailwhip over a graffiti-covered concrete bowl at a vibrant Barcelona skatepark, vivid magenta helmet and acid green frame, motion blur on bike, vivid cobalt sky and amber sun flares, action sports photography, ultra sharp",
    ALONDA + "as a parkour traceur vaulting between vivid saffron yellow and crimson rooftops in a Lisbon miradouro, black athletic wear with electric blue compression sleeves, sunset golden hour, vivid terracotta tile and Atlantic blue, urban sport portrait, ultra detailed",
    ALONDA + "as a kitesurfing champion mid-jump over vivid turquoise shallows in Tarifa Spain, vivid cobalt and saffron kite above, wetsuit in neon coral, Atlantic spray, dramatic cumulus clouds, vivid tropical action photography, ultra sharp",
    ALONDA + "as a quantum physicist in a Geneva CERN control room staring at a vivid holographic visualization of particle collision data, white lab coat, vivid magenta and electric cyan holographic displays, glowing chamber lights, science portrait, ultra detailed",
    ALONDA + "as a steampunk airship engineer in a brass and rivet workshop calibrating a glowing amber aether pressure gauge on a Victorian zeppelin gondola, copper goggles on forehead, vivid mahogany and emerald velvet workshop, alt-history portrait, ultra sharp",
    ALONDA + "as a Hestia Greek goddess tending a vivid hearth fire inside a marble Greek temple at dusk, flowing ivory chiton with crimson sash, vivid amber flames and olive branches, smoke rising into twilight cobalt sky, mythological portrait, ultra detailed",
    ALONDA + "as a deep-sea submersible pilot inside a titanium acrylic-domed bathyscaphe descending through vivid cobalt water, pressure gauge glowing amber, vast bioluminescent jellies outside the dome, dark abyss below, vivid teal and emerald glows, exploration portrait, ultra sharp",
    ALONDA + "as a body-paint festival performer at Brazil's Parintins folkloric festival painted in vivid cobalt and gold boi-bumbá designs, feathered headdress, vivid emerald jungle backdrop, drum beats suggested, vibrant cultural portrait, ultra detailed",
    ALONDA + "as an herbalist apothecary in a Provence stone cottage grinding vivid dried lavender and rose petals in a brass mortar, bundles of herbs hanging from ceiling, vivid violet and saffron, copper pots and amber tincture bottles, craft portrait, ultra sharp",
    ALONDA + "as a Bauhaus textile designer in a 1920s Weimar workshop painting bold geometric patterns on a loom-woven rug, vivid primary red blue and yellow, black turtleneck and bob haircut, bright modernist studio, design movement portrait, ultra detailed",
    ALONDA + "as a prehistoric cave painting conservator in Lascaux France carefully stabilizing a vivid ochre bison painting on limestone wall, white conservation suit, headlamp glow, vivid rust red and charcoal charcoal marks, archaeology portrait, ultra sharp",
    ALONDA + "as a kabuki theater performer in vivid crimson shikomi kumadori stage makeup and gold brocade kimono, white tabi socks on stage, vivid indigo backdrop with painted cherry tree, kumiko folding screen, dramatic stage lighting, traditional performing arts portrait, ultra detailed",
    ALONDA + "as a tidal energy engineer in a Scottish Orkney substation inspecting a vivid green turbine blade being lowered by crane at golden hour, hard hat and high-vis vest, vivid amber sunset and Atlantic steel blue sea, sustainable engineering portrait, ultra sharp",
    ALONDA + "as a botanical illustrator in a Victorian glasshouse at Kew Gardens painting a vivid crimson orchid specimen with a sable brush, watercolor palette on side table, emerald tropical foliage surrounding, soft skylight, vintage botanical art portrait, ultra detailed",
    ALONDA + "as an Arctic polar explorer standing at the bow of an icebreaker in vivid cobalt Svalbard fjord at midnight sun, red fur-trimmed parka, frost in eyebrows, vivid magenta dawn horizon, massive blue glacier in background, expedition portrait, ultra sharp",
    ALONDA + "as a Polish szopka nativity builder in a Kraków workshop crafting a vivid cathedral-shaped Christmas crèche with copper foil and colored tissue, vivid warm chapel lights, tiny spires and stained glass windows, vivid traditional folk craft portrait, ultra detailed",
    ALONDA + "as an Indonesian batik tulis artisan in a Yogyakarta workshop applying molten wax to undyed cotton with a canting tool in vivid indigo and soga brown, traditional kebaya blouse, vivid tropical garden courtyard, heritage craft portrait, ultra sharp",
    ALONDA + "as a Persian carpet natural dyer in a Kashan workshop stirring a vivid madder-root crimson dye bath with copper tongs, vivid saffron yellow skeins hanging above, terracotta walls, vivid sunset light, Iranian craft portrait, ultra detailed",
    ALONDA + "as a Cape Malay curry cook in a Bo-Kaap Cape Town kitchen stirring a vivid golden turmeric and cinnamon breyani pot, vivid magenta and lime green painted walls, copper pestle, vivid coral and emerald spice jars, South African food portrait, ultra sharp",
    ALONDA + "as a Corsican polyphonic paghjella singer in a cliffside village chapel at twilight, traditional black mourning shawl, three female singers behind her, vivid Mediterranean cobalt sea visible through window, golden candlelight, ethnographic music portrait, ultra detailed",
]

START = 541

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
                time.sleep(15); continue
            if e.code in (500, 502, 503):
                time.sleep(5); continue
            return None, last_err
        except Exception as e:
            last_err = repr(e)
            time.sleep(3)
    return None, last_err

def is_gray(path, threshold=0.55):
    try:
        im = Image.open(path).convert("RGB").resize((128, 128))
        gray = 0
        total = 0
        for px in im.getdata():
            r, g, b = px
            mn, mx = min(r, g, b), max(r, g, b)
            sat = (mx - mn) / 255.0 if mx else 0
            if sat < 0.10:
                gray += 1
            total += 1
        return (gray / total) > threshold
    except Exception:
        return False

results = []
for i, prompt in enumerate(PROMPTS):
    n = START + i
    body = prompt[len(ALONDA):] if prompt.startswith(ALONDA) else prompt
    slug = body[:60].strip().replace(",", "").replace(".", "").replace(" ", "_").replace("'", "").replace('"', '').lower()[:60]
    fname = f"{n}_" + slug + ".jpg"
    out_path = OUT / fname
    print(f"\n=== [{n}] {fname} ===", flush=True)
    attempts = 0
    success = False
    while attempts < 3:
        url, err = call_api(prompt)
        if not url:
            print(f"  [err] {err}", flush=True); break
        try:
            with urllib.request.urlopen(url, context=ctx, timeout=120) as r:
                data = r.read()
            tmp = OUT / f".tmp_{n}_{int(time.time())}.jpg"
            tmp.write_bytes(data)
            if is_gray(tmp):
                tmp.unlink()
                print(f"  [gray] regenerating...", flush=True)
                attempts += 1
                continue
            tmp.rename(out_path)
            print(f"  [ok] {len(data)} bytes", flush=True)
            results.append({"num": n, "file": fname, "url": url})
            success = True
            break
        except Exception as e:
            print(f"  [dl-err] {e}", flush=True); attempts += 1
    if not success:
        print(f"  [fail] too gray or too many errors", flush=True)
    time.sleep(2)

Path("/root/alonda/scripts/batch_541_560_results.json").write_text(json.dumps(results, indent=2))
print(f"\n[DONE] {len(results)}/{len(PROMPTS)} generated", flush=True)
