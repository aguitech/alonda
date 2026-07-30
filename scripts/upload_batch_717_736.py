#!/usr/bin/env python3
"""Upload new batch 717-736 to litterbox.catbox.moe (72h temp) with fallbacks."""
import json
import urllib.request
import ssl
from pathlib import Path

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

OUT_DIR = Path("/root/alonda/assets/images")
START = 717
END = 736

def upload_litterbox(path: Path) -> str | None:
    """Upload to litterbox.catbox.moe 72h temp."""
    try:
        with open(path, "rb") as f:
            file_data = f.read()
        boundary = "----hermesboundary12345"
        body = (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="reqtype"\r\n\r\nfileupload\r\n'
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="time"\r\n\r\n72h\r\n'
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="fileToUpload"; filename="{path.name}"\r\n'
            f"Content-Type: image/jpeg\r\n\r\n"
        ).encode() + file_data + f"\r\n--{boundary}--\r\n".encode()
        req = urllib.request.Request(
            "https://litterbox.catbox.moe/resources/internals/api.php",
            data=body,
            headers={
                "Content-Type": f"multipart/form-data; boundary={boundary}",
                "User-Agent": "curl/7.88.1",
            },
        )
        with urllib.request.urlopen(req, context=ctx, timeout=90) as r:
            out = r.read().decode().strip()
        if out.startswith("http"):
            return out
        print(f"  litterbox resp: {out}")
        return None
    except Exception as e:
        print(f"  litterbox err: {e}")
        return None

def upload_bash(path: Path) -> str | None:
    """Use curl fallback."""
    import subprocess
    try:
        r = subprocess.run(
            ["curl", "-s", "-A", "curl/7.88.1",
             "-F", "reqtype=fileupload",
             "-F", "time=72h",
             "-F", f"fileToUpload=@{path}",
             "https://litterbox.catbox.moe/resources/internals/api.php"],
            capture_output=True, text=True, timeout=90
        )
        out = r.stdout.strip()
        if out.startswith("http"):
            return out
        return None
    except Exception as e:
        print(f"  curl err: {e}")
        return None

results = []
for n in range(START, END + 1):
    matches = list(OUT_DIR.glob(f"{n}_*.jpg"))
    if not matches:
        print(f"[skip {n}] no file")
        continue
    path = matches[0]
    print(f"[{n}] {path.name}")
    url = upload_litterbox(path)
    if not url:
        url = upload_bash(path)
    if url:
        print(f"  -> {url}")
        results.append({"num": n, "file": path.name, "url": url})
    else:
        print(f"  [FAIL]")
        results.append({"num": n, "file": path.name, "url": None})

out = Path("/root/alonda/scripts/batch_717_736_uploads.json")
out.write_text(json.dumps(results, indent=2))
print(f"\n[DONE] {sum(1 for r in results if r['url'])}/{len(results)} uploaded")