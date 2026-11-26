"""Render an animated HTML source in this folder into docs/images/<name>.gif.

  python3 docs/images/src/render_anim.py journey          # journey.html -> journey.gif
  python3 docs/images/src/render_anim.py banner --width 1200 --fps 15

The page must set window.DURATION (seconds) and window.renderAt(t), a pure function of t,
and size its body to the canvas. No CSS animations or transitions.
Needs: pip install playwright && playwright install chromium (or CHROMIUM_PATH), and ffmpeg.
"""
import argparse
import math
import os
import subprocess
import tempfile
from pathlib import Path

from playwright.sync_api import sync_playwright

SRC = Path(__file__).resolve().parent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("name")
    ap.add_argument("--width", type=int, default=1200, help="output width in pixels")
    ap.add_argument("--fps", type=int, default=15)
    ap.add_argument("--colors", type=int, default=192)
    a = ap.parse_args()
    out = SRC.parent / f"{a.name}.gif"
    with tempfile.TemporaryDirectory(prefix=f"app-recipe-{a.name}-") as directory:
        frames = Path(directory)
        with sync_playwright() as p:
            exe = os.environ.get("CHROMIUM_PATH")
            browser = p.chromium.launch(executable_path=exe) if exe else p.chromium.launch()
            try:
                page = browser.new_page(viewport={"width": 1600, "height": 1000}, device_scale_factor=1)
                page.goto((SRC / f"{a.name}.html").as_uri())
                page.evaluate("async () => { await document.fonts.ready; }")
                size = page.evaluate("[document.body.offsetWidth, document.body.offsetHeight]")
                page.set_viewport_size({"width": size[0], "height": size[1]})
                page.wait_for_timeout(300)
                duration = page.evaluate("window.DURATION")
                for i in range(math.ceil(duration * a.fps)):
                    page.evaluate("t => window.renderAt(t)", i / a.fps)
                    page.screenshot(path=str(frames / f"{i:04d}.png"))
            finally:
                browser.close()
        src = ["-framerate", str(a.fps), "-i", str(frames / "%04d.png")]
        ff = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-threads", "2"]
        scale = f"scale={a.width}:-1:flags=lanczos"
        palette = frames / "palette.png"
        subprocess.run(ff + src + ["-vf", f"{scale},palettegen=stats_mode=diff:max_colors={a.colors}",
                                   "-frames:v", "1", str(palette)], check=True)
        subprocess.run(ff + src + ["-i", str(palette), "-lavfi",
                                   f"[0:v]{scale}[s];[s][1:v]paletteuse=dither=sierra2_4a:diff_mode=rectangle",
                                   "-loop", "0", str(out)], check=True)
    print(f"{out}: {out.stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    main()
