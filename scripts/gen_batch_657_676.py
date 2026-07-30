#!/usr/bin/env python3
"""Generate Alonda portraits batch 657-676 - new themes.
Mix: Greek myths (Medusa, Persephone, Hecate, Hephaestus), Norse myths (Odin, Freya),
Egyptian myths (Isis, Anubis), extreme sports (skydiving, free solo, big-wave),
modern professions (UX designer, neurosurgeon, sommelier), retro years (1980s aerobics, 1990s grunge).
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
    ALONDA + "as the Greek myth Medusa reimagined as a tragic heroine, emerald snakes coiled in platinum hair, golden circlet, vivid crimson cape draped over shoulder, holding a polished bronze mirror reflecting her own sorrowful gaze, vivid volcanic Greek island backdrop with cobalt sea, dramatic chiaroscuro light, vivid mythological portrait, ultra detailed",
    ALONDA + "as Persephone Greek queen of the underworld at the threshold between vivid emerald spring meadow above and cobalt shadowy Hades below, holding a vermilion pomegranate, white peplos with saffron trim, silver diadem, vivid dual-toned atmosphere split lighting, vivid mythological portrait, ultra sharp",
    ALONDA + "as Hecate Greek goddess of magic at a vivid triple crossroads lit by three towering torches, holding two spirit hounds on silver leashes, vivid midnight indigo robes shimmering with stars, crescent moon crown, swirling silver mist, vivid dark mythological portrait, ultra detailed",
    ALONDA + "as Hephaestus Greek god of the forge reimagined in a vivid volcanic smithy hammering a glowing vermilion blade on a brass anvil, vivid amber sparks flying, cobalt smith apron, golden prosthetic arm reflecting furnace light, vivid Olympian forge portrait, ultra sharp",
    ALONDA + "as Odin Norse Allfather on the rainbow bridge Bifrost with two cobalt ravens Huginn and Muninn perched on her shoulders, vivid silver eyepatch, golden spear Gungnir, vermilion and indigo Norse cloak, dramatic aurora borealis overhead, vivid Norse mythology portrait, ultra detailed",
    ALONDA + "as Freya Norse goddess of love and war riding a chariot pulled by vivid cobalt cats through a vivid saffron wheat field at golden hour, golden amber necklace Brisingamen, vivid vermilion feathered cloak, golden tears on cheek, vivid Nordic mythology portrait, ultra sharp",
    ALONDA + "as Isis Egyptian goddess of magic with vivid gilded falcon-wing headdress, ankh in one hand and vivid vermilion throne in the other, white linen sheath dress, vivid lapis lazuli and gold jewelry, dramatic Nile sunset behind, vivid Egyptian mythology portrait, ultra detailed",
    ALONDA + "as Anubis Egyptian god of mummification reimagined as a fierce jackal-headed guardian at a vivid saffron gilded temple gate, vivid cobalt weighing scales of justice, golden ankh collar, dramatic desert sunset, vivid Egyptian underworld portrait, ultra sharp",
    ALONDA + "as a tandem skydiver in freefall at 14000 feet with a vivid cobalt and saffron parachute just deployed, vivid vermilion jumpsuit, goggles pushed up on forehead, dramatic cloud formations and emerald patchwork farmland far below, vivid extreme sports adrenaline portrait, ultra detailed",
    ALONDA + "as a free-solo rock climber mid-ascent on a vivid sheer granite El Capitan wall with no ropes, vivid chalked hands gripping vermilion rock, white and cobalt climbing shoes, dramatic vertigo perspective of the valley below, vivid climbing portrait, ultra sharp",
    ALONDA + "as a big-wave surfer paddling into a towering vivid cobalt wave at Mavericks with a vivid vermilion and saffron surfboard, black wetsuit hood, spray exploding behind, dramatic Pacific storm light, vivid extreme ocean portrait, ultra detailed",
    ALONDA + "as a UX designer in a modern San Francisco studio presenting wireframes on a vivid 32-inch monitor showing a magenta and emerald mobile app interface, white headphones around neck, vivid saffron sticky notes covering a glass board, latte on desk, vivid tech portrait, ultra sharp",
    ALONDA + "as a neurosurgeon in a vivid ultramodern operating theater mid-procedure with a vivid magnified surgical microscope and vivid emerald and cobalt neuronavigation screens, teal scrubs and vermilion surgical cap, focused gaze, dramatic overhead lamp, vivid medical portrait, ultra detailed",
    ALONDA + "as a master sommelier in a Burgundy wine cellar holding a vivid crystal snifter swirling deep crimson Grand Cru wine, vivid cobalt cellar archways with stacked oak barrels, vermilion tasting apron, dramatic cellar torch light, vivid wine portrait, ultra sharp",
    ALONDA + "as a master watchmaker in a Swiss Geneva atelier assembling a vivid mechanical tourbillon movement under a vivid jeweler's loupe, cobalt tweezers, hundreds of tiny golden and ruby gears laid on vermilion felt mat, magnifying lamp, vivid horology portrait, ultra detailed",
    ALONDA + "as a 1980s Los Angeles aerobics instructor in a vivid neon leotard with leg warmers and a vivid sweatband, holding a vivid cassette player with tangled headphones, vivid magenta and turquoise aerobics studio with mirrors, big hair and bright blush, vivid retro 80s fitness portrait, ultra sharp",
    ALONDA + "as a 1990s Seattle grunge musician in a flannel shirt and ripped jeans, holding a vivid sunburst Fender Stratocaster guitar, vivid smoky dive bar stage with vermilion and cobalt stage lights, messy platinum hair, smudged eyeliner, vivid 90s grunge music portrait, ultra detailed",
    ALONDA + "as a biodynamic viticulturist in an Alsatian vineyard at dawn inspecting vivid purple Pinot Noir grape clusters on the vine, straw hat, vermilion rain boots, leather notebook, vivid emerald vineyard rows stretching into mist, vivid sustainable wine farming portrait, ultra sharp",
    ALONDA + "as an Alpine cheese affineur in a Swiss mountain cave maturing wheels of Gruyere on vivid spruce wood shelves, vivid cobalt and amber cave atmosphere, white apron, wooden curd knife, vivid cave wine cellar of cheese portrait, ultra detailed",
    ALONDA + "as a master chocolatier in a Brussels atelier tempering vivid vermilion and emerald couverture chocolate on a polished marble slab, vivid magenta cocoa pods hanging as decoration, gold leaf, dramatic atelier light, vivid Belgian chocolatier portrait, ultra sharp",
]

START = 657

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

Path("/root/alonda/scripts/batch_657_676_results.json").write_text(json.dumps(results, indent=2))
print(f"\n[DONE] {len(results)}/{len(PROMPTS)} generated", flush=True)
