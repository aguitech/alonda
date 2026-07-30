#!/usr/bin/env python3
"""Upload batch 381-400 to file.io (fallback)."""
import json, urllib.request, urllib.error, ssl
from pathlib import Path

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

OUT = Path("/root/alonda/assets/images")
NUMS = [str(n) for n in range(381, 401)]

results = {}
for n in NUMS:
    matches = sorted(OUT.glob(f"{n}_*.jpg"))
    if not matches:
        continue
    img = matches[0]
    name = img.name
    try:
        with open(img, "rb") as f:
            data = f.read()
        # file.io uses multipart/form-data
        boundary = "----hbound" + str(hash(name) & 0xffff)
        body = (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="file"; filename="{name}"\r\n'
            f"Content-Type: image/jpeg\r\n\r\n"
        ).encode() + data + f"\r\n--{boundary}--\r\n".encode()
        req = urllib.request.Request(
            "https://file.io",
            data=body,
            headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
            method="POST",
        )
        with urllib.request.urlopen(req, context=ctx, timeout=60) as r:
            resp = json.loads(r.read().decode())
        url = resp.get("link", "FAIL")
        results[name] = url
        print(f"{name} => {url}", flush=True)
    except Exception as e:
        print(f"[err] {name}: {type(e).__name__}: {e}", flush=True)
        results[name] = f"ERR:{e}"

with open("/root/alonda/scripts/batch_381_400_fileio.json", "w") as f:
    json.dump(results, f, indent=2)
print(f"[done] {len([u for u in results.values() if not str(u).startswith('ERR')])} uploaded", flush=True)