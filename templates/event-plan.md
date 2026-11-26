# Event plan for <app>

Lives in `docs/analytics/event-plan.md`. Reviewed with the PRDs (stage 2) and whenever a batch
adds a journey. Rules and limits: `recipe/analytics.md`. The `track()` module mirrors this table.

## Definitions

| Term | For this app |
| --- | --- |
| Active user | <opened the app / did the core action> |
| Activation | <first valuable action> within <window> |
| Core action | <the action that delivers value> |
| Churn | <cancelled / no core action for X days> |
| Consent | <where collection waits for consent; D## that decided it> |

## Events

| Event | Fires when | Parameters | Journey / screen | Question it answers |
| --- | --- | --- | --- | --- |
| `sign_up` | Account created | `method` | J01 / S03 | Which sign-in method converts? |
| `activation` | <first valuable action> | `journey` | J02 / S07 | How many reach the value? |
| `paywall_view` | Paywall shown | `trigger`, `variant` | J05 / S20 | Which trigger sells? |
| `purchase` | Store or RevenueCat confirmed | `plan`, `period` | J05 / S21 | Does the paywall convert? |
| `error_shown` | Message shown to the user | `code`, `screen` | any | Where do people get stuck? |

## User properties (up to 25)

| Property | Values | Why |
| --- | --- | --- |
| `plan` | free, trial, paid | Split every report by plan |

## Funnels to watch

1. Install → `sign_up` → `onboarding_complete` → `activation` (target: <x>% in <window>)
2. `paywall_view` → `trial_start` → `purchase`

## Never collected

Email, name, phone, typed text, precise location, anything identifying a person.
