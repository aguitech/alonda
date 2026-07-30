#!/usr/bin/env python3
"""Upload 540 directly."""
import json, urllib.request, ssl, time, sys
from pathlib import Path

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

p = Path("/root/alonda/assets/images/540_as_a_moroccan_henna_artist_in_a_marrakech_riad_courtyard_app.jpg")
boundary = "----hermesboundary" + str(int(time.time()))
data = p.read_bytes()
body = (
    f"--{boundary}\r\n"
    f'Content-Disposition: form-data; name="file"; filename="{p.name}"\r\n'
    f"Content-Type: image/jpeg\r\n\r\n"
).encode() + data + f"\r\n--{boundary}--\r\n".encode()
req = urllib.request.Request("https://tmpfiles.org/api/v1/upload", data=body, headers={
    "Content-Type": f"multipart/form-data; boundary={boundary}",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124.0 Safari/537.36"
})
with urllib.request.urlopen(req, context=ctx, timeout=120) as r:
    d = json.loads(r.read().decode())
url = d.get("data", {}).get("url", "FAIL")
print(url + "?download=1" if "?" not in url else url)

# Append to existing uploads file
uploads_file = Path("/root/alonda/scripts/batch_521_540_uploads.json")
results = json.loads(uploads_file.read_text())
results.append({"file": p.name, "url": url + ("?download=1" if "?" not in url else "")})
uploads_file.write_text(json.dumps(results, indent=2, ensure_ascii=False))
print(f"appended to {uploads_file}")
