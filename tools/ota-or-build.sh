#!/usr/bin/env bash
# Reports whether changes since the last build can go over the air (EAS Update) or need a new build.
#
#   ota-or-build.sh --checar              only reports (does not publish)
#   ota-or-build.sh "short message"      checks and publishes over the air to channel $CANAL
#
# Convention: each build commit gets a tag <prefix>-<n>, e.g.:
#   git tag preview-build-12 && git push origin preview-build-12
#
# Configure through the variables below (or export them before calling).
# The Expo token comes from the environment (EXPO_TOKEN); this script never prints it.
set -euo pipefail

APP_DIR="${APP_DIR:-apps/mobile}"          # Expo app folder inside the repo
TAG_PREFIXO="${TAG_PREFIXO:-preview-build}" # tag prefix of the last build
CANAL="${CANAL:-preview}"                   # EAS Update channel/branch
RAMO="${RAMO:-main}"                        # branch to publish from
PLATAFORMA="${PLATAFORMA:-android}"
# Text required in the exported bundle (e.g.: a public ID for the right environment). Empty = no check.
CONFERIR_NO_PACOTE="${CONFERIR_NO_PACOTE:-}"

# Paths included in the binary: changing any of them requires a new build to reach the phone.
NATIVE="^(${APP_DIR}/(package\.json|app\.json|app\.config\.(ts|js)|eas\.json|google-services\.json|GoogleService-Info\.plist|android/.*|ios/.*|assets/images/(icon|adaptive-icon|android-icon-[a-z]+|splash)[^/]*\.png)|pnpm-lock\.yaml|package-lock\.json|yarn\.lock)$"

[ "$(git branch --show-current)" = "$RAMO" ] || { echo "ERROR: publish from branch $RAMO"; exit 1; }
git fetch -q origin
[ -z "$(git status --porcelain --untracked-files=no)" ] || { echo "ERROR: uncommitted changes"; exit 1; }
[ "$(git rev-parse HEAD)" = "$(git rev-parse "origin/$RAMO")" ] || { echo "ERROR: HEAD differs from origin/$RAMO (push or pull needed)"; exit 1; }

BASE=$(git tag -l "${TAG_PREFIXO}-*" --sort=-version:refname | head -1)
[ -n "$BASE" ] || { echo "ERROR: no tag ${TAG_PREFIXO}-*; tag the last build commit"; exit 1; }

CHANGED=$(git diff --name-only "$BASE" HEAD | grep -E "$NATIVE" || true)
if [ -n "$CHANGED" ]; then
  echo "BUILD REQUIRED: native changes since $BASE:"
  echo "$CHANGED" | sed 's/^/  /'
  exit 2
fi
echo "OTA OK: only JS changed since $BASE ($(git diff --name-only "$BASE" HEAD -- "$APP_DIR" | wc -l) files in the app)"
[ "${1:-}" = "--checar" ] && exit 0

MSG="${1:?usage: ota-or-build.sh \"message\" | --checar}"
[ -n "${EXPO_TOKEN:-}" ] || { echo "ERROR: EXPO_TOKEN is not in the environment (source your secrets file)"; exit 1; }
SHA=$(git rev-parse --short HEAD)

cd "$APP_DIR"
rm -rf dist
npx expo export -p "$PLATAFORMA" --output-dir dist >/dev/null || { echo "ERROR: export failed"; exit 1; }
if [ -n "$CONFERIR_NO_PACOTE" ]; then
  grep -rqa -- "$CONFERIR_NO_PACOTE" dist || { echo "ERROR: '$CONFERIR_NO_PACOTE' missing from bundle (wrong environment?)"; exit 1; }
  echo "Bundle checked"
fi
npx eas-cli update --branch "$CANAL" --platform "$PLATAFORMA" --skip-bundler --input-dir dist \
  --message "$MSG ($SHA)" --non-interactive 2>&1 | grep -vi token
