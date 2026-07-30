#!/usr/bin/env python3
"""Upload batch 995-1014 to litterbox."""
import json
import os
import urllib.request
import urllib.error
import ssl
from pathlib import Path

OUT_DIR = Path('/root/alonda/assets/images')
LB = 'https://litterbox.catbox.moe/resources/internals/api.php'
ctx = ssl.create_default_context()

# Get the unique file for each number
uploads = []
START = 995
END = 1014
for n in range(START, END + 1):
    matches = list(OUT_DIR.glob(f'{n}_*.jpg'))
    if not matches:
        print(f"[SKIP] {n}: no file")
        continue
    img_path = matches[0]
    try:
        with open(img_path, 'rb') as f:
            img_bytes = f.read()
        boundary = '----alonda995boundaryXYZ'
        body = (
            f'--{boundary}\r\n'
            f'Content-Disposition: form-data; name="reqtype"\r\n\r\n'
            f'fileupload\r\n'
            f'--{boundary}\r\n'
            f'Content-Disposition: form-data; name="time"\r\n\r\n'
            f'72h\r\n'
            f'--{boundary}\r\n'
            f'Content-Disposition: form-data; name="fileToUpload"; filename="{img_path.name}"\r\n'
            f'Content-Type: image/jpeg\r\n\r\n'
        ).encode('utf-8') + img_bytes + f'\r\n--{boundary}--\r\n'.encode('utf-8')

        req = urllib.request.Request(
            LB,
            data=body,
            headers={'Content-Type': f'multipart/form-data; boundary={boundary}'},
            method='POST',
        )
        with urllib.request.urlopen(req, context=ctx, timeout=180) as resp:
            upload_url = resp.read().decode('utf-8', 'replace').strip()
        uploads.append({'n': n, 'file': img_path.name, 'url': upload_url})
        print(f'[UP OK] {n} {img_path.name} -> {upload_url}', flush=True)
    except Exception as e:
        print(f'[UP FAIL] {n}: {type(e).__name__}: {e}', flush=True)

Path('/root/alonda/scripts/batch_995_1014_uploads.json').write_text(
    json.dumps(uploads, indent=2)
)
print(f'\nUploaded {len(uploads)} files', flush=True)
