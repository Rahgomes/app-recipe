#!/usr/bin/env bash
# Scans a folder before sharing: keys, tokens, emails, IPs and terms you list.
#   check-secrets.sh <folder> [forbidden-terms-file]
# The terms file has one term per line (project name, internal domain, username...).
# Uses gitleaks if installed; always runs the pattern searches below.
set -uo pipefail
TARGET="${1:?usage: check-secrets.sh <folder> [terms.txt]}"
TERMS="${2:-}"
found=0

if command -v gitleaks >/dev/null; then
  gitleaks dir "$TARGET" --no-banner --redact || found=1
fi

PATTERNS=(
  'AIza[0-9A-Za-z_-]{35}'                 # Google/Firebase key
  'goog_[A-Za-z0-9]{20,}'                 # RevenueCat Android public key
  'appl_[A-Za-z0-9]{20,}'                 # RevenueCat iOS public key
  'sk_[A-Za-z0-9]{20,}'                   # secret key (various services)
  'ca-app-pub-[0-9]{16}'                  # real AdMob app/ad unit ID
  '-----BEGIN [A-Z ]*PRIVATE KEY-----'
  '"private_key_id"'
  'ghp_[A-Za-z0-9]{36}|github_pat_[A-Za-z0-9_]{50,}'
  'xox[baprs]-[A-Za-z0-9-]{10,}'
  '[0-9]{12}-[a-z0-9]{32}\.apps\.googleusercontent\.com'
  '\b([0-9]{1,3}\.){3}[0-9]{1,3}\b'       # IP (review: versions may match)
  '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}'   # email
)
for p in "${PATTERNS[@]}"; do
  r=$(grep -rnIE --exclude-dir=.git --exclude="$(basename "$0")" -- "$p" "$TARGET" 2>/dev/null) && { echo "== pattern: $p"; echo "$r"; found=1; }
done

if [ -n "$TERMS" ] && [ -f "$TERMS" ]; then
  while IFS= read -r t; do
    [ -z "$t" ] && continue
    r=$(grep -rniIF --exclude-dir=.git -- "$t" "$TARGET" 2>/dev/null) && { echo "== term: $t"; echo "$r"; found=1; }
  done < "$TERMS"
fi

[ $found -eq 0 ] && echo "Nothing found." || { echo; echo "Review the findings above before sharing."; exit 1; }
