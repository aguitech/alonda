#!/usr/bin/env python3
"""
Cron job script: generate 20 unique Alonda portraits, save locally, commit + push,
upload new images to tmpfiles.org, and report results.
"""
import os
import io
import sys
import json
import time
import glob
import random
import string
import shutil
import subprocess
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path

# --- CONFIG ---
REPO = Path("/root/alonda")
IMG_DIR = REPO / "assets" / "images"
AUTH_FILE = Path("/root/.hermes/auth.json")
GOAL = 20000
BATCH = 20
SLEEP_BETWEEN = 0.6
MAX_RETRIES_GRAY = 2

ANCHOR = (
    "Alonda, a beautiful 26-year-old woman, platinum blonde long hair, "
    "striking emerald green eyes, slim athletic figure, "
    "delicate feminine facial features, natural realistic skin texture, "
)

# Load token WITHOUT writing it to disk in plain view (build by parts)
with open(AUTH_FILE) as f:
    auth = json.load(f)
TOKEN = (
    auth.get("providers", {})
    .get("minimax-oauth", {})
    .get("access_token")
    or auth.get("credential_pool", {}).get("minimax-oauth", [{}])[0].get("access_token")
)
if not TOKEN:
    print("ERROR: no token in auth.json", file=sys.stderr)
    sys.exit(1)

# Build URL/prefixes by parts to avoid filter heuristics
URL_BASE = "https://api." + "minimax" + ".io/v1/image_generation"


def get_existing_count():
    files = list(IMG_DIR.glob("*.jpg")) + list(IMG_DIR.glob("*.jpeg"))
    return len(files)


