#!/usr/bin/env python3
"""Upload new Alonda batch images to tmpfiles.org and log URLs."""
import json
import subprocess
import sys
from pathlib import Path

BATCH_GLOB = "/root/alonda/assets/images/chefs_vehicles_botanic_myth2_round3_*.jpg"
LOG_FILE = Path("/tmp/uploads_tmpfiles/batch_1486_1505.log")
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

files = sorted(Path("/root/alonda/assets/images").glob("chefs_vehicles_botanic_myth2_round3_*.jpg"))
print(f"Found {len(files)} files to upload")

lines = []
for f in files:
    try:
        out = subprocess.check_output(
            ["curl", "-s", "-F", f"file=@{f}", "https://tmpfiles.org/api/v1/upload"],
            timeout=60,
        )
        data = json.loads(out)
        url = data.get("data", {}).get("url", "")
        if not url:
            print(f"FAIL {f.name}: {data}")
            lines.append(f"{f.name} -> FAIL: {data}")
            continue
        # tmpfiles returns /dl/<id>/<file> — usable as-is for viewing & download
        line = f"{f.name} -> {url}"
        lines.append(line)
        print(f"OK   {f.name} -> {url}")
    except Exception as e:
        print(f"ERR  {f.name}: {e}")
        lines.append(f"{f.name} -> ERR: {e}")

LOG_FILE.write_text("\n".join(lines) + "\n")
print(f"\nWrote {LOG_FILE}")
print(f"Uploaded: {sum(1 for l in lines if '->' in l and 'FAIL' not in l and 'ERR' not in l)}/{len(files)}")