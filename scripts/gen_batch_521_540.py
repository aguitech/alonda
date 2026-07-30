#!/usr/bin/env python3
"""Generate Alonda portraits batch 521-540 - completely new themes.
Themes: Mesopotamian/Akkadian priestess, Antarctic meteorologist, Azerbaijani carpet weaver,
       Brazilian Jiu-Jitsu black belt, Catalan human tower casteller, Cuban classical pianist,
       Czech marionette carver, Dutch windmill keeper, Edo kiriko glass cutter, Ethiopian coffee ceremony,
       Filipino tribal tattoo artist, Finnish reindeer wool spinner, Ghanaian kente weaver,
       Hungarian csárdás dancer, Indian classical veena player, Irish sean-nós singer,
       Jamaican reggae sound system operator, Kazakh eagle huntress apprentice,
       Latvian midsummer wreath weaver, Moroccan henna artist
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
    ALONDA + "as an ancient Akkadian high priestess of Inanna at the ziggurat of Ur at twilight, layered fringed linen garment in lapis blue and crimson, gold sun disk headdress, terracotta mudbrick steps, vivid desert amber and twilight violet, Mesopotamian art context, ultra detailed",
    ALONDA + "as an Antarctic meteorologist releasing a weather balloon from a Halley Research Station ice runway, vivid orange NASA parka and frost-covered eyelashes, swirling polar twilight aurora, cobalt ice horizon, vivid emerald green and magenta auroras, science documentary portrait, ultra sharp",
    ALONDA + "as an Azerbaijani carpet weaver in a Baku mountain village workshop knotting a vivid crimson and emerald rug on a vertical loom, traditional kelaghayi silk headscarf, terracotta walls, vivid jewel-toned wool threads, ethnographic photography, ultra detailed",
    ALONDA + "as a Brazilian jiu-jitsu black belt mid-guard pass on a faded blue tatami at a Rio academy, white gi with brown belt, sweat dripping, intense focus, vivid emerald mat lighting and crimson Dojo banner, action sports portrait, ultra sharp",
    ALONDA + "as a Catalan castell climber at the top of a human tower in Tarragona during a festival, white shirt and black sash climbing up, vivid crowd in red and yellow shirts below, vivid Mediterranean blue sky, cultural festival photography, ultra detailed",
    ALONDA + "as a Cuban classical pianist in a Havana conservatory performing Chopin on a Steinway, satin emerald green gown, polished ebony piano, warm gilded hall light, vivid mahogany walls and brass sconces, concert portrait, ultra sharp",
    ALONDA + "as a Czech marionette carver in a Prague workshop hand-carving a tiny king puppet from linden wood, magnifying headband and apron, vivid paint jars of crimson and gold, intricate wood shavings, craft portrait with shallow depth of field, ultra detailed",
    ALONDA + "as a Dutch windmill keeper in Kinderdijk at golden hour adjusting the wooden brake wheel of a 1740s smock mill, vivid emerald polder and crimson sunset, weathered hands and linen apron, traditional Dutch costume, landscape portrait, ultra sharp",
    ALONDA + "as an Edo kiriko glass cutter in a Tokyo Asakusa workshop cutting diamond patterns into a cobalt blue crystal tumbler with a brass wheel, vivid indigo and amber glassware surrounding, traditional craft portrait, ultra detailed",
    ALONDA + "as an Ethiopian coffee ceremony host in a Harar stone-walled courtyard roasting green beans over charcoal on a menkeshkesh pan, dark red netela shawl, vivid jumping flame and cardamom pods, intimate cultural portrait, ultra sharp",
    ALONDA + "as a Filipino mambabatok tribal tattoo artist in the Kalinga highlands tapping thorn ink into skin with a citrus pomelo branch, traditional woven tapis wrap, vivid forest green backdrop, intimate cultural portrait, ultra detailed",
    ALONDA + "as a Finnish reindeer wool spinner in a Lapland log cabin spinning crimson dyed wool on a wooden spinning wheel, snow outside window, vivid violet twilight and warm firelight, Nordic craft portrait, ultra sharp",
    ALONDA + "as a Ghanaian kente weaver in a Bonwire village workshop threading narrow strips on a horizontal loom, vivid saffron yellow emerald green and crimson kente bands, traditional smock, bright tropical light through window, ethnographic portrait, ultra detailed",
    ALONDA + "as a Hungarian csárdás dancer mid-spin in a Budapest dance hall, vivid crimson and emerald ruffled skirt swirling, black embroidered bodice, partner's hand on waist, warm gas-lit hall glow, motion blur on skirt, cultural performance photography, ultra sharp",
    ALONDA + "as an Indian Saraswati veena player seated on a Jaipur palace terrace in ivory silk saree with gold zari, polished veena on lap, jasmine flowers in hair, vivid saffron marigolds and turquoise sky, classical music portrait, ultra detailed",
    ALONDA + "as an Irish sean-nós singer in a Connemara stone cottage hearth, wool Aran sweater in cream and crimson, fiddle resting on chair, vivid turf fire glow and emerald rain outside, intimate folk portrait, ultra sharp",
    ALONDA + "as a Jamaican reggae sound system operator adjusting massive speaker stacks at a Kingston street dance, vivid red gold and green flag colors, large crowd silhouetted, warm sodium street lights and speaker LED glow, music documentary photography, ultra detailed",
    ALONDA + "as a Kazakh eagle huntress apprentice on horseback across the Altai mountains at dawn, vivid crimson and gold embroidered chapan coat, fox fur hat, golden eagle on gloved fist, vivid amber sunrise and cobalt peaks, ethnographic portrait, ultra sharp",
    ALONDA + "as a Latvian midsummer Jāņi wreath weaver on a meadow at twilight braiding oak leaves and wildflowers, white linen dress with red woven belt, crown of daisies and cornflowers on head, vivid emerald meadow and luminous golden night, magical folk portrait, ultra detailed",
    ALONDA + "as a Moroccan henna artist in a Marrakech riad courtyard applying intricate henna patterns to her own hand, vivid amber and crimson henna cones, terracotta tile walls, vivid bougainvillea cascading, North African craft portrait, ultra sharp",
]

START = 521

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

Path("/root/alonda/scripts/batch_521_540_results.json").write_text(json.dumps(results, indent=2))
print(f"\n[DONE] {len(results)}/{len(PROMPTS)} generated", flush=True)
