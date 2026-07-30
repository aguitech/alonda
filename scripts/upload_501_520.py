#!/usr/bin/env python3
"""Upload batch 501-520 to tmpfiles.org (fallback file.io)."""
import json, urllib.request, urllib.error, time, ssl, sys
from pathlib import Path

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

OUT_DIR = Path("/root/alonda/assets/images")
files = sorted([f for f in OUT_DIR.glob("5[01][0-9]_*.jpg") if not f.name.startswith("500_")])
print(f"Found {len(files)} files to upload", flush=True)

def upload_tmpfiles(path, retries=2):
    boundary = "----hermesboundary" + str(int(time.time()))
    with open(path, "rb") as f:
        data = f.read()
    fname = path.name
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="{fname}"\r\n'
        f"Content-Type: image/jpeg\r\n\r\n"
    ).encode() + data + f"\r\n--{boundary}--\r\n".encode()
    req = urllib.request.Request("https://tmpfiles.org/api/v1/upload", data=body, headers={"Content-Type": f"multipart/form-data; boundary={boundary}", "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"})
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, context=ctx, timeout=120) as r:
                d = json.loads(r.read().decode())
            url = d.get("data", {}).get("url")
            if url:
                return url + ("?download=1" if "?" not in url else ""), None
            return None, f"no url in response: {d}"
        except Exception as e:
            if attempt < retries - 1: time.sleep(3); continue
            return None, repr(e)
    return None, "exhausted retries"

def upload_fileio(path, retries=2):
    with open(path, "rb") as f:
        data = f.read()
    req = urllib.request.Request("https://file.io", data=data, headers={"Content-Type": "image/jpeg", "Content-Disposition": f'attachment; filename="{path.name}"', "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"})
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, context=ctx, timeout=120) as r:
                d = json.loads(r.read().decode())
            if d.get("success") and d.get("link"):
                return d["link"], None
            return None, f"file.io fail: {d}"
        except Exception as e:
            if attempt < retries - 1: time.sleep(3); continue
            return None, repr(e)
    return None, "exhausted"

results = []
for i, f in enumerate(files, 1):
    print(f"[{i}/{len(files)}] {f.name}", flush=True)
    url, err = upload_tmpfiles(f)
    if not url:
        print(f"  tmpfiles failed ({err}), trying file.io...", flush=True)
        url, err2 = upload_fileio(f)
    if url:
        print(f"  -> {url}", flush=True)
        results.append({"file": f.name, "url": url})
    else:
        print(f"  [fail] both backends failed", flush=True)
        results.append({"file": f.name, "error": str(err)})
    time.sleep(1)

Path("/root/alonda/scripts/batch_501_520_uploads.json").write_text(json.dumps(results, indent=2, ensure_ascii=False))
print(f"\n[DONE] uploaded {sum(1 for r in results if 'url' in r)}/{len(results)}", flush=True)
