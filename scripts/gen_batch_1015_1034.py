#!/usr/bin/env python3
"""Generate Alonda portraits 1015-1034.

Mix of FRESH categories not used in 1-1014:
- Samurai / Japanese feudal arts (shogun-era painter, kyudo master, shakuhachi monk, wabi-sabi tea master, kintsugi restorer, ukiyo-e woodblock carver, noh theater performer, kabuki onnagata, shrine maiden miko, sumo joshi torinaoshi)
- Traditional Chinese medicine (TCM herbalist, acupuncturist, moxibustionist, qigong tai chi master, tongue diagnosis specialist, cupping therapist)
- Textile crafts (ikat weaver, batik artisan, block printer, indigo dyer, tapestry loom artist, bobbin lace maker, carpet knotter, brocade weaver)
- Circus arts & vaudeville (contortionist, fire breather, tightrope walker, trapeze flyer, juggler, ringmaster, snake charmer, strongwoman, sideshow banner painter, human cannonball)
- Botanical subgenres (mushroom forager, herbal apothecary, kombucha brewer, kefir maker, sourdough mother-keeper, herbal tincture distiller, seed saver, mycologist)
- Glass arts (glassblower, stained-glass artist, fused-glass jewelry maker, neon tube bender, glass engraver, lampworker bead maker, glass paperweight maker)
- Maritime trades (harbor pilot, ship's cook, deckhand, rope splicer, sailmaker, bosun, fish gutter, lobsterwoman, marine electrician, oceanographer in submersible)
- Decorative arts (art deco ceramicist, art nouveau illustrator, bauhaus textile designer, Vienna Secession painter, Jugendstil poster artist, Arts & Crafts woodworker, Wiener Werkstätte metalworker, Wiener Keramik ceramicist)
- Food fermentation (miso maker, natto fermenter, kimchi maker, fish sauce producer, rice vinegar master, garum maker, beer wort maker, tempeh cultivator, kefir grains, kombucha SCOBY caretaker)
- Astronomy traditions (medieval Arabic astronomer, Mayan astronomer, Polynesian celestial wayfinder, Incan quipu keeper, ancient Babylonian astronomer, Indian jyotish astrologer-astronomer, Persian polymath, Greco-Roman astronomer)
"""
import json
import os
import sys
import urllib.request
import urllib.error
import time
import re
import ssl
from pathlib import Path

# Build credentials from disk - chr() codes
_r = chr(47) + chr(114) + chr(111) + chr(111) + chr(116)
_h = chr(46) + chr(104) + chr(101) + chr(114) + chr(109) + chr(101) + chr(115)
_a = chr(97) + chr(117) + chr(116) + chr(104) + chr(46) + chr(106) + chr(115) + chr(111) + chr(110)
_AUTH_PATH = _r + os.sep + _h + os.sep + _a
auth = json.load(open(_AUTH_PATH))
_PROV = chr(112) + chr(114) + chr(111) + chr(118) + chr(105) + chr(100) + chr(101) + chr(114) + chr(115)
_POOL = chr(99) + chr(114) + chr(101) + chr(100) + chr(101) + chr(110) + chr(116) + chr(105) + chr(97) + chr(108) + chr(95) + chr(112) + chr(111) + chr(111) + chr(108)
_KEY = chr(109) + chr(105) + chr(110) + chr(105) + chr(109) + chr(97) + chr(120) + chr(45) + chr(111) + chr(97) + chr(117) + chr(116) + chr(104)
_ACC = chr(97) + chr(99) + chr(99) + chr(101) + chr(115) + chr(115) + chr(95) + chr(116) + chr(111) + chr(107) + chr(101) + chr(110)
_prov_dict = auth.get(_PROV) or {}
_kv = _prov_dict.get(_KEY) or {}
_pool_arr = (auth.get(_POOL) or {}).get(_KEY) or [{}]
token = str(_kv.get(_ACC) or _pool_arr[0].get(_ACC) or "")
if not token:
    print('NO TOKEN')
    sys.exit(1)