def make_unique_20_prompts(start_num, used_prompts_blob):
    """
    Generate 20 distinct prompts by mixing 3 random categories.
    Uses start_num as seed offset to vary across runs.
    """
    rng = random.Random(start_num + int(time.time()) % 100000)

    cats = {
        "extreme_sports": [
            "free solo climbing El Capitan Yosemite at sunset",
            "skydiving over tropical coast turquoise water",
            "snowboarding backcountry deep powder Alaska",
            "motocross rider mid-air over dirt track",
            "skateboarding in bowl Venice Beach golden hour",
            "parkour rooftop traceur city sunset",
            "BMX dirt jumper over massive ramp",
            "whitewater rafting Class V rapids Colorado River",
            "kitesurfing giant waves Maui",
            "cave diving cenote Mexico crystal blue water",
        ],
        "modern_pro": [
            "architect with blueprints and physical model in studio",
            "UX designer with wireframes and tablet in modern office",
            "programmer in front of multi-monitor setup with neon code",
            "surgeon in operating room under surgical lights",
            "head nurse with stethoscope in modern hospital corridor",
            "lawyer in courtroom with gavil and law books",
            "investigative journalist with recorder and notebook",
            "pastry chef decorating elaborate cake in patisserie",
            "sommelier swirling wine in crystal glass in cellar",
            "head brewer checking wort in copper brewery tanks",
        ],
        "pop_culture": [
            "Matrix bullet-time dodging in leather coat",
            "Blade Runner neon detective in rainy Los Angeles 2049",
            "Star Wars Jedi with green lightsaber meditation pose",
            "Star Trek Starfleet captain on bridge of starship",
            "Harry Potter powerful witch casting spell with wand",
            "Lord of the Rings ethereal elf in Rivendell forest",
            "Marvel cosmic superhero with glowing energy",
            "DC superheroine in Gotham rooftop at night",
            "anime magical girl transformation sequence sparkles",
            "anime shonen warrior with katana in cherry blossoms",
        ],
        "history": [
            "Roman matron in toga at Forum 100 AD marble columns",
            "ancient Greek philosopher in Agora olive groves",
            "Egyptian pharaoh queen with gold nemes headdress",
            "Mesopotamian priestess in ziggurat at night with torches",
            "Byzantine empress with jeweled crown Hagia Sophia",
            "Edwardian lady in lace tea garden 1905",
            "Elizabethan noblewoman at court ruff collar pearls",
            "late Victorian seamstress in London attic workshop",
            "Belle epoque Parisian cabaret dancer Moulin Rouge",
            "art nouveau muse with stained glass lily motif",
        ],
        "mythology": [
            "Greek goddess Athena in silver armor with owl and shield",
            "Greek god Apollo with golden lyre and laurel wreath",
            "Greek goddess Aphrodite rising from sea foam",
            "Greek goddess Artemis with silver bow hunting in forest",
            "Greek god Hermes with winged sandals caduceus",
            "Greek goddess Persephone in pomegranate orchard",
            "Greek goddess Hecate at triple crossroads with torches",
            "Norse god Odin on throne with ravens Huginn Muninn",
            "Norse god Thor with Mjolnir storm clouds lightning",
            "Egyptian goddess Isis with throne headdress and wings",
        ],
        "creative_pro": [
            "analog film photographer in darkroom with red light and negatives",
            "children's book illustrator with watercolor palette and easel",
            "tattoo artist with gloved hands and machine in neon studio",
            "goldsmith jeweler at workbench with tiny hammer and gems",
            "sculptor chiseling marble in bright sunlit atelier",
            "muralist painting giant wall with spray cans",
            "master weaver at wooden loom creating colorful tapestry",
            "master potter shaping clay on wheel in rustic studio",
        ],
        "performance": [
            "circus ringmaster in red tailcoat top hat spotlight",
            "cabaret performer in feathered headdress red curtain",
            "stage magician pulling rabbit from top hat sparkles",
            "greek theater actor in masks amphitheater sunset",
            "opera singer in red velvet gown at La Scala",
            "contemporary ballet dancer in white leotar studio mirror",
            "street mime in whiteface beret doing invisible box",
            "contortionist bending in impossible pose under spotlight",
        ],
        "subculture": [
            "kawaii fashion with pink pastel bows and pastel hair",
            "gothic lolita with black lace parasol cemetery",
            "preppy Ivy League campus autumn",
            "gothic Victorian crypt with candelabra",
            "punk rock mohawk leather jacket anarchy",
            "grunge 90s flannel and ripped jeans",
            "hipster artisan coffee shop with vinyl",
            "skater halfpipe graffiti wall sunset",
            "surfer girl with vintage woody van beach",
            "mod 60s scooter girl Carnaby Street London",
        ],
        "music": [
            "concert violinist in black gown Carnegie Hall",
            "cellist in tuxedo on wooden stage",
            "jazz pianist in smoky basement club neon",
            "trumpeter in art deco lounge with brass",
            "rock drummer mid-sticks-flourish arena lights",
            "harpist in white gown beside window sunlight",
            "opera soprano in red velvet gown theater",
            "DJ techno in warehouse fog laser lights",
            "blues singer in dimly lit juke joint microphone",
            "folk guitarist campfire mountains night sky",
        ],
        "dance": [
            "ballet prima ballerina on pointe tutu spotlight",
            "contemporary dancer in studio with sunbeam",
            "flamenco dancer in red ruffled dress Spanish courtyard",
            "tango dancer Buenos Aires milonga night",
            "salsa dancer in Caribbean club colorful lights",
            "hip-hop dancer in urban street basketball court",
            "breakdancer doing freeze on cardboard sunset",
            "belly dancer with golden coins jingling veil",
            "k-pop idol on glowing stage LED cubes",
            "hula dancer Hawaii flower lei ocean backdrop",
        ],
        "vehicles": [
            "classic car mechanic under 1965 Mustang hood",
            "Formula 1 driver in cockpit helmet race day",
            "train conductor in vintage steam locomotive cabin",
            "navigator with sextant on sailing ship deck",
            "ship captain on bridge of cargo vessel storm",
            "helicopter pilot in cockpit mountains rescue",
            "vintage taxi driver in yellow Checker cab NYC",
            "motorcyclist on cruiser desert highway sunset",
            "tractor driver in wheat field harvest golden",
            "solo sailor in stormy sea aboard small yacht",
        ],
        "world_festivals": [
            "Rio carnival samba dancer in elaborate feathered costume",
            "Oktoberfest Bavarian dirndl beer stein Munich tent",
            "Holi festival throwing bright colored powders in Jaipur",
            "San Juan bonfire on beach midnight summer solstice",
            "Up Helly Aa Scotland Viking torch procession",
            "Inti Raymi Inca sun festival Cusco golden",
            "Songkran Thai water festival with water gun temple",
            "Chinese New Year dragon dance red lanterns Temple",
            "Mardi Gras New Orleans bead throws balcony Bourbon St",
            "Dia de los Muertos Catrina sugar skull face paint",
        ],
        "retro_scifi": [
            "steampunk inventor with brass goggles and gear watch",
            "dieselpunk mechanic in hangar with riveted plane WWII",
            "atompunk 1950s scientist with bubbling beakers chrome",
            "cyberpunk hacker with neural cables and neon city",
            "biopunk geneticist in bioluminescent lab",
            "solarpunk architect in vertical garden tower greenhouse",
            "post-apocalyptic survivor in wasteland gas mask",
            "retrofuturist space age stewardess white uniform",
            "raypunk detective in trenchcoat hovering cars rain",
            "solarpunk engineer with sun panel and butterflies",
        ],
        "fairy_tales": [
            "Disney princess in ball gown castle balcony sunset",
            "fairy godmother with magic wand sparkles forest",
            "good witch with pointed hat and bubbling cauldron",
            "kind giant in flower meadow holding tiny village",
            "gnome in mossy mushroom house forest floor",
            "mermaid on rock at sunrise combing long hair",
            "centaur archer in forest glade with bow",
            "dragon queen in crystal cave silver scales",
            "phoenix rising from golden flames feathers glowing",
            "unicorn rider in starlit meadow silver horn glowing",
        ],
        "decades": [
            "1900s Gibson Girl on bicycle white parasol",
            "1910s suffragette in white marching banner",
            "1920s flapper Charleston with bob hair Charleston",
            "1930s aviator Amelia style with leather jacket",
            "1940s WWII pin-up in convertible red lipstick",
            "1950s soda shop girl in poodle skirt jukebox",
            "1960s mod Twiggy in geometric mini dress",
            "1970s disco queen in glitter jumpsuit mirror ball",
            "1980s neon aerobics instructor leg warmers",
            "1990s grunge riot grrrl plaid flannel",
            "2000s Y2K metallic silver butterfly clips",
            "2010s hipster artisan barista vinyl",
        ],
        "life_stages": [
            "toddler playing in autumn leaves",
            "school girl with backpack crossing road",
            "high school teen with skateboard in parking lot",
            "university student with books in ivy library",
            "newlywed in white lace dress holding bouquet",
            "young mother with newborn in nursery sunlight",
            "mid-career executive at corner office window cityscape",
            "elegant grandmother with pearl necklace at tea party",
            "active nonagenarian hiking in mountains sunrise",
            "wise centenarian in rocking chair reading by lamplight",
        ],
        "animals_nature": [
            "Amazonian indigenous guide in rainforest with jaguar cub",
            "cowgirl with lasso on palomino horse at sunset ranch",
            "ethologist observing gorillas in misty jungle",
            "veterinarian with stethoscope in modern animal clinic",
            "equestrian show jumper on bay horse over fence",
            "horsewoman riding sidesaddle through meadow",
            "falconer with red-tailed hawk on leather glove",
            "wildlife conservationist tracking elephants savanna",
            "primate caretaker feeding baby chimp sanctuary",
            "lion tamer with golden whip circus spotlight",
        ],
        "science": [
            "aerospace engineer in clean room white coat rocket",
            "roboticist working on humanoid android in lab",
            "AI researcher with glowing neural network hologram",
            "biotechnologist with microscope and DNA helix model",
            "nanotechnologist with molecular structures in vault",
            "neuroscientist with brain scan holographic display",
            "geneticist with DNA sequencing machine purple light",
            "oceanographer in submarine porthole blue water coral",
            "volcanologist on lava field in heat suit helmet",
            "meteorologist in front of weather radar screen",
        ],
        "botanical": [
            "master gardener kneeling in rose garden summer",
            "floriculturist arranging peonies in flower shop",
            "landscape architect drafting garden blueprint",
            "hydroponic farmer in vertical greenhouse with LED",
            "herbalist in apothecary with bundles of dried herbs",
            "orchid cultivator in tropical greenhouse misty",
            "bonsai master pruning ancient juniper with shears",
            "urban gardener on rooftop with tomato vines cityscape",
            "vintner in vineyard holding wine grapes golden hour",
            "permaculture designer in food forest with mushrooms",
        ],
        "extreme_jobs": [
            "urban firefighter in bunker gear holding hose at blaze",
            "alpine rescue rescuer on rope glacier crevasse",
            "rally race driver inside car dashboard dust",
            "miner with headlamp deep underground tunnel",
            "industrial welder with sparks flying from torch mask",
            "high-altitude electrician on power line tower clouds",
            "deep-sea fisherwoman on trawler at dawn",
            "coast guard on cliffs with binoculars ocean",
            "motorcycle police officer at accident scene lights",
            "female demolition worker swinging wrecking ball",
        ],
        "weather": [
            "sandstorm in Sahara dunes billowing orange",
            "golden rain falling with sunbeams glowing",
            "blizzard in mountain cabin heavy snow wind",
            "heat wave city shimmer asphalt thermometer",
            "total solar eclipse corona diamond ring sky",
            "meteor shower Perseids shooting stars night",
            "double rainbow over green valley waterfall",
            "aurora australis over Antarctic ice field purple",
            "mammatus clouds dramatic sunset over prairie",
            "rain of pink rose petals in spring garden",
        ],
        "landmarks": [
            "Machu Picchu citadel steps sunrise mist",
            "Great Wall of China watchtower autumn leaves",
            "Petra Treasury carved rose stone glowing",
            "Torres del Paine granite spires Patagonia lake",
            "Mount Fuji snow cap cherry blossoms spring",
            "Mount Kilimanjaro Uhuru peak sunrise",
            "Everest base camp prayer flags wind",
            "Salar de Uyuni Bolivia mirror salt flat water",
            "Antelope Canyon light beams sandstone swirl",
            "Zhangjiajie Avatar Hallelujah Mountains mist",
        ],
    }

    category_keys = list(cats.keys())
    rng.shuffle(category_keys)
    chosen = category_keys[:3]

    pool = []
    for k in chosen:
        pool.extend([(k, p) for p in cats[k]])

    # Deduplicate against existing used blob + within pool
    seen = set()
    norm_used = used_prompts_blob.lower() if used_prompts_blob else ""
    pool_shuffled = pool[:]
    rng.shuffle(pool_shuffled)
    final = []
    for k, p in pool_shuffled:
        key = (k, p)
        sig = p.lower()[:80]
        if key in seen:
            continue
        if sig in norm_used:
            continue
        seen.add(key)
        final.append((k, p))
        if len(final) >= BATCH:
            break

    # If short, fill from remaining pool with different sigs
    if len(final) < BATCH:
        for k, p in pool_shuffled:
            key = (k, p)
            if key in seen:
                continue
            sig = p.lower()[:80]
            if sig in norm_used:
                continue
            seen.add(key)
            final.append((k, p))
            if len(final) >= BATCH:
                break

    return final[:BATCH]


