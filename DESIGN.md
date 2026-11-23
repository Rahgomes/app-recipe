# PRD: App recipe kit

Version 1.0 · November 2026

## 1. Problem

Someone with an app idea and access to AI agents can generate code quickly, but usually gets
stuck in four places:

1. **An unformed idea.** The agent receives "I want a scheduling app" and invents the rest. The
   result looks finished and solves no one's problem.
2. **Code before decisions.** Without a PRD, journeys and screens with IDs, each conversation
   decides the product again; the app becomes a patchwork of screens.
3. **Everything beyond code.** Accounts (Firebase, Expo, Play, Apple, RevenueCat, AdMob), store
   rules, the 14-day closed test, Data Safety, Apple's tax agreement. This is where launches
   slip by weeks.
4. **After the first build.** Every adjustment becomes a new APK, no one knows whether the fix
   reached the phone, and there is no way to switch off a serious bug.

## 2. Goal

A package someone receives, installs as a skill and uses to take an idea to the store, with the
agent guiding and the person deciding. Goals:

| Goal | Measure |
| --- | --- |
| Start from any point | Entry with no idea, a loose idea, a superprompt or an existing app |
| Work with what the person has | Three modes: Claude only; Claude + Codex; Claude + Codex + Antigravity |
| Clear gate at each stage | Every stage has a measurable "done when" |
| Avoid repeating our mistakes | Lessons from the journals of three apps, by topic, consulted at the right stage |
| Safe to share | No keys, project IDs, accounts, servers or customer data |

Out of scope: teaching React Native from scratch, replacing the owner's decisions (price,
brand, accounts), guaranteeing store approval.

## 3. Audience

| Persona | Has | Needs |
| --- | --- | --- |
| Entrepreneur who does not code | Idea, card, one agent | Guidance, clarity on what only they can do, understanding of costs |
| Web developer moving to mobile | React experience, one or two agents | Native pitfalls, stores, build vs OTA |
| Mobile developer | Everything | A process with gates, agent orchestration, store checklist |

## 4. Principles (where they came from)

| Principle | Origin in the journal |
| --- | --- |
| IDs from the first PRD (J## journey, S## screen, D## decision, B## backlog) | Became image, test and route names in case A |
| Technical review of the PRD against reality before code | Case A's PRD assumed a Mac, Functions on the free plan and ignored the 14-day closed test |
| Image before code, image follows code | Comparing a screenshot with the image caught what component tests cannot see |
| Vertical slice before breadth | 2 end-to-end journeys found integration defects early |
| OTA first | Case C used 11 builds before adding EAS Update |
| One agent implements, another reviews | Cross-review found real backend concurrency bugs |
| Closed test in parallel | Play's 14 days are the launch's critical path |

## 5. Functional scope

### 5.1 Entry and idea development
- Interview script with one question at a time and an agent recommendation for each.
- "No idea" mode: 3 suggestions based on the person's context, with pain, payer and risk.
- Superprompt template with required and optional fields (brand, colors, typography and stack
  are optional at this point).

### 5.2 App profile (tracks)
Six questions (existing app?, billing, server, screens, validation, platforms) that turn stages
on and off. Avoids running the whole recipe for an offline timer without an account.

### 5.3 Recipe in 16 stages (00 to 15)
Each has: goal, who does it (person vs agent), steps, artifact, gate, pitfalls and linked
lessons. Support stages (seeing the app, build or OTA) are consulted repeatedly.

### 5.4 Working modes
Role split by agent combination, how to produce screens without an image generator and how to
write a briefing that costs another agent less to execute.

### 5.5 Templates
Superprompt, interview, profile, PRD, decisions and backlog, screen spec, accounts and access,
briefing, journal.

### 5.6 Tools
- `contrast.py`: WCAG contrast ratio between color pairs.
- `ota-or-build.sh`: compares changes since the last build and says whether they can go OTA.
- `check-secrets.sh`: scans the kit (or your project) before sharing.
- `new-app-docs.sh`: creates the app's `docs/` folder with the templates.
- The repo is the source for sharing; local notes live in an untracked `LOCAL.md`.

## 6. Kit architecture: skill + subagents

| Piece | Role | Why this format |
| --- | --- | --- |
| **Skill** `SKILL.md` (the entire folder) | Orchestrates: identifies the starting point, profile and stage; loads only the current stage's file | The process is a conversation with the person (interview, approval). A skill runs in the main context, where the conversation happens. Claude Code and Codex read the `SKILL.md` format |
| **Subagent** `screen-checker` | Compares an app screenshot with the reference image and returns APPROVE/BLOCK | Bounded task, clear input and output, uses context for images: better isolated |
| **Subagent** `store-reviewer` | Before store submission: package permissions, Data Safety vs SDKs, legal text vs code, listing | Long, mechanical checklist without conversation: ideal for a separate context |
| Recipe files | Knowledge by stage | Loaded on demand: the agent does not read 16 files at once. `SKILL.md` under 6,000 characters and description under 350, to fit any agent's skill index |
| `LOCAL.md` (optional, personal) | Conventions of the user's environment | The recipe stays generic and the same for everyone; your details (vault, tools, agents) live in a single file that takes precedence and is not shared |

Why not an agent that "does everything": the interview and approvals need the person involved,
and a subagent cannot talk to them. Why not just documents: without the skill, the person needs
to know which file to open at each point.

## 7. Reference stack

React Native with Expo (current stable SDK, New Architecture), Expo Router, strict TypeScript,
Firebase (Auth, Firestore with offline cache, 2nd-gen Functions, Storage, App Check, Remote
Config, Crashlytics), EAS Build and EAS Update, RevenueCat for subscriptions, AdMob for ads,
Jest + Testing Library, Maestro (native E2E) and Playwright (web E2E), GitHub Actions.
Details and alternatives in `recipe/08-technical-foundation.md` and `OTHER-STACKS.md`.

## 8. Risks

| Risk | Mitigation |
| --- | --- |
| Outdated store rule or price | Every fact has a date; the skill requires checking the official page that day |
| Outdated library version | The recipe does not pin versions; uses `npx expo install` and an adoption checklist |
| Person pastes a secret in chat | Explicit rule in the skill; instructions to revoke immediately |
| Agent skips a gate to "move fast" | Output contract per stage; journal requires stating how it was measured |
| Kit leaks data from the source apps | Written generically; `check-secrets.sh` before each share |

## 9. Kit roadmap

| Version | Content |
| --- | --- |
| 1.0 | This version: recipe, templates, modes, lessons, skill and 2 subagents |
| 1.1 | Starter project (Expo + Firebase monorepo with CI, deny-all rules, basic UI kit) to clone |
| 1.2 | iOS track written from an app published on the App Store (currently partly based on documentation) |
| 1.3 | Flutter guide tested on a real app, if the case comes up |

## 10. How to measure whether it works

- Someone outside the team reaches the first development build running on their phone by
  following the kit, without asking for help outside the agent.
- None of the pitfalls in `LESSONS.md` recur in the new app (its journal shows this).
- Time from idea to open closed test: our cases provide a reference of about 10 working days
  with two agents in parallel.
