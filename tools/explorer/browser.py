#!/usr/bin/env python3
"""Explorer tester web engine: controls the app's web preview like a phone.

Opens a browser that stays alive between commands (a local server process), so the agent can
act step by step. The persona defines viewport, language, theme, touch and network.

  browser.py start <url> --persona <id> --out <output>   # launches the browser and opens the URL
  browser.py shot                 # numbered screenshot in <output>/NN.png + element list
  browser.py elements             # list only (role, name, center x,y, accessibility warnings)
  browser.py tap <x> <y>           # tap at position (screenshot pixels)
  browser.py tap-on "<name>"       # tap element by visible name or label
  browser.py type "<text>"         # type in the focused field
  browser.py key Enter            # key (Enter, Tab, Escape, Backspace)
  browser.py scroll [down|up]
  browser.py double <x> <y> [ms]   # double tap (default 80 ms between taps)
  browser.py back
  browser.py reload               # reload keeping stored app data (localStorage, IndexedDB)
  browser.py reset                # clear stored app data and start fresh (first use)
  browser.py network off|on       # disconnect and reconnect the network
  browser.py errors               # console, page and network errors, tagged with the triggering action
  browser.py stop

Web personas: see personas.md (large system fonts are only available in the Android engine).
Requires: pip install playwright && playwright install chromium (or CHROMIUM_PATH on 'start';
the browser process inherits the value). Responses include action number and network state.
"""
import json
import os
import subprocess
import sys
import time
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

STATE = Path(os.environ.get("EXPLORER_STATE", Path.home() / ".cache" / "explorer-web.json"))

PERSONAS = {
    # id: viewport, language, theme, slow network
    "senior-reader": {"w": 360, "h": 740, "idioma": "pt-BR", "tema": "light"},
    "in-a-hurry": {"w": 393, "h": 852, "idioma": "pt-BR", "tema": "dark"},
    "low-vision": {"w": 360, "h": 740, "idioma": "pt-BR", "tema": "light", "zoom": 1.5},
    "budget-phone": {"w": 360, "h": 640, "idioma": "pt-BR", "tema": "light", "lenta": True},
    "tablet": {"w": 800, "h": 1280, "idioma": "pt-BR", "tema": "light"},
    "offline": {"w": 393, "h": 852, "idioma": "pt-BR", "tema": "light"},
    "other-language": {"w": 393, "h": 852, "idioma": "en-US", "tema": "dark"},
    "skeptic": {"w": 393, "h": 852, "idioma": "pt-BR", "tema": "light"},
}

JS_ELEMENTS = r"""
() => {
  const sel = 'a,button,input,textarea,select,[role=button],[role=link],[role=tab],[role=checkbox],' +
              '[role=switch],[role=radio],[role=menuitem],[tabindex]:not([tabindex="-1"])';
  const out = [];
  for (const e of document.querySelectorAll(sel)) {
    const r = e.getBoundingClientRect();
    const st = getComputedStyle(e);
    if (r.width < 1 || r.height < 1 || st.visibility === 'hidden' || st.display === 'none') continue;
    if (r.bottom < 0 || r.top > innerHeight || r.right < 0 || r.left > innerWidth) continue;
    const field = ['input', 'textarea', 'select'].includes(e.tagName.toLowerCase());
    const label = field && e.labels && e.labels[0] ? e.labels[0].innerText.replace(e.value || '', '') : '';
    const name = (e.getAttribute('aria-label') || label || e.placeholder || (field ? '' : e.innerText) ||
                  e.getAttribute('title') || '').trim().replace(/\s+/g, ' ').slice(0, 60);
    const role = e.getAttribute('role') || e.tagName.toLowerCase();
    const warnings = [];
    if (!name) warnings.push('UNNAMED');
    if (r.width < 44 || r.height < 44) warnings.push(`TARGET ${Math.round(r.width)}x${Math.round(r.height)}`);
    if (e.disabled || e.getAttribute('aria-disabled') === 'true') warnings.push('disabled');
    if (field && e.value) warnings.push(`value: "${String(e.value).slice(0, 30)}"`);
    out.push({papel: role, nome: name, x: Math.round(r.left + r.width / 2), y: Math.round(r.top + r.height / 2), alertas: warnings});
  }
  return out;
}
"""

