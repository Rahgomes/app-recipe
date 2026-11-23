#!/usr/bin/env python3
"""Generates store listing screenshots (App Store and Google Play) from real app screenshots.

Usage:
  python3 listing.py listing.json                     # all stores and languages in the file
  python3 listing.py listing.json --language en-US     # just one language
  python3 listing.py listing.json --store play         # just one store

Builds a panorama (all screenshots side by side on a wide canvas), crops it into screenshots
at each store's size and saves to <output>/<language>/<store>/NN.png, plus:
  - preview-<language>-<store>.png: panorama at 1/4 size (how search displays it; read it there)
  - alt-<language>.txt: alternative text for each screenshot (Play, up to 140 characters)
  - terminal warnings: title too large for Play, contrast, terms the stores reject.

Requires: pip install playwright pillow && playwright install chromium
Browser at another path: CHROMIUM_PATH=/path/chrome python3 listing.py ...
"""
import argparse
import html
import json
import os
import re
import sys
from pathlib import Path

STORES = {
    # iPhone 6.9" (Apple scales down to smaller sizes); Play in 9:16 portrait
    "apple": (1320, 2868),
    "play": (1080, 1920),
}
FEATURE_GRAPHIC = (1024, 500)

# Words often rejected or discouraged by stores (warning, not a blocker)
RISKY_WORDS = [
    # pt-BR / en / es
    r"\bbaix[ae] (já|agora)\b", r"\bdownload now\b", r"\bdescarg[ae] (ya|ahora)\b",
    r"\binstal[ae] (já|agora)\b", r"\binstall now\b", r"\binstal[ae] (ya|ahora)\b",
    r"\btry now\b", r"\bprueb[ae] (ya|ahora)\b",
    r"#\s?1\b", r"\bmelhor app\b", r"\bbest\b", r"\bmejor (app|aplicación)\b",
    r"\btop\b", r"\bR\$\s?\d", r"\$\s?\d",
    r"\bdesconto\b", r"\bdiscount\b", r"\bdescuento\b",
    r"\bpromo", r"\b\d+\s?% off\b", r"\b\d+\s?% de descuento\b", r"\bsale\b", r"\boferta\b",
    r"\bmilh(ão|ões) de downloads\b", r"\bmillions? of downloads\b", r"\bmill(ón|ones) de descargas\b",
    r"\bandroid\b", r"\biphone\b", r"\bgoogle play\b", r"\bapp store\b",
]


