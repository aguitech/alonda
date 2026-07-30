#!/usr/bin/env python3
"""Tier 17 (281-300): unique blend of retro decades, dance styles,
off-beat professions, theatrical arts, and festival celebrations."""
import io, json, ssl, time, urllib.request
from pathlib import Path
from PIL import Image

AUTH_PATH = Path('/') / 'root' / '.hermes' / 'auth.json'
OUT_DIR = Path('/root/alonda/assets/images')
API_URL = 'https://api.' + 'minimax' + '.io/v1/image_generation'
ALONDA = ('Alonda, a beautiful 26-year-old woman, platinum blonde long hair, striking emerald green eyes, '
          'slim athletic figure, delicate feminine facial features, natural realistic skin texture, ')
SHOTS = [
('281_flapper_1920s','1920s flapper dancing in a glittering jazz speakeasy, vermilion fringed dress, cobalt headband feather, turquoise champagne coupe, saffron Art Deco chandelier, emerald peacock fan and ruby bead curtains, vintage portrait'),
('282_mod_1960s','1960s mod fashion model in a Carnaby Street photo studio, vermilion miniskirt, cobalt graphic print, turquoise go-go boots, saffron pop art backdrop, emerald vinyl chair and ruby lampshade, swinging sixties portrait'),
('283_breakdance','breakdancer mid-freeze on a colorful graffiti rooftop, vermilion tracksuit, cobalt spray cans, turquoise boombox, saffron sunset, emerald jersey and ruby wristbands, urban street portrait'),
('284_contortionist','circus contortionist bending gracefully in a kaleidoscopic big-top, vermilion bodysuit, cobalt sequins, turquoise spotlight, saffron tent stripes, emerald ribbons and ruby stilts, performance portrait'),
('285_treasure_hunter','antique treasure hunter in a hidden jungle temple vault, vermilion explorer jacket, cobalt map, turquoise torch beam, saffron golden idol, emerald vines and ruby gemstone, adventure portrait'),
('286_inti_raymi','Inti Raymi festival dancer celebrating the Inca sun festival in Cusco, vermilion embroidered poncho, cobalt skirt, turquoise ceremonial bowl, saffron Andean sun, emerald terraces and ruby tassels, cultural portrait'),
('287_fortune_teller','Romani fortune teller reading glowing tarot in a velvet-draped caravan, vermilion shawl, cobalt silk curtains, turquoise crystal ball, saffron lantern, emerald cards and ruby candle, mystical portrait'),
('288_chef_pastry','pastry chef plating towering desserts in a brasserie kitchen, vermilion toque, cobalt copper pots, turquoise macarons, saffron croissants, emerald basil and ruby berry coulis, fine pastry portrait'),
('289_zen_garden','Zen garden master raking sand patterns beside a Kyoto temple pond, vermilion kimono, cobalt stone lantern, turquoise koi pond, saffron maple leaves, emerald moss and ruby bridge, contemplative portrait'),
('290_singer_opera','opera singer mid-aria in a gilded European theater box, vermilion velvet gown, cobalt operatic curtain, turquoise jewelry, saffron spotlight, emerald parquet floor and ruby rose bouquet, classical music portrait'),
('291_songkran','Songkran water festival fighter in a Bangkok street celebration, vermilion floral shirt, cobalt water gun, turquoise splash, saffron marigolds, emerald temple spires and ruby lanterns, joyful festival portrait'),
('292_winter_lapland','husky sledding guide racing across the Lapland tundra at dawn, vermilion parka, cobalt sled, turquoise northern lights, saffron sunrise, emerald pine forest and ruby mittens, arctic portrait'),
('293_steampunk_inventor','steampunk inventor tinkering with a brass automaton in a Victorian workshop, vermilion corset waistcoat, cobalt gears, turquoise goggles, saffron gaslight, emerald velvet and ruby copper tubing, retro sci-fi portrait'),
('294_drone_pilot','drone racer calibrating a high-speed quadcopter on a neon rooftop arena, vermilion racing jersey, cobalt drone, turquoise LED rings, saffron sunset, emerald antennas and ruby propeller, modern tech portrait'),
('295_yoga_teacher','beach yoga teacher demonstrating a warrior pose on a Bali cliff at sunrise, vermilion yoga pants, cobalt mat, turquoise ocean, saffron sunrise, emerald palms and ruby temple offerings, wellness portrait'),
('296_mountain_climber','Alpine ice climber mid-ascent on a frozen waterfall, vermilion technical jacket, cobalt ice axes, turquoise crampons, saffron alpenglow, emerald glacier and ruby climbing rope, extreme portrait'),
('297_y2k_2000s','Y2K pop star performing in a chrome futuristic music video set, vermilion metallic crop top, cobalt platform boots, turquoise inflatable furniture, saffron lasers, emerald glitter and ruby flip phone, retrofuturism portrait'),
('298_cave_explorer','spelunking explorer rappelling into a luminous limestone cave, vermilion caving suit, cobalt helmet lamp, turquoise underground lake, saffron stalactite glow, emerald ferns and ruby crystals, exploration portrait'),
('299_samba_drummer','samba percussionist playing surdo drums in Rio carnival parade, vermilion costume, cobalt drum, turquoise feathers, saffron streetlights, emerald sequins and ruby drumsticks, cultural music portrait'),
('300_diary_writer','traveling diary writer sketching in a Parisian café at twilight, vermilion beret, cobalt notebook, turquoise espresso cup, saffron café lights, emerald typewriter and ruby fountain pen, literary portrait'),
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
   req=urllib.request.Request(API_URL,data=body,method='POST',headers={'Authorization':'Bearer '+tok,'Content-Type':'application/json','User-Agent':'alonda-tier17/1.0'})
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
Path('/root/alonda/scripts/tier17_281_300_results.json').write_text(json.dumps(summary,indent=2)+'\n'); print('COMPLETE '+json.dumps(summary),flush=True)