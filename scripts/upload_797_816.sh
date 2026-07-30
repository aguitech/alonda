#!/usr/bin/env bash
set -u
mkdir -p /root/alonda/scripts/uploads_797_816
RESULTS=/root/alonda/scripts/uploads_797_816/results.txt
: > "$RESULTS"
HOST="tmpfiles.org"

for n in 797 798 799 800 801 802 803 804 805 806 807 808 809 810 811 812 813 814 815 816; do
  img=$(ls /root/alonda/assets/images/${n}_*.jpg 2>/dev/null | head -1)
  [ -z "$img" ] && continue
  resp=$(curl -s -F "file=@${img}" "https://${HOST}/api/v1/upload")
  viewer=$(printf '%s' "$resp" | grep -oE "https://${HOST}/[A-Za-z0-9]+" | head -1)
  if [ -z "$viewer" ]; then
    printf '%s|%s|FAIL|resp=%s\n' "$n" "$(basename "$img")" "$resp" >> "$RESULTS"
    echo "[fail] $n (no viewer)"
    sleep 1
    continue
  fi
  real=$(curl -sL "$viewer" | grep -oE "https://${HOST}/dl/[A-Za-z0-9./_-]+\\.jpg" | head -1)
  if [ -n "$real" ]; then
    printf '%s|%s|%s\n' "$n" "$(basename "$img")" "$real" >> "$RESULTS"
    echo "[ok] $n -> $real"
  else
    printf '%s|%s|PARTIAL|viewer=%s\n' "$n" "$(basename "$img")" "$viewer" >> "$RESULTS"
    echo "[partial] $n -> $viewer"
  fi
  sleep 1
done
echo "=== DONE ==="