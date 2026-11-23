# 03. Technical review of PRDs

**Goal:** compare PRDs with reality before writing code. **Gate:** each conflict became a D##
decision with a rationale; no open conflicts.

## Required checks (all went wrong in at least one of our cases)

| Check | What we got wrong | How to check |
| --- | --- | --- |
| **Current** store rule for the account type | The PRD ignored that new personal Google Play accounts need a **closed test with 12 testers for 14 days** before production | Official Play Console page that day; this determines the launch date |
| Free plan against each service | The PRD assumed free Firebase with Functions; Spark does not run Functions, which need Blaze (pay as you go, with a free quota) | Pricing page for each service in the architecture |
| Developer's environment | The PRD assumed a Mac for iOS builds | EAS Build compiles iOS in the cloud, without a Mac |
| Deadline vs complexity | The PRD requested a custom sync queue in SQLite | Firestore's offline cache + server trigger provide the same guarantee with much less code |
| Superprompt rule vs its origin | "Use without an account" came from a complaint about phone numbers, not accounts | Read the evidence behind the rule |
| Digital feature subscription | (Correct decision) Charging for the app through your own gateway leads to store rejection | A subscription that unlocks an in-app feature goes through the store (see stage 13) |

## Decisions every app must record

| Topic | Question | This recipe's default |
| --- | --- | --- |
| Offline | Does the app work without internet? What happens to work done offline? | Save on device first; server validates later; pending data never appears as confirmed |
| Data | Where is the source of truth? | Firestore (cloud) or SQLite/file (local). See `firestore` below |
| Login | Which providers? | Email/password + Google. With Google on iOS, Apple requires "Sign in with Apple" |
| Multi-tenant | One account, one business? Team later? | Business document with members and roles from the start, even with only the owner |
| Updates | How does the fix reach the phone? | EAS Update from the first build (stage 12) |
| Tests | What is required per batch? | Unit + component + E2E for affected journeys |
| Security | Who can read and write what? | Deny-all rules; open only what tests cover. App Check |
| Privacy | What personal data is collected? Third-party data? | Collection inventory from now on (becomes Data Safety) |
| Account deletion | How and within what timeframe? | In-app and through a web link (both stores require it); cancellation window |

## Firestore modeling (if P3 = cloud)

- Model from the **screens**: each list on screen is a query; design the query before the collection.
- Multi-tenant: `businesses/{id}/...` with `members/{uid}`; `users/{uid}` links account to business.
- Numbers shown in lists (last visit, monthly total) come **ready in the document**, maintained
  by the server. Calculating in the app costs one read per item.
- Server-only fields (plan, counters, confirmed status) protected by rules.
- `schemaVersion` in every document from day one; lazy migration on read.
- Database region is **permanent**: choose one near your audience.
- Retention (TTL) must be enabled in the index, not just written in the field. We discovered late
  that the timeframe promised in the privacy policy was not being met.

## Outputs

- `docs/decisions.md` with D## (template in `templates/decisions-and-backlog.md`).
- `docs/backlog.md` with B## by phase (MVP, V1, V2) and status.
- Data collection inventory (Data Safety draft).
