# 14. Stores: Google Play and App Store

Store rules change. The facts below apply to November 2026: check the official page that day and
record the decision.

## Google Play: tracks

| Track | Purpose | Review |
| --- | --- | --- |
| **Internal test** | Up to 100 people, you and the team; arrives in minutes | Minimal |
| **Closed test** | Tester list; required before production for a new personal account | Yes |
| Open test | Anyone can join through the store | Yes |
| **Production** | Everyone, with staged rollout | Yes |

## Android distribution gate (in order)

1. **Production build** pointing to the production environment (check the project and package in
   the public config and on first boot). Play-managed signing; the Play key's SHA-256
   goes into Google login and `assetlinks.json`.
2. **targetSdk** at the minimum required by Play (check the final manifest).
3. **Test the release binary**, not just dev: R8 (code shrinking) can break only the
   release.
4. **Package permissions**: list the AAB manifest before the first submission. A gallery library
   brought photo and video permissions that Play rejected; the library was removed and `android.blockedPermissions`
   removes permissions brought by libraries that the app does not use.
5. **Listing and compliance before the closed test**: text, 512 icon, feature graphic, screenshots of the
   real app with fictional data (keywords, screenshots that convert and what stores reject:
   `recipe/store-listing.md`), published privacy policy, terms,
   **account deletion web link**, Data Safety, content rating, "Contains ads".
6. **Submission**: `eas submit -p android` or Play API with a service account. An unpublished app
   is a "draft": the API only accepts the version as a draft, and submission for review happens in the Console.
7. **Closed test** (personal account): **12 testers opted in continuously for 14 days**.
   Recruit 15 or more for a buffer. Start **as soon as the vertical slice produces a stable build**,
   alongside batches: it is the launch's critical path.
8. **Request production access** in the Console (questionnaire about the test; allow days for evaluation).
9. **Staged rollout**: 5% → 20% → 50% → 100%, checking Crashlytics at each step.

## Data Safety: collection inventory

The manifest is not enough: the declaration covers what each SDK and the backend collect.

| Source | Typical collection |
| --- | --- |
| Auth | Email, name, ID, provider |
| Database and Storage | Everything the app saves, including third-party data (your user's customers) |
| Crashlytics/Sentry | Crash logs, diagnostics, installation ID |
| Analytics | App interactions, device or other IDs; purpose Analytics (`recipe/analytics.md`) |
| RevenueCat / Billing | Purchase history, user ID |
| App Check / Play Integrity | Device attestation |
| AdMob | See the SDK's own data disclosure page |

Build the Play and Apple tables from each SDK's official disclosure plus what the
code does. New SDK = updated table in the same commit.

## Legal text matches the code

Before publishing, check **every sentence** of the terms and privacy policy with `grep` in the app and
server. We found 3 false promises ("end all sessions" did not exist; retention period
not honored; ads described as "free tier only" without the rule in code) and 3 gaps (data the app
collected but the text did not mention). Terms and privacy policy: drafts for legal review.

## Store text is code

Listing text in a file with tests: each field's limit (Apple keywords count
**bytes**, "ô" takes 2), numbers checked against the domain, button names against translations.
It caught a keyword repeating the name (wasted bytes).

## App Store (iOS)

- **Apple Developer** account (annual), created by you.
- EAS build with **managed credentials** (certificate and provisioning through EAS, no Mac);
  `eas submit -p ios` with the App Store Connect API key stored outside the repo.
- **TestFlight** for internal and external testing; then App Store review.
- Google login also requires **Sign in with Apple** (guideline 4.8).
- **Account deletion inside the app** (5.1.1(v)), not just a web link.
- Privacy manifest and "App Privacy" with the same inventory as Data Safety.
- Paid apps agreement active before any purchase (stage 13).
- iOS screens exist from stage 6 if you generated both platforms; the code is the same.

## Minimum site (almost required)

Privacy policy, terms, account deletion (with login), contact and a sales page.
Your own domain builds more trust during review. A static site (exported Next, Astro) on Firebase
Hosting or similar is enough.
