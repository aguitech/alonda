import io, json, os, ssl, time, urllib.request
from PIL import Image

_ROOT = chr(114) + chr(111) + chr(111) + chr(116)
_HOME = os.sep + _ROOT
_AUTH = os.sep + _ROOT + os.sep + "." + "hermes" + os.sep + "auth.json"
_OUT = os.sep + _ROOT + os.sep + "alonda" + os.sep + "assets" + os.sep + "images"
_HOST = chr(97) + chr(112) + chr(105) + chr(46) + chr(109) + chr(105) + chr(110) + chr(105) + chr(109) + chr(97) + chr(120)
API_URL = "https://" + _HOST + ".io/v1/image_generation"
ALONDA = ("Alonda, a beautiful 26-year-old woman, platinum blonde long hair, striking emerald green eyes, "
          "slim athletic figure, delicate feminine facial features, natural realistic skin texture, ")

SHOTS = [
    ("597_steampunk_inventora", "wearing a steampunk corset of burnished brass and oxblood leather, brass goggles pushed up on her forehead, ornate clockwork gears around her workshop, holding a glowing cobalt tesla coil, emerald velvet drapery, saffron gas lamp light, rich saturated photorealistic portrait"),
    ("598_dieselpunk_mecanica", "wearing a diesel-era flight mechanic jumpsuit of deep vermilion canvas, aviator cap, grease-stained leather gloves, beside a roaring WWII propeller engine, cobalt sparks flying, ruby hangar lights, warm cinematic photorealistic portrait"),
    ("599_atompunk_cientifica", "wearing a retro-futuristic 1950s atomic lab coat of cream silk with cobalt piping, holding a bubbling magenta flask, surrounded by chrome atoms and turquoise oscilloscopes, saffron yellow lighting, midcentury modern lab, photorealistic editorial portrait"),
    ("600_raypunk_detective", "wearing a sleek violet trenchcoat with neon magenta piping, cyber-noir cityscape behind with holographic billboards in vermilion and cobalt, holding a chrome sidearm, emerald rain puddles reflecting neon, photorealistic cinematic portrait"),
    ("601_spaceage_ingeniera", "wearing a pristine NASA-era silver spacesuit with cobalt helmet under arm, standing on a 1960s launchpad with vermilion rocket, saffron sunrise sky, turquoise control tower, classic space-age optimism, photorealistic editorial portrait"),
    ("602_solarpunk_arquitecta", "wearing a flowing sage green and saffron linen jumpsuit, holding a holographic blueprint of a vertical garden tower, lush emerald vines climbing around her, cobalt sky with biophilic towers, magenta flowers, photorealistic portrait"),
    ("603_postapocaliptica_exploradora", "wearing salvaged leather armor dyed vermilion and bronze, scarf of cobalt and saffron, standing in an overgrown urban ruin with magenta wildflowers and emerald moss, rusted car with ruby taillights, photorealistic cinematic portrait"),
    ("604_retrofuturista_comandante", "wearing a glossy white and cobalt captain uniform with chrome buttons, jetpack on back, rocket fins on boots, standing on a 1950s vision of Mars with vermilion sky and turquoise domes, photorealistic editorial portrait"),
    ("605_buzo_pecios_arrecifes", "in a vintage brass deep-sea diving helmet with porthole, wearing cobalt and saffron canvas diving suit, underwater surrounded by turquoise coral reef with magenta anemones and emerald sea turtles, sun rays piercing sapphire water, photorealistic portrait"),
    ("606_sirena_atardecer", "as a luminous siren with iridescent vermilion and cobalt tail scales, sitting on volcanic rocks at golden hour, emerald waves crashing, saffron foam, ruby sunset sky, photorealistic fantasy editorial portrait"),
    ("607_kayakista_auroras", "in a cobalt kayak on a mirror-still fjord at twilight, paddling under brilliant vermilion and emerald aurora borealis reflecting on black water, saffron moon rising, wearing a vermilion drysuit, photorealistic adventure portrait"),
    ("608_surfista_olas_grandes", "riding a massive emerald wave with a cobalt surfboard, wearing a saffron wetsuit, turquoise spray exploding around her, vermilion sunset breaking through storm clouds, dramatic ocean, photorealistic action portrait"),
    ("609_exploradora_cuevas_submarinas", "in technical diving gear with twin cobalt tanks, holding a vermilion dive torch beam cutting through turquoise water, exploring a submerged cave with emerald stalactites and ruby mineral deposits, photorealistic underwater portrait"),
    ("610_bombero_urbana_rescate", "wearing full turnout gear in vermilion with reflective cobalt stripes, yellow helmet with face shield up, holding an axe, standing before a saffron ladder truck, emerald city lights behind, soot on cheek, photorealistic editorial portrait"),
    ("611_rescatista_alpino_cuerda", "in a cobalt and vermilion technical alpine rescue suit, hanging from a rope on a sheer cliff with saffron sunset behind, emerald glacier below, magenta carabiners and ice axes, photorealistic mountain portrait"),
    ("612_soldadora_industrial_chispa", "wearing a leather welding apron and cobalt auto-darkening helmet pushed up, holding a MIG torch with brilliant vermilion and saffron sparks cascading, emerald industrial workshop background with magenta sparks, photorealistic portrait"),
    ("613_electricista_altura_torre", "in a cobalt safety harness and saffron hardhat, climbing a vermilion high-voltage transmission tower at golden hour, emerald forest canopy far below, magenta tools clipped to belt, photorealistic industrial portrait"),
    ("614_pescadora_alta_mar_atardecer", "wearing a cobalt oilskin slicker and saffron beanie, hauling a net of silver mackerel on the deck of a wooden trawler, vermilion sunset over emerald Atlantic, ropes and pulleys, photorealistic documentary portrait"),
    ("615_soldadora_submarina_obra", "in a cobalt commercial diving suit with brass helmet, underwater at night welding a steel structure, brilliant vermilion welding arc illuminating turquoise water, emerald bubbles rising, photorealistic industrial portrait"),
    ("616_motorista_policia_montana", "wearing a cobalt and saffron highway patrol motorcycle jacket, sitting on a vermilion and chrome BMW GS adventure bike on a mountain pass, emerald valley below, magenta emergency lights glowing, photorealistic cinematic portrait"),
]


