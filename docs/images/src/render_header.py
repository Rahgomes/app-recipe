"""Render docs/images/banner.png and stacks.png from header.html.
Needs: pip install playwright && playwright install chromium (or CHROMIUM_PATH)."""
import os
from pathlib import Path
from playwright.sync_api import sync_playwright

SRC = Path(__file__).parent
OUT = SRC.parent
with sync_playwright() as p:
    exe = os.environ.get("CHROMIUM_PATH")
    b = p.chromium.launch(executable_path=exe) if exe else p.chromium.launch()
    pg = b.new_page(viewport={"width": 1600, "height": 1200}, device_scale_factor=1)
    pg.goto((SRC / "header.html").as_uri())
    pg.wait_for_timeout(1500)
    for name in ("banner", "stacks"):
        pg.locator(f"#{name}").screenshot(path=str(OUT / f"{name}.png"))
    b.close()