JS_HOOK = r"""
() => {
  if (window.__explorer) return;
  window.__explorer = true; window.__errors = window.__errors || [];
  const ce = console.error.bind(console);
  console.error = (...a) => { window.__errors.push('console: ' + a.map(String).join(' ').slice(0, 300)); ce(...a); };
  addEventListener('error', ev => window.__errors.push('page: ' + (ev.message || ev.type)));
  addEventListener('unhandledrejection', ev => window.__errors.push('promise: ' + String(ev.reason).slice(0, 300)));
}
"""


def serve(url, persona_id, folder):
    from playwright.sync_api import sync_playwright

    p = PERSONAS[persona_id]
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    pw = sync_playwright().start()
    exe = os.environ.get("CHROMIUM_PATH")
    browser = pw.chromium.launch(executable_path=exe) if exe else pw.chromium.launch()
    ctx = browser.new_context(viewport={"width": p["w"], "height": p["h"]}, device_scale_factor=2, is_mobile=True,
                          has_touch=True, locale=p["idioma"], color_scheme=p["tema"],
                          timezone_id=os.environ.get("EXPLORER_TZ", "America/Sao_Paulo"))
    ctx.add_init_script(f"({JS_HOOK})()")
    pg = ctx.new_page()
    network_errors = []
    pg.on("pageerror", lambda e: network_errors.append(f"page: {e}"))
    pg.on("requestfailed", lambda r: network_errors.append(f"network: {r.method} {r.url[:120]} {r.failure}"))
    pg.on("response", lambda r: r.status >= 500 and network_errors.append(f"server {r.status}: {r.url[:120]}"))
    if p.get("lenta"):
        cdp = ctx.new_cdp_session(pg)
        cdp.send("Network.emulateNetworkConditions",
                 {"offline": False, "latency": 400, "downloadThroughput": 50_000, "uploadThroughput": 20_000})
    pg.goto(url, wait_until="domcontentloaded")
    state = {"n": 0, "acoes": 0, "offline": False, "erros": []}

    def collect_errors(source):
        new_errors = network_errors + pg.evaluate("(window.__errors || []).splice(0)")
        network_errors.clear()
        state["erros"] += [f"[{source}] {e}" for e in new_errors]

    def settle():
        try:
            pg.wait_for_load_state("networkidle", timeout=4000)
        except Exception:
            pass
        pg.wait_for_timeout(500)
        if p.get("zoom"):
            pg.evaluate(f"document.documentElement.style.zoom='{p['zoom']}'")

    def screenshot():
        state["n"] += 1
        file_path = folder / f"{state['n']:02d}.png"
        pg.screenshot(path=str(file_path), scale="css")
        return {"captura": str(file_path), "url": pg.url, "rede": "off" if state["offline"] else "on",
                "elementos": pg.evaluate(JS_ELEMENTS)}

    def handle_command(cmd):
        action, args = cmd["acao"], cmd.get("args", [])
        if action == "shot":
            return screenshot()
        if action == "elements":
            return {"elementos": pg.evaluate(JS_ELEMENTS)}
        if action == "tap":
            pg.touchscreen.tap(float(args[0]), float(args[1]))
        elif action == "double":
            pg.touchscreen.tap(float(args[0]), float(args[1]))
            pg.wait_for_timeout(int(args[2]) if len(args) > 2 else 80)
            pg.touchscreen.tap(float(args[0]), float(args[1]))
        elif action == "tap-on":
            target = pg.get_by_role("button", name=args[0]).or_(pg.get_by_role("link", name=args[0])) \
                .or_(pg.get_by_label(args[0])).or_(pg.get_by_placeholder(args[0])) \
                .or_(pg.get_by_text(args[0], exact=True))
            target.first.tap(timeout=5000)
        elif action == "type":
            editable = pg.evaluate("(() => { const a = document.activeElement; return !!a && (a.isContentEditable || "
                                   "['INPUT','TEXTAREA'].includes(a.tagName)); })()")
            if not editable:
                return {"erro": "no text field focused: tap the field first (tap-on \"<label>\" or tap x y)"}
            pg.keyboard.type(args[0], delay=30)
        elif action == "key":
            pg.keyboard.press(args[0])
        elif action == "scroll":
            dy = -0.7 if args and args[0] == "up" else 0.7
            pg.mouse.wheel(0, dy * p["h"])
        elif action == "back":
            pg.go_back()
        elif action == "reload":
            pg.reload()
        elif action == "network":
            state["offline"] = args[0] == "off"
            ctx.set_offline(state["offline"])
        elif action == "reset":
            pg.evaluate("localStorage.clear(); sessionStorage.clear(); indexedDB.databases && "
                        "indexedDB.databases().then(l => l.forEach(d => indexedDB.deleteDatabase(d.name)))")
            ctx.clear_cookies()
            pg.goto(url, wait_until="domcontentloaded")
        elif action == "errors":
            collect_errors(state.get("ultima", "start"))
            items = list(dict.fromkeys(state["erros"]))
            state["erros"] = []
            return {"erros": items}
        else:
            return {"erro": f"unknown action: {action}"}
        settle()
        state["acoes"] += 1
        state["ultima"] = f"action {state['acoes']}: {action} {' '.join(args)}".strip()
        collect_errors(state["ultima"])
        return {"ok": True, "acao": state["acoes"], "rede": "off" if state["offline"] else "on",
                "url": pg.url}

    class H(BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def do_POST(self):
            cmd = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
            if cmd["acao"] == "stop":
                self._r({"ok": True})
                raise KeyboardInterrupt
            try:
                r = handle_command(cmd)
            except Exception as e:  # the agent sees the error and decides
                r = {"erro": str(e).splitlines()[0][:300]}
            self._r(r)

        def _r(self, obj):
            data = json.dumps(obj, ensure_ascii=False).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

    srv = HTTPServer(("localhost", 0), H)
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps({"porta": srv.server_port, "pid": os.getpid()}))
    settle()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        browser.close()
        pw.stop()
        STATE.unlink(missing_ok=True)


