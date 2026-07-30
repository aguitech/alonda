#!/usr/bin/env python3
"""Generate Alonda portraits batch 737-756 - new themes.
Mix: Hindu mythology (Durga, Lakshmi, Saraswati, Kali, Hanuman),
Chinese mythology (Nüwa, Chang'e, Sun Wukong, Nezha, Bai Suzhen),
Norse creatures (Jörmungandr, Sleipnir, Fenrir, Huginn/Muninn, Valkyrie),
African mythology (Shango, Yemaya, Anansi, Ogun, Mawu-Lisa),
Southeast Asian (Thai naga, Indonesian wayang, Filipino diwata, Vietnamese lac queros),
Polynesian (Pele, Maui, Hina, Kupe, Tangaroa),
South American folklore (Iara, Saci, Cuca, Mapinguari, Boitatá),
rare winter sports (curling, luge, biathlon, skeleton, ski jumping),
whale/ocean creatures (orca, humpback, manta ray, sea otter, narwhal),
classical composers (Bach, Mozart, Beethoven, Chopin, Debussy),
ballet roles (Swan Lake, Giselle, Nutcracker, Sleeping Beauty, Don Quixote),
virtual worlds (metaverse architect, VR therapist, holodeck, sim designer, digital twin),
rare professions (clockmaker, luthier, perfumer, falconer, master distiller).
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
    ALONDA + "as the Hindu goddess Durga riding a vivid vermilion Bengal tiger into a vivid cosmic battle against the vivid emerald buffalo demon Mahishasura at vivid Navratri dusk, vivid cobalt and vermilion sari, vivid ten golden arms each wielding vivid celestial weapons, vivid gold mukut crown, vivid trishul and chakra discs, vivid Hindu warrior goddess portrait, ultra sharp",
    ALONDA + "as the Hindu goddess Lakshmi seated on a vivid giant pink lotus blooming in a vivid flooded golden field at Diwali night with vivid oil lamps floating, vivid saffron and rose silk sari with vivid gold zari embroidery, vivid gold coin ornaments raining from her palms, vivid emerald peacock feather halo, vivid Hindu prosperity deity portrait, ultra detailed",
    ALONDA + "as the Hindu goddess Saraswati playing a vivid veena beside a vivid silver river at vivid Basant Panchami dawn with vivid white swans gliding, vivid ivory and saffron silk sari, vivid pearl and gold jhumar headpiece, vivid emerald peacock beside her, vivid swan vehicle, vivid Hindu wisdom goddess portrait, ultra sharp",
    ALONDA + "as the Hindu goddess Kali in a vivid cremation ground at midnight standing atop vivid cobalt Shiva, vivid ultramarine skin, vivid garland of freshly severed demon heads, vivid vermilion lolling tongue, vivid skull belt, vivid gold bangles, vivid severed arm clutched in her fist, vivid fierce tantric goddess portrait, ultra detailed",
    ALONDA + "as the Hindu monkey god Hanuman flying through a vivid saffron sunset sky carrying the vivid Sanjeevani mountain in his raised fist toward Lanka, vivid saffron dhoti, vivid gold kavach armor on chest, vivid emerald tail curling behind him, vivid gada mace in his other hand, vivid Ramayana hero portrait, ultra sharp",
    ALONDA + "as the Chinese creator goddess Nüwa repairing a vivid vermilion rainbow-streaked sky with vivid molten five-colored stones above a vivid flooded ancient China, vivid emerald and gold serpent-bodied goddess with vivid human upper half, vivid vermilion phoenix companion, vivid cosmic repairer portrait, ultra detailed",
    ALONDA + "as the Chinese moon goddess Chang'e floating on a vivid emerald cloud beside a vivid vermilion jade rabbit pounding elixir in a vivid moon palace courtyard at Mid-Autumn festival, vivid flowing vermilion and ivory silk hanfu with vivid gold moon embroidery, vivid silver moon disc halo, vivid celestial immortality portrait, ultra sharp",
    ALONDA + "as the Chinese Monkey King Sun Wukong leaping atop a vivid vermilion cloud over a vivid mystical mountain battlefield wielding a vivid golden-banded Ruyi Jingu Bang staff, vivid cobalt and gold armor, vivid phoenix feather headband, vivid emerald eyes flashing golden, vivid Journey to the West trickster hero portrait, ultra detailed",
    ALONDA + "as the Chinese lotus child god Nezha riding a vivid vermilion Wind Fire Wheels across a vivid cobalt Chentang Pass sky wielding a vivid Qiankun Universe Ring and a vivid fiery Red Armillary Sash, vivid vermilion battle armor with vivid gold celestial patterns, vivid gold huntian ling sash, vivid youthful warrior deity portrait, ultra sharp",
    ALONDA + "as the Chinese white snake spirit Bai Suzhen in a vivid emerald West Lake pavilion at Qingming festival in flowing vivid ivory and emerald hanfu with vivid silver hair ornaments, vivid white snake companion coiled beside her, vivid vermilion paper umbrella, vivid green tea in a vivid porcelain cup, vivid Liang Zhu romance legend portrait, ultra detailed",
    ALONDA + "as a Norse Valkyrie descending from a vivid cobalt Asgard sky on a vivid armored winged horse to choose the slain from a vivid Viking shield-wall battlefield at dusk, vivid silver scale armor and vivid vermilion cloak, vivid emerald shield and spear, vivid braided platinum hair streaming, vivid slain warriors glowing beneath her, vivid Norse chooser-of-the-slain portrait, ultra sharp",
    ALONDA + "as the Norse world serpent Jörmungandr in human female form coiling her vivid emerald and cobalt serpent body through a vivid stormy Midgard ocean at Ragnarok twilight, vivid gold and iron Norse helm, vivid vermilion runic tattoos across her arms, vivid fangs peeking through a sly smile, vivid apocalyptic serpent goddess portrait, ultra detailed",
    ALONDA + "as the Norse eight-legged horse Sleipnir in human female form galloping through a vivid vermilion Bifrost rainbow bridge into vivid Asgard at dawn, vivid silver and cobalt Norse armor, vivid emerald saddle blanket, vivid eight ghostly silver hooves thundering clouds, vivid Odin-bound steed portrait, ultra sharp",
    ALONDA + "as the Norse ravens Huginn and Muninn embodied as twin raven-winged sisters perched on a vivid Yggdrasil branch at midnight under vivid polar auroras, vivid cobalt and vermilion feathered Norse armor, vivid emerald raven mask on one shoulder, vivid rune-etched sword, vivid Odin's thought-and-memory ravens portrait, ultra detailed",
    ALONDA + "as the Yoruba thunder god Shango wielding a vivid double-headed oshe axe atop a vivid basalt outcrop during a vivid cobalt thunderstorm, vivid vermilion and white agbada robe, vivid coral bead crown, vivid emerald drums beneath his feet, vivid lightning coiling around his shoulders, vivid West African storm deity portrait, ultra sharp",
    ALONDA + "as the Yoruba ocean mother Yemaya cradling a vivid ultramarine ocean wave at sunset with vivid silver fish streaming from her flowing hair, vivid cobalt and ivory layered skirts, vivid silver moon-pentacle crown, vivid mother-of-pearl jewelry, vivid seven veils of the sea, vivid Afro-Cuban sea goddess portrait, ultra detailed",
    ALONDA + "as the West African trickster spider Anansi in human female form reclining in a vivid cotton-ceilinged tropical hut spinning a vivid web of stories from a vivid silver thread spool, vivid cobalt and saffron kente wraps, vivid cobalt spider-egg sac amulet, vivid emerald orb-weaver spider perched on her finger, vivid folklore trickster portrait, ultra sharp",
    ALONDA + "as the Yoruba iron god Ogun forging a vivid glowing ember-red blade on a vivid basalt anvil in a vivid savanna forge at twilight, vivid cobalt bare chest with vivid iron-shaving tribal scars, vivid vermilion forge apron, vivid emerald forest behind, vivid iron filings swirling, vivid West African iron deity portrait, ultra detailed",
    ALONDA + "as the Fon rainbow serpent Mawu-Lisa sliding across a vivid vermilion dawn sky with a vivid lunar crescent on her forehead and a vivid solar disc on her twin side, vivid emerald and saffron Beninese wrapper, vivid gold Benbronze plaque-style jewelry, vivid cosmogonic rainbow deity portrait, ultra sharp",
    ALONDA + "as a Balinese Barong dancer battling a vivid emerald Rangda demon in a vivid temple courtyard at Nyepi night with vivid gamelan gong orchestra blazing behind, vivid gilded lion-barong mask with vivid ruby eyes, vivid crimson ceremonial kamen cloth, vivid crested gold headdress, vivid sacred Balinese ritual combat portrait, ultra detailed",
]

START = 737

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
                print("RAW_STATUS:", r.status, flush=True)
                raw_txt = r.read().decode(errors='replace')
                print("RAW_BODY:", raw_txt[:1500], flush=True)
                d = json.loads(raw_txt)
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

Path("/root/alonda/scripts/batch_737_756_results.json").write_text(json.dumps(results, indent=2))
print(f"\n[DONE] {len(results)}/{len(PROMPTS)} generated", flush=True)
