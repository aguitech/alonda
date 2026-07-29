#!/usr/bin/env python3
"""Tier 15 (241-260): fresh themes — Sumerian, Persian, Incan, Korean, Tibetan,
Polynesian, Maasai, Shaolin, Bharatanatyam, Capoeira, Mariachi, Bossa nova,
Taiko, Origami, Storm chaser, Cave diver, Coral reef guardian, Aerial silk,
Strongwoman, Marionette."""
import io, json, ssl, time, urllib.request
from pathlib import Path
from PIL import Image

AUTH_PATH = Path('/') / 'root' / '.hermes' / 'auth.json'
OUT_DIR = Path('/root/alonda/assets/images')
API_URL = 'https://api.' + 'minimax' + '.io/v1/image_generation'
ALONDA = ('Alonda, a beautiful 26-year-old woman, platinum blonde long hair, striking emerald green eyes, '
          'slim athletic figure, delicate feminine facial features, natural realistic skin texture, ')
SHOTS = [
('241_sumerian','Sumerian high priestess in a ziggurat at twilight, vermilion fringed kaunakes robe, cobalt lapis headdress, turquoise glazed brick columns, saffron incense smoke, emerald date palms and ruby stars, ancient Mesopotamia portrait'),
('242_persian_poet','Persian poet in a rose garden inspired by Rumi, vermilion silken robes, cobalt miniature-painted tiles, turquoise fountain, saffron roses, emerald vines and ruby wine goblet, poetic mystic portrait'),
('243_incan','Incan sun priestess atop a Machu Picchu terrace at solstice, vermilion tunic with gold sun brooch, cobalt llamas, turquoise terraces, saffron alpenglow, emerald mountains and ruby ceremonial bowls, Andean portrait'),
('244_korean_hanbok','Korean court lady in a hanbok at Gyeongbokgung palace, vermilion jeogori, cobalt chima, turquoise lacquered hanok roof, saffron dancheong patterns, emerald pines and ruby royal seal, Joseon portrait'),
('245_tibetan_nun','Tibetan Buddhist nun spinning a prayer wheel in a high monastery, vermilion monastic robes, cobalt mountain backdrop, turquoise prayer flags, saffron butter lamps, emerald prayer beads and ruby silk brocade, Himalayan portrait'),
('246_polynesian_nav','Polynesian navigator reading the stars from a voyaging canoe, vermilion tapa cloth wrap, cobalt ocean, turquoise wave spray, saffron sun compass, emerald island silhouette and ruby shell necklaces, Pacific voyaging portrait'),
('247_maasai_queen','Maasai warrior queen on the savanna, vermilion shuka cloak, cobalt bead collar, turquoise beaded jewelry, saffron acacia sunset, emerald grasslands and ruby shield, East African portrait'),
('248_shaolin','Shaolin kung fu master mid-form in a misty mountain temple, vermilion sash, cobalt temple tiles, turquoise prayer flags, saffron incense, emerald bamboo grove and ruby monk robes, martial arts portrait'),
('249_bharatanatyam','Indian classical Bharatanatyam dancer mid-mudra in a temple courtyard, vermilion silk sari, cobalt temple gopuram, turquoise anklet bells, saffron marigolds, emerald peacocks and ruby kumkum bindi, dance portrait'),
('250_capoeira','capoeira mestre mid-ginga kick in a Salvador roda, vermilion abada pants, cobalt berimbau, turquoise drums, saffron Bahia sun, emerald palm trees and ruby Cordao da Bica, Afro-Brazilian martial dance portrait'),
('251_mariachi','mariachi singer in a plaza at dusk, vermilion charro suit with silver botonadura, cobalt embroidered trim, turquoise guitar, saffron papel picado banners, emerald agave and ruby trumpet, Mexican folk music portrait'),
('252_bossa_nova','bossa nova singer on a Copacabana balcony at twilight, vermilion silk dress, cobalt skyline, turquoise samba beats, saffron moon, emerald sea breeze and ruby vinyl record, Brazilian jazz portrait'),
('253_taiko','taiko drummer mid-strike on a great drum in a matsuri, vermilion happi coat, cobalt hachimaki headband, turquoise stage lanterns, saffron fireworks, emerald temple gate and ruby drumsticks, Japanese festival portrait'),
('254_origami','origami master in a paper crane studio, vermilion kimono, cobalt paper folds, turquoise cranes and dragons suspended, saffron paper light, emerald paper maple leaves and ruby paper roses, Japanese craft portrait'),
('255_storm_chase','storm chaser leaning into hurricane winds on a Kansas plain, vermilion weather station jacket, cobalt supercell clouds, turquoise lightning fork, saffron funnel, emerald wheat field and ruby anemometer, science portrait'),
('256_cave_diver','cave diver in a cenote at sunrise, vermilion drysuit, cobalt limestone walls, turquoise water surface, saffron sunbeam shaft, emerald stalactites and ruby dive lights, exploration portrait'),
('257_coral_guard','coral reef guardian transplanting a coral fragment, vermilion rashguard, cobalt reef wall, turquoise tropical fish, saffron sunlight, emerald sea fans and ruby sea star, marine biology portrait'),
('258_aerial_silk','aerial silk performer mid-drop in a circus big top, vermilion silk fabric, cobalt rigging, turquoise sequins, saffron spotlight, emerald velvet curtain and ruby bunting, circus arts portrait'),
('259_strongwoman','strongwoman lifting a barbell on a carnival stage, vermilion leotard, cobalt crowd banner, turquoise star backdrop, saffron spotlight, emerald vintage weights and ruby carnival lights, vaudeville strongwoman portrait'),
('260_marionette','marionette puppeteer mid-pose in a baroque theater, vermilion velvet waistcoat, cobalt stage flats, turquoise marionette strings, saffron footlights, emerald curtain and ruby puppet crown, theater arts portrait'),
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
   req=urllib.request.Request(API_URL,data=body,method='POST',headers={'Authorization':'Bearer '+tok,'Content-Type':'application/json','User-Agent':'alonda-tier15/1.0'})
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
Path('/root/alonda/scripts/tier15_241_260_results.json').write_text(json.dumps(summary,indent=2)+'\n'); print('COMPLETE '+json.dumps(summary),flush=True)