# Image sources

Every image in `docs/images/` is generated from a file in this folder, so changing a text or
translating it is an edit plus one command. Needs `pip install playwright`, a Chromium
(`playwright install chromium`, or `CHROMIUM_PATH=/path/to/chrome`) and `ffmpeg`.

| Output | Source | Command |
| --- | --- | --- |
| `banner.gif` | `banner.html` | `python3 render_anim.py banner` |
| `journey.gif` | `journey.html` | `python3 render_anim.py journey` |
| `ota.gif` | `ota.html` | `python3 render_anim.py ota` |
| `store.gif` | `store.html` + `assets/listing/` (real output of `tools/store-listing/listing.py` on its example) | `python3 render_anim.py store` |
| `explorer.gif` | `explorer.html` (recreates `demo-app.html`, the sample app with planted bugs) | `python3 render_anim.py explorer` |
| `banner.png`, `stacks.png` | `header.html` | `python3 render_header.py` |
| `flow.png` | `flow.html` | `./render.sh` |

Animated pages expose `window.DURATION` and `window.renderAt(t)`, a pure function of time with no
CSS animations, so every frame is reproducible. `render_anim.py` takes `--width`, `--fps` and
`--colors` to trade quality for file size.