def send_command(action, args):
    if not STATE.exists():
        sys.exit("Browser not started: run 'browser.py start <url> --persona <id> --out <output>'")
    port = json.loads(STATE.read_text())["porta"]
    req = urllib.request.Request(f"http://localhost:{port}", data=json.dumps({"acao": action, "args": args}).encode(),
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            return json.loads(r.read())
    except Exception as e:
        if action == "stop":
            return {"ok": True}
        sys.exit(f"No response from browser ({e}). Run 'stop' and 'start' again.")


def print_response(r):
    if "elementos" in r:
        if "captura" in r:
            print(f"screenshot: {r['captura']}  ({r['url']}; network {r['rede']})")
        for e in r["elementos"]:
            al = f"  [{', '.join(e['alertas'])}]" if e["alertas"] else ""
            print(f"- {e['papel']} \"{e['nome']}\" @ {e['x']},{e['y']}{al}")
        if not r["elementos"]:
            print("(no visible touchable elements)")
    elif "erros" in r:
        print("\n".join(r["erros"]) or "no errors")
    else:
        print(json.dumps(r, ensure_ascii=False))


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        return
    action, remaining = sys.argv[1], sys.argv[2:]
    if action == "start":
        import argparse
        ap = argparse.ArgumentParser()
        ap.add_argument("url")
        ap.add_argument("--persona", default="in-a-hurry", choices=list(PERSONAS))
        ap.add_argument("--out", required=True)
        a = ap.parse_args(remaining)
        if STATE.exists():
            send_command("stop", [])
            time.sleep(1)
        log = open(Path(a.out).resolve().parent / "browser.log", "a") if Path(a.out).resolve().parent.exists() else subprocess.DEVNULL
        subprocess.Popen([sys.executable, __file__, "_servir", a.url, a.persona, a.out],
                         stdout=log, stderr=log, start_new_session=True)
        for _ in range(60):
            if STATE.exists():
                print(f"Browser ready: persona {a.persona}, {PERSONAS[a.persona]}")
                return
            time.sleep(0.5)
        sys.exit("The browser did not start within 30 s (see browser.log).")
    if action == "_servir":
        serve(*remaining[:3])
        return
    print_response(send_command(action, remaining))


if __name__ == "__main__":
    main()
