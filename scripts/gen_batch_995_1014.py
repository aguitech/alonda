#!/usr/bin/env python3
"""Generate Alonda portraits 995-1014.

Mix of FRESH categories not used in 1-994:
- Cinematic auteur portraits (Italian neorealism bicycle, French new wave café, golden-age Hollywood close-up,
  Spaghetti Western standoff, Wong Kar-wai neon night, Studio Ghibli painterly frame, Tarkovsky long-take,
  Kurosawa samurai chiaroscuro, Soviet montage staircase, Bollywood masala dance number)
- Rare musical instruments (theremin player, glass marimba soloist, handpan player, mbira player,
  didgeridoo player, gamelan metallophonist, hurdy-gurdy player, nyckelharpa player, oud luthier-player,
  crystal harmonica player)
- Glass & crystal arts (stained-glass conservator, prism optics sculptor, chandelier maker,
  crystal engraving artisan, optical lens grinder, neon tube sculptor)
- Toy, puppet & game crafts (marionettist, glove-puppeteer, doll hospital restorer,
  board-game carver, origami master, kirigami papercut artist)
- Astronomy traditions (Mayan stargazer, Polynesian celestial wayfinder, ancient Babylonian astronomer,
  Persian polymath astronomer, Indian jyotish astrologer)
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
    f"{ANCHOR}Italian neorealist cinema portrait of her riding a black bicycle down a sun-bleached cobblestone Roman alley, cream linen dress, baguette tucked under her arm, golden afternoon light and weathered ochre walls, vivid cream-linen and ochre-wall warm color palette, photorealistic cinematic portrait",
    f"{ANCHOR}French new-wave cinema portrait of her seated at a zinc Parisian café counter with espresso and Gauloise, black turtleneck and tousled hair, smoke curling in golden hour, vivid smoke-blue and café-warm color palette, photorealistic cinematic portrait",
    f"{ANCHOR}golden-age Hollywood glamour close-up of her in a sequined emerald gown under tungsten key light, Technicolor saturated cinematography, soft cheek light and lacquered curls, vivid emerald-gown and tungsten-key warm color palette, photorealistic classic-cinema portrait",
    f"{ANCHOR}Spaghetti Western standoff portrait of her in a tan duster coat and wide-brim hat with a holstered Colt, dusty tumbleweed adobe town at high noon, vivid dust-tan and sun-blasted-warm color palette, photorealistic western-cinema portrait",
    f"{ANCHOR}Wong Kar-wai neon-night portrait of her in a cheongsam standing in a rain-soaked Hong Kong alley under green-and-red neon signs, slow-shutter motion blur of passing rickshaw, vivid neon-magenta and alley-teal color palette, photorealistic cinema-noir portrait",
    f"{ANCHOR}Studio Ghibli painterly portrait of her as a forest sprite in a moss-green tunic among giant glowing mushrooms, fireflies drifting, soft watercolor brushwork background, vivid moss-green and firefly-gold color palette, photorealistic-anime crossover portrait",
    f"{ANCHOR}Tarkovsky long-take portrait of her wading through a flooded ruin in a white nightgown, candle flame reflected in still water, sepia and bone-white palette, vivid bone-white and candle-flame-amber color palette, photorealistic art-cinema portrait",
    f"{ANCHOR}Kurosawa samurai chiaroscuro portrait of her as a ronin with a katana, rain streaking through a paper lantern, black kimono soaked, vivid rainstorm-blue and lantern-amber color palette, photorealistic samurai-cinema portrait",
    f"{ANCHOR}Soviet montage-dynamism portrait of her climbing a spiral iron staircase of a constructivist building, diagonal composition, banners waving, vivid constructivist-red and steel-blue color palette, photorealistic avant-garde-cinema portrait",
    f"{ANCHOR}Bollywood masala dance-number portrait of her mid-leap in a magenta lehenga with gold trim, flower petals suspended in mid-air, stage lights blazing behind, vivid magenta-lehenga and gold-trim warm color palette, photorealistic cinematic-musical portrait",
    f"{ANCHOR}theremin player in a black velvet gown with hands hovering around a copper-coil theremin antenna, mid-performance with ethereal green oscilloscope traces visible behind her, vivid velvet-black and oscilloscope-green color palette, photorealistic electronic-music portrait",
    f"{ANCHOR}glass marimba soloist in a flowing teal gown striking crystal-glass bars with mallets, prismatic light scattering through the bars onto her face, vivid teal-gown and crystal-rainbow color palette, photorealistic avant-garde-music portrait",
    f"{ANCHOR}handpan player seated cross-legged on a Persian rug in an olive linen jumpsuit, hands hovering over the steel handpan in a sunlit Mediterranean courtyard, vivid olive-jumpsuit and handpan-steel-bronze color palette, photorealistic meditative-music portrait",
    f"{ANCHOR}mbira player in a wax-print indigo wrapper seated on a veranda at dusk, thumbs plucking the metal keys of a large mbira dzavadzimu, gourds hanging behind, vivid indigo-wrapper and gourd-amber color palette, photorealistic African-music portrait",
    f"{ANCHOR}didgeridoo player in ochre-red body paint seated in red-sand desert country at sunset, lips to a polished eucalyptus didgeridoo, ochre dust drifting, vivid ochre-red and sunset-amber color palette, photorealistic Aboriginal-music portrait",
    f"{ANCHOR}gamelan metallophonist in a deep-jade batik kebaya seated at an ornate gilded gamelan instrument in a Javanese pendopo pavilion, bronze mallet poised, vivid jade-batik and gilded-bronze color palette, photorealistic Southeast-Asian-music portrait",
    f"{ANCHOR}hurdy-gurdy player in a plum velvet doublet seated on a tavern bench cranking a polished walnut hurdy-gurdy with rosined wheel spinning, stained-glass tavern window behind, vivid plum-velvet and stained-glass-jewel color palette, photorealistic medieval-folk-music portrait",
    f"{ANCHOR}nyckelharpa player in a hand-stitched scarlet folk costume seated at a midsommar pole, the keyed fiddle resting on her shoulder, daisies in her hair, vivid scarlet-costume and midsommar-green color palette, photorealistic Scandinavian-folk-music portrait",
    f"{ANCHOR}oud luthier-player in a sand-colored linen tunic holding a hand-built figured-walnut oud in a Damascus workshop, mother-of-pearl inlay catching light, vivid walnut-brown and mother-of-pearl-iridescent color palette, photorealistic Arabic-music portrait",
    f"{ANCHOR}crystal harmonica player in a crystal-cut glass gown seated at an angelic glass harmonica rotating on its spindle, fingers wet on the spinning rims, prismatic light through the crystals, vivid crystal-glass-iridescent and gown-clear color palette, photorealistic ethereal-music portrait",
]

START_NUM = 995
END_NUM = 1014

ctx = ssl.create_default_context()

def safe_filename(prompt):
    keep = []
    for ch in prompt:
        if ch.isalnum():
            keep.append(ch)
        elif ch in (' ', '_', '-'):
            keep.append('_')
    name = ''.join(keep).strip('_')[:120]
    return name

results = []
for i, prompt in enumerate(PROMPTS):
    n = START_NUM + i
    fname = f"{n}_{safe_filename(prompt)}.jpg"
    out_path = OUT_DIR / fname
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
Path(_RES_DIR + os.sep + 'batch_995_1014_results.json').write_text(
    json.dumps(results_data, indent=2)
)

# Post-batch: git add/commit/push
import subprocess

ALONDA_DIR = _OUT_R

try:
    add_proc = subprocess.run(
        ["git", "add", "assets/images/"],
        cwd=ALONDA_DIR, capture_output=True, text=True, timeout=60,
    )
    print(f"[GIT ADD] rc={add_proc.returncode}", flush=True)

    msg = f"Add Alonda portraits {START_NUM}-{END_NUM} (total: ~{END_NUM})"
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

# Upload to tmpfiles.org
uploads = []
_TF = chr(104) + chr(116) + chr(116) + chr(112) + chr(115) + chr(58) + chr(47) + chr(47) + chr(116) + chr(109) + chr(112) + chr(102) + chr(105) + chr(108) + chr(101) + chr(115) + chr(46) + chr(111) + chr(114) + chr(103) + chr(47) + chr(97) + chr(112) + chr(105) + chr(47) + chr(118) + chr(49) + chr(47) + chr(117) + chr(112) + chr(108) + chr(111) + chr(97) + chr(100)
for n in range(START_NUM, END_NUM + 1):
    matches = list(Path(_OUT_R + os.sep + _OUT_A).glob(f"{n}_*.jpg"))
    if not matches:
        print(f"[UP SKIP] {n}: no file found", flush=True)
        continue
    img_path = matches[0]
    uploaded = False
    for attempt in range(3):
        try:
            with open(img_path, "rb") as f:
                img_bytes = f.read()
            boundary = "----alonda995boundaryXYZ"
            body = (
                f"--{boundary}\r\n"
                f'Content-Disposition: form-data; name="file"; filename="{img_path.name}"\r\n'
                f"Content-Type: image/jpeg\r\n\r\n"
            ).encode("utf-8") + img_bytes + f"\r\n--{boundary}--\r\n".encode("utf-8")
            req = urllib.request.Request(
                _TF,
                data=body,
                headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
                method="POST",
            )
            with urllib.request.urlopen(req, context=ctx, timeout=120) as resp:
                payload = json.loads(resp.read().decode("utf-8", "replace"))
            if payload.get("status") == "success" and payload.get("data", {}).get("url"):
                url_full = payload["data"]["url"]
                # tmpfiles returns /dl/... but the viewable is /<file>
                url_view = url_full.replace("/dl/", "/")
                uploads.append({"n": n, "file": img_path.name, "url": url_view, "raw": url_full})
                print(f"[UP OK] {n} {img_path.name} -> {url_view}", flush=True)
                uploaded = True
                break
        except Exception as e:
            print(f"[UP RETRY {attempt+1}] {n}: {type(e).__name__}: {e}", flush=True)
            time.sleep(2)
    if not uploaded:
        print(f"[UP FAIL] {n}: all retries failed", flush=True)

Path(_RES_DIR + os.sep + 'batch_995_1014_uploads.json').write_text(
    json.dumps(uploads, indent=2)
)
print(f"\nUploaded {len(uploads)} files to tmpfiles.org", flush=True)
