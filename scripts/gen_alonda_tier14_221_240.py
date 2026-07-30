#!/usr/bin/env python3
import io, json, ssl, time, urllib.request
from pathlib import Path
from PIL import Image

AUTH_PATH = Path('/') / 'root' / '.hermes' / 'auth.json'
OUT_DIR = Path('/root/alonda/assets/images')
API_URL = 'https://api.' + 'minimax' + '.io/v1/image_generation'
ALONDA = ('Alonda, a beautiful 26-year-old woman, platinum blonde long hair, striking emerald green eyes, '
          'slim athletic figure, delicate feminine facial features, natural realistic skin texture, ')
SHOTS = [
('221_medusa','Medusa the Gorgon reimagined as a heroine in a marble temple, emerald snakes woven into platinum hair, vermilion robe, cobalt shadow, saffron torchlight and turquoise serpents, mythic portrait'),
('222_apollo','Apollo the sun deity in golden chariot light, saffron and vermilion drapery, turquoise laurel, emerald lyre, cobalt sky and radiant solar portrait, classic Greek mythology'),
('223_athena','Athena the strategist in a starlit library, cobalt armor with turquoise owl emblem, saffron shield, emerald owls, magenta scrolls and silver starlight, goddess portrait'),
('224_aphrodite','Aphrodite rising from a turquoise cove, pearl and coral drapery, saffron roses, emerald sea foam, magenta sunset and soft golden goddess light, romantic mythology portrait'),
('225_paraglider','paraglider soaring above the Dolomites at dawn, vermilion canopy, cobalt harness, turquoise peaks, emerald valley, saffron sunbeams and crisp adventure portrait'),
('226_motocross','motocross rider launching off a saffron desert jump, vermilion KTM bike, cobalt helmet, turquoise dust, emerald scrubland and ruby exhaust flare, dynamic extreme-sport portrait'),
('227_skateboarder','skateboarder mid-kickflip in a vivid bowl, cobalt wheels, magenta grip tape, turquoise ramps, saffron graffiti, emerald palms and sunlit extreme-sport portrait'),
('228_bmx','BMX rider performing a superman trick in a colorful urban park, ruby frame, cobalt ramps, turquoise ground paint, saffron sunlight and magenta crowd, action portrait'),
('229_kite_surfer','kite surfer carving on a turquoise lagoon, vermilion kite, cobalt board, emerald splashes, saffron sunset and magenta spray, water-sport portrait'),
('230_software_architect','software architect in a colorful modern office, coral shirt, cobalt multi-monitor rig, turquoise IDE, emerald plants, magenta whiteboard and warm amber ambient, modern portrait'),
('231_chef_pastry','pastry chef in a brasserie kitchen, vermilion apron, cobalt copper pots, turquoise marble counter, saffron croissants, emerald herbs and ruby berries, culinary portrait'),
('232_sommelier','sommelier in a candlelit wine cellar, magenta velvet jacket, turquoise cellar arch, emerald bottles, saffron candlelight and ruby wine in glass, refined portrait'),
('233_matrix_bullettime','matrix bullet-time hero suspended mid-air in a corridor, emerald digital rain, vermilion coat, cobalt cyberpunk arches, saffron neon and magenta reflections, cinematic sci-fi portrait'),
('234_blade_runner','blade runner detective in a rain-soaked neon city, vermilion trench coat, cobalt rain, turquoise holograms, emerald kanji and saffron street glow, cinematic noir portrait'),
('235_star_trek','starfleet captain on the bridge of a starship, vermilion command tunic, cobalt console lights, turquoise viewscreen nebula, emerald alien sky and gold uniform piping, sci-fi portrait'),
('236_mesopotamian','ancient Mesopotamian priestess in a ziggurat at sunrise, vermilion fringed robe, cobalt lapis jewelry, turquoise glazed bricks, saffron incense and emerald palms, ancient portrait'),
('237_byzantine','Byzantine empress in a gold-mosaic cathedral, vermilion imperial silk, cobalt and emerald mosaics, turquoise candles, saffron halos and regal historic portrait'),
('238_water_elemental','water elemental sorceress summoning a tidal wave on a cliff, turquoise liquid magic, emerald sea spray, vermilion cloak, cobalt storm clouds and saffron lightning, fantasy portrait'),
('239_earth_elemental','earth elemental druid raising a crystalline forest, emerald vines, turquoise moss, vermilion mushrooms, cobalt stones and saffron pollen shafts, fantasy nature portrait'),
('240_cosmos','cosmos explorer gazing at a spiral nebula on an asteroid, vermilion suit, cobalt helmet visor, turquoise nebula clouds, emerald aurora, saffron stars and magenta planets, cosmic portrait'),
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
   req=urllib.request.Request(API_URL,data=body,method='POST',headers={'Authorization':'Bearer '+tok,'Content-Type':'application/json','User-Agent':'alonda-tier14/1.0'})
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
Path('/root/alonda/scripts/tier14_221_240_results.json').write_text(json.dumps(summary,indent=2)+'\n'); print('COMPLETE '+json.dumps(summary),flush=True)