def color_luminance(hex_color):
    hex_color = hex_color.lstrip("#")
    r, g, b = (int(hex_color[i:i + 2], 16) / 255 for i in (0, 2, 4))
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def contrast(a, b):
    la, lb = sorted((color_luminance(a), color_luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def localized_text(value, language):
    if isinstance(value, dict):
        return value.get(language) or next(iter(value.values()))
    return value or ""


def title_html(t):
    """*word* becomes an accent (accent font, italic, accent color); | inserts a line break."""
    t = html.escape(t)
    t = re.sub(r"\*(.+?)\*", r'<em>\1</em>', t)
    return t.replace("|", "<br>")


def image_path(base, value, language):
    return (base / value.replace("{language}", language)).resolve()


def build_html(cfg, base, language, w, h):
    theme = cfg["theme"]
    shots = cfg["shots"]
    n = len(shots)
    u = w / 100  # 1u = 1% of screenshot width
    backgrounds = {"strong": theme["strong"], "light": theme["light"], "dark": theme["dark"]}
    text_colors = {"strong": theme.get("text_on_strong", "#FFFFFF"), "light": theme.get("text_on_light", "#141414"),
               "dark": theme.get("text_on_dark", "#FFFFFF")}
    accent_colors = {"strong": theme.get("accent_on_strong", text_colors["strong"]),
                "light": theme.get("accent_on_light", theme["strong"]),
                "dark": theme.get("accent_on_dark", theme["strong"])}
    font, accent_font = theme.get("font", "Manrope"), theme.get("accent_font", theme.get("font", "Manrope"))
    families = "&".join(f"family={f.replace(' ', '+')}:ital,wght@0,400;0,700;0,800;1,400;1,700"
                        for f in dict.fromkeys([font, accent_font]))
    frame = cfg.get("frame", "screen")

    backgrounds_html, content = [], []
    for i, c in enumerate(shots):
        kind = c.get("background", "light")
        x0 = i * w
        backgrounds_html.append(f'<div class="bg" style="left:{x0}px;background:{backgrounds[kind]}"></div>')
        large = c.get("big", False)
        size = c.get("title_size", 11)
        content.append(
            f'<div class="title" data-i="{i}" style="left:{x0 + 7 * u}px;top:{c.get("title_y", 9) * u}px;'
            f'width:{86 * u}px;color:{text_colors[kind]};font-size:{size * u}px;--accent:{accent_colors[kind]};'
            f'--large:{(c.get("big_size", 30) if large else size) * u}px">'
            f'{title_html(localized_text(c.get("title"), language))}</div>')
        screens = c.get("screens") or ([{"image": c["image"]}] if c.get("image") else [])
        for t in screens:
            src = image_path(base, t["image"], language)
            if not src.exists():
                sys.exit(f"Screenshot not found: {src}")
            tw = t.get("w", 70) * u
            tx = x0 + t.get("x", 15) * u
            ty = t.get("y", 40) * u
            rot = t.get("rot", c.get("tilt", 0))
            css_class = "screen device" if frame == "device" else "screen"
            content.append(f'<img class="{css_class}" src="{src.as_uri()}" style="left:{tx}px;top:{ty}px;'
                            f'width:{tw}px;transform:rotate({rot}deg)">')
        for e in c.get("stickers", []):
            src = image_path(base, e["image"], language)
            if not src.exists():
                sys.exit(f"Sticker not found: {src}")
            shadow = "filter:drop-shadow(0 1.2vw 2vw rgba(0,0,0,.28));" if e.get("shadow", True) else ""
            content.append(f'<img class="sticker" src="{src.as_uri()}" style="left:{x0 + e["x"] * u}px;'
                            f'top:{e["y"] * u}px;width:{e["w"] * u}px;transform:rotate({e.get("rot", 0)}deg);{shadow}">')
    radius = 5.5 * u
    return f"""<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?{families}&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:{w * n}px;height:{h}px;position:relative;overflow:hidden;background:#000}}
.bg{{position:absolute;top:0;width:{w}px;height:{h}px}}
.title{{position:absolute;font-family:'{font}',sans-serif;font-weight:800;line-height:1.02;letter-spacing:-.02em;z-index:5}}
.title em{{font-family:'{accent_font}',serif;font-style:italic;font-weight:400;color:var(--accent);font-size:var(--large);line-height:.95}}
.screen{{position:absolute;border-radius:{radius}px;box-shadow:0 {3 * u}px {7 * u}px rgba(0,0,0,.30);z-index:3}}
.screen.device{{border:{1.6 * u}px solid #121212;border-radius:{radius + 1.6 * u}px}}
.sticker{{position:absolute;z-index:4}}
</style></head><body>{''.join(backgrounds_html)}{''.join(content)}</body></html>"""


def build_feature_graphic(cfg, base, language):
    fg = cfg.get("feature_graphic")
    if not fg:
        return None
    w, h = FEATURE_GRAPHIC
    theme = cfg["theme"]
    font = theme.get("font", "Manrope")
    src = image_path(base, fg["image"], language) if fg.get("image") else None
    img = (f'<img src="{src.as_uri()}" style="position:absolute;right:70px;top:60px;width:230px;border-radius:26px;'
           f'transform:rotate(-6deg);box-shadow:0 18px 40px rgba(0,0,0,.3)">') if src else ""
    return f"""<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family={font.replace(' ', '+')}:wght@800&display=swap" rel="stylesheet">
<style>*{{margin:0}}body{{width:{w}px;height:{h}px;background:{theme['strong']};position:relative;overflow:hidden;
font-family:'{font}',sans-serif}}</style></head><body>
<div style="position:absolute;left:64px;top:50%;transform:translateY(-50%);width:560px;color:{theme.get('text_on_strong', '#fff')};
font-weight:800;font-size:64px;line-height:1.05">{title_html(localized_text(fg.get('title'), language))}</div>{img}</body></html>"""


def open_html(pg, content, output):
    """Opens HTML from a file (a blank page does not load file:// images)."""
    tmp = output / ".page.html"
    tmp.write_text(content, encoding="utf-8")
    pg.goto(tmp.as_uri(), wait_until="networkidle")
    pg.evaluate("document.fonts.ready")
    pg.wait_for_function("[...document.images].every(i => i.complete)")
    tmp.unlink()


def launch_browser(p):
    exe = os.environ.get("CHROMIUM_PATH")
    return p.chromium.launch(executable_path=exe) if exe else p.chromium.launch()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("config")
    ap.add_argument("--language")
    ap.add_argument("--store", choices=list(STORES))
    ap.add_argument("--out", help="output folder (default: 'output' field in the file)")
    a = ap.parse_args()

    cfg_path = Path(a.config).resolve()
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    base = cfg_path.parent
    output = Path(a.out).resolve() if a.out else (base / cfg.get("output", "output")).resolve()
    output.mkdir(parents=True, exist_ok=True)
    languages = [a.language] if a.language else cfg.get("languages", ["pt-BR"])
    stores = [a.store] if a.store else cfg.get("stores", list(STORES))
    shots = cfg["shots"]
    warnings = []

    limits = {"apple": (1, 10), "play": (2, 8)}
    for store in stores:
        lo, hi = limits[store]
        if not lo <= len(shots) <= hi:
            warnings.append(f"{store}: {len(shots)} screenshots (accepts {lo} to {hi})")
    if "play" in stores and len(shots) < 4:
        warnings.append("play: fewer than 4 screenshots makes the app ineligible for large recommendation formats")

    theme = cfg["theme"]
    pairs = [("strong", "text_on_strong", "#FFFFFF"), ("light", "text_on_light", "#141414"),
             ("dark", "text_on_dark", "#FFFFFF")]
    for background, key, default in pairs:
        r = contrast(theme[background], theme.get(key, default))
        if r < 4.5:
            warnings.append(f"title contrast on background '{background}' is {r:.1f}:1 (minimum 4.5:1)")

    from playwright.sync_api import sync_playwright
    from PIL import Image

    with sync_playwright() as p:
        browser = launch_browser(p)
        for language in languages:
            alts = []
            for i, c in enumerate(shots, 1):
                t = localized_text(c.get("title"), language).replace("*", "").replace("|", " ")
                for pattern in RISKY_WORDS:
                    if re.search(pattern, t, re.I):
                        warnings.append(f"{language} screenshot {i}: '{t}' contains a term stores reject or ask you to avoid ({pattern})")
                alt = localized_text(c.get("alt"), language) or t
                if len(alt) > 140:
                    warnings.append(f"{language} screenshot {i}: alternative text has {len(alt)} characters (Play accepts 140)")
                alts.append(f"{i:02d}: {alt}")
            (output / language).mkdir(parents=True, exist_ok=True)
            (output / f"alt-{language}.txt").write_text("\n".join(alts) + "\n", encoding="utf-8")

            for store in stores:
                w, h = STORES[store]
                pg = browser.new_page(viewport={"width": w * len(shots), "height": h}, device_scale_factor=1)
                open_html(pg, build_html(cfg, base, language, w, h), output)
                pg.evaluate("document.fonts.ready")
                heights = pg.evaluate("[...document.querySelectorAll('.title')].map(e=>e.getBoundingClientRect().height)")
                for i, height_px in enumerate(heights, 1):
                    frac = height_px / h
                    if store == "play" and frac > 0.20:
                        warnings.append(f"{language} play screenshot {i}: title takes up {frac:.0%} of the height "
                                      "(Google recommends up to 20%)")
                folder = output / language / store
                folder.mkdir(parents=True, exist_ok=True)
                panorama = folder.parent / f"panorama-{store}.png"
                pg.screenshot(path=str(panorama), full_page=False)
                img = Image.open(panorama).convert("RGB")  # no transparency (Apple requirement)
                for i in range(len(shots)):
                    img.crop((i * w, 0, (i + 1) * w, h)).save(folder / f"{i + 1:02d}.png")
                img.resize((img.width // 4, img.height // 4), Image.LANCZOS).save(output / f"preview-{language}-{store}.png")
                panorama.unlink()
                pg.close()

            if "play" in stores:
                feature_html = build_feature_graphic(cfg, base, language)
                if feature_html:
                    pg = browser.new_page(viewport=dict(zip(("width", "height"), FEATURE_GRAPHIC)))
                    open_html(pg, feature_html, output)
                    file_path = output / language / "play" / "feature-graphic.png"
                    pg.screenshot(path=str(file_path))
                    Image.open(file_path).convert("RGB").save(file_path)
                    pg.close()
        browser.close()

    print(f"Screenshots in {output}")
    if warnings:
        print("\nWARNINGS (review before submitting):")
        for warning in dict.fromkeys(warnings):
            print(" -", warning)
    else:
        print("No warnings.")


if __name__ == "__main__":
    main()
