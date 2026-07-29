#!/usr/bin/env python3
"""Tier 16 (261-280): unique blend of botanical technology, high-risk transport,
world festivals, weather phenomena, and creative crafts."""
import io, json, ssl, time, urllib.request
from pathlib import Path
from PIL import Image

AUTH_PATH = Path('/') / 'root' / '.hermes' / 'auth.json'
OUT_DIR = Path('/root/alonda/assets/images')
API_URL = 'https://api.' + 'minimax' + '.io/v1/image_generation'
ALONDA = ('Alonda, a beautiful 26-year-old woman, platinum blonde long hair, striking emerald green eyes, '
          'slim athletic figure, delicate feminine facial features, natural realistic skin texture, ')
SHOTS = [
('261_orchid_lab','botanical engineer cultivating luminous orchids in a glass biodome laboratory, vermilion utility jacket, cobalt hydroponic tubes, turquoise petals, saffron grow lights, emerald leaves and ruby nutrient vials, futuristic horticulture portrait'),
('262_rally_pilot','rally driver beside a mud-splashed electric rally car on a mountain hairpin, vermilion racing suit, cobalt vehicle panels, turquoise telemetry display, saffron dust cloud, emerald pines and ruby safety lights, motorsport portrait'),
('263_carnival_rio','Rio carnival costume designer backstage before the parade, vermilion feather headdress, cobalt sequined bodice, turquoise plumes, saffron spotlights, emerald samba banners and ruby glitter, festive portrait'),
('264_sandstorm','desert meteorologist observing a dramatic sandstorm from a research outpost, vermilion scarf, cobalt instruments, turquoise goggles, saffron dunes, emerald oasis and ruby warning beacon, atmospheric science portrait'),
('265_stained_glass','stained-glass artisan assembling a radiant window in a cathedral workshop, vermilion apron, cobalt lead came, turquoise glass shards, saffron sunlight, emerald peacock motif and ruby glass roses, craft portrait'),
('266_quantum_lab','quantum physicist in a cryogenic laboratory beside a glowing quantum processor, vermilion blazer, cobalt machinery, turquoise circuit light, saffron data holograms, emerald cables and ruby indicator LEDs, science portrait'),
('267_sky_train','train conductor on a fantastical alpine sky railway, vermilion uniform, cobalt locomotive, turquoise viaduct, saffron sunrise, emerald peaks and ruby signal lanterns, transport adventure portrait'),
('268_holi','Holi festival dancer throwing clouds of colored powder in Jaipur, vermilion sari, cobalt scarf, turquoise powder burst, saffron marigolds, emerald bangles and ruby powder haze, joyful cultural portrait'),
('269_bonsai','bonsai master shaping an ancient juniper in a serene mountain studio, vermilion work robe, cobalt ceramic pot, turquoise pruning tools, saffron lantern, emerald needles and ruby maple accent, Japanese horticulture portrait'),
('270_coast_guard','coast guard rescue swimmer on a stormy Atlantic cutter deck, vermilion flotation suit, cobalt ocean, turquoise rescue boat, saffron beacon, emerald rain gear and ruby flare, maritime hero portrait'),
('271_neurotech','neurotechnology researcher wearing a noninvasive brain-computer interface in a colorful clinic, vermilion lab coat, cobalt scanner, turquoise neural visualizations, saffron lamps, emerald plants and ruby electrodes, medical technology portrait'),
('272_whisky_taster','whisky master distiller evaluating amber spirits in a Scottish distillery, vermilion tartan vest, cobalt copper stills, turquoise glass reflections, saffron whisky, emerald peat moss and ruby seal, artisan portrait'),
('273_bungee','bungee jumper poised above a rainforest gorge, vermilion harness, cobalt bridge, turquoise river, saffron sunlight, emerald jungle canopy and ruby safety rope, extreme adventure portrait'),
('274_typography','letterpress printer arranging colorful movable type in an old print shop, vermilion apron, cobalt press, turquoise ink rollers, saffron paper, emerald type cases and ruby poster sheets, creative craft portrait'),
('275_mardi_gras','Mardi Gras mask maker in New Orleans workshop, vermilion velvet mask, cobalt feathers, turquoise beads, saffron lamplight, emerald sequins and ruby carnival ribbons, costume arts portrait'),
('276_antarctic','Antarctic glaciologist on a blue ice expedition, vermilion parka, cobalt glacier, turquoise ice cave, saffron low sun, emerald expedition flags and ruby instruments, polar science portrait'),
('277_pizzaiola','artisan pizza maker spinning dough in a Naples wood-fired kitchen, vermilion apron, cobalt tiled oven, turquoise basil, saffron mozzarella, emerald herbs and ruby tomatoes, culinary portrait'),
('278_mecha_pilot','mecha pilot standing in a rain-soaked neon hangar, vermilion flight suit, cobalt robotic armor, turquoise holograms, saffron maintenance sparks, emerald panels and ruby warning lights, cinematic science fiction portrait'),
('279_tango','tango dancer in a Buenos Aires milonga, vermilion dress, cobalt suit, turquoise bandoneon, saffron chandeliers, emerald velvet and ruby roses, passionate dance portrait'),
('280_rainbow_sky','landscape photographer beneath a double rainbow over rolling hills, vermilion raincoat, cobalt camera, turquoise rain beads, saffron sunbreak, emerald meadow and ruby wildflowers, nature portrait'),
]


