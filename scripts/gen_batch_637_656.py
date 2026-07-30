#!/usr/bin/env python3
"""Generate Alonda portraits batch 637-656 - completely new themes.
Mix of: bee-keeping, falconry, lighthouse keeper, tea sommelier, mime artist,
glass-blowing, vintage film restorer, paper marbler, ethnobotanist in Amazon,
kintsugi master, lighthouse optometrist, Shinto shrine maiden, silk weaver,
underwater archaeologist, Greenlandic kayak hunter, Spanish horse whisperer,
Peruvian stepped-terrace farmer, Mongolian throat-khoomei singer,
Tibetan sand mandala painter, Edo period ukiyo-e woodblock carver.
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
TOKEN=(_prov.get(_provider_key) or {}).get("access_token") or (_pool.get(_provider_key) or [{}])[0].get("access_token")
if not TOKEN:
    print("FATAL: no token", file=sys.stderr); sys.exit(2)
print(f"[token] len={len(TOKEN)}", flush=True)

ALONDA = (
    "Alonda, a beautiful 26-year-old woman, platinum blonde long hair, "
    "striking emerald green eyes, slim athletic figure, "
    "delicate feminine facial features, natural realistic skin texture, "
)

PROMPTS = [
    ALONDA + "as a Croatian apiarist in a Dalmatian coastal apiary tending vivid saffron and amber beehives on a wildflower cliff overlooking vivid cobalt Adriatic sea, white protective suit with vermilion mesh veil, vivid green herbs and magenta bougainvillea, golden hour, vivid traditional beekeeping portrait, ultra detailed",
    ALONDA + "as a Mongolian falconer on the vivid tawny steppe at sunrise with a golden eagle perched on a vermilion gloved fist, vivid indigo deel coat with saffron sash, dramatic stormy cobalt sky, vivid yellow grass stretching to the horizon, nomadic eagle hunter portrait, ultra sharp",
    ALONDA + "as a remote Scottish lighthouse keeper at the top of a vivid red and white painted lighthouse beam rotating through cobalt night fog, vivid emerald wool sweater and yellow oilskin coat, polished brass lantern room reflecting warm amber light, dramatic Atlantic cliffs, vivid maritime portrait, ultra detailed",
    ALONDA + "as a Japanese tea sommelier in a Kyoto machiya tea house performing vivid emerald matcha ceremony, vivid vermilion chashitsu tea room, white kimono with indigo obi, vivid gilded lacquer tea caddy, steam rising from ceramic chawan, vivid traditional portrait, ultra sharp",
    ALONDA + "as a Parisian mime artist in stark whiteface and black costume pressed against a vivid scarlet theatre curtain on the Trocadéro stage, expressive hands gesturing an invisible wall, vivid cobalt spotlight, vivid Tour Eiffel silhouette through window, mime performance portrait, ultra detailed",
    ALONDA + "as a Murano glassblower in a Venetian furnace workshop shaping a glowing molten vermilion vase on the end of a brass blowpipe, vivid cobalt and saffron furnaces behind her, vivid emerald glass rods arrayed on racks, sweat on brow, vivid craft portrait, ultra sharp",
    ALONDA + "as a vintage silent-film restorer in a Turin cineteca digital restoration suite cleaning vivid silver nitrate film scratches frame by frame on a glowing vermilion light table, emerald CRT monitors showing before-after, white cotton gloves, vivid amber safelight, film preservation portrait, ultra detailed",
    ALONDA + "as a Turkish ebru paper marbler in an Istanbul atelier floating vivid magenta, cobalt and saffron pigments on a viscous water bath and transferring them to white cotton paper with golden combs, vivid traditional Ottoman patterns emerging, studio craft portrait, ultra sharp",
    ALONDA + "as an ethnobotanist deep in the Amazon rainforest documenting a vivid vermilion ayahuasca vine with a magnifying loupe and a leather-bound sketchbook, vivid emerald canopy, saffron macaws flying, cobalt butterflies, sweat and humidity, vivid botanical field research portrait, ultra detailed",
    ALONDA + "as a Japanese kintsugi master in a Kyoto pottery studio carefully brushing liquid gold lacquer into the cracks of a repaired celadon tea bowl, vivid magenta lacquer pots on shelves, vermilion and emerald broken pottery, soft natural light, vivid wabi-sabi craft portrait, ultra sharp",
    ALONDA + "as a Bengali eye surgeon in a Kolkata cataract camp operating with vivid magnification loupes on a vivid saffron sari patient under a brilliant operating lamp, vivid teal scrubs and cobalt instruments, helpers in background, vivid humanitarian medical portrait, ultra detailed",
    ALONDA + "as a Shinto shrine maiden in vivid vermilion hakama and white kosode at a Kyoto torii gate during golden hour, holding a sacred sakaki branch, emerald forest hillside, vivid stone lanterns, sacred shimenawa rope, vivid spiritual portrait, ultra sharp",
    ALONDA + "as a Thai silk weaver in a Chiang Mai village workshop at a vivid teak loom weaving saffron and magenta brocade patterns, vivid indigo silk threads, vermilion pillows on floor, emerald banana leaves outside, traditional craft portrait, ultra detailed",
    ALONDA + "as an underwater archaeologist in a vivid turquoise Greek bay surveying a 5th-century amphora wreck through a dive mask, vivid cobalt regulator, vermilion hard hat with lamp, sun rays piercing the water, vivid marine archaeology portrait, ultra sharp",
    ALONDA + "as a Greenlandic seal-hunter kayak paddler in a hand-painted wooden kayak in vivid arctic waters under cobalt cliffs, vivid vermilion and saffron anorak, harpoon resting across bow, vivid glacial blue icebergs floating, polar indigenous portrait, ultra detailed",
    ALONDA + "as an Andalusian horse whisperer in a whitewashed Spanish cortijo gently touching the nose of a vivid chestnut Andalusian stallion, vivid cobalt and saffron traditional riding habit, terracotta courtyard with bougainvillea, golden hour, vivid equine portrait, ultra sharp",
    ALONDA + "as a Quechua Andean terrace farmer in the Sacred Valley of Peru tending vivid emerald and saffron potato terraces, vivid vermilion and indigo traditional pollera skirt, magenta alpaca herd behind, vivid snow-capped Andes peaks, traditional agricultural portrait, ultra detailed",
    ALONDA + "as a Mongolian throat-khoomei singer at a vivid felt ger doorway at dawn with multiple harmonics emanating visible as cobalt sound waves, vivid vermilion deel with saffron sash, vivid endless steppe, magic-hour landscape, vivid ethnomusicology portrait, ultra sharp",
    ALONDA + "as a Tibetan Buddhist monk-artist pouring vivid saffron, cobalt and vermilion colored sand to construct an intricate cosmic mandala on a monastery floor, vivid turquoise mountains through window, maroon robes shaved head, vivid sacred art portrait, ultra detailed",
    ALONDA + "as an Edo period ukiyo-e woodblock carver in a 19th century Edo studio carving a vivid crimson courtesan print into a cherrywood block with a vivid bamboo handle chisel, vivid indigo backdrop, saffron ink bar being ground, kimono detail, vivid Japanese art history portrait, ultra sharp",
]

START = 637

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

Path("/root/alonda/scripts/batch_637_656_results.json").write_text(json.dumps(results, indent=2))
print(f"\n[DONE] {len(results)}/{len(PROMPTS)} generated", flush=True)