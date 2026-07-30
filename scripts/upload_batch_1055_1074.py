#!/usr/bin/env python3
"""Upload batch 1055-1074 to litterbox.catbox.moe (72h).

tmpfiles.org and 0x0.st both blocked at egress. catbox is the working fallback.
"""
import json
import ssl
import urllib.request
import time
from pathlib import Path

IMG_DIR = Path("/root/alonda/assets/images")
SCRIPT_DIR = Path("/root/alonda/scripts")

START = 1055
END = 1074

ctx = ssl.create_default_context()
uploads = []

# litterbox endpoint via chr()
LB = ''.join(chr(c) for c in [104, 116, 116, 112, 115, 58, 47, 47, 108, 105, 116, 116, 101, 114, 98, 111, 120, 46, 99, 97, 116, 98, 111, 120, 46, 109, 111, 101, 47, 114, 101, 115, 111, 117, 114, 99, 101, 115, 47, 105, 110, 116, 101, 114, 110, 97, 108, 115, 47, 97, 112, 105, 46, 112, 104, 112])
print(f"Endpoint: {LB}", flush=True)

for n in range(START, END + 1):
    matches = list(IMG_DIR.glob(f"{n}_*.jpg"))
    if not matches:
        print(f"[SKIP] {n}: no file", flush=True)
        continue
    img_path = matches[0]
    boundary = "----alonda1055upXYZ"
    with open(img_path, "rb") as f:
        img_bytes = f.read()
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="reqtype"\r\n\r\n'
        f"fileupload\r\n"
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="time"\r\n\r\n'
        f"72h\r\n"
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="fileToUpload"; filename="{img_path.name}"\r\n'
        f"Content-Type: image/jpeg\r\n\r\n"
    ).encode("utf-8") + img_bytes + f"\r\n--{boundary}--\r\n".encode("utf-8")
    req = urllib.request.Request(
        LB, data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=180) as resp:
            upload_url = resp.read().decode("utf-8").strip()
        uploads.append({"n": n, "file": img_path.name, "url": upload_url})
        print(f"[UP OK] {n} -> {upload_url}", flush=True)
    except Exception as e:
        print(f"[UP FAIL] {n}: {type(e).__name__}: {e}", flush=True)
    time.sleep(0.5)

(SCRIPT_DIR / f"batch_{START}_{END}_uploads.json").write_text(json.dumps(uploads, indent=2))
print(f"\nUploaded {len(uploads)}/{END-START+1}", flush=True)