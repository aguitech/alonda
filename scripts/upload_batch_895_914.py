#!/usr/bin/env python3
"""Upload batch 895-914 to tmpfiles.org with proper direct-URL extraction.
tmpfiles now requires fetching the preview page and extracting the timestamped /dl/ URL.
"""
import json
import subprocess
import time
import sys
import re
from pathlib import Path

OUT = Path('/root/alonda/assets/images')
LOG = Path('/root/alonda/scripts/batch_895_914_uploads.json')

def upload_tmpfiles(path):
    """Returns dict {preview_url, direct_url, status} or None on failure."""
    try:
        # Step 1: POST to get the preview URL
        result = subprocess.run(
            ['curl', '-s', '-F', f'file=@{path}', 'https://tmpfiles.org/api/v1/upload'],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode != 0:
            return None
        out = json.loads(result.stdout)
        if out.get('status') != 'success':
            return None
        preview_url = out['data']['url']  # e.g. https://tmpfiles.org/XXX/filename
        # Step 2: Fetch the preview page to extract the direct URL
        result2 = subprocess.run(
            ['curl', '-s', '-L', preview_url],
            capture_output=True, text=True, timeout=60
        )
        if result2.returncode != 0:
            return None
        # Extract the timestamped direct URL
        m = re.search(r'https://tmpfiles\.org/dl/[\d.]+/[a-zA-Z0-9]+/[^"\']+\.jpg', result2.stdout)
        if not m:
            return None
        direct_url = m.group(0)
        return {"preview": preview_url, "direct": direct_url}
    except Exception as e:
        print(f"    tmpfiles err: {e}", flush=True)
        return None

def upload_fileio(path):
    try:
        result = subprocess.run(
            ['curl', '-s', '-F', f'file=@{path}', 'https://file.io'],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode == 0:
            out = json.loads(result.stdout)
            if out.get('success'):
                return {"direct": out.get('link')}
    except Exception:
        pass
    return None

def upload_0x0st(path):
    try:
        result = subprocess.run(
            ['curl', '-s', '-F', f'file=@{path}', 'https://0x0.st'],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode == 0 and result.stdout.strip():
            url = result.stdout.strip()
            if url.startswith('http'):
                return {"direct": url}
    except Exception:
        pass
    return None

results = []
files = []
for n in range(895, 915):
    matches = sorted(OUT.glob(f'{n}_*.jpg'))
    if matches:
        files.append(matches[0])

print(f"Uploading {len(files)} files...", flush=True)
for f in files:
    out = upload_tmpfiles(f)
    if not out:
        print(f"  tmpfiles failed for {f.name}, trying file.io...", flush=True)
        out = upload_fileio(f)
    if not out:
        print(f"  file.io failed for {f.name}, trying 0x0.st...", flush=True)
        out = upload_0x0st(f)
    if out:
        url = out.get('direct') or out.get('preview')
        print(f"  [OK] {f.name} -> {url}", flush=True)
        results.append({
            "n": int(f.name.split('_')[0]),
            "file": f.name,
            "preview_url": out.get('preview'),
            "url": url,
        })
    else:
        print(f"  [FAIL] {f.name} - all hosts failed", flush=True)
        results.append({
            "n": int(f.name.split('_')[0]),
            "file": f.name,
            "url": None,
        })
    time.sleep(0.3)

LOG.write_text(json.dumps(results, indent=2))
ok = sum(1 for r in results if r.get('url'))
print(f"\nDONE: {ok}/{len(results)} uploaded successfully", flush=True)
