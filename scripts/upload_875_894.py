#!/usr/bin/env python3
"""Upload new portraits 875-894 to tmpfiles.org."""
import json
import subprocess
import sys
from pathlib import Path

OUT = Path('/root/alonda/assets/images')
files = sorted(OUT.glob('87[5-9]_alonda_*.jpg')) + sorted(OUT.glob('89[0-4]_alonda_*.jpg'))
files = sorted(set(files), key=lambda p: int(p.name.split('_')[0]))

results = []
for f in files:
    try:
        out = subprocess.run(
            ['curl', '-s', '-F', f'file=@{f}', 'https://tmpfiles.org/api/v1/upload'],
            capture_output=True, text=True, timeout=60,
        )
        try:
            d = json.loads(out.stdout)
            url = d.get('data', {}).get('url', 'NO_URL')
        except Exception:
            url = 'PARSE_FAIL'
        results.append((f.name, url))
        print(f"{f.name} -> {url}", flush=True)
    except Exception as e:
        results.append((f.name, f'ERR:{e}'))
        print(f"{f.name} -> ERR:{e}", flush=True)

Path('/root/alonda/scripts/uploads_875_894.json').write_text(json.dumps(results, indent=2))
print(f"\nUploaded: {len(results)} files. Summary in scripts/uploads_875_894.json")