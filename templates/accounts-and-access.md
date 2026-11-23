# Template: accounts and access

`docs/accounts-and-access.md`. **Never** put a secret value here: only the variable name and
where it is stored.

| When | Account / resource | You create | Save in (outside the repo) | The agent configures later | Status |
| --- | --- | --- | --- | --- | --- |
| Stage 7 | Google Cloud (billing) | Card, payment profile | | | |
| Stage 7 | Firebase `<app>-dev` | Project, Blaze plan, budget alert | | Database, rules, Functions, apps | |
| Stage 7 | Firebase `<app>-prod` | Same | | Same | |
| Stage 7 | Expo / EAS | Account | `EXPO_TOKEN` in `~/.secrets/<app>.env` and CI | Project, profiles, channels | |
| Stage 7 | GitHub | Private repository | Repo secret `EXPO_TOKEN` | CI | |
| Stage 7 | Play Console | Developer account, app, service account | Service account JSON file | Version submission, products | |
| Stage 7 | Apple Developer | Account, paid apps agreement, tax | App Store Connect API key | Build and submission | |
| Stage 13 | RevenueCat | Account | v2 secret key | Apps, products, entitlement, webhook | |
| Stage 13 | AdMob | Account, payments | | App and ad unit IDs through variables | |
| Stage 14 | Domain | Purchase, DNS | | Website, verification | |

## How to store them (Linux/Mac)

```bash
mkdir -p ~/.secrets && chmod 700 ~/.secrets
nano ~/.secrets/<app>.env            # you type it; the agent never sees the value
chmod 600 ~/.secrets/<app>.env
# agent usage, without printing:
( set -a; source ~/.secrets/<app>.env; set +a; eas build --profile preview --platform android )
```

On Windows, use a folder under your user directory outside the project and system environment
variables, or a vault (1Password CLI, Bitwarden CLI).
