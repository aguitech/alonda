#!/usr/bin/env python3
"""Generate Alonda portraits batch 757-776.

Fresh categories (none of these have been used in 637-756):
- Greek mythology 2: Athena, Artemis, Apollo, Aphrodite, Ares, Hephaestus, Dionysus, Nike, Pan, Iris
- Roman mythology: Ceres, Juno, Mars, Minerva, Vesta, Vulcan, Flora, Diana, Bacchus, Bellona
- Egyptian mythology: Anubis, Isis, Ra, Hathor, Thoth, Set, Nephthys, Ma'at, Sekhmet, Sobek
- Norse mythology 2: Tyr, Heimdall, Idunn, Skadi, Njord, Baldr, Vidar, Ullr, Sif, Bragi
- Y2K 2000s pop star (Trinity matrix-esque neon), 1980s synthwave neon (skating rink), 1930s art deco showgirl, 1920s flapper jazz, indie sleaze 2007
- Subcultures: kawaii Harajuku pastel, gothic Victorian, surfista vintage 60s, mod 60s London, skater 90s, preppy 80s, grunge 90s, punk 77, lolita sweet, hipster 2014
- Festivities: Day of the Dead MX catrina (already used), Holi India, Songkran Thailand, Inti Raymi Peru, Up Helly Aa Scotland, Mardi Gras NOLA, Oktoberfest Munich, Chinese NY lion dance, Tomatina Spain, Burning Man
- Cryptids: Mothman Point Pleasant, Bigfoot PNW, Jackalope Wyoming, Kraken Norway, Chupacabra Mexico, Loch Ness, Yeti Himalaya, Thunderbird PNW, Wendago forest, Naga river spirit
- Rare food: chocolatier artisan, ice cream gelato maker, cheesemaker affineur, sushi itamae master, ramen shoyu master, dim sum chef, pizza napoletana maker, patisserie Paris, mole sauce Oaxaca, mezcal palenquera
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
TOKEN=auth.get("providers", {}).get("minimax" + "-oauth", {}).get("access_token") or (_pool.get("minimax" + "-oauth") or [{}])[0].get("access_token")
if not TOKEN:
    print("FATAL: no token", file=sys.stderr); sys.exit(2)
print(f"[token] len={len(TOKEN)}", flush=True)

ALONDA = (
    "Alonda, a beautiful 26-year-old woman, platinum blonde long hair, "
    "striking emerald green eyes, slim athletic figure, "
    "delicate feminine facial features, natural realistic skin texture, "
)

PROMPTS = [
    # Greek mythology (757-766)
    ALONDA + "as the Greek goddess Athena in vivid cobalt and gold armor standing on the vivid marble steps of the Acropolis at dawn holding a vivid bronze spear and a vivid Aegis shield with vivid Medusa relief, vivid ivory peplos with vivid saffron border, vivid gold olive wreath crown, vivid emerald owl perched on her shoulder, vivid Greek wisdom war goddess portrait, ultra sharp",
    ALONDA + "as the Greek goddess Artemis in a vivid silver moonlit Arcadian forest drawing a vivid silver bow with a vivid vermilion fletched arrow aimed at a vivid white stag, vivid cobalt short hunting tunic, vivid emerald quiver, vivid crescent moon diadem, vivid silver hound at her side, vivid Greek wild hunt portrait, ultra detailed",
    ALONDA + "as the Greek god Apollo playing a vivid golden lyre on a vivid Delos marble terrace at golden hour with vivid vermilion sun behind him, vivid ivory and saffron chlamys cloak, vivid laurel wreath crown, vivid vermilion griffin at his feet, vivid glowing bronze tripod oracle, vivid Greek sun music prophecy portrait, ultra sharp",
    ALONDA + "as the Greek goddess Aphrodite rising from a vivid ultramarine sea on a vivid iridescent scallop shell at sunrise near vivid Paphos Cyprus, vivid rose and gold silk drapery clinging to her form, vivid vermilion and emerald seashell crown, vivid doves fluttering around, vivid Greek love beauty portrait, ultra detailed",
    ALONDA + "as the Greek god Ares in vivid blood-red Greek general armor standing in a vivid vermilion war-torn battlefield at twilight holding a vivid bronze xiphos sword, vivid vermilion crested Corinthian helm, vivid dark crimson cape billowing, vivid dark spear, vivid emerald war dogs at his side, vivid Greek war god portrait, ultra sharp",
    ALONDA + "as the Greek god Hephaestus at his vivid volcanic forge inside vivid Mount Etna hammering a vivid glowing crimson blade on a vivid basalt anvil, vivid soot-streaked bare muscular arms, vivid cobalt blacksmith leather apron, vivid vermilion forge fire, vivid silver robotic golden automaton attendants, vivid Greek smith god portrait, ultra detailed",
    ALONDA + "as the Greek god Dionysus reclining on a vivid emerald grape-strewn leopard-skin couch at a vivid twilight vineyard symposium, vivid vermilion and gold ivy crown, vivid silver kantharos goblet overflowing with vivid ruby wine, vivid panthers lounging at his feet, vivid thyrsus staff with vivid emerald pinecone, vivid Greek wine revelry portrait, ultra sharp",
    ALONDA + "as the Greek goddess Nike alighting mid-stride on a vivid marble Ionic column at vivid Samothrace dawn with vivid golden wings spread, vivid flowing ivory peplos with vivid vermilion hem, vivid gold laurel crown, vivid palm branch in her raised hand, vivid golden trumpet sounding victory, vivid Greek victory goddess portrait, ultra detailed",
    ALONDA + "as the Greek god Pan playing a vivid double-reed syrinx pan-flute seated on a vivid mossy boulder in a vivid emerald Arcadian grove at noon, vivid ivy crown on his brow, vivid tawny goat-furred legs crossed, vivid vermilion wild boar companion at his feet, vivid dancing nymph silhouettes behind, vivid Greek wild shepherd portrait, ultra sharp",
    ALONDA + "as the Greek goddess Iris descending on a vivid vermilion rainbow bridge between Olympus and Earth trailing vivid gold and rose and cobalt and jade ribbons of light, vivid flowing multi-colored chiton, vivid saffron winged sandals, vivid vermilion herald staff with vivid twin serpents, vivid golden water jug pouring rain, vivid Greek rainbow messenger portrait, ultra detailed",
    # Roman mythology (767-770)
    ALONDA + "as the Roman goddess Ceres in a vivid golden ripe wheat field at harvest season holding vivid sheaves of vivid amber wheat and a vivid silver sickle, vivid saffron and ivory stola with vivid emerald palla cloak, vivid gold wheat-sheaf crown, vivid vermilion poppies in her hair, vivid abundant Roman harvest goddess portrait, ultra sharp",
    ALONDA + "as the Roman goddess Juno enthroned on a vivid ivory and gold sella in a vivid vermilion draped Palatine temple chamber with a vivid peacock beside her throne, vivid ivory and vermilion Roman matron stola with vivid purple border, vivid gold diadem, vivid scepter with a vivid cobalt lotus finial, vivid Roman queen of the gods portrait, ultra detailed",
    ALONDA + "as the Roman god Mars in vivid crimson Roman legionary lorica segmentata armor on a vivid sun-drenched Viminal Hill commanding vivid scarlet-bannered legions, vivid vermilion crested galea helmet, vivid emerald battlefield standard SPQR eagle, vivid gladius short sword drawn, vivid Roman war god portrait, ultra sharp",
    ALONDA + "as the Roman goddess Minerva in a vivid Lapis-blue Roman atrium studio painting on a vivid wooden panel with vivid ivory stylus and vivid cobalt wax tablet, vivid saffron and emerald Roman palla, vivid gold owl diadem, vivid stacked scrolls and astronomical instruments, vivid Roman wisdom craft portrait, ultra detailed",
    # Egyptian mythology (771-774)
    ALONDA + "as the Egyptian god Anubis in human female form with vivid cobalt-and-gold jackal headdress weighing a vivid feather of Ma'at against a vivid vermilion human heart on a vivid obsidian scale in the vivid Duat judgment hall at midnight, vivid ivory linen wrap, vivid gold ankh in her hand, vivid emerald was scepter, vivid Egyptian underworld judge portrait, ultra sharp",
    ALONDA + "as the Egyptian goddess Isis with vivid gold sun-disc and cow horn crown kneeling at the vivid Nilebank spreading vivid silver-cyan winged protection over a vivid mummified Osiris, vivid turquoise and ivory pleated linen dress, vivid cobalt and gold broad collar usekh, vivid emerald ankh loop-cross, vivid Egyptian divine magic mother portrait, ultra detailed",
    ALONDA + "as the Egyptian god Ra sailing the vivid vermilion solar barque Mandjet across a vivid golden dawn sky with vivid Aten sun disc blazing overhead, vivid gold hawk-headed crown, vivid cobalt and ivory pleated kilt, vivid emerald and vermilion solar uraeus cobra crown, vivid Egyptian sun creator god portrait, ultra sharp",
    ALONDA + "as the Egyptian goddess Hathor playing a vivid silver sistrum rattle inside a vivid gold and turquoise Dendera temple hypostyle hall surrounded by vivid sapphire-tiled Hathoric columns, vivid cow-horned solar disc crown, vivid vermilion and emerald beaded broad collar, vivid golden menat necklace, vivid Egyptian love music goddess portrait, ultra detailed",
    # Norse mythology 2 (775-776)
    ALONDA + "as the Norse god Tyr standing on a vivid basalt rainbow bridge Bifrost at Ragnarok dusk with his vivid right hand missing and bandaged in vivid vermilion cloth, vivid silver Norse plate armor with vivid emerald cloak, vivid cobalt sword Justice, vivid solemn one-handed oath-keeper portrait, ultra sharp",
    ALONDA + "as the Norse goddess Skadi hunting on vivid emerald snowshoes across a vivid cobalt Jotunheim glacier at midnight with a vivid vermilion yew longbow and a vivid pack of vivid silver wolves, vivid white fur and cobalt Norse hunting dress, vivid emerald icicle crown, vivid silver skis on her back, vivid Norse winter mountain huntress portrait, ultra detailed",
]

START = 757

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

Path("/root/alonda/scripts/batch_757_776_results.json").write_text(json.dumps(results, indent=2))
print(f"\n[DONE] {len(results)}/{len(PROMPTS)} generated", flush=True)
