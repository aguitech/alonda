#!/usr/bin/env python3
"""Generate Alonda portraits batch 697-716 - new themes.
Mix: Celtic myths (Morrigan, Brigid, Cerridwen), Hindu myths (Parvati, Saraswati, Lakshmi),
Slavic myths (Baba Yaga, Rusalka, Svarog), sci-fi fantasy (Dune Fremen, Witcher, Mandalorian,
Mass Effect, Horizon Zero Dawn), global street markets (Marrakesh, Bangkok, Istanbul),
rare weather phenomena, modern subcultures (visual kei, e-girl, cottagecore, dark academia).
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
KEY = "minimax" + "-oauth"
TOKEN = (_prov.get(KEY) or {}).get("access_token") or (_pool.get(KEY) or [{}])[0].get("access_token")
if not TOKEN:
    print("FATAL: no token", file=sys.stderr); sys.exit(2)
print(f"[token] len={len(TOKEN)}", flush=True)

ALONDA = (
    "Alonda, a beautiful 26-year-old woman, platinum blonde long hair, "
    "striking emerald green eyes, slim athletic figure, "
    "delicate feminine facial features, natural realistic skin texture, "
)

PROMPTS = [
    ALONDA + "as the Celtic war goddess The Morrigan perched on a vivid neon-lit basalt pillar above a vivid violet battlefield at twilight, vivid raven feathers cascading from her hair, vivid cobalt and vermilion raven-scale armor, vivid glowing emerald eye, vivid dramatic war-goddess portrait, ultra sharp",
    ALONDA + "as the Celtic fire goddess Brigid tending vivid saffron flames in a vivid Kildare sacred hearth at Samhain night, vivid saffron woven cloak, vivid cowslip and snowdrop garlands in platinum hair, vivid molten gold holy fire, vivid Celtic divine smith portrait, ultra detailed",
    ALONDA + "as the Celtic moon goddess Cerridwen stirring a vivid cosmic cauldron of vivid nebula-blue Awen potion under a vivid full moon, vivid silver crescent headdress, vivid owl feathers in her cloak, vivid steaming iridescent brew, vivid Celtic sorceress portrait, ultra sharp",
    ALONDA + "as the Hindu goddess Parvati in a vivid Mumbai street art mural pose holding a vivid vermilion lotus, vivid saffron silk sari with vivid emerald zari border, vivid gold nath nose ring, vivid marigold garlands piled around, vivid Hindu divine feminine portrait, ultra detailed",
    ALONDA + "as the Hindu goddess Saraswati playing a vivid golden veena on a vivid white lotus at dawn, vivid ivory silk sari, vivid peacock feather tucked behind her ear, vivid flowing water from her vina, vivid stack of sacred manuscripts at her feet, vivid wisdom goddess portrait, ultra sharp",
    ALONDA + "as the Hindu goddess Lakshmi standing amid a vivid shower of vivid vermilion and saffron and gold coins and lotus petals during Diwali, vivid emerald and crimson silk sari, vivid gold jewelry, vivid glowing oil lamps flanking her, vivid prosperity goddess portrait, ultra detailed",
    ALONDA + "as the Slavic forest witch Baba Yaga in a vivid bioluminescent mushroom forest clearing beside her vivid walking hut on vivid neon-orange chicken legs, vivid cobalt mortar pestle, vivid wild boar skull headdress, vivid emerald moss carpet, vivid dark Slavic folklore portrait, ultra sharp",
    ALONDA + "as the Slavic water spirit Rusalka combing her hair at midnight beside a vivid turquoise moonlit river, vivid waterlogged linen dress trailing into the river, vivid pale luminescent skin glow, vivid emerald riverweed in hair, vivid mournful Slavic water nymph portrait, ultra detailed",
    ALONDA + "as the Slavic forge god Svarog hammering a vivid glowing crimson blade on a vivid celestial anvil above vivid storm clouds, vivid molten sparks cascading, vivid cobalt blacksmith apron, vivid lightning halo, vivid Slavic sky smith deity portrait, ultra sharp",
    ALONDA + "as a Dune Fremen warrior of Arrakis sipping vivid emerald water from a vivid cylindrical stilltent catchpocket in a vivid vermilion desert at twilight, vivid deep brown stillsuit with vivid water-ring tubes, vivid pale blue within-blue eyes emphasized by vivid spice, vivid orange sky, vivid sci-fi desert portrait, ultra detailed",
    ALONDA + "as a Witcher of the School of the Wolf in a vivid Kaer Morhen courtyard at dusk holding a vivid steel longsword inscribed with runes, vivid cobalt leather armor with vivid silver wolf medallion, vivid emerald cat-eye contacts, vivid orange witcher mutagens glowing softly, vivid dark fantasy warrior portrait, ultra sharp",
    ALONDA + "as a Mandalorian bounty hunter of Clan Vizsla inside a vivid cobalt-lit razor crest cockpit in vivid hyperspace, vivid beskar helmet reflecting vivid starlight, vivid vermilion cape, vivid blaster rifle across her lap, vivid green alien child sleeping in the rear seat, vivid Star Wars sci-fi portrait, ultra detailed",
    ALONDA + "as a Mass Effect Spectre aboard a vivid Citadel presidium skycar with vivid Citadel dome backdrop and vivid nebula through the window, vivid N7 crimson white armor plates, vivid omni-tool glowing cobalt on her wrist, vivid biotic cyan aura flickering, vivid sci-fi commander portrait, ultra sharp",
    ALONDA + "as a Horizon Zero Dawn Nora huntress in a vivid Colorado Plateau canyon at sunrise climbing a vivid red sandstone spire with a vivid amber bow slung across her back, vivid leather and woven plant-fiber armor, vivid Focus headpiece over one eye, vivid green mechanical creatures on horizon, vivid post-apocalyptic tribal hunter portrait, ultra detailed",
    ALONDA + "as a Marrakesh spice market vendor in a vivid ochre-walled souk stall surrounded by vivid piles of vivid saffron paprika turmeric and vivid rose petals, vivid cobalt kaftan with vivid gold embroidery, vivid stacked brass bowls, vivid Atlas Mountains glowing amber through the arched doorway, vivid Moroccan market portrait, ultra sharp",
    ALONDA + "as a Bangkok floating market vendor poling a vivid longtail boat piled high with vivid mango rambutan and vivid dragon fruit at dawn, vivid vermilion conical hat, vivid saffron sampan boat, vivid emerald and magenta water lilies floating, vivid tropical market portrait, ultra detailed",
    ALONDA + "as a Grand Bazaar carpet merchant in vivid Istanbul examining a vivid hand-knotted crimson and emerald Turkish kilim unfurled across vivid stone steps, vivid emerald and gold Ottoman jacket, vivid haggard merchant gaze, vivid blue mosque dome visible through arch, vivid Istanbul bazaar portrait, ultra sharp",
    ALONDA + "as a visual kei musician backstage at a vivid Tokyo Shinjuku live house applying vivid cobalt and magenta eyeliner and vivid chalk-white foundation, vivid vermilion teased hair piled into vivid neon-streaked spikes, vivid silver platform boots, vivid Japanese alternative fashion portrait, ultra detailed",
    ALONDA + "as a cottagecore baker in a vivid Cotswolds stone cottage kitchen pulling a vivid golden sourdough loaf from a vivid cast iron AGA oven at golden hour, vivid cream linen apron, vivid wildflower crown of cornflowers and poppies, vivid ceramic mixing bowls on a vivid oak counter, vivid pastoral cozy portrait, ultra sharp",
    ALONDA + "as a dark academia literature student in a vivid Oxford Bodleian library reading room at dusk surrounded by vivid towering oak bookshelves, vivid burgundy velvet blazer with vivid gold buttons, vivid green-shaded brass reading lamp, vivid stack of leather-bound classics, vivid scholarly portrait, ultra detailed",
]

START = 697

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

Path("/root/alonda/scripts/batch_697_716_results.json").write_text(json.dumps(results, indent=2))
print(f"\n[DONE] {len(results)}/{len(PROMPTS)} generated", flush=True)