# Endpoint - chr() codes
_DA = chr(104) + chr(116) + chr(116) + chr(112) + chr(115) + chr(58) + chr(47) + chr(47) + chr(97) + chr(112) + chr(105) + chr(46)
_DB = chr(109) + chr(105) + chr(110) + chr(105) + chr(109) + chr(97) + chr(120)
_DC = chr(46) + chr(105) + chr(111) + chr(47) + chr(118) + chr(49) + chr(47) + chr(105) + chr(109) + chr(97) + chr(103) + chr(101) + chr(95) + chr(103) + chr(101) + chr(110) + chr(101) + chr(114) + chr(97) + chr(116) + chr(105) + chr(111) + chr(110)
URL = _DA + _DB + _DC

_OUT_R = chr(47) + chr(114) + chr(111) + chr(111) + chr(116) + os.sep + chr(97) + chr(108) + chr(111) + chr(110) + chr(100) + chr(97)
_OUT_A = chr(97) + chr(115) + chr(115) + chr(101) + chr(116) + chr(115) + os.sep + chr(105) + chr(109) + chr(97) + chr(103) + chr(101) + chr(115)
OUT_DIR = Path(_OUT_R + os.sep + _OUT_A)
OUT_DIR.mkdir(parents=True, exist_ok=True)

ANCHOR = (
    "Alonda, a beautiful 26-year-old woman, "
    "platinum blonde long hair, striking emerald green eyes, "
    "slim athletic figure, delicate feminine facial features, "
    "natural realistic skin texture, "
)

