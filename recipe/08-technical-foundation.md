# 08. Technical foundation

**Goal:** a skeleton that is tested, secure and ready for OTA updates from the start. **Gate:** CI green;
deny-all rules with tests; first development build running on a phone, already with
EAS Update.

## Reference stack (Nov/2026; check versions that day)

| Part | Choice | Note |
| --- | --- | --- |
| Base | Current stable Expo SDK, React Native with New Architecture | Expo Go stops being useful when a native module is added: use a development build |
| Routes | Expo Router | Stack on the outside, tabs in a `(tabs)` group. A hidden route inside Tabs failed to navigate on the web |
| Language | TypeScript `strict` | |
| Monorepo | pnpm: `apps/mobile`, `functions`, `packages/shared`, `apps/site` (optional) | Pure business logic in `shared`, used by the app and server |
| Cloud backend | Firebase: Auth, Firestore, 2nd-gen Functions, Storage, App Check | React Native Firebase modular API |
| Local backend | `expo-sqlite` (also runs on the web, wasm) or a file | For P3 = local |
| Validation | zod, the same schema in the form, Function and document | |
| Forms | react-hook-form | |
| UI state | zustand | Firestore already caches the data: do not wrap it in TanStack Query |
| Animation | Reanimated + Gesture Handler | Respect "reduce motion" |
| Errors | Crashlytics (or Sentry) from the 1st build | Account ID only, never personal data |
| Analytics | Google Analytics for Firebase behind one typed `track()` | Events from the plan only; off in dev; consent defaults (`recipe/analytics.md`) |
| Updates | `expo-updates` (EAS Update) **in the first build** | See stage 12 |
| Tests | jest-expo + Testing Library; Firebase Emulator; Maestro (native) and Playwright (web) | Stage 10 |
| Quality | ESLint (typescript-eslint strict, security plugin), Prettier, knip (dead code), gitleaks, osv-scanner | `no-floating-promises` is critical with Firestore |
| CI | GitHub Actions | A Linux runner with KVM runs an Android emulator for E2E |

## Skeleton setup order

1. Monorepo, Expo app with TS strict, Expo Router, token-based theme and contrast test.
2. Lint, Prettier, knip, tests; lightweight pre-commit.
3. Firestore and Storage **deny-all** rules, with Emulator tests.
4. Single Firebase initialization, switching to the Emulator in development.
5. Route gate by account stage (signed out, registration incomplete, ready).
6. CI: quality (lint, tsc, tests, knip), rules (Emulator), security (gitleaks, osv-scanner),
   web preview (publishes the web version with fictional data after all three pass).
7. EAS project, `.easignore`, **`expo-updates` configured**, development build.

## Code patterns that paid off

- **A port for every native module**: camera, notifications, files, ads and purchases sit behind
  an interface (`AdsPort`, `CuePort`...). Native adapter in a `.native.tsx` file, web
  or empty version in `.tsx`, and a fake in tests. Web previews and tests keep working without
  scattered `if (Platform)` checks.
- **Injected clock**: nothing in the domain reads `Date.now`; pass `now` as a parameter. Time tests
  become cheap and deterministic.
- **Write first, validate later** (cloud): the app writes to the offline cache; rules enforce structure and
  authorization; a server trigger decides the business rule (pending becomes confirmed or
  conflict). Pending data never appears as confirmed.
- **A webhook is not the truth**: the server fetches state from the source and saves the event version
  to avoid going back in time.
- **Public route** (the app's web page): every submission counts toward the limit, uploads are create-only,
  business logic stays on the server, and an overall hourly cap does not depend on IP (IPs can be spoofed).
- **Screen tests belong in `src/test`**, never in `app/`: Expo Router turned tests
  into Android routes and broke the build (the web hid the error).
- `.gitignore` with a path (`/functions/lib/`), never bare `lib/`: it ignored site code.
- A constant called `KEY` or `TOKEN` with a dot in its text triggers a gitleaks false positive: use names
  such as `STORAGE_ENTRY`.

## Before adopting a library

Checklist and library table in `recipe/libraries.md`. The two most costly lessons there:
in RN, the lockfile mixes app and tooling (`pnpm why` before "fixing" a vulnerability), and
`npx expo-doctor` **after every new native library** (it found a missing dependency that would crash the app on startup).

## Build traps

- Do not override `compileSdk`/`targetSdk` without checking the Expo SDK default: forcing a lower
  version broke Gradle.
- A library with heavy C++ (Skia) exhausted memory in a cloud build: test builds use only `arm64`.
- Before requesting a build, local `npx expo export -p android` catches bundling errors in
  seconds.
- `npx expo config --type introspect --json` shows the final manifest and Info.plist without compiling.
- Failed build log: download it and search for "went wrong" or "requires".
