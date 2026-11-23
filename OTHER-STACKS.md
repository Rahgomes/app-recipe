# Other stacks: what to reuse

The recipe was tested with React Native + Expo + Firebase. If you take another path, almost all
of the **process** still applies; the technical part needs new research. Ask the agent to follow
the stages and mark anything specific to your stack as "not tested by the recipe".

## What applies to any stack

| Stage | Applies? |
| --- | --- |
| 1 to 3: idea, superprompt, PRDs with IDs, technical review | Yes |
| 4 and 5: brand through code, design system by role, contrast | Yes |
| 6: screens from images, inventory, contact sheet, flow map | Yes (the base prompt replaces "Material 3/HIG" if the visual style is custom) |
| 7: store accounts, secrets outside the repo, two environments | Yes |
| 9 and 10: vertical slice, batches, cross-review, three test layers | Yes, with other tools |
| 13: store subscriptions, RevenueCat, AdMob | Yes: both SDKs exist for Flutter and native |
| 14 and 15: stores, Data Safety, legal text vs code, safety net | Yes |

## Flutter

| Recipe piece | Equivalent |
| --- | --- |
| Expo Router | go_router |
| zustand | Riverpod or Bloc |
| zod | freezed + json_serializable, or manual validation |
| React Native Firebase | FlutterFire (same services) |
| EAS Build | Codemagic, GitHub Actions with Flutter, or local build (iOS needs a Mac or cloud service) |
| **EAS Update (over the air)** | Shorebird (code push for Flutter). Without it, every adjustment is a new store release |
| Jest + Testing Library | flutter_test (widget) + integration_test |
| Maestro | Maestro works the same way (it operates on top of the app) |
| Web preview | Flutter web, with limitations similar to RN web |

## Native (Kotlin / Swift)

Two codebases, two teams or twice the time. Makes sense when the app depends heavily on system
features (widget, watch, AR, professional audio). OTA updates do not exist for native code:
everything goes through the store. Firebase, RevenueCat and AdMob have official native SDKs.

## Supabase or your own API instead of Firebase

| Change | How |
| --- | --- |
| Offline | Not built in as it is with Firestore. Use a local database (SQLite, WatermelonDB, PowerSync) with a sync queue: this is the work the recipe avoided |
| Rules | Row Level Security in Postgres; test with a local database (Docker) |
| Functions | Edge Functions or your API; same rule: the server decides business logic |
| Benefit | SQL, reports, joins, versioned migrations |

## No backend (P3 = local)

The timer case: SQLite on the device (also runs on the web), backup through an exported file,
compatibility with the old format proven by a test. No account, no Firebase Emulator, no rules.
Cheaper and simpler; the cost is no synchronization between devices.
