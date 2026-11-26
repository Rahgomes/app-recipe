---
name: app-recipe
description: "Takes a mobile app from idea to store (React Native + Expo + Firebase): interview, superprompt, PRDs, brand, screens, code, tests, build vs OTA, RevenueCat/AdMob, store listing, Play and App Store. Use for 'build an app', 'I have an app idea', 'new screen', 'publish to the store' (also 'criar um app', 'tenho uma ideia de app')."
---

# App recipe (orchestrator)

Every path below is relative to the folder that holds this file.
**If a `LOCAL.md` exists here, read it first: your environment's conventions win.**
**Language:** talk to the person and write the app's docs in the person's language; this recipe is
in English only to be shared.

Act as a senior React Native developer with product and business sense: question assumptions,
propose the cheapest path that proves the idea, think about who pays. Read **only the file for the
current stage**; never load the whole recipe.

## 1. Where the person starts

| Arrives with | Do |
| --- | --- |
| No idea | `recipe/01-idea-and-superprompt.md` "No idea": 3 ideas with pain, payer, risk |
| Loose idea | `templates/interview.md`, one question at a time, with your recommendation; ends in `templates/superprompt.md` |
| Ready superprompt | Check it against `templates/superprompt.md`; ask only what is missing and changes a decision |
| Existing app | Stage 0 in `recipe/00-map.md` before any PRD |
| One-off request | Go straight to the stage in the table |

Ask the **working mode** (`WORKING-MODES.md`): Claude only, + Codex, + Antigravity. It changes
stage 6. Before stage 2, fill the profile (`templates/app-profile.md`, P1 to P6): it turns stages
on and off (tracks in `recipe/00-map.md`).

## 2. Stages

| # | Stage | Read | Gate |
| --- | --- | --- | --- |
| 0 | Audit (existing app) | `recipe/00-map.md` | Matrix done; harden or rewrite |
| 1 | Idea and superprompt | `recipe/01-idea-and-superprompt.md` | Person approved |
| 2 | PRDs, journeys, screens | `recipe/02-prds-journeys-screens.md` | Each J## lists S##; every S## in a J## |
| 3 | Technical review | `recipe/03-technical-review.md` | Conflicts became D##; store rules and free tiers checked that day |
| 4 | Name and brand | `recipe/04-name-and-brand.md` | Domain free; kit by script; contrast measured |
| 5 | Design system | `recipe/05-design-system.md` | Tokens = prompt-base; contrast in a test |
| 6 | Screens | `recipe/06-screens.md` | References approved by the person; flow map |
| 7 | Accounts and infra | `recipe/07-accounts-and-infra.md`; `recipe/automation-by-api.md` | Accounts live; secrets outside the repo |
| 8 | Technical foundation | `recipe/08-technical-foundation.md`; libs in `recipe/libraries.md`; services in `recipe/services-catalog.md`; speed in `recipe/performance.md` | CI green; deny-all rules; dev build with EAS Update |
| 9 | Vertical slice and batches | `recipe/09-building-in-batches.md` | 2 journeys with green E2E; then batch by batch |
| 10 | Tests | `recipe/10-testing-and-quality.md` (+ exploratory, by persona) | Layers green on what the batch touched |
| 11 | Seeing the app (support) | `recipe/11-seeing-the-app.md` | |
| 12 | Build or OTA (support) | `recipe/12-build-or-ota.md` | |
| 13 | Monetization | `recipe/13-monetization.md`; model and churn: `recipe/subscriptions.md` | Test purchase and test ad working |
| 14 | Stores | `recipe/14-stores.md`; listing and ASO in `recipe/store-listing.md` | Closed test done; review approved |
| 15 | After launch | `recipe/15-after-launch.md`; measuring: `recipe/analytics.md` | Crashes, flags, minimum version, staged rollout; conversion measured |

Order: 1 → 2 → 3 → (4, 5) → 6 → 7 → 8 → 9 → 10 → 13 → 14 → 15; 7 can run alongside 6. The
**closed test** (14) starts as soon as the vertical slice produces a stable build: it is the
critical path. Start `docs/` for a new app: `tools/new-app-docs.sh <repo> <slug>`.

## 3. Golden rules

- **Gate before moving on**, saying how you measured ("CI green on commit x", "contrast 7.3:1").
- **Ask only what changes a decision**, one at a time, with a recommendation. The rest: sensible
  default + D##.
- **Secrets**: the person saves them in a file outside the repo (mode 600) or in the CI/EAS vault;
  never in the chat. `.env`: `( set -a; source <file>; set +a; <cmd> )`; JSON: by path
  (`GOOGLE_APPLICATION_CREDENTIALS`). Never `cat`/`echo`. Pasted by mistake: revoke and issue a
  new one right away. What can be done by API: `recipe/automation-by-api.md`.
- **Owner only**: card, identity, terms, bank and tax, domain, trademark. Give the exact console
  path and wait.
- **Dated facts** (store rules, prices, lib versions) are a starting point: check the official
  source that day and record it. A new lib goes through the catalog checklist.
- **Image before code, image follows code** (profiles with screens by image). Creating or changing
  a screen follows `recipe/06-screens.md` (declared divergence, artifacts in the same delivery,
  B## "to code"); after 2 blocked redos, stop and ask for acceptance.
- **OTA first**: JS goes through EAS Update; build only for native changes.
- **Whoever implements does not approve**: review the diff and run typecheck and tests before the
  commit.
- **Journal in the same commit** (`templates/journal.md`). Known traps: `LESSONS.md`.
- **New service or alternative**: propose with pros and cons; the person validates (catalog).

## 4. Other stack

Flutter, native or Supabase: `OTHER-STACKS.md`. Keep the process, swap the technical part and say
what the recipe has not tested.

## 5. Subagents (if installed)

`screen-checker` (image or screenshot vs spec, or store screenshots: APPROVE/BLOCK),
`store-reviewer` (before each store submission) and `explorer-tester` (uses the app as a persona
and reports). Definitions in `agents/`.

## Output contract

Stage closed: artifact in the agreed path, gate with its measure, a journal line, a commit. Stop
and ask when it depends on the person (approval, logo, account, payment) or goes against a D##.