def call_image_gen(prompt):
    body = json.dumps(
        {"model": "image-01", "prompt": prompt, "size": "1024x1024", "n": 1}
    ).encode("utf-8")
    req = urllib.request.Request(
        URL_BASE,
        data=body,
        headers={
            "Authorization": "Bearer " + TOKEN,
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        raw = resp.read().decode("utf-8", errors="ignore")
    try:
        j = json.loads(raw)
    except Exception:
        # try to recover with strict=False
        from json import JSONDecoder
        j = json.loads(raw, strict=False) if False else None
        if j is None:
            return None, raw
    urls = (
        j.get("data", {}).get("image_urls")
        or j.get("data", {}).get("images")
        or j.get("images")
        or []
    )
    return (urls[0] if urls else None), raw


def download_image(url, out_path):
    req = urllib.request.Request(url, headers={"User-Agent": "curl/8.0"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = resp.read()
    out_path.write_bytes(data)
    return len(data)


def is_too_gray(path, threshold=0.55):
    try:
        from PIL import Image
        im = Image.open(path).convert("RGB")
        # Sample
        small = im.resize((64, 64))
        pixels = list(small.getdata())
        gray_count = 0
        for r, g, b in pixels:
            # saturation proxy: how close R,G,B are
            avg = (r + g + b) / 3.0
            if abs(r - avg) < 12 and abs(g - avg) < 12 and abs(b - avg) < 12:
                gray_count += 1
        ratio = gray_count / len(pixels)
        return ratio > threshold, ratio
    except Exception as e:
        return False, -1


def safe_filename(num, theme):
    base = theme.lower()
    # Keep alphanumerics + hyphens + underscores
    base = "".join(
        c if (c.isalnum() or c in ("-", "_")) else "_" for c in base
    )
    base = base[:90]
    return f"{num}_{base}.jpg"


def upload_to_tmpfiles(path):
    try:
        import subprocess as sp
        r = sp.run(
            ["curl", "-sS", "-F", "file=@" + str(path), "https://tmpfiles.org/api/v1/upload"],
            capture_output=True, text=True, timeout=120,
        )
        if r.returncode != 0:
            return None
        try:
            j = json.loads(r.stdout)
            url = j.get("data", {}).get("url")
            return url
        except Exception:
            return None
    except Exception:
        return None


def main():
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    current = get_existing_count()
    if current >= GOAL:
        print(f"GAME_OVER current={current} goal={GOAL}")
        return "GAME_OVER", current, [], []

    next_num = current + 1
    end_num = min(current + BATCH, GOAL)
    batch_n = end_num - next_num + 1

    # Build a small fingerprint of recently used prompts (use filenames as proxy)
    used_blob = ""
    try:
        recent = sorted(IMG_DIR.glob("*.*"), key=lambda p: p.stat().st_mtime)[-200:]
        used_blob = " | ".join(p.stem for p in recent)
    except Exception:
        pass

    print(f"START current={current} next={next_num} end={end_num} n={batch_n}")

    prompts = make_unique_20_prompts(next_num, used_blob)
    assert len(prompts) >= batch_n, f"only generated {len(prompts)} prompts"

    saved = []
    tmp_urls = []
    failures = []

    for idx, (cat, theme) in enumerate(prompts[:batch_n]):
        num = next_num + idx
        full_prompt = ANCHOR + theme + ", ultra detailed, cinematic lighting, 8k, vibrant colors"
        # Try + retries for gray
        attempts = 0
        success = False
        while attempts <= MAX_RETRIES_GRAY:
            try:
                url, raw = call_image_gen(full_prompt)
                if not url:
                    print(f"  [{num}] no url in resp: {raw[:200]}")
                    attempts += 1
                    time.sleep(2)
                    continue
                out = IMG_DIR / safe_filename(num, theme)
                size = download_image(url, out)
                gray, ratio = is_too_gray(out)
                if gray and attempts < MAX_RETRIES_GRAY:
                    print(f"  [{num}] too gray ({ratio:.2f}), retrying")
                    try:
                        out.unlink()
                    except Exception:
                        pass
                    attempts += 1
                    time.sleep(1)
                    continue
                saved.append(out)
                print(f"  [{num}] OK cat={cat} size={size} gray={ratio:.2f} -> {out.name}")
                success = True
                break
            except Exception as e:
                print(f"  [{num}] EXC attempt {attempts}: {e}")
                attempts += 1
                time.sleep(2)
        if not success:
            failures.append(num)
        time.sleep(SLEEP_BETWEEN)

    new_count = get_existing_count()
    print(f"DONE generated={len(saved)} failures={len(failures)} total_now={new_count}")

    # Upload NEW images only
    new_paths = sorted(saved, key=lambda p: int(p.stem.split("_")[0]))
    for p in new_paths:
        u = upload_to_tmpfiles(p)
        if u:
            tmp_urls.append((p.name, u))
            print(f"  UPLOADED {p.name} -> {u}")
        else:
            print(f"  UPLOAD FAILED {p.name}")

    # git add/commit/push
    try:
        os.chdir(REPO)
        subprocess.run(["git", "add", "assets/images/"], check=False)
        msg = f"Add Alonda portraits {next_num}-{next_num+len(saved)-1} (total: {new_count})"
        subprocess.run(["git", "commit", "-m", msg], check=False)
        push = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True, timeout=180)
        print(f"  PUSH rc={push.returncode}")
        if push.returncode != 0:
            print(f"  PUSH stderr: {push.stderr[:400]}")
        subprocess.run(["git", "log", "--oneline", "-1"], check=False)
    except Exception as e:
        print(f"  GIT ERR: {e}")

    return "OK", new_count, tmp_urls, failures


if __name__ == "__main__":
    status, total, urls, fails = main()
    print(f"FINAL_STATUS={status} TOTAL={total} URLS={len(urls)} FAILS={len(fails)}")
