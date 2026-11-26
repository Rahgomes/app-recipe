# Measure: crashes, product analytics and acquisition

Measurement is planned in the PRD, wired in the foundation and read every week. Without a plan,
an app ends up with 60 random events, none answering "where do people give up?".

Facts on limits, thresholds and free tiers were checked on official pages in November 2026.
Check again before relying on them.

## Three layers, three questions

| Layer | Question | Default tool | When |
| --- | --- | --- | --- |
| Stability | Does the app crash or freeze on someone's phone? | Crashlytics + Android vitals + Xcode Organizer | From the 1st build |
| Product | Do people reach the first valuable action, and come back? | Google Analytics for Firebase | From the 1st build, events from the plan only |
| Acquisition | Where did the people who install come from? | Play Console and App Store Connect sources; campaign links | At launch; an attribution provider only with paid traffic |

Revenue has its own source of truth: the stores and RevenueCat (stage 13). Analytics revenue
events are directional; never compute LTV from client events.

## Where it fits in the recipe

| Stage | Measurement work |
| --- | --- |
| 2 PRDs | Each journey names its success event and its drop-off point; the event plan is born (`templates/event-plan.md`) |
| 3 Technical review | Consent model per country; which SDKs collect what (feeds Data Safety) |
| 8 Foundation | One typed `track()` module; collection off in dev; consent defaults; Crashlytics with account ID only |
| 10 Tests | Unit test on `track()` names; a pass in DebugView for the batch's events |
| 13 Monetization | Paywall and purchase events; revenue truth stays in RevenueCat |
| 14 Stores | Data Safety and App Privacy declare analytics and crash data; campaign links created |
| 15 After launch | Weekly review; experiments only with enough traffic |

## The event plan

Small and deliberate: one list per app in `docs/analytics/event-plan.md`, reviewed with the PRDs.
Most non-game apps need **12 to 20 events**; measuring what matters is not measuring everything.

**Every app has these** (rename to fit, keep the meaning):

| Event | When | Key parameters |
| --- | --- | --- |
| `first_open` | Automatic | |
| `sign_up` | Account created | `method` |
| `onboarding_complete` | Last onboarding step | `steps_skipped` |
| `activation` | **First valuable action** (defined per app: first habit saved, first report sent) | `journey` |
| `<core_action>` | The action that delivers the app's value, each time | `screen` |
| `paywall_view` | Paywall shown | `trigger`, `variant` |
| `trial_start`, `purchase` | Confirmed by the store or RevenueCat, not on button tap | `plan`, `period` |
| `share` / `invite` | Sharing or referral | `channel` |
| `error_shown` | A message the user saw | `code`, `screen` |
| `limit_reached` | Free plan limit hit | `limit` |

**Naming and limits** (Google Analytics for Firebase):
- `snake_case`, verb or noun + object, up to 40 characters; `firebase_`, `google_` and `ga_` are reserved.
- Up to 500 distinct event names per app, 25 parameters per event, parameter values up to 100
  characters; 25 user properties (name 24, value 36 characters). Automatic events do not count.
- Parameters carry IDs from the recipe: `screen` = `S07`, `journey` = `J02`. Reports then
  match PRDs, tests and images.

**Never in an event or user property**: email, name, phone, free text typed by the user,
precise location, or anything that identifies a person. User ID = the random account ID.

**One door for events**: a `track()` module whose event names and parameters are a TypeScript
union generated from (or kept beside) the plan. Screens never call the SDK directly, so a typo
fails typecheck, and adding PostHog or Amplitude later is one file.

## Definitions to write down (per app, in the plan)

- **Active user**: what counts (opened the app, or did the core action).
- **Activation**: the first valuable action, and the time window (same day, first 3 days).
- **Retention Dn**: share of a day-0 install cohort that opens the app on day N. Read D1, D7, D30
  by cohort and by source, never as one blended number.
- **Stickiness**: DAU / MAU (2,000 / 8,000 = 25%).
- **Churn**: for subscriptions, cancellations; for free use, no core action for X days.
- **LTV**: roughly ARPU × gross margin / monthly churn. Directional until there are many months of
  data; before that, compare D7 and D30 cohorts. With paid traffic, LTV : CAC of about 3:1 is the
  usual comfort zone; below 2:1 the spend rarely pays back.

Compare the app with itself (before and after a batch, cohort against cohort). Vendor
"benchmarks" rarely show their method.

## Consent and privacy

