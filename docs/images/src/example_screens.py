#!/usr/bin/env python3
"""Renders the fictional "Routine" app screens used by the store-listing example.

Writes tools/store-listing/example/screens/01..05.png and stickers/star|fire|bell.png.
Needs: pip install playwright && playwright install chromium (or CHROMIUM_PATH).
"""
import os
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[3] / "tools" / "store-listing" / "example"
BASE = """<html><head><style>*{margin:0;box-sizing:border-box;font-family:'DejaVu Sans',sans-serif}
body{width:390px;height:844px;background:#FFF8F1;color:#1d1a17;padding:54px 20px 0;position:relative}
.sb{position:absolute;top:14px;left:26px;right:26px;display:flex;justify-content:space-between;font-weight:700;font-size:15px}
h1{font-size:28px;margin:8px 0 14px}.c{background:#fff;border-radius:18px;padding:16px;margin-bottom:12px;box-shadow:0 2px 8px rgba(0,0,0,.06)}
.r{display:flex;align-items:center;gap:12px}.k{width:34px;height:34px;border-radius:50%;border:3px solid #FF6A2B;display:grid;place-items:center;color:#fff;font-weight:900}
.k.on{background:#FF6A2B}.m{color:#7b6f66;font-size:13px}
.btn{position:absolute;left:20px;right:20px;bottom:40px;background:#FF6A2B;color:#fff;border-radius:16px;padding:18px;text-align:center;font-weight:800;font-size:17px}
.bar{height:10px;background:#f1e4d8;border-radius:9px;overflow:hidden}.bar i{display:block;height:100%;background:#FF6A2B}
.g{display:grid;grid-template-columns:repeat(7,1fr);gap:6px}.g b{aspect-ratio:1;border-radius:7px;background:#f1e4d8}
.g b.on{background:#FF6A2B}.g b.mid{background:#ffb48f}
</style></head><body><div class="sb"><span>9:41</span><span>100%</span></div>CONTENT</body></html>"""


def habit(name, sub, done):
    return (f'<div class="c r"><div class="k {"on" if done else ""}">{"✓" if done else ""}</div>'
            f'<div><b>{name}</b><div class="m">{sub}</div></div></div>')


SCREENS = {
    "01": "<h1>Today</h1><div class='c'><b>3 of 5 done</b><div class='bar' style='margin-top:10px'><i style='width:60%'></i></div></div>"
          + habit("Drink water", "8 glasses · 6 done", True) + habit("Read 10 pages", "before bed", True)
          + habit("Walk", "20 min", True) + habit("Meditate", "5 min", False) + habit("No phone in bed", "10 pm", False),
    "02": "<h1>New habit</h1><div class='c'><div class='m'>Name</div><b style='font-size:20px'>Walk 20 minutes</b></div>"
          "<div class='c'><div class='m'>When</div><b>Mon · Wed · Fri · 7 am</b></div><div class='c'><div class='m'>Reminder</div><b>On</b></div>"
          "<div class='btn'>Create habit</div>",
    "03": "<h1>Streak</h1><div class='c' style='text-align:center'><div style='font-size:64px;font-weight:900;color:#FF6A2B'>21</div>"
          "<b>days in a row</b><div class='m'>your best</div></div><div class='c'><div class='g'>"
          + "".join(f"<b class='{'on' if i % 5 else 'mid'}'></b>" for i in range(28)) + "</div></div>",
    "04": "<h1>This week</h1><div class='c'><b>86% complete</b><div class='bar' style='margin-top:10px'><i style='width:86%'></i></div></div>"
          + habit("Drink water", "7 of 7 days", True) + habit("Read", "6 of 7 days", True) + habit("Meditate", "4 of 7 days", False),
    "05": "<h1>Your plan</h1><div class='c'><b>Free</b><div class='m'>3 habits, reminders</div></div>"
          "<div class='c' style='border:2px solid #FF6A2B'><b>Full</b><div class='m'>unlimited habits, history, widgets</div></div>"
          "<div class='btn'>Try 7 days</div>",
}
STICKERS = {"star": "⭐", "fire": "🔥", "bell": "🔔"}

(ROOT / "screens").mkdir(parents=True, exist_ok=True)
(ROOT / "stickers").mkdir(parents=True, exist_ok=True)
with sync_playwright() as p:
    exe = os.environ.get("CHROMIUM_PATH")
    b = p.chromium.launch(executable_path=exe) if exe else p.chromium.launch()
    pg = b.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=3)
    for k, v in SCREENS.items():
        pg.set_content(BASE.replace("CONTENT", v))
        pg.screenshot(path=str(ROOT / "screens" / f"{k}.png"))
    for name, emoji in STICKERS.items():
        s = b.new_page(viewport={"width": 200, "height": 200}, device_scale_factor=2)
        s.set_content(f"<html><body style='margin:0;background:transparent;font-size:150px;line-height:200px;"
                      f"text-align:center'>{emoji}</body></html>")
        s.screenshot(path=str(ROOT / "stickers" / f"{name}.png"), omit_background=True)
        s.close()
    b.close()
print("example screens and stickers written to", ROOT)
