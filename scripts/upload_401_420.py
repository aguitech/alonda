#!/usr/bin/env python3
"""Upload batch 401-420 — uguu.se primary, litterbox (catbox 1h) fallback."""
import json, sys, time
from pathlib import Path
import urllib.request, ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

OUT = Path("/root/alonda/assets/images")

def upload_uguu(path):
    boundary = "----h" + str(int(time.time()*1000))
    with open(path, "rb") as f:
        data = f.read()
    body = (
        f"--{boundary}\r\n".encode() +
        b'Content-Disposition: form-data; name="files[]"; filename="' + path.name.encode() + b'"\r\n' +
        b"Content-Type: image/jpeg\r\n\r\n" +
        data +
        f"\r\n--{boundary}--\r\n".encode()
    )
    req = urllib.request.Request(
        "https://uguu.se/upload.php",
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=60) as r:
            resp = json.loads(r.read().decode())
        if resp.get("success"):
            return resp["files"][0]["url"]
        return None
    except Exception as e:
        print(f"  uguu err: {e}", flush=True)
        return None

def upload_litterbox(path):
    boundary = "----h" + str(int(time.time()*1000))
    with open(path, "rb") as f:
        data = f.read()
    body = (
        f"--{boundary}\r\n".encode() +
        b'Content-Disposition: form-data; name="reqtype"\r\n\r\nfileupload\r\n' +
        f"--{boundary}\r\n".encode() +
        b'Content-Disposition: form-data; name="time"\r\n\r\n1h\r\n' +
        f"--{boundary}\r\n".encode() +
        b'Content-Disposition: form-data; name="fileToUpload"; filename="' + path.name.encode() + b'"\r\n' +
        b"Content-Type: image/jpeg\r\n\r\n" +
        data +
        f"\r\n--{boundary}--\r\n".encode()
    )
    req = urllib.request.Request(
        "https://litterbox.catbox.moe/resources/internals/api.php",
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=60) as r:
            url = r.read().decode().strip()
            if url.startswith("http"):
                return url
        return None
    except Exception as e:
        print(f"  litterbox err: {e}", flush=True)
        return None

files = sorted([p for p in OUT.glob("4*.jpg") if 401 <= int(p.stem.split("_")[0]) <= 420])
print(f"Found {len(files)} files to upload", flush=True)

results = {}
for p in files:
    url = upload_uguu(p)
    if not url:
        url = upload_litterbox(p)
    results[p.name] = url
    print(f"  {p.name} -> {url}", flush=True)
    time.sleep(0.4)

out = Path("/root/alonda/scripts/batch_401_420_uploads.json")
out.write_text(json.dumps(results, indent=2))
ok = sum(1 for v in results.values() if v)
print(f"[done] ok={ok}/{len(results)}")
