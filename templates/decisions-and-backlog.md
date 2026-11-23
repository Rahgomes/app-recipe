# Templates: decisions (D##) and backlog (B##)

## docs/decisions.md

```markdown
# Technical decisions

| ID | Date | Decision | Why | Rejected alternative | Review when |
| --- | --- | --- | --- | --- | --- |
| D01 | 2026-11-18 | Expo + EAS Build | No Mac; iOS build in the cloud | Local build | Paid builds exceed X/month |
| D02 | | Save on device, validate on server | Real offline support with little code | Custom SQLite queue | |
| D03 | | Package br.com.<app>.app | Immutable after publishing | | Never |
| D04 | | EAS Update from the first build, runtimeVersion fingerprint | Adjust without a build | Build for every adjustment | |
```

Rule: a decision that contradicts an earlier D## gets a new D## citing the old one. Do not delete it.

## docs/backlog.md

```markdown
# Product backlog

| ID | Idea | Source | Phase | Status | Screens | PRD |
| --- | --- | --- | --- | --- | --- | --- |
| B01 | Suggest an improvement | Owner review | MVP | to code | C03 | 02 |
| B02 | Monthly reports | Competitor X | V2 | idea | S30 | |
```

Status: idea → planned → to code → in batch → live → discarded (with reason).
A screen designed before coding gets "to code", citing the screen and requirement.
