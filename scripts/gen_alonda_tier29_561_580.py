#!/usr/bin/env python3
import io, json, ssl, time, urllib.request
from pathlib import Path
from PIL import Image

AUTH_PATH=Path('/') / 'root' / '.hermes' / 'auth.json'
OUT_DIR = Path('/root/alonda/assets/images')
API_URL = 'https://api.'+'minimax'+'.io/v1/image_generation'
ALONDA = ('Alonda, a beautiful 26-year-old woman, platinum blonde long hair, striking emerald green eyes, '
          'slim athletic figure, delicate feminine facial features, natural realistic skin texture, ')
SHOTS = [
('561_artemis','mythic Artemis-inspired huntress in a moonlit pine forest, silver tunic with coral trim, saffron quiver, turquoise crescent diadem, cobalt bow, ruby foxes and emerald ferns, cinematic fantasy portrait'),
('562_celtic_druid','Celtic druidess performing a sunrise ritual at Stonehenge, ivory robe with vermilion Celtic knots, emerald mistletoe staff, turquoise torc, saffron dawn light and magenta heather, atmospheric portrait'),
('563_anubis_priestess','mythic Egyptian priestess of Anubis in a vivid temple hall, cobalt pleated gown with gold lapis, turquoise ankh, ruby lotus offerings, saffron torchlight and emerald columns, cinematic fantasy portrait'),
('564_blues_harp','blues harmonica player in a saturated New Orleans juke joint, crimson satin dress, turquoise harmonica rack, cobalt piano, saffron stage bulbs and magenta velvet curtains, evocative music portrait'),
('565_indie_folk','indie folk singer-songwriter on a foggy Pacific coast cliff, mustard knit sweater, vermilion guitar, turquoise sea foam, emerald pines and rose sunrise, atmospheric music portrait'),
('566_kpop_idol','K-pop idol on a saturated candy-bright stage, holographic mint crop top, magenta pleated skirt, turquoise LED wall, saffron spotlights and ruby confetti, glamorous music portrait'),
('567_1980s_aerobic','1980s aerobic instructor in a Miami pastel studio, electric pink leotard, turquoise leg warmers, cobalt headband, saffron Reeboks and magenta streamers, vibrant retro portrait'),
('568_2000s_y2k','2000s Y2K fashion muse in a chrome metallic cafe, frosty blue mini dress, magenta rhinestone sunglasses, turquoise iMac, saffron bubble chair and ruby lip gloss, nostalgic pop-portrait'),
('569_dieselpunk_mechanic','dieselpunk 1940s mechanic in a riveted aircraft hangar, olive flight suit with crimson patches, cobalt wrench, turquoise rivets, saffron sodium lamps and emerald propeller, retrofuturist portrait'),
('570_atompunk_scientist','atompunk 1950s nuclear physicist in a starburst-era laboratory, teal lab coat, magenta clipboard, turquoise Geiger counters, ruby atomic model and saffron chrome chairs, retrofuturist portrait'),
('571_carnival_rio','carnaval Rio samba dancer at the Sambadrome, towering cobalt and fuchsia feathered headdress, emerald sequined bikini, turquoise fringe, saffron stage pyrotechnics, vibrant cultural portrait'),
('572_inti_raymi','Inti Raymi Inca festival celebrant in Cusco at golden hour, crimson and gold ceremonial poncho, turquoise chakana necklace, emerald terraces, saffron sun disc and magenta petunias, Andean festival portrait'),
('573_songkran','Songkran water festival reveler in Chiang Mai, soaked magenta silk blouse, turquoise water-splash halo, cobalt temple backdrop, saffron marigold garlands and emerald water guns, joyful festival portrait'),
('574_mardi_gras','Mardi Gras krewe queen on a New Orleans balcony at twilight, royal purple cape with gold fleur-de-lis, emerald mask, turquoise beads, magenta balloons and saffron gas-lamp glow, festive portrait'),
('575_huli_wigman','Huli wigman initiate from Papua New Guinea highlands, ceremonial ochre and turmeric body paint, cobalt feathered headdress, turquoise billi leaves, saffron rainforest light and ruby parrot feathers, ethnographic portrait'),
('576_moroccan_zellige','Moroccan zellige tile artisan in a Fez workshop, sapphire and saffron apron, emerald chisel, turquoise fountain courtyard, cobalt mosaic wall and rose-pink bougainvillea, craft portrait'),
('577_falun_dafa','discreet modern portrait of a serene Falun Gong practitioner meditating in a misty bamboo grove, soft white silk blouse with pale aqua sash, vermilion maple leaf in hand, gentle dawn light, peaceful non-political portrait'),
('578_butterfly_conservatory','butterfly conservatory curator in a tropical vivarium, ivory linen jumpsuit, dozens of morpho turquoise and saffron monarchs perched on her hands and shoulders, emerald philodendrons and ruby heliconia, naturalist portrait'),
('579_aurora_ice_sculptor','aurora-themed ice sculptor working on a luminous frozen block in Tromso, cobalt parka with magenta fur trim, turquoise chisel, emerald ice shavings, saffron work lights and violet aurora overhead, Nordic craft portrait'),
('580_bioluminescent_cave','explorer inside a glowworm-lit cave in Waitomo, reflective hard hat with magenta lamp, turquoise cave pool, emerald stalactites dripping with golden bioluminescent glow, adventure portrait'),
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
   req=urllib.request.Request(API_URL,data=body,method='POST',headers={'Authorization':'Bearer '+tok,'Content-Type':'application/json','User-Agent':'alonda-tier29/1.0'})
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
Path('/root/alonda/scripts/tier29_561_580_results.json').write_text(json.dumps(summary,indent=2)+'\n'); print('COMPLETE '+json.dumps(summary),flush=True)
