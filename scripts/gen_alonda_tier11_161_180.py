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
('161_roman_empress','ancient Roman empress in a marble forum at sunrise, ivory-and-crimson stola, laurel crown, turquoise mosaics and golden columns, vibrant historical editorial portrait'),
('162_egyptian_pharaoh','Egyptian pharaoh in a jewel-toned temple, lapis collar and gold headdress, turquoise hieroglyph walls, scarlet lotus flowers and warm sunbeams, colorful regal portrait'),
('163_free_climber','free solo climber on a sunlit red-rock cliff, electric teal and orange climbing gear, cobalt sky, magenta chalk dust and dramatic canyon depth, dynamic sports portrait'),
('164_parkour_rooftop','parkour athlete leaping between colorful rooftops in Barcelona, cobalt-and-coral streetwear, saffron sunset, turquoise tiles and vivid motion, cinematic action portrait'),
('165_surgeon','cardiothoracic surgeon in a brilliant modern operating theater, emerald scrubs, cobalt cap and coral accents, glowing monitors and clean colorful light, professional portrait'),
('166_ux_designer','UX designer presenting an inclusive mobile interface in a bright creative studio, magenta blazer, turquoise prototypes, saffron sticky notes and emerald plants, polished professional portrait'),
('167_analog_photographer','analog photographer in a sunlit darkroom, cobalt denim apron, ruby camera, amber prints and turquoise chemistry trays, richly textured creative portrait'),
('168_jewelry_goldsmith','jewelry goldsmith crafting a filigree necklace at a colorful workbench, emerald apron, sapphire gems, saffron tools and rose-gold glow, detailed artisan portrait'),
('169_circus_aerialist','circus aerialist suspended above a jewel-toned big-top stage, crimson costume with turquoise sequins, violet curtains, golden spotlights and confetti, elegant performance portrait'),
('170_magic_illusionist','glamorous stage illusionist beside a glowing cabinet, midnight-blue and vermilion costume, emerald cards, magenta smoke and saffron theater lights, theatrical portrait'),
('171_gothic_style','modern gothic fashion portrait in a rain-lit cathedral courtyard, black velvet with saturated ruby and violet details, turquoise stained glass and dramatic crimson roses, editorial portrait'),
('172_kawaii_style','kawaii street-style portrait in Harajuku, pastel turquoise and pink layered outfit, playful accessories, candy-colored shopfronts and bright cherry blossoms, joyful fashion portrait'),
('173_spring_kyoto','spring morning in Kyoto beside a canal, flowing coral kimono with turquoise embroidery, emerald bamboo, pink cherry blossoms and golden light, serene travel portrait'),
('174_machu_picchu','adventurer overlooking Machu Picchu at dawn, saffron expedition jacket, turquoise woven scarf, emerald terraces, magenta clouds and vivid mountain atmosphere, cinematic portrait'),
('175_petra_archaeologist','archaeologist at Petra in warm afternoon light, cobalt field jacket and coral scarf, rose sandstone, turquoise sky and saffron dust, colorful discovery portrait'),
('176_coast_guard','coast guard rescuer on a vivid ocean patrol boat, crimson waterproof jacket, cobalt sea, turquoise spray and golden rescue equipment, heroic maritime portrait'),
('177_medieval_herbalist','medieval herbalist in a colorful apothecary garden, emerald cloak, saffron satchel, violet flowers, turquoise glass bottles and warm candlelight, fantasy historical portrait'),
('178_quantum_astronaut','quantum astronaut inside a crystalline observatory above an alien ocean, white suit with magenta and cobalt panels, emerald aurora and saffron stars, vivid science-fiction portrait'),
('179_jazz_pianist','jazz pianist in a smoky jewel-toned club, sapphire suit with crimson accents, glowing piano, turquoise stage lights and golden reflections, glamorous music portrait'),
('180_salsa_dancer','salsa dancer in a Havana plaza at sunset, swirling emerald-and-magenta dress, cobalt shutters, saffron architecture and colorful motion, vibrant dance portrait'),
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
   req=urllib.request.Request(API_URL,data=body,method='POST',headers={'Authorization':'Bearer '+tok,'Content-Type':'application/json','User-Agent':'alonda-tier11/1.0'})
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
Path('/root/alonda/scripts/tier11_161_180_results.json').write_text(json.dumps(summary,indent=2)+'\n'); print('COMPLETE '+json.dumps(summary),flush=True)