def token():
 d=json.loads(AUTH_PATH.read_text()); v=d.get('providers',{}).get('minimax-oauth')
 if isinstance(v,dict): v=v.get('access_token')
 if not v:
  v=d.get('credential_pool',{}).get('minimax-oauth',[{}])[0]; v=v.get('access_token') if isinstance(v,dict) else v
 if not v: raise RuntimeError('token missing')
 return v

def gray(blob):
 im=Image.open(io.BytesIO(blob)).convert('RGB'); im.thumbnail((512,512)); px=list(im.getdata())
 return 100*sum(max(r,g,b)-min(r,g,b)<=15 for r,g,b in px)/len(px)

def generate(prompt, label, tok):
 body=json.dumps({'model':'image-01','prompt':prompt,'size':'1024x1024','n':1}).encode()
 last=None
 for attempt in range(1,4):
  try:
   req=urllib.request.Request(API_URL,data=body,method='POST',headers={'Authorization':'Bearer '+tok,'Content-Type':'application/json','User-Agent':'alonda-tier16/1.0'})
   with urllib.request.urlopen(req,timeout=180,context=ssl.create_default_context()) as r: d=json.loads(r.read())
   urls=d.get('data',{}).get('image_urls',[])
   if not urls: raise RuntimeError('no image URL: '+json.dumps(d)[:300])
   with urllib.request.urlopen(urllib.request.Request(urls[0],headers={'User-Agent':'Mozilla/5.0'}),timeout=120) as r: b=r.read()
   Image.open(io.BytesIO(b)).verify(); print(label+' generated',flush=True); return b
  except Exception as e:
   last=e; print(label+' attempt '+str(attempt)+' failed: '+str(e),flush=True)
   if attempt<3: time.sleep(4*attempt)
 raise RuntimeError(str(last))

OUT_DIR.mkdir(parents=True,exist_ok=True); tok=token(); summary=[]
for i,(key,scene) in enumerate(SHOTS,1):
 base='A colorful, vibrant, photorealistic editorial portrait of '+ALONDA+scene+'. Waist-up or three-quarter composition with Alonda clearly visible, accurate anatomy, cinematic lighting, rich saturated colors, sharp facial detail, premium magazine photography, no text, no watermark, not monochrome.'
 b=generate(base,key,tok); g=gray(b); regen=False
 if g>55:
  regen=True; b=generate(base+' REGENERATE IN BRILLIANT FULL COLOR: intensely saturated cobalt, turquoise, vermilion, magenta, saffron and emerald accents everywhere; bright colorful lighting; absolutely no grayscale, monochrome, muted, desaturated, black-and-white or sepia.',key+' vivid',tok); g=gray(b)
  if g>55: raise RuntimeError(key+' remains too gray: '+str(g))
 out=OUT_DIR/(key+'.jpg'); Image.open(io.BytesIO(b)).convert('RGB').save(out,'JPEG',quality=94,optimize=True)
 summary.append({'file':out.name,'gray_percent':round(g,2),'regenerated':regen,'bytes':out.stat().st_size}); print(f'[{i}/20] {key} gray={g:.2f}%',flush=True); time.sleep(2)
Path('/root/alonda/scripts/tier16_261_280_results.json').write_text(json.dumps(summary,indent=2)+'\n'); print('COMPLETE '+json.dumps(summary),flush=True)