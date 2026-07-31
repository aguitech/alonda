#!/usr/bin/env python3
"""Upload batch 1434-1453 to tmpfiles.org with file.io fallback."""
import json
import subprocess
import glob
import os
import time

BASE = "/root/alonda"
files = sorted(glob.glob(f"{BASE}/assets/images/143[4-9]_*.jpg") +
               glob.glob(f"{BASE}/assets/images/14[45][0-9]_*.jpg"))
files = [f for f in files if os.path.isfile(f)]
print(f"Found {len(files)} files to upload")

results = []
for path in files:
    name = os.path.basename(path)
    url = None
    # Try tmpfiles with Mozilla UA override
    try:
        r = subprocess.run(
            ["curl", "-sS", "-A", "Mozilla/5.0", "-F", f"file=@{path}",
             "https://tmpfiles.org/api/v1/upload"],
            capture_output=True, text=True, timeout=120,
        )
        if r.returncode == 0:
            try:
                j = json.loads(r.stdout)
                url = j.get("data", {}).get("url")
            except Exception:
                pass
    except Exception as e:
        print(f"  tmpfiles exc for {name}: {e}")
    # Fallback 0x0.st
    if not url:
        try:
            r = subprocess.run(
                ["curl", "-sS", "-A", "Mozilla/5.0", "-F", f"file=@{path}",
                 "https://0x0.st"],
                capture_output=True, text=True, timeout=120,
            )
            if r.returncode == 0 and r.stdout.strip().startswith("http"):
                url = r.stdout.strip()
        except Exception as e:
            print(f"  0x0.st exc for {name}: {e}")
    # Fallback file.io
    if not url:
        try:
            r = subprocess.run(
                ["curl", "-sS", "-F", f"file=@{path}", "https://file.io"],
                capture_output=True, text=True, timeout=120,
            )
            if r.returncode == 0:
                try:
                    j = json.loads(r.stdout)
                    url = j.get("link")
                except Exception:
                    pass
        except Exception as e:
            print(f"  file.io exc for {name}: {e}")
    print(f"  {name} -> {url}")
    results.append({"file": name, "url": url})
    time.sleep(0.4)

with open(f"{BASE}/scripts/batch_1434_1453_uploads.json", "w") as f:
    json.dump(results, f, indent=2)
print(f"DONE uploaded {sum(1 for r in results if r['url'])}/{len(results)}")