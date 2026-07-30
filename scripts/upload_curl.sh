#!/bin/bash
set -u
cd /root/alonda/assets/images
RESULTS=()
COUNT=0
for f in 461_skin_texture_as_the_greek_goddess_athena_in.jpg \
         462_skin_texture_as_a_wingsuit_base_jumper_mid-f.jpg \
         463_skin_texture_as_a_cyberpunk_hacker_in_a_neon.jpg \
         464_skin_texture_as_a_peruvian_textile_artist_we.jpg \
         465_skin_texture_as_the_norse_goddess_freyja_rid.jpg \
         466_skin_texture_as_a_wingsuit_pilot_diving_thro.jpg \
         467_skin_texture_as_a_quantum_physicist_in_a_fut.jpg \
         468_as_a_himalayan_yak_herder_with_vivid_prayer_flags.jpg \
         469_as_a_bigfoot_researcher_with_glowing_mushrooms.jpg \
         470_skin_texture_as_a_venetian_glassblower_shapi.jpg \
         471_skin_texture_as_a_french_foreign_legion_sold.jpg \
         472_skin_texture_as_a_street_magician_performing.jpg \
         473_skin_texture_as_an_amazonian_shipibo_shaman.jpg \
         474_skin_texture_as_a_formula_1_test_driver_in_c.jpg \
         475_skin_texture_as_a_japanese_kintsugi_artist_c.jpg \
         476_skin_texture_as_a_mongolian_throat_singer_in.jpg \
         477_skin_texture_as_a_marine_biologist_diving_in.jpg \
         478_skin_texture_as_a_spanish_flamenco_dancer_in.jpg \
         479_skin_texture_as_a_victorian-era_ghost_hunter.jpg \
         480_skin_texture_as_a_thai_fruit_carver_sculptin.jpg; do
  if [ ! -f "$f" ]; then
    echo "MISSING: $f" >&2
    continue
  fi
  COUNT=$((COUNT+1))
  RESP=$(curl -s -F "file=@$f" https://tmpfiles.org/api/v1/upload 2>&1)
  if echo "$RESP" | grep -q '"status":"success"'; then
    URL=$(echo "$RESP" | python3 -c "import sys,json; d=json.load(sys.stdin); u=d['data']['url']; print(u.replace('tmpfiles.org/','tmpfiles.org/dl/'))")
    echo "[$COUNT/20] OK $f -> $URL"
    echo "{\"$f\": \"$URL\"}"
  else
    echo "[$COUNT/20] FAIL $f: $RESP"
  fi
  sleep 1
done > /tmp/uploads.txt 2>&1
cat /tmp/uploads.txt
