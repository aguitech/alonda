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
('181_medusa','mythic Medusa-inspired warrior in a cobalt temple garden, jeweled emerald armor, ruby serpentine crown, turquoise columns, saffron sunlight and vivid bougainvillea, cinematic fantasy portrait'),
('182_snowboarder','snowboarder carving through a luminous alpine bowl, electric magenta jacket, turquoise board, cobalt mountains, saffron goggles and powder sparkling in brilliant sun, dynamic sports portrait'),
('183_programmer','software programmer in a colorful midnight studio, coral jacket, emerald mechanical keyboard, cyan code reflections, violet neon plants and warm golden desk light, modern professional portrait'),
('184_bladerunner','rainy retrofuturist detective on a neon street, crimson trench coat, turquoise holographic signs, magenta umbrellas, cobalt reflections and amber headlights, cinematic science-fiction portrait'),
('185_belle_epoque','Belle Époque fashion muse outside a Parisian café, ivory-and-coral gown, emerald parasol, turquoise details, gold filigree and vibrant art nouveau flowers, elegant historical portrait'),
('186_cosmic_eclipse','cosmic eclipse observer on a desert plateau, iridescent cobalt cloak, magenta corona, saffron dunes, emerald constellation map and brilliant turquoise horizon, celestial portrait'),
('187_stained_glass','stained-glass artisan in a sunlit workshop, ruby and turquoise apron, colorful glass panels, saffron tools, emerald reflections and jewel-toned shards, detailed craft portrait'),
('188_contemporary_ballet','contemporary ballet dancer in a vivid geometric gallery, flowing vermilion costume, cobalt floor, emerald light ribbons, magenta shadows and graceful motion, fine-art portrait'),
('189_punk_skater','punk skater at a colorful urban plaza, electric lime and magenta jacket, turquoise skateboard, cobalt murals, ruby hair accents and sunny street energy, editorial portrait'),
('190_autumn_vermont','autumn traveler beside a Vermont lake, saffron knit coat, emerald scarf, ruby maple forest, turquoise water and rose sunset mist, richly colored seasonal portrait'),
('191_great_wall','explorer on the Great Wall in clear morning light, crimson expedition coat, turquoise scarf, emerald hills, saffron stone and magenta wildflowers, epic travel portrait'),
('192_alpine_rescuer','alpine rescue specialist on a vivid glacier ridge, orange-red technical gear, cobalt rope, turquoise ice, emerald valley and golden sunrise, heroic adventure portrait'),
('193_medieval_alchemist','medieval alchemist in a jewel-toned laboratory, violet robe, emerald glass vessels, ruby elixirs, saffron manuscripts and turquoise candle smoke, atmospheric historical portrait'),
('194_space_station','astronaut botanist tending a floating garden aboard a space station, white suit with coral and cobalt panels, emerald leaves, magenta planet glow and golden stars, optimistic science-fiction portrait'),
('195_violinist','violinist performing in a saturated jewel-toned concert hall, sapphire velvet gown, crimson violin, turquoise stage light, saffron orchestra glow and expressive motion, music portrait'),
('196_tango','tango dancer in a Buenos Aires courtyard at blue hour, swirling scarlet dress, emerald partner accents, cobalt balconies, magenta bougainvillea and golden lanterns, passionate dance portrait'),
('197_orchid_grower','orchid cultivator in a luminous tropical greenhouse, turquoise overalls, magenta orchids, emerald leaves, saffron watering can and rainbow glass reflections, botanical portrait'),
('198_vintage_motorcycle','vintage motorcycle rider on a coastal highway, coral leather jacket, cobalt motorcycle, turquoise ocean, saffron helmet and ruby sunset, colorful road portrait'),
('199_holi_festival','Holi festival celebrant in Jaipur, flowing white outfit covered in vivid magenta, turquoise, saffron and emerald powder, colorful architecture and joyful movement, vibrant cultural portrait'),
('200_underwater_cave','cave diver exploring a glowing underwater cavern, cobalt wetsuit with coral gear, turquoise rays, emerald coral, magenta sea fans and golden bubbles, adventurous marine portrait'),
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
   req=urllib.request.Request(API_URL,data=body,method='POST',headers={'Authorization':'Bearer '+tok,'Content-Type':'application/json','User-Agent':'alonda-tier12/1.0'})
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
Path('/root/alonda/scripts/tier12_181_200_results.json').write_text(json.dumps(summary,indent=2)+'\n'); print('COMPLETE '+json.dumps(summary),flush=True)
