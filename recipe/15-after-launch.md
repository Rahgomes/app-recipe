# 15. Safety net and after launch

Set this up **before** publishing. Each item solves a problem that otherwise requires a new
version and store review.

| Item | What it solves | How |
| --- | --- | --- |
| EAS Update | Fix a screen or text in minutes | Channel per profile; publish to `preview` first, with green E2E on `production` |
| Crashlytics | Know when the app crashes on someone's phone | Off in dev; account ID only; `ErrorBoundary` at the root |
| Feature flags | Disable a broken feature without publishing | Remote Config with the template versioned in the repo and a test ensuring the app and template have the same defaults |
| Minimum version | Retire a version with a serious flaw | `minimumVersion` parameter; below it, an "Update" screen with the store link |
| App Check | Only the real app calls the server | Play Integrity / App Attest before launch |
| Staged rollout | New errors affect few people | 5% → 20% → 50% → 100% |
| Dependabot/Renovate | Library security fixes | Patch only, weekly, grouped |
| SDK plan | Avoid falling behind | One month after each new Expo SDK, on its own branch: changelog, `expo-doctor`, tests, E2E, test build |
| Support | Know what happened to the person reporting an issue | About screen with version, build, update and diagnostic code; ticket with screenshots and automatic technical log |

## Post-launch routine

- **Keep the journal**: each batch with what went right and wrong.
- **What's new in the app**: a batch with new features updates the release notes users see.
- **User suggestions**: append-only collection, with a weekly limit; when one becomes a feature,
  notify whoever requested it ("Your suggestion became a feature").
- **Two tracks** when V2 is large: V1 live receiving OTA fixes, V2 in parallel
  on a branch with its own channel. Do not mix them.
- **An error that disappears from the screen is costly**: message near the button and error code in the technical
  log from the start. A generic message hid a cause for days.

## Improve conversion (with real traffic)

Test only after the listing gets enough visits; with little traffic, the result is noise.

| Tool | App Store | Google Play |
| --- | --- | --- |
| Listing A/B test | Product Page Optimization: up to 3 variants against the current one, one test at a time, up to 90 days; icon, screenshots and video; Apple recommends 90% confidence | Store listing experiments: up to 2 variants; icon, feature graphic, screenshots and (localized) descriptions; measures installation and 1-day retention |
| Page by audience | Custom Product Pages (up to 70), with their own keywords and an ad link | Custom store listings (up to 50) by country, keyword, campaign or people who uninstalled |

- **One hypothesis per test** ("first screenshot with a large number converts better"), at least one
  week, current version as the control. Variant = another `listing.json`.
- **A losing hypothesis is also a result**: in a case Apple itself publishes, the page without
  video beat the one with video. Test before producing an expensive video.
- **Order of work**: first 3 screenshots → icon → title and subtitle → video.
- **Dates and seasons**: themed screenshots on important dates for the audience, if they fit the app.
- **Reviews**: rating and volume drop when a batch breaks something; check them alongside crashes by version.
- Conversion "benchmarks" in vendor blogs often lack sources: compare the app with
  itself, before and after.

## Metrics to check weekly

| Metric | Where |
| --- | --- |
| Crashes by version | Crashlytics |
| Listing visits → installation (conversion), by source (search, browse, link) | Play Console / App Store Connect |
| Installs, uninstalls, rating and new reviews (reply) | Play Console / App Store Connect |
| Activation (first valuable action) and 1-, 7- and 30-day retention | App analytics |
| Free → paid conversion, cancellations | RevenueCat |
| Ad revenue per thousand impressions | AdMob |
| Backend cost | Google Cloud billing (with an alert) |
