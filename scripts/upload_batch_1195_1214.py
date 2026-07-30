#!/usr/bin/env python3
"""Upload Alonda portraits 1195-1214 to tmpfiles.org via curl subprocess."""
import json
import subprocess
import os
from pathlib import Path

OUT_DIR = Path("/root/alonda/assets/images")
START = 1195
END = 1214

results = {}

for n in range(START, END + 1):
    matches = sorted(OUT_DIR.glob(f"{n}_*.jpg"))
    if not matches:
        print(f"[SKIP] no file for {n}", flush=True)
        continue
    img = matches[0]
    print(f"  uploading {img.name}...", flush=True)

    try:
        out = subprocess.check_output(
            ["curl", "-s", "-A", "Mozilla/5.0",
             "-F", f"file=@{img}",
             "https://tmpfiles.org/api/v1/upload"],
            timeout=120,
            stderr=subprocess.STDOUT,
        ).decode().strip()
        data = json.loads(out)
        if data.get("status") == "success":
            url = data["data"]["url"]
            results[img.name] = url
            print(f"    -> {url}", flush=True)
            continue
        else:
            print(f"    tmpfiles non-success: {out}", flush=True)
    except subprocess.CalledProcessError as e:
        print(f"    tmpfiles curl error: {e.output.decode(errors='ignore')}", flush=True)
    except Exception as e:
        print(f"    tmpfiles err: {e}", flush=True)

    results[img.name] = None

print(f"\n=== Uploaded {sum(1 for v in results.values() if v)}/{len(results)} ===", flush=True)

with open("/root/alonda/scripts/batch_1195_1214_uploads.json", "w") as f:
    json.dump(results, f, indent=2)
print(f"Saved to batch_1195_1214_uploads.json", flush=True)
