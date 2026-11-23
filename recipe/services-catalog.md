# Services catalog: defaults and alternatives

The recipe uses the **Default** column (tested in a real app). Alternatives are suggestions: the agent
presents pros and cons and **the person validates** before switching. Record the choice as D##.
Prices and free plans change: check the official page that day.

## By need

| Need | Default | Alternatives | When to switch |
| --- | --- | --- | --- |
| Framework | React Native + Expo | Flutter, native (see `OTHER-STACKS.md`) | Team already knows another stack; heavy system feature |
| Cloud build | EAS Build | Local build (`npx expo run:android`), GitHub Actions with Gradle, Codemagic | Many builds per month and EAS cost becomes significant |
| OTA updates | EAS Update | No mature equivalent for Expo | |
| Store submission | `eas submit` or Play API | Fastlane | Already using Fastlane |
| Backend | Firebase (Auth, Firestore, Functions, Storage) | Supabase (Postgres, RLS), custom API (Node + Postgres) | Needs SQL, heavy reporting, joins; accepts building offline support by hand |
| Device-only data | `expo-sqlite` | MMKV (fast key-value), WatermelonDB (sync), JSON file | Small volume: MMKV; custom sync: WatermelonDB |
| Login | Firebase Auth (email + Google; Apple on iOS) | Clerk, Supabase Auth | Backend is not Firebase |
| Subscription | RevenueCat | Adapty, Qonversion, Superwall (paywall), directly through stores | Fees become significant; paywall A/B tests (Adapty/Superwall) |
| Ads | AdMob (`react-native-google-mobile-ads`) | AppLovin MAX, Unity Ads (mediation) | Ad revenue is significant and you want mediation |
| Ad consent | Google UMP (comes with AdMob) | Certified third-party CMP | |
| Crashes | Crashlytics | Sentry (errors + performance + source map) | Wants performance tracing and server errors in one place |
| Product metrics | Firebase Analytics | PostHog, Amplitude, Mixpanel | Detailed funnels and retention; PostHog has a generous free plan |
| Push notifications | `expo-notifications` + FCM/APNs | OneSignal, Notifee (advanced local) | Campaigns and segmentation without code: OneSignal |
| Local notifications | `expo-notifications` | Notifee | Advanced Android channels and actions |
| Feature flags and config | Firebase Remote Config | PostHog flags, Statsig | Already using PostHog |
| Backend protection | App Check (Play Integrity / App Attest) | | Required with Firebase |
| Native E2E | Maestro (local and in CI) | Maestro Cloud, Detox | No machine with KVM: Maestro Cloud |
| Web E2E and accessibility | Playwright + axe | | |
| CI | GitHub Actions | EAS Workflows, Azure DevOps, GitLab CI | Code hosted elsewhere |
| Preview by link | EAS Hosting | Firebase Hosting (channel), Vercel, Netlify | Project already there |
| Testers outside the store | Play internal track | Firebase App Distribution, TestFlight (iOS) | Tester without a Google account on the list |
| Site and legal pages | Statically exported Next on Firebase Hosting | Astro, Framer, Carrd | No developer: Framer or Carrd |
| Transactional email | Function with Brevo, Resend or SendGrid | Firebase "Trigger Email" extension | On the day sending starts: SPF, DKIM and DMARC on the sender domain (rule in rah-ecosystem), otherwise it goes to spam |
| Dependency updates | Dependabot (patch only, weekly) | Renovate (groups by Expo SDK) | Large monorepo |
| Code security | gitleaks + osv-scanner in CI | Snyk, Socket | |
| Store review | `expo-store-review` | | Ask after a success, never on first use |
| Mandatory update | Remote Config with minimum version | Android in-app updates | |
| Icons | Expo library (`@expo/vector-icons`) or custom SVG | Lucide | |

## MCP servers (the agent operates the service directly)

Several recipe services have official or community MCP servers that let the agent query
and configure without you copying anything. Check availability and permissions that day, and prefer
official ones:

| Service | What it enables |
| --- | --- |
| Firebase (`firebase mcp`, included in firebase-tools) | Projects, rules, Firestore, Auth, logs |
| Expo (Expo MCP server) | Builds, updates, SDK documentation |
| RevenueCat | Products, entitlements, offerings |
| GitHub | PRs, Actions, issues |
| Context7 | Current library documentation |

MCP with write credentials has real power: use a service account with minimum roles and a dev
environment first.
