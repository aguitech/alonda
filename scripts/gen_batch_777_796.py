#!/usr/bin/env python3
"""Generate Alonda portraits batch 777-796.

Fresh categories (none of these have been used in 1-776):
- Celtic mythology 2: Morrigan, Brigid, Cernunnos, Danu, Lugh, Aine, Manannan, Macha, Boann, Epona
- Slavic mythology: Baba Yaga, Vasilisa, Koschei, Rusalka, Domovoi, Leshy, Zmey Gorynych, Vila, Poludnitsa, Svarog
- Japanese folklore: Yuki-onna, Kitsune, Tanuki, Oni, Kaguya, Momotaro, Inugami, Jorogumo, Raiju, Tengu
- Mesoamerican gods 2: Tlaloc, Xochiquetzal, Tezcatlipoca, Xipe Totec, Coatlicue, Chalchiuhtlicue, Mixcoatl, Itzpapalotl, Huehuecoyotl, Patecatl
- Hindu mythology 2: Indra, Varuna, Agni, Yama, Kubera, Saraswati 2, Parvati, Durga 2, Vishnu, Shiva
- Dance traditions: Bharatanatyam, Kathak, Odissi, Kuchipudi, Kathakali, Manipuri, Mohiniyattam, Sattriya, Mayurbhanj Chau, Lavani
- Underwater realms: coral reef guardian, abyss explorer, shipwreck archaeologist, mermaid kingdom, hydrothermal vent scientist, submarine pilot, jellyfish whisperer, seahorse tamer, pearl diver, underwater photographer
- Mountain professions: alpine rescuer, ski patroller, mountain guide, ice climber, ski instructor, avalanche forecaster, hut keeper, mountain meteorologist, paragliding tandem pilot, helicopter rescue crew
- Street food world: taco cart vendor, gyro street chef, banh mi seller, arepa maker, empanada vendor, pupusa maker, falafel street cook, halal cart, pretzel vendor, churro street maker
- Modern subcultures 2: e-girl, soft grunge, VSCO girl 2019, indie kid, cottagecore, goblincore, mermaidcore, fairycore, goblin mode, coastal grandmother
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
_access = (_prov.get(KEY) or {}).get("access_token")
if not _access:
    _first = (_pool.get(KEY) or [{}])[0]
    _access = _first.get("access_token")
TOKEN = str(_access) if _access else ""
if not isinstance(TOKEN, str) or len(TOKEN) < 10:
    print("FATAL: no token", file=sys.stderr); sys.exit(2)
print(f"[token] len={len(TOKEN)}", flush=True)

ALONDA = (
    "Alonda, a beautiful 26-year-old woman, platinum blonde long hair, "
    "striking emerald green eyes, slim athletic figure, "
    "delicate feminine facial features, natural realistic skin texture, "
)

PROMPTS = [
    # Celtic mythology 2 (777-786)
    ALONDA + "as the Celtic goddess Morrigan in vivid midnight-black feathered battle cloak standing on a vivid vermilion battlefield cairn at twilight with two vivid emerald ravens perched on her shoulders and a vivid crimson spear, vivid silver war crown, vivid cobalt Celtic torc, vivid mist swirling at her feet, vivid Irish war fate sovereignty goddess portrait, ultra sharp",
    ALONDA + "as the Celtic goddess Brigid tending a vivid emerald eternal flame inside a vivid whitewashed Kildare sacred hearth with vivid saffron and crimson brighid's crosses stacked at her side, vivid ivory and vermilion woven wool cloak, vivid gold solar crown, vivid white cow beside her, vivid Irish poetry healing smithcraft goddess portrait, ultra detailed",
    ALONDA + "as the Celtic god Cernunnos in human female form seated cross-legged on a vivid moss-draped oak throne in a vivid emerald forest glade wearing a vivid gold antler crown with vivid verdant moss and vines growing on the antlers, vivid gold torc coiled in one hand, vivid vermilion and emerald stag at his feet, vivid Celtic wild lord of animals portrait, ultra sharp",
    ALONDA + "as the Celtic mother goddess Danu reclining on a vivid emerald riverbank amid a vivid carpet of vivid vermilion and saffron wildflowers pouring vivid amber honey from a vivid silver vessel into a vivid flowing turquoise river, vivid flowing ivory and gold gown, vivid gold crown of wheat, vivid Celtic primordial mother goddess portrait, ultra detailed",
    ALONDA + "as the Celtic god Lugh in vivid saffron and gold armor wielding a vivid flaming spear and a vivid silver sling on the vivid green Plains of Moytura at sunset, vivid radiant many-skilled sun god face, vivid ivory cloak, vivid Celtic skilled craftsman war leader portrait, ultra sharp",
    ALONDA + "as the Celtic sun goddess Aine standing on a vivid golden summer hilltop at midsummer dawn with vivid amber sunlight radiating from her lifted hands and vivid crimson and saffron wildflowers blooming at her feet, vivid ivory silk gown with vivid gold Celtic knot embroidery, vivid gold crescent moon diadem, vivid Irish love summer sovereignty portrait, ultra detailed",
    ALONDA + "as the Celtic sea god Manannan mac Lir riding a vivid emerald wave-shaped chariot pulled by vivid silver-maned horses across a vivid ultramarine western sea at twilight, vivid flowing seaweed-green Celtic robes, vivid gold trident, vivid misty Irish otherworld horizon, vivid Celtic sea otherworld ruler portrait, ultra sharp",
    ALONDA + "as the Celtic war goddess Macha running a vivid crimson chariot pulled by vivid black horses across a vivid emerald Ulster battlefield with vivid red war paint streaked across her face, vivid saffron war cloak billowing, vivid silver sword drawn, vivid horses' hooves throwing vivid vermilion sparks, vivid Irish war horse goddess portrait, ultra detailed",
    ALONDA + "as the Celtic river goddess Boann kneeling by the vivid turquoise Boyne river source pouring a vivid silver vessel of vivid amber water that flows into a vivid emerald rippling river, vivid ivory gown, vivid gold fish amulet around her neck, vivid Celtic river name-sake goddess portrait, ultra sharp",
    ALONDA + "as the Celtic horse goddess Epona riding a vivid vermilion mare across a vivid emerald Celtic summer meadow with vivid saffron and crimson wildflowers, vivid cobalt Celtic bridle on the mare, vivid ivory and gold flowing cape, vivid silver apple of discord held aloft, vivid Roman-Celtic horse protector goddess portrait, ultra detailed",
    # Slavic mythology (787-791)
    ALONDA + "as the Slavic witch Baba Yaga standing on vivid chicken legs at the entrance of a vivid cobalt and silver hut deep in a vivid emerald birch forest with vivid vermilion mushrooms and a vivid white skull lantern, vivid black hooded robe, vivid iron mortar and pestle, vivid mortar flying through a vivid crimson sunset sky, vivid Slavic dark forest witch portrait, ultra sharp",
    ALONDA + "as the Slavic heroine Vasilisa the Beautiful holding a vivid emerald glowing skull lantern walking through a vivid midnight black birch forest with vivid crimson eyes glowing in the dark between the trees, vivid flowing ivory and gold peasant dress, vivid red embroidered sarafan, vivid Slavic brave maiden portrait, ultra detailed",
    ALONDA + "as the Slavic deathless sorcerer Koschei the Immortal's beautiful victim opposite him, a vivid princess held inside a vivid crystal coffin submerged in a vivid turquoise lake guarded by vivid cobalt and silver chains, vivid flowing emerald gown, vivid crown of vivid silver icicles, vivid Slavic enchanted captive portrait, ultra sharp",
    ALONDA + "as the Slavic water nymph Rusalka rising from a vivid ultramarine moonlit river at midnight with vivid emerald waterweed woven through her platinum hair and vivid pale luminous skin, vivid flowing turquoise and silver water-silk dress, vivid silver crown of river reeds, vivid Slavic river spirit portrait, ultra detailed",
    ALONDA + "as the Slavic household spirit Domovoi depicted as a vivid small bearded old man emerging from behind a vivid vermilion Russian stove in a vivid warm izba kitchen holding a vivid white mouse familiar, vivid brown wool peasant tunic, vivid Slavic protective house spirit portrait, ultra sharp",
    # Japanese folklore (792-796)
    ALONDA + "as the Japanese snow woman Yuki-onna drifting through a vivid silver snowstorm at midnight with vivid cobalt icicle crown and a vivid flowing translucent white kimono trailing into the snow, vivid porcelain pale luminous skin, vivid silver breath in the frozen air, vivid Japanese snow spirit portrait, ultra detailed",
    ALONDA + "as a Japanese nine-tailed Kitsune in human female form with vivid silver and crimson fox ears and vivid nine flowing fluffy tails fanned behind her, vivid vermilion shrine maiden hakama and white kosode, vivid white fox mask tucked at her waist, vivid Inari forest shrine at night, vivid Japanese fox spirit portrait, ultra sharp",
    ALONDA + "as a Japanese Tanuki shapeshifter in human female form with vivid brown tanuki ears peeking from her hair and a vivid wide straw hat, vivid vermilion and gold leaf-shaped magical leaf on her forehead, vivid sake flask at her hip, vivid Japanese mischievous shape-shifting raccoon dog spirit portrait, ultra detailed",
    ALONDA + "as a Japanese Oni woman warrior with vivid cobalt and vermilion demon horns and vivid crimson ritual face paint, vivid cobalt and gold samurai armor, vivid kanabo spiked iron club on her back, vivid crimson flames dancing at her feet, vivid Japanese demon warrior portrait, ultra sharp",
    ALONDA + "as the Japanese moon princess Kaguya-hime ascending toward the vivid silver full moon in a vivid flowing vermilion and gold junihitoe twelve-layer ceremonial kimono with a vivid emperor's procession of vivid celestial guards below her, vivid vermilion phoenix feather crown, vivid Japanese moon-bound celestial princess portrait, ultra detailed",
]

START = 777

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

Path("/root/alonda/scripts/batch_777_796_results.json").write_text(json.dumps(results, indent=2))
print(f"\n[DONE] {len(results)}/{len(PROMPTS)} generated", flush=True)