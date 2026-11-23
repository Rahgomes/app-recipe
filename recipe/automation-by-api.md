# Automation by API: what the agent does on its own with the right credential

The agent can do much of the setup "behind the scenes", without you copying and pasting in
consoles. There is one rule: **you create the credential and save it in a file outside the repository; the
agent uses its path without ever displaying the value.**

## How to give the credential to the agent

```bash
mkdir -p ~/.secrets && chmod 700 ~/.secrets
# key/token: paste it in the editor, not in chat
nano ~/.secrets/<app>.env && chmod 600 ~/.secrets/<app>.env
# service account JSON file: save directly from the download screen
mv ~/Downloads/<file>.json ~/.secrets/<app>-<service>.json && chmod 600 ~/.secrets/<app>-*.json
```

The `.env` contains `NAME=value` lines; `set -a` exports them to the child command. JSON is passed by path,
never through `source`. The agent uses it like this, and only this way:

```bash
( set -a; source ~/.secrets/<app>.env; set +a; eas build --profile preview --platform android )
GOOGLE_APPLICATION_CREDENTIALS=~/.secrets/<app>-play.json node scripts/play-publish.js
```

Forbidden for the agent: `cat`, `echo`, `printenv` of secrets; putting values in versioned files,
logs, journals or messages. Secret pasted into chat by mistake: revoke it and generate another.

## Map: credential → what the agent does

| Service | Credential (you create) | Minimum permission | Agent does |
| --- | --- | --- | --- |
| Firebase / Google Cloud | CLI login (`firebase login --no-localhost`: you authorize the link) | Dev project owner | Database, rules, indexes, Functions, Function secrets, apps, SHA-1, Remote Config |
| Firebase in CI | Service account (JSON) | Deploy-only roles | Automatic deployment |
| Expo / EAS | Access token (`EXPO_TOKEN`) | Project account | Builds, updates, EAS environment variables, preview hosting |
| GitHub | `gh auth login` or token with `repo` and `workflow` | Repository only | CI, repo secrets, PRs |
| Google Play | Service account with API access in Play Console | Release versions, manage products (no financial access unless needed) | Create and activate subscriptions, upload AAB to internal/closed track, store listing |
| RevenueCat | **v2** secret key | Project read and configuration | Apps, products, entitlements, packages, webhook |
| App Store Connect | API key (.p8 + key ID + issuer ID) | App Manager | Build and submission through EAS, TestFlight |
| AdMob | AdMob API OAuth login | Read | Reports. Creating apps and ad units usually happens in the console |
| Domain / DNS | Provider API token | Domain zone only | Verification records and CNAME |

## What remains yours

- First login to each console, card, identity verification, accepting terms.
- Agreements and tax and bank details (Apple, Google, AdMob).
- First submission for review of an unpublished app (the API only accepts drafts).
- Play license testing (tester email list) and tester enrollment.
- DNS, domain and IAM role changes: the agent may prefer to give you a ready script
  to run instead of executing it alone. This is good practice, not a defect.

## Traps

- Two projects with the same name in Google Cloud: the role goes to the wrong one. Check the **ID**.
- Production credentials only when the time comes; development runs with dev credentials.
- RevenueCat: catalog setup (apps, products, entitlements, offerings, webhook) uses API v2,
  with a v2 secret key with write permission. v1 is for subscribers (query, grant
  promotional entitlement), not the catalog.
- A new Play service account can take up to a day to work with the API.
