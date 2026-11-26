#!/usr/bin/env bash
# Creates the app recipe docs/ tree with template files. Does not overwrite anything that exists.
# Usage: new-app-docs.sh <repo-root> <slug>     slug: lowercase letters, digits and hyphens (e.g.: my-app)
set -euo pipefail
[ $# -eq 2 ] || { sed -n '2,3p' "$0" | sed 's/^# //'; exit 2; }
slug=$2
[[ $slug =~ ^[a-z0-9][a-z0-9-]{0,40}$ ]] || { echo "invalid slug: '$slug'" >&2; exit 2; }
case $1 in *..*) echo "root containing '..' rejected: $1" >&2; exit 2;; esac
mkdir -p -- "$1"; R=$(readlink -f -- "$1"); today=$(date +%F)
mkdir -p "$R"/docs/{prd,brand,design,screens/android,screens/ios,images/{reference,android,ios,archived},flows,recipe,analytics}
create_file() { [ -e "$R/$1" ] && { echo "exists: $1"; return; }; cat >"$R/$1"; echo "created: $1"; }

create_file "docs/prd/00 - Start here.md" <<M
# $slug: start here

PRD reading order. IDs: J## journey, S## screen (state variant with suffix: S07o
offline), D## decision, B## backlog. Superprompt in 00-superprompt.md.
M
create_file docs/decisions.md <<M
# Technical decisions

Append only. A change of mind becomes a new D## stating which one it replaces.

| ID | Date | Decision | Why | Rejected alternative | Review when |
| --- | --- | --- | --- | --- | --- |
| D01 | $today | MVP platforms: (to decide) | | | |
M
create_file docs/backlog.md <<M
# Product backlog

Status: idea, planned, to code, in batch, live, discarded (with reason).

| ID | Idea | Source | Phase | Status | Screens | PRD |
| --- | --- | --- | --- | --- | --- | --- |
M
create_file docs/accounts-and-access.md <<M
# Accounts and access

Never secret values here: only the variable name and where it is stored (outside the repository).

| When | Account / resource | You create | Store in | The agent configures later | Status |
| --- | --- | --- | --- | --- | --- |
M
create_file docs/design/prompt-base.md <<M
# Visual base prompt for $slug

## Base block

\`\`\`text
Mobile app screen, 390x844, plain light background, no frame, no blur, no glow,
no vignette, no torn edges, no surrounding device.
Product: $slug, ...
Visual language: ...
Colors by role: primary ..., background ..., surface ..., text ..., success ..., warning ..., danger ...
Typography: ... Touch target >= 48. Status = text + icon + color, never color alone.
Fictional data in the app's language. No logo unless the screen calls for it.
Never: ...
\`\`\`
M
create_file docs/design/DESIGN-SYSTEM.md <<M
# Design system for $slug

Tokens in src/theme/tokens.ts (the same values as the base prompt).

| Role | Light | Dark | Measured contrast |
| --- | --- | --- | --- |

## Base components

## Status vocabulary
M
create_file docs/analytics/event-plan.md <<M
# Event plan for $slug

Template and rules: the app recipe's templates/event-plan.md and recipe/analytics.md.

## Definitions

| Term | For this app |
| --- | --- |
| Active user | |
| Activation | |
| Core action | |
| Churn | |
| Consent | |

## Events

| Event | Fires when | Parameters | Journey / screen | Question it answers |
| --- | --- | --- | --- | --- |
M
create_file docs/recipe/JOURNAL.md <<M
# Journal for $slug

## Infrastructure setup

| # | Step | Who | How (command or console path) | Trap |
| --- | --- | --- | --- | --- |

## Journal

Format: \`date · stage · ✅ / ❌ / 🔁 / ⚠️ · what | why\`. A lesson starts with "Lesson:".

- $today · 0 · ✅ · docs/ structure created by the app recipe | starting point.
M
