#!/usr/bin/env bash
# Re-renders docs/images/flow.png from flow.html (needs: pip install playwright && playwright install chromium).
set -euo pipefail
cd "$(dirname "$0")"
python3 - <<'PY'
import os
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    exe = os.environ.get("CHROMIUM_PATH")
    b = p.chromium.launch(executable_path=exe) if exe else p.chromium.launch()
    pg = b.new_page(viewport={"width": 1920, "height": 1080}, device_scale_factor=1)
    pg.goto("file://" + os.path.abspath("flow.html")); pg.wait_for_timeout(2500)
    over = pg.evaluate("[...document.querySelectorAll('.step')].filter(e=>e.scrollWidth>e.clientWidth).length")
    pg.screenshot(path="../flow.png"); b.close()
print("flow.png written; overflowing steps:", over)
PY
