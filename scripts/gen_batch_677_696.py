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
    ALONDA + "as a Serbian gusle epic singer on a vivid misty Balkan mountain cliff at dawn, vivid vermilion embroidered vest, vivid cobalt and saffron folk skirt, single-string gusle carved with serpent motifs, vivid dramatic dawn portrait, ultra sharp",
    ALONDA + "as a Tibetan Buddhist sand mandala artist kneeling in vivid saffron robes inside a vivid Himalayan monastery grinding vivid turquoise and vermilion and amber mineral pigments into fine sand, brass funnels laid out in precise rainbow rows, vivid meditative craft portrait, ultra detailed",
    ALONDA + "as a Mongolian contortionist performing on a vivid crimson and gold silk carpet inside a vivid felt ger under cobalt twilight, vivid vermilion and turquoise bodysuit, dramatic arched back pose with one leg over her own shoulder, vivid nomadic performance portrait, ultra sharp",
    ALONDA + "as an Egyptian hieroglyph stone carver chiseling a vivid cobalt and saffron royal cartouche into a vivid sandstone temple wall at Luxor, vivid white linen wrap skirt, vivid ochre dust on her arms, dramatic golden afternoon light, vivid ancient craftswoman portrait, ultra detailed",
    ALONDA + "as a Polynesian tapa cloth maker in a vivid Samoan fale beating vivid mulberry bark on a vivid wooden anvil into soft tapa fabric, vivid ochre and indigo geometric patterns painted on the stretched cloth, vivid emerald leaves behind, vivid Pacific artisan portrait, ultra sharp",
    ALONDA + "as an Iranian qanat water diviner descending a vivid hand-carved sandstone shaft into a vivid underground aqueduct in the Dasht-e Lut desert, vivid cobalt headlamp glow on her face, vivid wet sandstone reflections, vivid saffron rope coiled over shoulder, vivid archaeological exploration portrait, ultra detailed",
    ALONDA + "as a Patagonian gaucho riding a vivid dark-maned criollo horse through vivid violet wildflower pampas at the foot of vivid cobalt Torres del Paine spires, vivid bombachas pants, vivid silver belt buckle, vivid wide-brimmed hat, vivid gaucho equestrian portrait, ultra sharp",
    ALONDA + "as a Malaysian wayang kulit shadow puppeteer behind a vivid backlit white cotton screen casting vivid cobalt and saffron buffalo and warrior silhouettes, vivid hand-carved leather puppets dangling from bamboo rods, vivid orange oil lamp glow, vivid Southeast Asian puppet portrait, ultra detailed",
    ALONDA + "as a Vietnamese water puppet master at a vivid emerald rice paddypool stage rodding vivid lacquered wooden puppets across the water surface, vivid vermilion conical hat, vivid golden carp puppet mid-leap, vivid lotus blooms floating, vivid water puppet craftswoman portrait, ultra sharp",
    ALONDA + "as a Nepalese thangka painter in a vivid Boudhanath monastery studio applying the final vivid ultramarine and saffron pigment to a vivid Green Tara thangka, vivid brass bowls of crushed mineral paint, vivid hand-ground mala beads, vivid contemplative Buddhist art portrait, ultra detailed",
    ALONDA + "as a Tunisian zellige mosaic master chiseling vivid cobalt emerald vermilion and amber glazed terracotta tiles with a vivid steel hammer on a vivid Nabeul workshop stone, vivid geometric eight-point star half-assembled, vivid white mosaic pattern emerging, vivid Maghreb artisan portrait, ultra sharp",
    ALONDA + "as a Fijian fire walker in a vivid Beqa Lagoon village ceremony stepping barefoot across vivid glowing red-hot river stones at dusk, vivid emerald and vermilion frangipani lei, vivid palms swaying behind, vivid crowd watching in shadows, vivid Pacific ritual portrait, ultra detailed",
    ALONDA + "as a Philippine tikar mat weaver in a vivid T boli dreamweaver atelier on Mindanao weaving vivid magenta indigo and saffron pandanus strips into a vivid geometric coil mat, vivid brass needles and vivid beaded jewelry laid out, vivid T boli beadwork headdress, vivid Southeast Asian craft portrait, ultra sharp",
    ALONDA + "as a Turkish whirling dervish in a vivid Konya Mevlana semahane spinning with arms extended, vivid flowing white robe fanning out into a vivid cone, vivid camel-hair sikke headdress in vivid cream, vivid cyan dome behind, vivid Sufi mystical dance portrait, ultra detailed",
    ALONDA + "as a Korean hanji paper maker in a vivid Jeongeup village courtyard dipping a vivid wooden frame into a vivid pulp vat of mulberry fibers, vivid wet sheets drying on a vivid stone wall in vivid golden sun, vivid white apron, vivid traditional hanji artisan portrait, ultra sharp",
    ALONDA + "as a Bhutanese archery champion at the vivid Thimphu archery range drawing a vivid bamboo composite bow with a vivid vermilion fletched bamboo arrow aimed at a vivid painted wooden target far away, vivid kira ankle-length dress in vivid mustard yellow, vivid kabney scarf, vivid Bhutan national sport portrait, ultra detailed",
    ALONDA + "as a Peruvian quena bamboo flute player on a vivid Sacsayhuaman stone terrace above vivid Cusco at golden hour, vivid Andean poncho in vivid magenta and turquoise stripes, vivid golden quena held to lips, vivid Inca walls glowing amber, vivid Andean musician portrait, ultra sharp",
    ALONDA + "as a Kazakh dombra player on a vivid emerald spring steppe holding a vivid carved wooden pear-shaped long-necked lute, vivid chapan robe in vivid crimson silk, vivid tiaras and silver jewelry, vivid saigas on horizon, vivid Central Asian minstrel portrait, ultra detailed",
    ALONDA + "as an Icelandic lava cave explorer rappelling into a vivid Raufarholshellir cave passage lit by vivid cyan and amber headlamp reflections on vivid basalt walls, vivid crimson climbing harness, vivid rope disappearing into vivid cobalt darkness below, vivid ice stalactites overhead, vivid subterranean portrait, ultra sharp",
    ALONDA + "as a Saharan Tuareg indigo dyer stirring a vivid deep indigo dye vat in a vivid Agadez workshop, vivid white robes splattered with vivid blue dye, vivid white tagelmust headwrap, vivid Tuareg silver cross pendant, vivid Saharan craftswoman portrait, ultra detailed",
]

START = 677

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

Path("/root/alonda/scripts/batch_677_696_results.json").write_text(json.dumps(results, indent=2))
print(f"\n[DONE] {len(results)}/{len(PROMPTS)} generated", flush=True)
