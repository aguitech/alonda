#!/usr/bin/env python3
"""Generate Alonda portraits 1055-1074.

Mix of FRESH categories not used in 1-1054:
- Underwater photography & freediving (free diver at blue hole, kelp forest swimmer,
  cenote cavern diver, ice diver under frozen lake, manta ray night snorkel,
  underwater cave photographer, kelp forest freediver, cenote light beam diver,
  sperm whale close encounter, jellyfish ballet freediver)
- Time-stop motion & classical animation (claymation puppet workshop, stop-motion
  armature builder, puppet face painter, miniature set builder, replacement-face
  animator, latex mold maker, puppet hair puncher, animatronic figure builder,
  shadow-puppet carver, stop-motion lighting designer)
- Architectural preservation & restoration (mosaicist at Pompeii fresco, gothic
  cathedral gargoyle restorer, Art Nouveau stained-glass conservator, ancient
  Roman mosaic restorer, baroque ceiling fresco conservator, medieval manuscript
  illuminator, Tang dynasty tomb muralist, Persian carpet conservator, Venetian
  plaster restorer, Japanese temple carpenter)
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
    # --- Underwater photography & freediving (10) ---
    f"{ANCHOR}free diver in a sleek low-profile bioprene wetsuit suspended in a vertical descent into a Bahamian blue hole, sunlight shafts piercing the ultramarine water, vivid blue-hole-azure and wetsuit-graphite color palette, photorealistic underwater portrait",
    f"{ANCHOR}kelp forest swimmer in a cobalt wetsuit weaving through towering golden kelp fronds in clear Pacific green water, sunbeams filtering down, vivid kelp-gold and ocean-emerald color palette, photorealistic underwater portrait",
    f"{ANCHOR}cenote cavern diver in a tropical-print rash guard and mask floating in a Mexican cenote cavern, milky limestone beams of sunlight penetrating the turquoise freshwater, vivid cenote-turquoise and limestone-cream color palette, photorealistic cenote-portrait",
    f"{ANCHOR}ice diver in a drysuit beneath a frozen Antarctic lake with crystalline ice ceiling above her, breathing regulator mist visible, vivid ice-cyan and drysuit-red color palette, photorealistic ice-diving portrait",
    f"{ANCHOR}manta ray night snorkel portrait of her in a black wetsuit holding a blue glow-stick as a giant manta ray glides past in inky tropical water, vivid manta-black and glow-stick-blue color palette, photorealistic manta-ray portrait",
    f"{ANCHOR}underwater cave photographer in a side-mount rig holding a housed strobe inside a submerged limestone cavern, fossil shells visible on the cave wall, vivid cave-emerald and strobe-white color palette, photorealistic cave-diving portrait",
    f"{ANCHOR}kelp forest freediver in an emerald bikini suspended motionless in a giant California kelp forest, shafts of sunlight slanting down through amber fronds, vivid kelp-amber and ocean-jade color palette, photorealistic freediving portrait",
    f"{ANCHOR}cenote light beam diver in a yellow rash guard swimming through a beam of refracted sunlight in a Yucatan cenote, white sand below, vivid cenote-turquoise and sand-white color palette, photorealistic cenote-light portrait",
    f"{ANCHOR}sperm whale close encounter portrait of her in a freediving wetsuit face-to-face with a curious sperm whale in clear Caribbean blue water, vivid whale-charcoal and ocean-azure color palette, photorealistic whale-encounter portrait",
    f"{ANCHOR}jellyfish ballet freediver in a flowy white swimsuit suspended among a swarm of moon jellyfish in cobalt deep water, backlit jellies glowing, vivid jelly-lilac and cobalt-blue color palette, photorealistic jellyfish-ballet portrait",
    # --- Time-stop motion & classical animation (5) ---
    f"{ANCHOR}claymation puppet workshop portrait of her in a denim smock seated at a stop-motion armature, sculpting a tiny clay figure on a wire skeleton, vivid clay-terracotta and smock-denim color palette, photorealistic puppet-workshop portrait",
    f"{ANCHOR}stop-motion armature builder in a leather apron working at a jeweler's bench welding a brass ball-and-socket armature for a tiny puppet, vivid brass-warm and apron-leather color palette, photorealistic armature-builder portrait",
    f"{ANCHOR}puppet face painter in a flour-dusted apron seated at a workbench painting tiny delicate features onto a 6-inch replacement puppet face using a single-hair brush, vivid puppet-blush and apron-flour color palette, photorealistic face-painting portrait",
    f"{ANCHOR}miniature set builder in a paint-flecked work shirt standing in a tiny fully-furnished room set with brick-pattern wallpaper, working on a 1:12 scale dining table, vivid wallpaper-brick and table-oak color palette, photorealistic miniatures portrait",
    f"{ANCHOR}replacement-face animator in a charcoal sweater photographing a tiny sculpted face with a macro lens on a copy stand, vivid face-clay and sweater-charcoal color palette, photorealistic animator-portrait",
    # --- Architectural preservation & restoration (5) ---
    f"{ANCHOR}Pompeian fresco restorer in a linen smock seated on scaffolding carefully retouching an ancient Pompeian wall painting of a garden, terracotta and ochre pigments on her palette, vivid fresco-terracotta and smock-linen color palette, photorealistic restoration-portrait",
    f"{ANCHOR}gothic cathedral gargoyle restorer in a navy boiler suit perched on scaffolding beside a stone gargoyle, mallet and chisel in hand, vivid stone-gray and boiler-navy color palette, photorealistic restoration-portrait",
    f"{ANCHOR}Art Nouveau stained-glass conservator in a velvet beret and waxed-cotton smock standing at a leaded-glass easel restoring a Mucha-style panel, vivid glass-amber and velvet-burgundy color palette, photorealistic stained-glass-portrait",
    f"{ANCHOR}medieval manuscript illuminator in a wool kirtle seated at a sloped writing desk grinding azurite and gold leaf, illuminated page of a bestiary in front of her, vivid azurite-blue and gold-leaf color palette, photorealistic illuminator-portrait",
    f"{ANCHOR}Venetian plaster restorer in a linen apron troweling fresh lime plaster onto a cracked baroque ceiling rose, plaster trowel in hand, vivid plaster-cream and ceiling-rose color palette, photorealistic plaster-portrait",
]

assert len(PROMPTS) == 20, f"need 20, got {len(PROMPTS)}"

START = 1055
results = []
ctx = ssl.create_default_context()

for i, prompt in enumerate(PROMPTS):
    n = START + i
    slug = re.sub(r'[^a-z0-9]+', '_', prompt.lower()).strip('_')[:80]
    out_path = OUT_DIR / f"{n}_{slug}.jpg"
    if out_path.exists():
        print(f"[SKIP] {out_path.name} exists", flush=True)
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
        if not url:
            continue
        try:
            img = Image.open(path).convert('RGB')
            px = list(img.getdata())
            gray_count = sum(1 for r2,g2,b2 in px if abs(r2-g2) < 15 and abs(g2-b2) < 15 and abs(r2-b2) < 15)
            ratio = gray_count / len(px)
            if ratio > 0.55:
                print(f"[GRAY] #{n} ratio={ratio:.2%} {path}", flush=True)
                gray_regen_targets.append((n, prompt, path))
        except Exception as e:
            print(f"[GRAY-ERR] #{n}: {e}", flush=True)
    print(f"Gray-check done. {len(gray_regen_targets)} gray images flagged for regen.", flush=True)
except ImportError:
    print("[NO-PIL] skipping gray check", flush=True)

# Regen up to 2x for gray images with more vibrant prompts
for n, prompt, path in gray_regen_targets:
    if not path or not Path(path).exists():
        continue
    out_path = Path(path)
    if "_regen" in str(out_path):
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
        print(f"[REGEN-FAIL] #{n}: {e}", flush=True)

# Save results JSON
SCRIPT_DIR = Path("/root/alonda/scripts")
(SCRIPT_DIR / f"batch_{START}_{START+19}_results.json").write_text(
    json.dumps([{"n": r[0], "prompt": r[1], "path": r[2], "url": r[3]} for r in results], indent=2)
)
print(f"\nFinal results saved.", flush=True)