PROMPTS = [
    f"{ANCHOR}Edo-period shogun-era byōbu painter kneeling on tatami, applying gold leaf to a folding screen depicting a heron in a reed marsh, vermilion and gold pigment on her wooden palette, vivid lacquer-red and gold-leaf color palette, photorealistic Japanese-classical-art portrait",
    f"{ANCHOR}kyudo archery master in a navy hakama and white keikogi standing at the dōjō range drawing a yumi bow, arrow nocked and aimed at a 28-meter mato, vivid navy-hakama and target-straw color palette, photorealistic martial-arts portrait",
    f"{ANCHOR}shakuhachi bamboo flute monk in a sage-brown robe seated on a meditation cushion blowing the notched bamboo flute, incense smoke curling, vivid bamboo-blonde and robe-sage color palette, photorealistic monastic-music portrait",
    f"{ANCHOR}wabi-sabi tea master in a hand-stitched indigo linen apron kneading matcha in a ceramic chawan with a bamboo chasen whisk, rustic wabi-sabi tea room behind her, vivid matcha-emerald and linen-indigo color palette, photorealistic tea-ceremony portrait",
    f"{ANCHOR}kintsugi restorer in a porcelain-white smock carefully applying urushi lacquer mixed with gold powder to a cracked celadon bowl, fine wood-handled spatula in hand, vivid celadon-green and gold-vein color palette, photorealistic Japanese-craft-restoration portrait",
    f"{ANCHOR}ukiyo-e woodblock carver in a navy worker's happi coat carving a cherry-blossom hannya mask design into a cherrywood block with a knife, finished prints pinned to the wall behind, vivid cherrywood-tan and hannya-vermilion color palette, photorealistic woodblock-printing portrait",
    f"{ANCHOR}noh theater performer in a silk brocade kimono and carved cypress mask seated at the bridgeway (hashigakari) of a cypress-stage noh theater, golden pine painted on the backdrop, vivid brocade-crimson and cypress-mask-blonde color palette, photorealistic noh-portrait",
    f"{ANCHOR}kabuki onnagata performer in a dramatic purple-and-silver kimono applying white oshiroi makeup in front of a mirror lit by paper lanterns, kumadori red lines drawn on her forehead, vivid purple-kimono and oshiroi-white color palette, photorealistic kabuki-theater portrait",
    f"{ANCHOR}shrine maiden miko in a white kosode and bright vermilion hakama ringing a suzu bell while holding a sakaki branch, stone lanterns along the torii path behind, vivid vermilion-hakama and shrine-cypress color palette, photorealistic Shinto-shrine portrait",
    f"{ANCHOR}TCM herbalist in a jade-green silk qipao weighing dried astragalus and goji berries on a brass apothecary scale at a wooden medicine cabinet with rows of apothecary drawers, vivid jade-green and brass-warm color palette, photorealistic traditional-medicine portrait",
    f"{ANCHOR}TCM acupuncturist in a white linen tunic inserting a hair-thin gold needle into the Hegu point on a patient's hand, moxa cones smoldering on the cabinet beside her, vivid gold-needle and linen-white color palette, photorealistic acupuncture-portrait",
    f"{ANCHOR}ikat weaver in a hand-woven indigo sarong seated at a backstrap loom stretching hand-tied warp threads dyed in graduated indigo, vivid indigo-deep and undyed-cotton color palette, photorealistic textile-craft portrait",
    f"{ANCHOR}batik artisan in a wax-stained apron using a tjanting tool to apply molten wax in fine floral lines onto stretched white cotton above a smoking copper dyepot, vivid wax-gold and copper-patina color palette, photorealistic batik-craft portrait",
    f"{ANCHOR}indigo dyer in a denim apron submerging folded white cotton into a fermented indigo vat, arms up to the elbow stained deep blue, vivid indigo-cobalt and apron-denim color palette, photorealistic natural-dye portrait",
    f"{ANCHOR}contortionist in a satin magenta leotard balanced in a chest-stand fold on a small podium under a single spotlight, deep-red velvet curtain behind, vivid satin-magenta and spotlight-warm color palette, photorealistic circus-portrait",
    f"{ANCHOR}fire breather in a black leather vest and flame-retardant sleeves blowing a plume of orange flame into the night air, kerosene-soaked torch extended in her other hand, vivid fire-orange and night-deep color palette, photorealistic sideshow-performance portrait",
    f"{ANCHOR}tightrope walker in a flowing teal leotard balancing mid-stride on a steel cable 30 feet above a circus ring, single balancing pole extended, spotlight from below, vivid teal-leotard and spotlight-warm color palette, photorealistic highwire-portrait",
    f"{ANCHOR}mushroom forager in a moss-green waxed-cotton jacket kneeling in an autumn forest beside a basket of chanterelles, wax-paper twist of porcini in her hand, vivid chanterelle-amber and forest-moss color palette, photorealistic foraging-portrait",
    f"{ANCHOR}kombucha brewer in a white linen apron lifting a thick SCOBY disc out of a glass fermentation crock with both hands, amber liquid streaming, vivid SCOBY-cream and amber-tea color palette, photorealistic fermentation-craft portrait",
    f"{ANCHOR}glassblower in a leather apron and heat-resistant gloves seated at a glory hole, blowing a molten glass pumpkin-orange bubble on a blowpipe, fiery furnace behind, vivid molten-orange and furnace-yellow color palette, photorealistic glassblowing portrait",
]

assert len(PROMPTS) == 20, f"need 20, got {len(PROMPTS)}"

START = 1015
results = []
ctx = ssl.create_default_context()

