# 00. Recipe map

## The stages

| # | Stage | Type | Who | Output | Done when |
| --- | --- | --- | --- | --- | --- |
| 0 | Codebase audit | existing app only | Agent | `docs/audit.md` | Matrix done; decision to harden or rewrite |
| 1 | Idea and superprompt | essential | You + agent | `docs/prd/00-superprompt.md` | You approved the superprompt |
| 2 | PRDs, journeys and screens with IDs | essential | Agent (you review) | `docs/prd/` | Journeys J## with screens S## |
| 3 | Technical review | essential | Agent | `docs/decisions.md` (D##), `docs/backlog.md` (B##) | No open conflicts |
| 4 | Name and brand | essential | You decide, agent produces | `docs/brand/` | Domain available, icon kit, contrast measured |
| 5 | Lightweight design system | essential | Agent | `docs/design/`, `src/theme/tokens.ts` | Tokens + components + base prompt match |
| 6 | Screens | essential | Agent (you approve references) | `docs/screens/`, `docs/images/` | References approved; flow map |
| 7 | Accounts and infrastructure | essential | You create, agent configures | `docs/accounts-and-access.md` | Accounts live; secrets outside the repo |
| 8 | Technical foundation | essential | Agent | Code | CI green; first dev build with EAS Update |
| 9 | Vertical slice and batches | essential | Agents | Code + tests | 2 journeys with green E2E; then batch by batch |
| 10 | Tests and quality | essential | Agents | Tests + CI | Three layers green on what the batch touched |
| 11 | Seeing the app | support | You | | |
| 12 | Build or OTA | support | Agent | | |
| 13 | Monetization | based on profile | You + agent | Subscription and/or ad | Test purchase and test ad working |
| 14 | Stores | essential | You + agent | Published app | Review approved |
| 15 | After launch | essential | Agent | Safety net | Crashes, flags, minimum version, staged rollout |

Order: 1 → 2 → 3 → (4, 5) → 6 → 7 → 8 → 9 → 10 → 13 → 14 → 15.
Stage 7 can start alongside 6. The **closed test** in stage 14 starts as soon as the vertical
slice produces a stable build, in parallel with batches.

## App profile (tracks)

Answer in `templates/app-profile.md` before stage 2.

| # | Question | Answers | Changes |
| --- | --- | --- | --- |
| P1 | Does the app already exist? | New · Existing | 0, 1, 4, 5, 6, 8 |
| P2 | Is there billing? | None · Ads · Subscription · Both | 3, 13, 14 |
| P3 | Does it need a server? | Local (data on device) · Cloud (account, sync) · Both | 3, 7, 8, 9 |
| P4 | How are screens created? | AI-generated · External reference (screenshots, Figma) · Straight to code | 6 |
| P5 | Where do you validate? | Device only (Expo, APK) · Store (closed test) · User pilot | 14 |
| P6 | Platforms | Android · iOS · Both | 7, 13, 14 |

### What each answer changes

| Stage | New | Existing | Variations |
| --- | --- | --- | --- |
| 0 | skip | essential | See below |
| 1 | essential | refine | Existing: the superprompt describes the evolution, not the whole app |
| 3 | essential | essential | Local: focus on data model, migration and clock. No billing: skip store payment rules |
| 4 | essential | check | Existing: contrast and icon only; do not redesign without a reason |
| 5 | essential | extract | Existing: tokens come from the current theme |
| 6 | essential | refine | P4 defines the path (generated, reference, code) |
| 8 | essential | harden or rewrite | Local: no Firebase Emulator; SQLite or device storage |
| 13 | based on P2 | based on P2 | None: skip. Ads: AdMob + consent. Subscription: RevenueCat |
| 14 | essential | essential | No billing: listing, privacy and legal pages only. iOS: Apple account and TestFlight |

## Stage 0: audit (existing app)

1. Run the app (web or device) and capture each screen as it is (`docs/images/current/`).
   On the web this can be automated: `npx expo export --platform web`, serve the folder on a free
   port (check that the port really belongs to your app) and capture with Playwright at 390×844.
2. Build the matrix: **feature × appears in UI × actually implemented × persistence × tests ×
   gap**. Classify: complete, partial, UI only.
3. For each UI setting, **trace where the code reads it**. Typical finding in a tool-generated
   app: a settings button that changes nothing (sound that vibrates, ignored vibration,
   "silent mode" that detects nothing).
4. Check SDK age, existing tests, dependencies with vulnerabilities.
5. Decide with the person:
   - **Harden**: the stack is sound; add tests, CI, lint without changing the foundation.
   - **Rewrite**: SDK far behind, zero tests, UI that promises what it does not do. New project
     on the recipe's foundation; old code in a `legacy/` folder until ported.
6. Old data: if the app saves anything on the device, the new app must read the old format.
   Strong proof: open a `git worktree` at the old commit, generate the real file and test reading it.

## App document structure

`tools/new-app-docs.sh <repo> <slug>` creates this tree with the templates (does not overwrite):

```
docs/
  prd/                    00-superprompt.md, "00 - Start here", numbered PRDs
  decisions.md            D## (technical decision with rationale; append only)
  backlog.md              B## (idea with phase and status)
  accounts-and-access.md  who creates what, where it is stored (no value), what the agent does next
  brand/                  concepts, final kit, generating script
  design/                 prompt-base.md, DESIGN-SYSTEM.md, references.md
  screens/                inventory (single source) and specs per platform
  images/                 reference/, android/, ios/, archived/
  flows/                  navigable journey map
  recipe/JOURNAL.md       journal and infrastructure steps for this app
```