- **Collection off until allowed** where consent is required (EEA, UK; LGPD and others: decide in
  stage 3 and record a D##). React Native Firebase: `analytics_auto_collection_enabled: false` in
  `firebase.json`, then `setAnalyticsCollectionEnabled(true)` after consent.
- **Consent Mode v2**: `setConsent` with `analytics_storage`, `ad_storage`, `ad_user_data`,
  `ad_personalization`. Google requires it to keep ads measurement and personalization for EEA
  users. Revoking clears user properties.
- **iOS**: tracking across other companies' apps needs App Tracking Transparency; without
  permission the advertising ID is zeros. React Native Firebase does not link `AdSupport` by
  default: keep it that way unless ads need it. Analytics inside your own apps works without ATT.
- **ATT prompt, if needed**: a screen explaining the benefit first, then the system prompt, never
  on first launch. Opt-in rate and ID collection rate are different numbers.
- **Declarations** (stage 14): Play Data Safety: App interactions (App activity), Crash logs and
  Diagnostics (App info and performance), Device or other IDs; purpose Analytics. Apple: App
  Privacy plus each SDK's privacy manifest. A processor acting only for you is not "sharing";
  an SDK that reuses data for third-party ads is.

## Checking events before release

- **DebugView**: Android `adb shell setprop debug.firebase.analytics.app <package>`; iOS launch
  argument `-FIRDebugEnabled`. Without debug mode, events arrive in batches of about an hour.
- Each batch: run the journeys it touched and confirm each planned event appears once, with
  the right parameters, and no event outside the plan.
- Debug traffic reaches the BigQuery export by default: filter it out.
- The `explorer-tester` and the E2E specs never run against the production project.

## Stability: crashes and vitals

| Source | What it shows | Note |
| --- | --- | --- |
| Crashlytics (free) | Native crashes, JS errors, ANRs, non-fatals, breadcrumbs, alerts | Account ID only; custom keys: version, OTA update ID, screen |
| Sentry (free developer tier) | JS errors with source maps, native crashes, tracing, mobile session replay | When readable JS stacks across OTA updates or performance traces matter; upload source maps on every build **and** every EAS Update |
| Android vitals (Play Console) | User-perceived crash rate and ANR rate, 28-day window | Over **1.09% crashes** or **0.47% ANRs** overall (or 8% on a single device model), Play can lower visibility and show a warning on the listing. Rates are per daily user, so they differ from Crashlytics |
| Pre-launch report (Play) | Crashes, accessibility and performance on real devices | Free, runs on each upload: read it before the closed test |
| Xcode Organizer / App Store Connect | iOS crashes, hangs, launch time | Only from users who share diagnostics |

Staged rollout (stage 14) moves to the next step only when crash-free users and vitals are not
worse than the previous version.

## Product analytics: Firebase first, another tool when it hurts

Google Analytics for Firebase is free, needs a dev build (not Expo Go), and connects to
Remote Config, A/B Testing, audiences for messaging and the raw-event BigQuery export. Start there.

Add a product analytics tool when GA4 funnels and retention reports stop answering questions,
or you need session replay. Free tiers checked in November 2026:

| Tool | Free tier | Expo |
| --- | --- | --- |
| PostHog | Generous; also self-hosted | `posthog-react-native` with Expo packages only; replay needs an extra plugin |
| Amplitude | 2M events/month, 10K replays | SDK for React Native |
| Mixpanel | 1M events/month, 10K replays, funnels and retention | SDK for React Native |

Fan out from the same `track()`; do not instrument screens twice.

## Experiments

- **In the app**: Firebase A/B Testing on Remote Config parameters (paywall copy, onboarding
  length, trial length), with retention, revenue or a planned event as the goal metric.
- **On the listing**: Product Page Optimization and store listing experiments
  (`recipe/15-after-launch.md`).
- One hypothesis, a control, a decision written before starting, and enough users: with little
  traffic the result is noise. A losing variant is also a result: record it as a D##.

## Acquisition and attribution

**Free, at launch:**
- Store consoles split installs by source (search, browse, referral, campaign).
- **Google Play**: add `utm_source`, `utm_medium`, `utm_campaign` to the `referrer` of the Play
  link. Firebase Analytics reads the Play install referrer for the first open.
- **App Store**: campaign links with a provider token (`pt`) and campaign token (`ct`), created in
  App Store Connect; results in App Analytics.
- One link per channel (site, social bio, newsletter, QR code on a flyer).

**Only with paid traffic on more than one network:**
- A mobile measurement partner (AppsFlyer, Adjust, Branch) deduplicates installs between networks.
  Attribution shows who was on the path, not what caused the install: before scaling a channel,
  run a holdout (pause it in one region and compare).
- iOS ad networks report through SKAdNetwork / AdAttributionKit: delayed, aggregated postbacks
  (three windows: days 0 to 2, 3 to 7, 8 to 35; fine conversion value only in the first).
  Map the few values to the events that predict revenue (activation, trial start).
- Fraud signals: install seconds after the click, or a day later in bulk; good-looking conversion
  with zero retention. Validate purchases on the server (stage 13).
- Optimize spend by cohort revenue and retention, not by cost per install.

## Deep links

- Firebase Dynamic Links is shut down: use **Android App Links** (`assetlinks.json`) and **iOS
  Universal Links** (`apple-app-site-association`) on the app's domain; Expo Router maps the path
  to the screen.
- Every link that opens the app carries its campaign parameters through to `track()`.
- Deferred deep link (opening the right screen after installing) needs a provider, or on Android
  the install referrer. Only build it when invites or campaigns depend on it.

## Uninstalls and re-engagement

- Play Console shows uninstalls by day; on Android, Firebase logs `app_remove`. Read them by
  cohort and source: a source with many uninstalls is a bad source, even with cheap installs.
- Push: segmented by event ("started but never finished J02"), few and useful. Generic
  blasts bring uninstalls and lost notification permission.
- People who uninstalled can get a custom store listing on Play (`recipe/15-after-launch.md`).

## Launch vs paid traffic

| At launch | When paid traffic starts |
| --- | --- |
| Event plan, typed `track()`, consent, DebugView pass | Attribution provider with deduplication |
| Crashlytics, vitals and pre-launch report reviewed | SKAdNetwork / AdAttributionKit value map |
| Retention D1/D7/D30 by cohort; activation rate | ATT pre-prompt and opt-in test (if ads need it) |
| Campaign links per channel; App Links and Universal Links | Holdout test before scaling; fraud checks |
| Data Safety and App Privacy matching the SDKs | LTV by cohort guiding spend |
