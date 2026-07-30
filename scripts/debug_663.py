#!/usr/bin/env python3
"""Debug - try a single request and see the raw response."""
import json, ssl, urllib.request, urllib.error, sys
from pathlib import Path

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

auth = json.loads(Path("/root/.hermes/auth.json").read_text())
_prov = auth.get("providers") or {}
_pool = auth.get("credential_pool") or {}
KEY = "minimax" + "-oauth"
TOKEN=*** or {}).get("access_token") or (_pool.get(KEY) or [{}])[0].get("access_token")
if not TOKEN:
    print("FATAL: no token", file=sys.stderr); sys.exit(2)

ALONDA = (
    "Alonda, a beautiful 26-year-old woman, platinum blonde long hair, "
    "striking emerald green eyes, slim athletic figure, "
    "delicate feminine facial features, natural realistic skin texture, "
)
PROMPT = ALONDA + "as Isis Egyptian goddess portrait, vivid gilded falcon headdress, white linen dress, lapis lazuli jewelry, Nile sunset, vivid mythology portrait, ultra detailed"

url = "https://api." + "minimax" + ".io/v1/image_generation"
body = json.dumps({"model": "image-01", "prompt": PROMPT, "size": "1024x1024", "n": 1}).encode()
req = urllib.request.Request(url, data=body, headers={
    "Authorization": "Bearer " + TOKEN,
    "Content-Type": "application/json",
})

try:
    with urllib.request.urlopen(req, context=ctx, timeout=180) as r:
        raw = r.read().decode()
    print("STATUS:", r.status)
    print("RAW RESPONSE (first 2000 chars):")
    print(raw[:2000])
    d = json.loads(raw)
    print("PARSED keys:", list(d.keys()))
    if 'data' in d:
        print("data keys:", list(d['data'].keys()) if d['data'] else "None")
        print("data type:", type(d['data']))
        print("data value:", str(d['data'])[:500])
except urllib.error.HTTPError as e:
    print(f"HTTP {e.code}:")
    print(e.read().decode(errors='replace')[:1000])
except Exception as e:
    print("EXCEPTION:", repr(e))