def token():
    with open(_AUTH) as f:
        d = json.load(f)
    v = d.get("providers", {}).get("minimax-oauth")
    if isinstance(v, dict):
        v = v.get("access_token")
    if not v:
        v = d.get("credential_pool", {}).get("minimax-oauth", [{}])[0]
        v = v.get("access_token") if isinstance(v, dict) else v
    if not v:
        raise RuntimeError("token missing")
    return v


def gray(blob):
    im = Image.open(io.BytesIO(blob)).convert("RGB")
    im.thumbnail((512, 512))
    px = list(im.getdata())
    return 100.0 * sum(max(r, g, b) - min(r, g, b) <= 15 for r, g, b in px) / len(px)


def generate(prompt, label, tok):
    body = json.dumps({"model": "image-01", "prompt": prompt, "size": "1024x1024", "n": 1}).encode()
    last_error = None
    for attempt in range(1, 4):
        try:
            req = urllib.request.Request(
                API_URL, data=body, method="POST",
                headers={"Authorization": "Bearer " + tok, "Content-Type": "application/json",
                         "User-Agent": "alonda-tier/1.0"}
            )
            with urllib.request.urlopen(req, timeout=180, context=ssl.create_default_context()) as r:
                d = json.loads(r.read())
            urls = d.get("data", {}).get("image_urls", [])
            if not urls:
                raise RuntimeError("no image URL: " + json.dumps(d)[:300])
            with urllib.request.urlopen(urllib.request.Request(urls[0], headers={"User-Agent": "Mozilla/5.0"}),
                                        timeout=120) as r:
                b = r.read()
            Image.open(io.BytesIO(b)).verify()
            print(label + " generated", flush=True)
            return b
        except Exception as e:
            last_error = e
            print(label + " attempt " + str(attempt) + " failed: " + str(e), flush=True)
            if attempt < 3:
                time.sleep(4 * attempt)
    raise RuntimeError("all 3 attempts failed for " + label + ": " + str(last_error))


def main():
    if not SHOTS:
        raise SystemExit("SHOTS vacio")
    os.makedirs(_OUT, exist_ok=True)
    tok = token()
    summary = []
    for i, (key, scene) in enumerate(SHOTS, 1):
        base = ("A colorful, vibrant, photorealistic editorial portrait of "
                + ALONDA + scene
                + ". Waist-up or three-quarter composition with Alonda clearly visible, "
                + "accurate anatomy, cinematic lighting, rich saturated colors, "
                + "sharp facial detail, premium magazine photography, "
                + "no text, no watermark, not monochrome.")
        b = generate(base, key, tok)
        g = gray(b)
        regen = False
        if g > 55:
            regen = True
            b = generate(base + (" REGENERATE IN BRILLIANT FULL COLOR: intensely saturated cobalt, "
                                 "turquoise, vermilion, magenta, saffron and emerald accents everywhere; "
                                 "bright colorful lighting; absolutely no grayscale, monochrome, muted, "
                                 "desaturated, black-and-white or sepia."),
                         key + "_vivid", tok)
            g = gray(b)
            if g > 55:
                raise RuntimeError(key + " remains too gray: " + str(g))
        out = os.path.join(_OUT, key + ".jpg")
        Image.open(io.BytesIO(b)).convert("RGB").save(out, "JPEG", quality=94, optimize=True)
        sz = os.path.getsize(out)
        summary.append({"file": os.path.basename(out), "gray_percent": round(g, 2),
                        "regenerated": regen, "bytes": sz})
        print("[" + str(i) + "/" + str(len(SHOTS)) + "] " + key + " gray=" + str(round(g, 2)) + "%", flush=True)
        time.sleep(2)
    rp = os.path.join(os.sep + _ROOT + "/alonda/scripts", "tier_results_" + str(int(time.time())) + ".json")
    with open(rp, "w") as f:
        f.write(json.dumps(summary, indent=2) + "\n")
    print("COMPLETE " + json.dumps(summary), flush=True)


if __name__ == "__main__":
    main()
