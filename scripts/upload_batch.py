#!/usr/bin/env python3
"""Upload new portraits to tmpfiles.org AND resolve to direct file URLs."""
import json
import re
import subprocess
import sys
import urllib.request
from pathlib import Path

IMG_DIR = Path('/root/alonda/assets/images')
SCRIPT_DIR = Path('/root/alonda/scripts')

start, end = int(sys.argv[1]), int(sys.argv[2])

results = []
for n in range(start, end + 1):
    matches = sorted(IMG_DIR.glob(f"{n}_*.jpg"))
    if not matches:
        print(f"[{n}] no file")
        results.append({"n": n, "file": None, "url": None, "direct": None,
                        "error": "no file"})
        continue
    fp = matches[0]
    try:
        out = subprocess.check_output(
            ["curl", "-sS", "-F", f"file=@{fp}",
             "https://tmpfiles.org/api/v1/upload"],
            timeout=60,
        )
        j = json.loads(out)
        if j.get("status") != "success":
            print(f"[{n}] FAIL: {out[:200]}")
            results.append({"n": n, "file": fp.name, "url": None, "direct": None,
                            "error": out[:200]})
            continue
        page_url = j["data"]["url"]
        # Resolve to direct file URL by fetching the preview page once.
        # tmpfiles.org returns 403 to urllib but works with curl-like headers.
        curl_out = subprocess.check_output(
            ["curl", "-sSL", "-A", "Mozilla/5.0 (X11; Linux x86_64) "
             "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
             "-H", "Accept: text/html", page_url],
            timeout=30,
        ).decode('utf-8', errors='replace')
        m = re.search(r'src="(https://tmpfiles\.org/dl/\d+\.[a-f0-9]+/'
                      r'[^"]+\.(?:jpg|jpeg))"', curl_out, re.I)
        if not m:
            print(f"[{n}] ok (page only) -> {page_url}")
            results.append({"n": n, "file": fp.name, "url": page_url,
                            "direct": None, "error": "no direct url in page"})
            continue
        direct = m.group(1)
        # Sanity-check the direct URL actually returns image bytes (via curl)
        head = subprocess.check_output(
            ["curl", "-sSI", "-A", "Mozilla/5.0", direct],
            timeout=30,
        ).decode('utf-8', errors='replace')
        size_m = re.search(r'content-length:\s*(\d+)', head, re.I)
        ct_m = re.search(r'content-type:\s*(\S+)', head, re.I)
        sz = int(size_m.group(1)) if size_m else 0
        ct = ct_m.group(1).rstrip(';') if ct_m else ''
        ok = ct.startswith('image/') and sz > 5000
        print(f"[{n}] {'ok' if ok else 'BAD'} ({sz}B, {ct}) -> {direct}")
        results.append({"n": n, "file": fp.name, "url": page_url,
                        "direct": direct if ok else None,
                        "size": sz, "content_type": ct,
                        "ok": ok})
    except Exception as e:
        print(f"[{n}] EXC: {type(e).__name__} {e}")
        results.append({"n": n, "file": fp.name, "url": None, "direct": None,
                        "error": str(e)})

upload_file = SCRIPT_DIR / f"batch_{start}_{end}_uploads.json"
upload_file.write_text(json.dumps(results, indent=2, ensure_ascii=False))
ok = sum(1 for r in results if r.get("ok"))
print(f"\nWrote {upload_file}")
print(f"Direct URLs verified: {ok}/{len(results)}")
