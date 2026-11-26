"""Render docs/images/journey.gif from journey.html.
Needs: pip install playwright && playwright install chromium (or CHROMIUM_PATH),
plus ffmpeg on PATH. Run: python3 docs/images/src/render_journey.py
"""
import math
import os
from pathlib import Path
import subprocess
import tempfile

from playwright.sync_api import sync_playwright

WIDTH = 1200
FPS = 15
SRC = Path(__file__).resolve().parent
OUT = SRC.parent / "journey.gif"


def main():
    with tempfile.TemporaryDirectory(prefix="app-recipe-journey-") as directory:
        frames = Path(directory)
        with sync_playwright() as p:
            exe = os.environ.get("CHROMIUM_PATH")
            browser = p.chromium.launch(executable_path=exe) if exe else p.chromium.launch()
            try:
                page = browser.new_page(
                    viewport={"width": 1600, "height": 900}, device_scale_factor=1
                )
                page.goto((SRC / "journey.html").as_uri())
                page.evaluate("async () => { await document.fonts.ready; }")
                duration = page.evaluate("window.DURATION")
                for frame in range(math.ceil(duration * FPS)):
                    page.evaluate("t => window.renderAt(t)", frame / FPS)
                    page.screenshot(path=str(frames / f"{frame:04d}.png"))
            finally:
                browser.close()

        # Two passes keep palette generation from buffering the entire loop.
        source = ["-framerate", str(FPS), "-i", str(frames / "%04d.png")]
        ffmpeg = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-threads", "2"]
        scale = f"scale={WIDTH}:-1:flags=lanczos"
        palette = frames / "palette.png"
        subprocess.run(
            ffmpeg + source + [
                "-filter_threads", "1", "-vf",
                f"{scale},palettegen=stats_mode=diff:max_colors=192",
                "-frames:v", "1", "-threads", "1", str(palette),
            ], check=True,
        )
        subprocess.run(
            ffmpeg + source + [
                "-i", str(palette), "-filter_complex_threads", "1", "-lavfi",
                f"[0:v]{scale}[scaled];"
                "[scaled][1:v]paletteuse=dither=sierra2_4a:diff_mode=rectangle",
                "-threads", "2", "-loop", "0", str(OUT),
            ], check=True,
        )

    size_kb = OUT.stat().st_size / 1024
    print(f"{OUT}: {size_kb:.1f} KB")
    if size_kb >= 4096:
        print("Above the 4 MB target. Lower WIDTH or FPS and render again.")


if __name__ == "__main__":
    main()
