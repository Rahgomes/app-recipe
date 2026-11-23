#!/usr/bin/env python3
"""Builds docs/images/store-listing.gif and docs/images/explorer.gif from the real tools.

  python3 docs/images/src/example_screens.py   # once, if the example screens changed
  python3 docs/images/src/make_gifs.py

Needs: pip install playwright pillow && playwright install chromium (or CHROMIUM_PATH).
"""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

REPO = Path(__file__).resolve().parents[3]
IMAGES = REPO / "docs" / "images"
SRC = IMAGES / "src"
BG = (11, 16, 32)
FG = (238, 241, 255)
MUTED = (150, 160, 200)
ACCENT = (124, 240, 196)
WARN = (255, 196, 92)


def font(size, bold=False):
    for name in (["DejaVuSans-Bold.ttf"] if bold else ["DejaVuSans.ttf"]):
        for d in ("/usr/share/fonts/truetype/dejavu", "/usr/share/fonts/dejavu", "/Library/Fonts"):
            if Path(d, name).exists():
                return ImageFont.truetype(str(Path(d, name)), size)
    return ImageFont.load_default()


def save_gif(frames, durations, path):
    pal = [f.convert("P", palette=Image.ADAPTIVE, colors=128) for f in frames]
    pal[0].save(path, save_all=True, append_images=pal[1:], duration=durations, loop=0, optimize=True)
    print(f"{path.name}: {len(frames)} frames, {path.stat().st_size // 1024} KB")


def store_listing_gif():
    out = Path(tempfile.mkdtemp())
    subprocess.run([sys.executable, str(REPO / "tools/store-listing/listing.py"),
                    str(REPO / "tools/store-listing/example/listing.json"), "--store", "apple", "--out", str(out)],
                   check=True)
    lang = json.loads((REPO / "tools/store-listing/example/listing.json").read_text())["languages"][0]
    shots = sorted((out / lang / "apple").glob("[0-9][0-9].png"))
    W, H = 1000, 560
    th = 400
    tiles = [Image.open(s).convert("RGB").resize((int(th * 1320 / 2868), th), Image.LANCZOS) for s in shots]
    tw = tiles[0].width
    x0 = (W - tw * len(tiles)) // 2
    title, small = font(30, True), font(18)
    frames, durations = [], []
    for k in range(1, len(tiles) + 1):
        f = Image.new("RGB", (W, H), BG)
        d = ImageDraw.Draw(f)
        d.text((40, 28), "One JSON file + real screens", font=title, fill=FG)
        d.text((40, 70), "→ a connected panorama, cut to each store's size", font=small, fill=MUTED)
        for i in range(k):
            f.paste(tiles[i], (x0 + i * tw, 120))
        frames.append(f)
        durations.append(450)
    last = frames[-1].copy()
    d = ImageDraw.Draw(last)
    d.text((40, H - 32), "Apple 1320×2868 · Play 1080×1920 · feature graphic · alt text · store-rule warnings",
           font=font(16), fill=ACCENT)
    frames.append(last)
    durations.append(3200)
    save_gif(frames, durations, IMAGES / "store-listing.gif")


def explorer_gif():
    out = Path(tempfile.mkdtemp())
    env = dict(os.environ, EXPLORER_STATE=str(out / "state.json"))
    b = [sys.executable, str(REPO / "tools/explorer/browser.py")]

    def run(*args):
        r = subprocess.run(b + list(args), capture_output=True, text=True, env=env)
        return (r.stdout + r.stderr).strip()

    run("start", (SRC / "demo-app.html").as_uri(), "--persona", "in-a-hurry", "--out", str(out / "shots"))
    steps = [  # (command, note shown on the frame, is it a finding?)
        (["shot"], "persona: in-a-hurry · dark mode · 393×852", False),
        (["tap-on", "Continue"], "", False),
        (["tap-on", "Not now"], "", False),
        (["shot"], "habit names barely visible in dark mode", True),
        (["tap-on", "New habit"], "", False),
        (["tap-on", "Name"], "", False),
        (["type", "Walk"], "", False),
        (["network", "off"], "network dropped before saving", False),
        (["tap-on", "Save habit"], "", False),
        (["network", "on"], "", False),
        (["shot"], "habit saved offline is gone, no message", True),
        (["elements"], "settings button: 28×28, below the 44 px target", True),
    ]
    W, H = 1000, 560
    mono, small, bold = font(17), font(16), font(20, True)
    frames, durations, log, findings = [], [], [], []
    shot_img = None
    for cmd, note, finding in steps:
        res = run(*cmd)
        if cmd[0] == "shot":
            path = res.splitlines()[0].split("shot: ")[-1].split("  (")[0].strip()
            if Path(path).exists():
                shot_img = Image.open(path).convert("RGB")
        log.append("$ " + " ".join(cmd))
        if finding:
            findings.append(note)
        f = Image.new("RGB", (W, H), BG)
        d = ImageDraw.Draw(f)
        if shot_img:
            s = shot_img.resize((int(500 * shot_img.width / shot_img.height), 500), Image.LANCZOS)
            f.paste(s, (30, 30))
        x = 320
        d.text((x, 30), "explorer-tester", font=bold, fill=FG)
        for i, line in enumerate(log[-9:]):
            d.text((x, 70 + i * 26), line, font=mono, fill=MUTED if i < len(log[-9:]) - 1 else ACCENT)
        if note and not finding:
            d.text((x, 320), note, font=small, fill=FG)
        d.text((x, 360), "Findings", font=bold, fill=WARN)
        for i, fnd in enumerate(findings):
            d.text((x, 392 + i * 26), f"A{i + 1}. {fnd}", font=small, fill=FG)
        frames.append(f)
        durations.append(900 if not finding else 1600)
    durations[-1] = 3500
    run("stop")
    save_gif(frames, durations, IMAGES / "explorer.gif")


if __name__ == "__main__":
    store_listing_gif()
    explorer_gif()
