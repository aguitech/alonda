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
('201_roman_empress','ancient Roman empress in a marble forum at sunrise, vermilion stola with gold embroidery, turquoise mosaics, emerald laurel, saffron sunlight and cinematic historical atmosphere, regal portrait'),
('202_free_climber','free solo climber on a sunlit red-rock tower, electric cobalt harness, magenta chalk bag, turquoise sky, saffron cliffs and emerald valley far below, dynamic extreme-sport portrait'),
('203_ux_designer','UX designer presenting an immersive holographic interface in a colorful studio, coral blazer, cyan wireframes, violet furniture, emerald plants and warm amber lamps, modern professional portrait'),
('204_jedi','space-fantasy Jedi guardian in a crystalline canyon, indigo robe with ruby trim, luminous turquoise energy blade, emerald alien flora, saffron moons and dramatic cinematic light, heroic portrait'),
('205_ancient_greek','ancient Greek oracle beside a sea temple, flowing ivory and cobalt drapery, coral columns, emerald olive branches, magenta bougainvillea and golden Mediterranean light, mythic portrait'),
('206_aurora_borealis','astronomer beneath an intense aurora borealis in Iceland, emerald and turquoise sky ribbons, magenta parka, cobalt volcanic rocks, saffron lantern and star-filled night, celestial portrait'),
('207_book_illustrator','children book illustrator in a whimsical atelier, ruby cardigan, turquoise ink bottles, saffron paper, emerald painted birds and magenta flowers, charming creative portrait'),
('208_cabaret','cabaret singer on a jewel-toned stage, crimson feathered costume, cobalt velvet curtains, emerald spotlight, turquoise sequins, saffron footlights and glamorous theatrical mood, performance portrait'),
('209_kawaii','kawaii fashion enthusiast in a pastel Tokyo arcade, pink-and-turquoise outfit, lavender accessories, emerald plush toys, saffron neon signs and playful glossy color, editorial portrait'),
('210_santorini_summer','summer traveler on a Santorini terrace, flowing white dress with coral sash, cobalt domes, turquoise Aegean sea, saffron bougainvillea and magenta sunset, travel portrait'),
('211_petra','explorer at Petra treasury after rain, terracotta expedition coat, turquoise scarf, rose sandstone, emerald desert shrubs and golden shafts of light, epic travel portrait'),
('212_urban_firefighter','urban firefighter beside a bright rescue truck at dusk, vermilion protective gear, cobalt helmet, turquoise reflections, emerald city lights and saffron emergency glow, heroic portrait'),
('213_weaving_loom','master weaver at a traditional loom, magenta and saffron textiles, turquoise shuttle, emerald threads, ruby patterns and sunlit artisan workshop, detailed craft portrait'),
('214_quantum_scientist','quantum scientist in a luminous laboratory, cobalt coat, holographic turquoise probability fields, magenta instruments, emerald glass and warm gold highlights, futuristic science portrait'),
('215_salsa','salsa dancer in a Havana courtyard, swirling scarlet skirt, turquoise walls, emerald palms, saffron lanterns and magenta flowers, energetic dance portrait'),
('216_artisan_baker','artisan baker in a colorful old bakery, coral apron, golden loaves, turquoise tile oven, emerald herbs, ruby jam jars and saffron morning light, culinary portrait'),
('217_helicopter_pilot','helicopter pilot above a tropical coastline, cobalt flight suit with vermilion patches, turquoise rotor reflections, emerald islands and brilliant saffron sunrise, aviation portrait'),
('218_songkran','Songkran water festival celebrant in Chiang Mai, vivid turquoise water splash, magenta floral shirt, saffron temple details, emerald foliage and joyful sunlight, cultural portrait'),
('219_deep_sea_wreck','technical diver exploring a glowing shipwreck, cobalt suit with orange gear, turquoise beams, emerald marine life, magenta corals and golden bubbles, underwater adventure portrait'),
('220_steampunk_inventor','steampunk inventor in an ornate airship workshop, copper goggles, teal leather coat, ruby gauges, emerald brass machinery, saffron vapor and rich cinematic color, retrofuturist portrait'),
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
   req=urllib.request.Request(API_URL,data=body,method='POST',headers={'Authorization':'Bearer '+tok,'Content-Type':'application/json','User-Agent':'alonda-tier13/1.0'})
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
Path('/root/alonda/scripts/tier13_201_220_results.json').write_text(json.dumps(summary,indent=2)+'\n'); print('COMPLETE '+json.dumps(summary),flush=True)
