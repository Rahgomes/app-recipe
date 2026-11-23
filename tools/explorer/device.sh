#!/usr/bin/env bash
# Explorer tester Android engine: emulator or phone connected through adb (USB or Wi-Fi).
#
#   device.sh setup <package> --persona <id>   # font, theme, app language, no animation
#   device.sh out <output>                    # where to save screenshots (default ./explorer)
#   device.sh open | relaunch                 # opens the app (relaunch = force-stop and open)
#   device.sh shot                            # screenshot NN.png + element list
#   device.sh elements                        # list: role, name, center x,y, warnings
#   device.sh tap X Y | swipe X1 Y1 X2 Y2 | type "..." | key enter|back|delete
#   device.sh scroll down|up
#   device.sh background                      # sends the app to the background and returns
#   device.sh network off|on
#   device.sh errors                          # crashes and JS errors since the last request
#   device.sh restore                         # resets font, theme and animation
#
# Coordinates match the screenshot (actual device pixels). Requires adb and python3.
set -euo pipefail
STATE="${EXPLORER_STATE_ADB:-$HOME/.cache/explorer-adb}"
mkdir -p "$STATE"
DIR="$(cd "$(dirname "$0")" && pwd)"
a() { adb "${ADB_ARGS[@]}" "$@"; }
ADB_ARGS=()
[[ -n "${ANDROID_SERIAL:-}" ]] && ADB_ARGS=(-s "$ANDROID_SERIAL")
package_name() { cat "$STATE/pacote" 2>/dev/null || { echo "Run 'setup <package>' first." >&2; exit 1; }; }
output_folder() { local p; p="$(cat "$STATE/pasta" 2>/dev/null || echo ./explorer)"; mkdir -p "$p"; echo "$p"; }
settle() { sleep "${SETTLE:-1.2}"; }

persona_settings() {  # font theme language
  case "$1" in
    senior-reader) echo "1.3 no pt-BR" ;;
    in-a-hurry) echo "1.0 yes pt-BR" ;;
    low-vision) echo "2.0 no pt-BR" ;;
    budget-phone) echo "1.15 no pt-BR" ;;
    tablet) echo "1.0 no pt-BR" ;;
    offline) echo "1.0 no pt-BR" ;;
    other-language) echo "1.0 yes en-US" ;;
    skeptic) echo "1.0 no pt-BR" ;;
    *) echo "Unknown persona: $1 (see personas.md)" >&2; exit 1 ;;
  esac
}

elements() {
  a shell uiautomator dump /sdcard/explorer.xml >/dev/null 2>&1 || { echo "(uiautomator did not respond; try again)"; return; }
  local density; density="$(a shell wm density | grep -o '[0-9]*' | tail -1)"
  a exec-out cat /sdcard/explorer.xml | python3 -I "$DIR/android_tree.py" "${density:-420}"
}

cmd="${1:-}"; shift || true
case "$cmd" in
  setup)
    pkg="$1"; shift
    p="in-a-hurry"; [[ "${1:-}" == "--persona" ]] && p="$2"
    read -r font theme language <<<"$(persona_settings "$p")"
    echo "$pkg" >"$STATE/pacote"; echo 0 >"$STATE/n"
    a shell settings put system font_scale "$font"
    a shell cmd uimode night "$theme" >/dev/null
    for k in window_animation_scale transition_animation_scale animator_duration_scale; do
      a shell settings put global "$k" 0; done
    a shell settings put secure autofill_service null || true
    a shell cmd locale set-app-locales "$pkg" --locales "$language" 2>/dev/null \
      || echo "Warning: per-app language requires Android 13+; change the system language manually if needed."
    [[ "$p" == "tablet" ]] && echo "Tablet persona: use a tablet emulator (screen size does not change through commands)."
    [[ "$p" == "budget-phone" ]] && echo "Budget-phone persona: prefer a small emulator (e.g.: 720x1280) and a slow emulator network."
    echo "Ready: $pkg, persona $p (font $font, dark $theme, language $language)" ;;
  out) mkdir -p "$1"; echo "$1" >"$STATE/pasta"; echo "0" >"$STATE/n"; echo "Screenshots in $1" ;;
  open) a shell monkey -p "$(package_name)" -c android.intent.category.LAUNCHER 1 >/dev/null 2>&1; settle; echo ok ;;
  relaunch) a shell am force-stop "$(package_name)"; a shell monkey -p "$(package_name)" -c android.intent.category.LAUNCHER 1 >/dev/null 2>&1; sleep 3; echo ok ;;
  shot)
    n=$(( $(cat "$STATE/n" 2>/dev/null || echo 0) + 1 )); echo "$n" >"$STATE/n"
    file_path="$(output_folder)/$(printf '%02d' "$n").png"
    a exec-out screencap -p >"$file_path"
    echo "screenshot: $file_path"; elements ;;
  elements) elements ;;
  tap) a shell input tap "$1" "$2"; settle; echo ok ;;
  swipe) a shell input swipe "$1" "$2" "$3" "$4" 400; settle; echo ok ;;
  scroll)
    read -r w h <<<"$(a shell wm size | grep -o '[0-9]*x[0-9]*' | tail -1 | tr x ' ')"
    if [[ "${1:-down}" == "up" ]]; then a shell input swipe $((w/2)) $((h*3/10)) $((w/2)) $((h*7/10)) 400
    else a shell input swipe $((w/2)) $((h*7/10)) $((w/2)) $((h*3/10)) 400; fi
    settle; echo ok ;;
  type) t="${1// /%s}"; a shell input text "'${t//\'/}'"; settle; echo ok ;;
  key)
    case "$1" in enter) k=KEYCODE_ENTER;; back) k=KEYCODE_BACK;; delete) k=KEYCODE_DEL;; *) k="$1";; esac
    a shell input keyevent "$k"; settle; echo ok ;;
  back) a shell input keyevent KEYCODE_BACK; settle; echo ok ;;
  background) a shell input keyevent KEYCODE_HOME; sleep 2; a shell monkey -p "$(package_name)" -c android.intent.category.LAUNCHER 1 >/dev/null 2>&1; sleep 2; echo ok ;;
  network)
    if [[ "$1" == "off" ]]; then a shell svc wifi disable; a shell svc data disable; else a shell svc wifi enable; a shell svc data enable; fi
    sleep 2; echo "network $1" ;;
  errors)
    out="$(a logcat -d -b crash 2>/dev/null; a logcat -d 'AndroidRuntime:E' 'ReactNativeJS:E' 'ReactNative:E' '*:S' 2>/dev/null)"
    a logcat -c 2>/dev/null || true
    grep -v '^--------- beginning' <<<"$out" | tail -40 || true
    [[ -z "$(grep -v '^--------- beginning' <<<"$out")" ]] && echo "no errors" ;;
  restore)
    a shell settings put system font_scale 1.0
    a shell cmd uimode night no >/dev/null
    for k in window_animation_scale transition_animation_scale animator_duration_scale; do
      a shell settings put global "$k" 1; done
    a shell svc wifi enable; a shell svc data enable; echo "device restored" ;;
  *) sed -n '2,18p' "$0"; exit 1 ;;
esac
