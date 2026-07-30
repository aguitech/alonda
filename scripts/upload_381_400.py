#!/usr/bin/env python3
"""Upload batch 381-400 to tmpfiles.org and print URLs."""
import json, urllib.request, urllib.error, ssl, sys
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
        print(f"[skip] {n}: no file", flush=True)
        continue
    img = matches[0]
    name = img.name
    try:
        with open(img, "rb") as f:
            data = f.read()
        boundary = "----hbound" + str(hash(name) & 0xffff)
        body = (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="file"; filename="{name}"\r\n'
            f"Content-Type: image/jpeg\r\n\r\n"
        ).encode() + data + f"\r\n--{boundary}--\r\n".encode()
        req = urllib.request.Request(
            "https://tmpfiles.org/api/v1/upload",
            data=body,
            headers={
                "Content-Type": f"multipart/form-data; boundary={boundary}",
                "User-Agent": "curl/8.5.0",
            },
            method="POST",
        )
        with urllib.request.urlopen(req, context=ctx, timeout=60) as r:
            resp = json.loads(r.read().decode())
        url = resp.get("data", {}).get("url", "FAIL")
        results[name] = url
        print(f"{name} => {url}", flush=True)
    except Exception as e:
        print(f"[err] {name}: {type(e).__name__}: {e}", flush=True)
        results[name] = f"ERR:{e}"

# Save for record
with open("/root/alonda/scripts/batch_381_400_tmpfiles.json", "w") as f:
    json.dump(results, f, indent=2)
print(f"[done] {len(results)} uploaded", flush=True)