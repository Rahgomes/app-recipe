# Libraries and how to call services

Versions change: install with `npx expo install <package>` (chooses the SDK-compatible version), and do not copy
version numbers from documents.

## Reference libraries

| Library | Purpose | MVP |
| --- | --- | --- |
| `expo-router` | File-based routes, deep links, auth groups | Required |
| `@react-native-firebase/{app,auth,firestore,functions,storage,app-check}` (modular API) | Backend | If Firebase |
| `@react-native-firebase/crashlytics` (or `@sentry/react-native`) | Crashes without personal data | Required |
| `@react-native-firebase/remote-config` | Switches and minimum version | Required before launch |
| `expo-updates` | OTA updates | Required from the 1st build |
| `zod` | Single schema: form, Function, document, route params | Required |
| `react-hook-form` + `@hookform/resolvers` | Forms without re-rendering on each keystroke | Required |
| `zustand` | UI state and local session | Required |
| `@tanstack/react-query` | Only HTTP that is not Firestore | Optional |
| `expo-secure-store` | Small secrets on the device | Required |
| `expo-crypto` | UUID and randomness (never `Math.random` for IDs) | Required |
| `react-native-reanimated` + `react-native-gesture-handler` | Animation and gestures | Required |
| `react-native-safe-area-context` | Safe areas (edge-to-edge) | Required |
| `expo-build-properties` | targetSdk, R8, `allowBackup` | Required |
| `expo-application` | Actual version and build for the About screen | Required |
| `expo-notifications` | Local reminders and push | Depends on app |
| `react-native-purchases` (RevenueCat) | Subscription | If paid |
| `react-native-google-mobile-ads` | AdMob banner + UMP | If ads |
| `@react-native-google-signin/google-signin` | Native Google login | If Google |
| `expo-apple-authentication` | Sign in with Apple | If iOS with social login |
| `expo-screen-capture` | Block screenshots containing third-party data | If present |
| `jest-expo` + `@testing-library/react-native` | Unit and component tests | Required |
| `@firebase/rules-unit-testing` + Emulator | Rules and Functions | If Firebase |
| ESLint (`eslint-config-expo` + typescript-eslint strict + security plugin), Prettier, knip | Quality | Required |

Excluded from the MVP for cost versus benefit: Detox (Maestro is simpler), Formik, Redux Toolkit,
SSL pinning, styled-components.

## Three ways to call services

| Source | How | Do not do |
| --- | --- | --- |
| **Firestore** | `onSnapshot` listener in a hook per feature; the offline cache is the UI cache (`hasPendingWrites`, `fromCache` give sync state). Writes go to the device first; rules enforce structure and authorization; a trigger decides business logic | Wrap Firestore in TanStack Query (two caches); loop over `get()` instead of a listener |
| **Callable Function** | Action the client cannot decide (payment, invitation, business rule). Same zod schema on both sides, App Check required, typed error becomes a message | Open HTTP Function for a callable operation; third-party secret in the app |
| **Third-party HTTP** | `fetch` + `schema.parse(await res.json())` + TanStack Query. APIs with secrets go through a Function | Trust a type without validation; private key in `EXPO_PUBLIC_*` (ships inside the app) |

## Before adopting a library

1. Security and maintenance: package page on Snyk or osv.dev (vulnerabilities by version,
   latest release, number of maintainers).
2. `npm view <package> version time.modified repository license scripts`.
3. New Architecture and current SDK support (reactnative.directory or README).
4. MIT, Apache-2.0 or BSD license. GPL or no license: the person's decision.
5. **Reject** if: high-severity vulnerability without a fix; native library without a release for over 12 months;
   suspicious `postinstall`.
6. pnpm blocks install scripts: allow only what is needed, after reading them.
7. After installing: `osv-scanner` on the lockfile; `npx expo-doctor` if it has native code (which
   requires a new build).
8. Record in the journal or D##: `library, version, check, date`.
