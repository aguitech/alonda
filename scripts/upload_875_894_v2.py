#!/usr/bin/env python3
"""Upload all portraits 875-894 to tmpfiles.org."""
import json
import subprocess
from pathlib import Path

OUT = Path('/root/alonda/assets/images')
files = [OUT / f"{n}_alonda_a_beautiful_26_year_old_woman_platinum_blonde_long_hair_striking_emerald_.jpg"
         for n in range(875, 895)]
files = [f for f in files if f.exists()]
files.sort(key=lambda p: int(p.name.split('_')[0]))

results = []
for f in files:
    out = subprocess.run(
        ['curl', '-s', '-F', f'file=@{f}', 'https://tmpfiles.org/api/v1/upload'],
        capture_output=True, text=True, timeout=60,
    )
    try:
        d = json.loads(out.stdout)
        url = d.get('data', {}).get('url', 'NO_URL')
    except Exception:
        url = 'PARSE_FAIL:' + out.stdout[:100]
    results.append((f.name, url))
    print(f"{f.name} -> {url}", flush=True)

Path('/root/alonda/scripts/uploads_875_894.json').write_text(json.dumps(results, indent=2))
print(f"\nUploaded: {len(results)}/{len(files)} files.")