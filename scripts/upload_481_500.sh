#!/bin/bash
# Upload batch 481-500 to tmpfiles.org via curl
set +e
cd /root/alonda/assets/images
OUT=/root/alonda/scripts/batch_481_500_uploads.json
echo "[" > $OUT
first=1
uploaded=0
failed=0
for f in 48[1-9]*.jpg 49[0-9]*.jpg 500_*.jpg; do
  [ -e "$f" ] || continue
  resp=$(curl -s -F "file=@$f" https://tmpfiles.org/api/v1/upload 2>&1)
  url=$(echo "$resp" | python3 -c "
import sys, json
try:
    d = json.loads(sys.stdin.read())
    print(d.get('data',{}).get('url',''))
except:
    print('')
" 2>/dev/null)
  if [ -n "$url" ]; then
    dl_url="${url}/download"
    echo "  ✓ $f -> $dl_url"
    if [ $first -eq 0 ]; then echo "," >> $OUT; fi
    first=0
    python3 -c "import json; print(json.dumps({'file':'$f','url':'$dl_url'}, ensure_ascii=False))" >> $OUT
    uploaded=$((uploaded+1))
  else
    echo "  ✗ $f (fail)"
    failed=$((failed+1))
  fi
  sleep 1
done
echo "" >> $OUT
echo "]" >> $OUT
echo ""
echo "Done: $uploaded uploaded, $failed failed"
