#!/usr/bin/env python3
"""Upload new 461-480 portraits to tmpfiles.org with file.io fallback."""
import json, urllib.request, urllib.error, time
from pathlib import Path

OUT = Path("/root/alonda/assets/images")
NEW_FILES = sorted([str(p) for p in OUT.glob("46[1-9]_*.jpg")] +
                   [str(p) for p in OUT.glob("4[78][0-9]_*.jpg")])

print(f"Files to upload: {len(NEW_FILES)}", flush=True)

def upload_tmpfiles(path):
    boundary = "----HFORM" + str(int(time.time()))
    with open(path, "rb") as f:
        data = f.read()
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="{Path(path).name}"\r\n'
        f"Content-Type: image/jpeg\r\n\r\n"
    ).encode() + data + f"\r\n--{boundary}--\r\n".encode()
    req = urllib.request.Request(
        "https://tmpfiles.org/api/v1/upload",
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        d = json.loads(r.read().decode())
    url = d.get("data", {}).get("url")
    return url

def upload_fileio(path):
    with open(path, "rb") as f:
        req = urllib.request.Request(
            "https://file.io",
            data=f.read(),
            headers={"Content-Type": "image/jpeg"},
        )
        req.add_header("File-Name", Path(path).name)
    with urllib.request.urlopen(req, timeout=120) as r:
        d = json.loads(r.read().decode())
    return d.get("link")

def upload_0x0(path):
    with open(path, "rb") as f:
        req = urllib.request.Request(
            "https://0x0.st",
            data=f.read(),
            headers={"Content-Type": "image/jpeg"},
        )
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read().decode().strip()

results = {}
for path in NEW_FILES:
    name = Path(path).name
    print(f"\n=== {name} ===", flush=True)
    url = None
    for attempt in (("tmpfiles", upload_tmpfiles), ("fileio", upload_fileio), ("0x0", upload_0x0)):
        label, fn = attempt
        try:
            url = fn(path)
            if url:
                print(f"  [{label}] {url}", flush=True)
                break
        except Exception as e:
            print(f"  [{label}-err] {str(e)[:100]}", flush=True)
            continue
    if url:
        # tmpfiles returns view URL; convert to direct
        if "tmpfiles.org" in url and "/dl/" not in url:
            url = url.replace("tmpfiles.org/", "tmpfiles.org/dl/")
        results[name] = url
    else:
        results[name] = None
    time.sleep(0.5)

Path("/root/alonda/scripts/batch_461_480_uploads.json").write_text(json.dumps(results, indent=2))
print(f"\n[DONE] {sum(1 for v in results.values() if v)}/{len(results)} uploaded", flush=True)