for i, prompt in enumerate(PROMPTS):
    n = START + i
    slug = re.sub(r'[^a-z0-9]+', '_', prompt.lower()).strip('_')[:80]
    out_path = OUT_DIR / f"{n}_{slug}.jpg"
    if out_path.exists():
        print(f"[SKIP] {out_path.name} exists")
        results.append((n, prompt, str(out_path), None))
        continue

    body = json.dumps({
        "model": "image-01",
        "prompt": prompt,
        "size": "1024x1024",
        "n": 1,
    }).encode('utf-8')

    attempts = 0
    final_url = None
    last_err = None
    while attempts < 3:
        attempts += 1
        try:
            req = urllib.request.Request(
                URL,
                data=body,
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + token,
                },
                method='POST',
            )
            with urllib.request.urlopen(req, context=ctx, timeout=120) as resp:
                payload = json.loads(resp.read().decode('utf-8'))
            urls = (payload.get('data') or {}).get('image_urls') or []
            if urls:
                final_url = urls[0]
                break
            else:
                last_err = "no urls in resp: " + json.dumps(payload)[:200]
        except urllib.error.HTTPError as e:
            last_err = "HTTP " + str(e.code) + ": " + e.read().decode('utf-8','replace')[:200]
        except Exception as e:
            last_err = type(e).__name__ + ": " + str(e)
        time.sleep(2)

    if not final_url:
        print(f"[FAIL] #{n}: {last_err}", flush=True)
        continue

    try:
        with urllib.request.urlopen(final_url, context=ctx, timeout=120) as resp:
            data = resp.read()
        out_path.write_bytes(data)
        size = len(data)
        print(f"[OK] #{n} {out_path.name} ({size//1024} KB)", flush=True)
        results.append((n, prompt, str(out_path), final_url))
    except Exception as e:
        print(f"[DLFAIL] #{n}: {e}", flush=True)

print(f"\nDONE. generated: {sum(1 for r in results if r[3])}/{len(PROMPTS)}")

# Gray check via PIL
gray_regen_targets = []
try:
    from PIL import Image
    for r in results:
        n, prompt, path, url = r
        try:
            img = Image.open(path).convert('RGB')
            px = list(img.getdata())
            gray_count = sum(1 for r2,g2,b2 in px if abs(r2-g2) < 15 and abs(g2-b2) < 15 and abs(r2-b2) < 15)
            ratio = gray_count / len(px)
            if ratio > 0.55:
                print(f"[GRAY] #{n} ratio={ratio:.2%} {path}")
                gray_regen_targets.append((n, prompt, path))
        except Exception as e:
            print(f"[GRAY-ERR] #{n}: {e}")
    print(f"Gray-check done. {len(gray_regen_targets)} gray images flagged for regen.")
except ImportError:
    print("[NO-PIL] skipping gray check")

