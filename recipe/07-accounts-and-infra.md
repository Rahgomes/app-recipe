# 07. Accounts and infrastructure

**Goal:** all accounts created, separate environments and secrets outside the repository.
**Gate:** each account in the profile exists; `docs/accounts-and-access.md` filled in; no secret
values in versioned files.

## Who does what

Only you: card, identity verification, accepting terms, bank account and tax details, domain,
trademark registration. The agent: everything possible through CLI or API **after** you
authorize it. Table template in `templates/accounts-and-access.md`.

### Where to store secrets

| Secret | Where |
| --- | --- |
| Expo token | Local file outside the repo (e.g., `~/.secrets/<app>.env`, mode 600) and `EXPO_TOKEN` secret in CI |
| Service account (Firebase, Play) | Local file outside the repo; in CI, repository secret; minimum roles |
| RevenueCat secret key | Local file; on the server, Functions Secret Manager |
| RevenueCat public key, AdMob IDs | Build variable (`EXPO_PUBLIC_*`); not secret, but environment-specific |
| `google-services.json` / `GoogleService-Info.plist` | Not secret, but environment-specific: EAS file variable, outside the repo |

Never: private key in `EXPO_PUBLIC_*` (it ships inside the app), secret pasted in chat, `cat` of
a secret file in a shared terminal. Leaked? Revoke and issue a new one immediately.

## Order and steps

| # | Step | Who | How | Pitfall |
| --- | --- | --- | --- | --- |
| I1 | Google Cloud billing account | You | console.cloud.google.com → Billing | |
| I2 | Firebase projects `<app>-dev` and `<app>-prod`, Blaze plan, budget alert | You | Firebase → Usage and billing | **An alert is not a cap** |
| I3 | Firebase CLI login on the development machine | You + agent | `firebase login --no-localhost`: the CLI shows a link, you authorize and return the code | Safer than a JSON key; the link expires in minutes. JSON key only for CI, later, with minimum roles |
| I3a | **Two projects with the same name** | You | Google Cloud selector → check the **ID** column | A project created through Google Cloud gets an ID with a number; roles and APIs enabled in the wrong project have no effect. Always enter through the Firebase console |
| I4 | Firestore in your audience's region | You enable the API; agent creates | `firebase firestore:databases:create "(default)" --location <region> --delete-protection ENABLED` | Region is permanent |
| I5 | Rules and indexes | Agent | `firebase deploy --only firestore:rules,firestore:indexes,storage --project <id>` | Database starts locked; open only what tests cover |
| I6 | Storage in the same region | You | Firebase → Storage → Get started | The "no-cost" location (US) charges for cross-region traffic |
| I6a | Storage agent role | Agent | Grant `firebaserules.firestoreServiceAgent` to the Storage agent | If `storage.rules` uses `firestore.get`, without this role uploads fail in new projects with a generic error |
| I7 | Login | You | Authentication → Get started → Email/password and Google | The Web OAuth client is only created when you enable Google in the console. App SHA-1 and SHA-256 registered (EAS upload key **and** Play signing key) |
| I8 | Android/iOS app registered | Agent | `firebase apps:create android "<app> (dev)" --package-name <package>.dev` | Config file per environment |
| I9 | Functions secrets | Agent | `printf '%s' "$VAR" \| firebase functions:secrets:set NAME --data-file=-` | Value never appears on screen, in logs or in commits |
| I10 | Functions | Agent | `firebase deploy --only functions` | (1) Cloud Build runs `npm install` and does not understand pnpm's `workspace:*`: package the deploy folder with only the bundle. (2) First deployment may fail while permissions propagate: retry in a few minutes. (3) Callable whose creation failed starts locked (403): delete and recreate |
| I11 | Costs under control | Agent | `maxInstances` on every Function; artifact cleanup (`functions:artifacts:setpolicy --days 1`); mandatory App Check | |
| I12 | Expo/EAS | You create the account; agent does the rest | `eas project:init` and dev build | With `app.config.ts`, init does not write automatically: paste `projectId` into `extra.eas`. Create `.easignore` first (the first upload included 359 MB of doc images) |
| I13 | Play Console | You | Developer account (one-time fee), create the app, service account with API access | New personal account: mandatory closed test (stage 14) |
| I14 | Apple Developer (if iOS) | You | Annual subscription; paid apps agreement | See stage 13 (agreement and tax) |
| I15 | RevenueCat (if subscriptions) | You + agent | See stage 13 | **v2** secret key with configuration permission if the agent will work on the dashboard |
| I16 | AdMob (if ads) | You + agent | App, banner ad unit, category blocking, payments | Only test units during development: clicking a real ad gets the account shut down |

## Two environments, always

- `dev`: everything you test. `prod`: close to launch.
- The production build **must point to prod**. Check before submitting:
  `APP_VARIANT=production npx expo config --type public` and a check of the generated package.
- Prod Remote Config never published = all switches at defaults. Publish it.

## Let the agent work without you pasting anything

Almost everything in Play (products, subscriptions, version submission to the internal track)
and RevenueCat (apps, products, entitlement, webhook) is available through APIs with a service
account. You create the service account once, save the file outside the repo and the agent uses
its path.

For sensitive actions (DNS, domain, IAM roles), the agent may prefer not to execute on its own:
ask for the ready script and run it yourself.
