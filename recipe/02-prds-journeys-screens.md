# 02. PRDs, journeys and screens with IDs

**Goal:** turn the superprompt into documents that become code without ambiguity.
**Gate:** every journey lists its screens by ID; every screen belongs to at least one journey.

## IDs from the start

| Prefix | Meaning | Example |
| --- | --- | --- |
| J## | Journey (an end-to-end user goal) | J01 Create account and business |
| S## | Screen | S07 Today |
| S##x | Screen state variant | S07o offline, S09l plan limit, S29r cancel deletion |
| D## | Technical decision | D04 Save on device first, validate on server |
| B## | Backlog item | B12 Monthly reports (V2) |
| A## | Human review addendum | A2 Closed days |

IDs become **image, test and route names**. A change of mind midway costs an inventory entry,
not a reorganization.

## PRD package (adapt to the app's size)

| # | Document | Content |
| --- | --- | --- |
| 00 | Start here | PRD map, glossary, what counts as MVP |
| 01 | Vision, phases and roadmap | Promise, audience, MVP vs V1 vs V2 |
| 02 | Journeys and screens | J## with steps and S##; rules for each field |
| 03 | Competitors and differentiators | Table of what each does; what you do better |
| 04 | Plans and billing | Free vs paid, limits, ads, price as a hypothesis |
| 05 | Batch plan | Delivery order, vertical slice first |
| 06+ | One PRD per major feature | Requirements FR##, acceptance criteria, screens, data |

Feature PRD template in `templates/prd.md`.

## Rules the PRD must include (learned during screen review)

- **Each field's rule**: required or optional, range, prefilled or example, input mask. Write it
  **before** generating the screen; otherwise the screen invents it and the code copies the screen.
- **Edge states**: empty, loading, error, offline, plan limit reached, account pending deletion.
  Each with a screen (S##x variant). A disabled button without an explanation is a UX and
  accessibility pitfall.
- **Money and dates**: integer cents, user's time zone, checked weekday (an incorrect example
  date "Tuesday, 18th" passed through three screens before a test caught it).
- **Fixed example data per screen**: who appears, day, time, amount. Image generators do not keep
  context between screens, and the same customer appeared on different days.
- **What the app never does**: certify, diagnose, promise results. This goes into the terms and
  store listing.

## Single-source screen inventory

A list (spreadsheet, JSON or script) with: ID, name, journeys, active tab, content, fictional data.
It produces platform specs, the flow map and the implementation checklist. New screen = new
line. Template in `templates/screen.md`.

## Human review through images

After stage 6, you review **through the flow map** (navigable journey), not isolated screens.
In our cases, each review round produced an addendum (A##) with rules the text hid: unmarked
required field, information only visible in details, hidden action.
