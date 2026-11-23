#!/usr/bin/env python3
"""Reads uiautomator XML (stdin) and lists touchable elements with centers and warnings.

Usage: adb exec-out cat /sdcard/x.xml | python3 android_tree.py <density_dpi>
Warnings: UNNAMED (touchable without text or description) and TARGET smaller than 48 dp.
"""
import re
import sys
import xml.etree.ElementTree as ET

dpi = int(sys.argv[1]) if len(sys.argv) > 1 else 420
dp = dpi / 160
xml = sys.stdin.read()
xml = xml[xml.find("<?xml"):] if "<?xml" in xml else xml
try:
    root = ET.fromstring(xml)
except ET.ParseError:
    sys.exit("(unreadable uiautomator XML; try again)")


def node_name(node):
    n = (node.get("text") or node.get("content-desc") or "").strip()
    if n:
        return n
    for child in node.iter():  # a touchable element without its own label inherits text from within
        t = (child.get("text") or child.get("content-desc") or "").strip()
        if t:
            return t
    return ""


seen = 0
for node in root.iter("node"):
    touchable = node.get("clickable") == "true" or node.get("long-clickable") == "true" or node.get("checkable") == "true"
    editable = node.get("class", "").endswith("EditText")
    if not (touchable or editable):
        continue
    m = re.findall(r"\d+", node.get("bounds", ""))
    if len(m) != 4:
        continue
    x1, y1, x2, y2 = map(int, m)
    if x2 <= x1 or y2 <= y1:
        continue
    name = node_name(node)[:60]
    role = "field" if editable else node.get("class", "").split(".")[-1] or "touchable"
    warnings = []
    if not name:
        warnings.append("UNNAMED")
    wd, hd = (x2 - x1) / dp, (y2 - y1) / dp
    if wd < 48 or hd < 48:
        warnings.append(f"TARGET {wd:.0f}x{hd:.0f}dp")
    if node.get("enabled") == "false":
        warnings.append("disabled")
    al = f"  [{', '.join(warnings)}]" if warnings else ""
    print(f'- {role} "{name}" @ {(x1 + x2) // 2},{(y1 + y2) // 2}{al}')
    seen += 1
if not seen:
    print("(node touchable elements on screen)")
