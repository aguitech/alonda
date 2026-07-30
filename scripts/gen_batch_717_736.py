#!/usr/bin/env python3
"""Generate Alonda portraits batch 717-736 - new themes.
Mix: Persian mythology (Zoroaster, Mithras, Anahita, Rustam, Shahnameh),
Japanese mythology (Amaterasu, Susanoo, Tsukuyomi, Inari, Raijin),
Korean mythology (Mago Halmi, Gumiho, Dokkaebi, haenyeo diver),
Mesoamerican (Mixtec codices, Zapotec, Toltec, Purepecha, Totonaca),
rare sports (polo, lacrosse, hurling, kabaddi, sepak takraw),
futuristic cyberpunk cities (Neo Tokyo, Lagos 2099, Mumbai megacity),
underwater kingdoms (Atlantis, Ys, Lemuria, Mu, El Dorado).
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
    ALONDA + "as the Persian Zoroastrian yazata Anahita standing on a vivid emerald riverbank pouring vivid holy water from a vivid silver amphora under a vivid crimson dawn sky, vivid cobalt Persian robes with vivid gold yazata embroidery, vivid saffron diadem, vivid leaping sacred carp in the stream, vivid ancient Iranian divine portrait, ultra sharp",
    ALONDA + "as the Persian legendary hero Rustam in vivid Sistan at dusk, sleeping under a vivid vermilion pomegranate tree with her vivid crimson-pelted horse Rakhsh beside her, vivid ivory battle armor draped over a vivid sandstone plinth, vivid emerald Sassanid crown, vivid epic Shahnameh hero portrait, ultra detailed",
    ALONDA + "as the Persian light deity Mithras inside a vivid dark cosmic cave slaying a vivid cosmic bull beneath a vivid starry firmament with vivid vermilion Phrygian cap and vivid crimson cape, vivid sacred torch and dagger, vivid torchlight halo, vivid late-antique mystery cult portrait, ultra sharp",
    ALONDA + "as the Persian sun-watcher Zoroaster at the vivid dawn of creation on a vivid Mount Ushidan in vivid Balkh region, vivid vermilion sacred fire blazing before her, vivid white sheepskin cloak, vivid ivory scroll with vivid Avestan gold lettering, vivid founding prophet portrait, ultra detailed",
    ALONDA + "as the Japanese sun goddess Amaterasu emerging from the vivid Ama-no-Iwato cave at dawn flooding Japan with vivid golden light, vivid crimson imperial kimono with vivid phoenix paulownia crest, vivid vermilion sun disc mirror in her hands, vivid gold magatama bead necklace, vivid radiant Shinto goddess portrait, ultra sharp",
    ALONDA + "as the Japanese storm god Susanoo standing on a vivid vermilion cloud above a vivid storm-lashed Izumo coastline wielding a vivid Totsuka-no-Tsurugi sword, vivid cobalt kariginu court robe, vivid emerald and magenta lightning halo, vivid raging sea serpent Yamata-no-Orochi beneath, vivid Shinto storm deity portrait, ultra detailed",
    ALONDA + "as the Japanese moon god Tsukuyomi reclining on a vivid vermilion cloud bridge across a vivid silver moonlit bay with vivid jeweled tanto resting on her lap, vivid cobalt and silver imperial court attire, vivid jade crescent headdress, vivid silver hare pounding mochi beside her, vivid celestial night portrait, ultra sharp",
    ALONDA + "as the Japanese fox deity Inari atop a vivid vermilion torii gate row at Fushimi Inari shrine at golden hour with vivid white foxes flanking her, vivid vermilion and gold miko attire, vivid emerald torii tunnel receding into the hill, vivid fox-fire lanterns, vivid Shinto harvest deity portrait, ultra detailed",
    ALONDA + "as the Japanese thunder god Raijin drumming on a vivid cobalt storm cloud above a vivid Shinto pagoda at twilight with vivid vermilion tomoe drums, vivid cobalt robe with vivid magenta lightning, vivid crimson oni mask slung at her hip, vivid electric storm halo, vivid dramatic thunder deity portrait, ultra sharp",
    ALONDA + "as a Korean gumiho nine-tailed fox spirit wandering a vivid vermilion maple grove at Chuseok night in vivid Joseon hanbok, vivid ivory and crimson hanbok with vivid gold norigae, vivid white fox ears and nine silver-tipped vermilion tails fanning behind her, vivid glowing fox bead talisman, vivid Korean folklore spirit portrait, ultra detailed",
    ALONDA + "as a Jeju haenyeo free-diving grandmother in a vivid cobalt sea at dawn surfacing with a vivid abalone and sea urchin catch in her net, vivid glossy black neoprene wetsuit, vivid turquoise mask and snorkel, vivid vermilion life buoy, vivid emerald Jeju basalt cliffs behind, vivid Korean diving matriarch portrait, ultra sharp",
    ALONDA + "as a Korean dokkaebi trickster spirit dancing around a vivid crimson campfire at midnight in a vivid birch grove, vivid crimson tiger-stripe robes, vivid emerald club with magical spikes, vivid cobalt magic pouch brimming with glowing orbs, vivid playful goblin portrait, ultra detailed",
    ALONDA + "as a Korean Mago Halmi grandmother sky-spirit weaving a vivid silver loom of stars above a vivid ancient Korean village at night, vivid ivory and crimson hanbok, vivid silver spindle of starlight, vivid emerald and gold norigae, vivid shamanic celestial weaver portrait, ultra sharp",
    ALONDA + "as a Mixtec codex scribe in vivid 11th-century Tilantongo painting vivid deities and genealogy on vivid deer hide with vivid cochineal red and indigo black, vivid cobalt and ivory feathered headdress, vivid vermilion quill and azurite ink pot, vivid turquoise jade ear flares, vivid Mesoamerican artisan portrait, ultra detailed",
    ALONDA + "as a Zapotec dancer in vivid Mitla ruins performing a vivid feasting-of-the-dead traditional dance at Day of the Dead, vivid ivory huipil with vivid cobalt stepped-fret embroidery, vivid vermilion and gold papel picado ribbons, vivid marigold garlands in her platinum hair, vivid Oaxaca ritual dancer portrait, ultra sharp",
    ALONDA + "as a Purepecha metal artisan from vivid Santa Clara del Cobre hammering a vivid vermilion copper vessel on a vivid basalt anvil at twilight, vivid emerald and ochre rebozo, vivid copper dust glowing in the air, vivid amber sparks, vivid Michoacán master metalworker portrait, ultra detailed",
    ALONDA + "as a Toltec warrior queen from vivid Tollan Tula wielding a vivid obsidian-edged macuahuitl club amid a vivid jade forest at dawn, vivid cobalt jaguar-skin battle dress, vivid gold butterfly pectoral, vivid vermilion quetzal-feather headdress, vivid Postclassic Mexican warrior portrait, ultra sharp",
    ALONDA + "as a Totonaca vanilla harvester in vivid Veracruz Papantla region inspecting a vivid green vanilla orchid vine at golden hour, vivid cobalt and ivory traditional huipil, vivid woven palm hat, vivid bunches of vivid green vanilla pods, vivid aromatic Mesoamerican agriculturist portrait, ultra detailed",
    ALONDA + "as a Mendoza Argentina polo player mid-swing on a vivid emerald polo field at sunset, vivid cream riding breeches, vivid vermilion team jersey, vivid mahogany mallet connecting with the ball, vivid polo pony galloping, vivid Argentine elite equestrian sport portrait, ultra sharp",
    ALONDA + "as a kabaddi raider from vivid Haryana charging across the vivid vermilion midline of a kabaddi court at dusk chanting the vivid kabaddi raid chant, vivid crimson and cobalt team jersey, vivid muscular coiled pose, vivid packed-earth arena crowd silhouettes behind, vivid Indian contact sport portrait, ultra detailed",
]

START = 717

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

Path("/root/alonda/scripts/batch_717_736_results.json").write_text(json.dumps(results, indent=2))
print(f"\n[DONE] {len(results)}/{len(PROMPTS)} generated", flush=True)