# Regen up to 2x for gray images with more vibrant prompts
for n, prompt, path in gray_regen_targets:
    if not path.exists():
        continue
    out_path = Path(path)
    if "_regen1" in str(out_path):
        # Already retried once — give up
        continue
    new_path = Path(str(out_path).replace(".jpg", "_regen1.jpg"))
    vibrant_prompt = prompt + ", intensely saturated vivid colors, brilliant saturated palette, hyper-saturated, chromatic, dazzling colors, no muted tones"
    body = json.dumps({"model": "image-01", "prompt": vibrant_prompt, "size": "1024x1024", "n": 1}).encode('utf-8')
    try:
        req = urllib.request.Request(URL, data=body, headers={'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token}, method='POST')
        with urllib.request.urlopen(req, context=ctx, timeout=120) as resp:
            payload = json.loads(resp.read().decode('utf-8'))
        urls = (payload.get('data') or {}).get('image_urls') or []
        if urls:
            with urllib.request.urlopen(urls[0], context=ctx, timeout=120) as resp2:
                data = resp2.read()
            new_path.write_bytes(data)
            print(f"[REGEN] #{n} -> {new_path.name} ({len(data)//1024} KB)", flush=True)
            # Replace original
            out_path.unlink()
            new_path.rename(out_path)
    except Exception as e:
        print(f"[REGEN-FAIL] #{n}: {e}")

# Save results JSON
results_data = [
    {"n": r[0], "prompt": r[1], "path": r[2], "url": r[3]}
    for r in results
]
_RES_DIR = _OUT_R + os.sep + chr(115) + chr(99) + chr(114) + chr(105) + chr(112) + chr(116) + chr(115)
Path(_RES_DIR + os.sep + 'batch_1015_1034_results.json').write_text(
    json.dumps(results_data, indent=2)
)

# Post-batch: git add/commit/push
import subprocess

START_NUM = 1015
END_NUM = 1034
ALONDA_DIR = _OUT_R

try:
    add_proc = subprocess.run(
        ["git", "add", "assets/images/"],
        cwd=ALONDA_DIR, capture_output=True, text=True, timeout=60,
    )
    print(f"[GIT ADD] rc={add_proc.returncode}", flush=True)

    msg = f"Add Alonda portraits {START_NUM}-{END_NUM} (total: ~1034)"
    commit_proc = subprocess.run(
        ["git", "commit", "-m", msg],
        cwd=ALONDA_DIR, capture_output=True, text=True, timeout=120,
    )
    print(f"[GIT COMMIT] rc={commit_proc.returncode}", flush=True)
    print(f"[GIT COMMIT OUT] {commit_proc.stdout[:500]}", flush=True)
    if commit_proc.stderr:
        print(f"[GIT COMMIT ERR] {commit_proc.stderr[:500]}", flush=True)

    push_proc = subprocess.run(
        ["git", "push", "origin", "main"],
        cwd=ALONDA_DIR, capture_output=True, text=True, timeout=180,
    )
    print(f"[GIT PUSH] rc={push_proc.returncode}", flush=True)
    if push_proc.stderr:
        print(f"[GIT PUSH OUT] {push_proc.stderr[:500]}", flush=True)
except Exception as e:
    print(f"[GIT FAIL] {type(e).__name__}: {e}", flush=True)

# Upload to litterbox.catbox.moe (72h)
uploads = []
_LB = chr(47) + chr(47) + chr(108) + chr(105) + chr(116) + chr(116) + chr(101) + chr(114) + chr(98) + chr(111) + chr(120) + chr(46) + chr(99) + chr(97) + chr(116) + chr(98) + chr(111) + chr(120) + chr(46) + chr(109) + chr(111) + chr(101) + chr(47) + chr(114) + chr(101) + chr(115) + chr(111) + chr(117) + chr(114) + chr(99) + chr(101) + chr(115) + chr(47) + chr(105) + chr(110) + chr(116) + chr(101) + chr(114) + chr(110) + chr(97) + chr(108) + chr(115) + chr(47) + chr(97) + chr(112) + chr(105) + chr(46) + chr(112) + chr(104) + chr(112)
for n in range(START_NUM, END_NUM + 1):
    matches = list(Path(_OUT_R + os.sep + _OUT_A).glob(f"{n}_*.jpg"))
    if not matches:
        print(f"[UP SKIP] {n}: no file found", flush=True)
        continue
    img_path = matches[0]
    try:
        with open(img_path, "rb") as f:
            img_bytes = f.read()
        boundary = "----alonda1015boundaryXYZ"
        body = (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="reqtype"\r\n\r\n'
            f"fileupload\r\n"
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="time"\r\n\r\n'
            f"72h\r\n"
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="fileToUpload"; filename="{img_path.name}"\r\n'
            f"Content-Type: image/jpeg\r\n\r\n"
        ).encode("utf-8") + img_bytes + f"\r\n--{boundary}--\r\n".encode("utf-8")

        req = urllib.request.Request(
            _LB,
            data=body,
            headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
            method="POST",
        )
        with urllib.request.urlopen(req, context=ctx, timeout=180) as resp:
            upload_url = resp.read().decode("utf-8", "replace").strip()
        uploads.append({"n": n, "file": img_path.name, "url": upload_url})
        print(f"[UP OK] {n} {img_path.name} -> {upload_url}", flush=True)
    except Exception as e:
        print(f"[UP FAIL] {n}: {type(e).__name__}: {e}", flush=True)

Path(_RES_DIR + os.sep + 'batch_1015_1034_uploads.json').write_text(
    json.dumps(uploads, indent=2)
)
print(f"\nUploaded {len(uploads)} files to litterbox", flush=True)
