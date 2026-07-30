#!/usr/bin/env python3
"""Upload the 20 new portraits (915-934) to tmpfiles.org."""
import json
import urllib.request
import urllib.error
import time
from pathlib import Path

OUT_DIR = Path('/root/alonda/assets/images')
results = {}

for n in range(915, 935):
    matches = list(OUT_DIR.glob(f"{n}_*.jpg"))
    if not matches:
        print(f"  {n}: MISSING", flush=True)
        continue
    fpath = matches[0]
    try:
        # tmpfiles API
        boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
        with open(fpath, 'rb') as f:
            file_data = f.read()
        body = (
            f"--{boundary}\r\n"
            f"Content-Disposition: form-data; name=\"file\"; filename=\"{fpath.name}\"\r\n"
            f"Content-Type: image/jpeg\r\n\r\n"
        ).encode() + file_data + f"\r\n--{boundary}--\r\n".encode()
        req = urllib.request.Request(
            'https://tmpfiles.org/api/v1/upload',
            data=body,
            method='POST',
            headers={'Content-Type': f'multipart/form-data; boundary={boundary}'},
        )
        with urllib.request.urlopen(req, timeout=60) as r:
            resp = json.loads(r.read())
            url = resp.get('data', {}).get('url', '')
            results[n] = {'file': fpath.name, 'url': url, 'size': fpath.stat().st_size}
            print(f"  {n}: {url}", flush=True)
    except Exception as e:
        print(f"  {n}: ERR {e}", flush=True)
        results[n] = {'file': fpath.name, 'error': str(e)}
    time.sleep(0.5)

with open('/root/alonda/scripts/batch_915_934_uploads.json', 'w') as f:
    json.dump(results, f, indent=2)
print(f"=== Uploaded {sum(1 for v in results.values() if v.get('url'))}/{len(results)} ===")
