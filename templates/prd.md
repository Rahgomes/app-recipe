# Feature PRD template

```markdown
# PRD <nn>: <feature name>

Version <x> · <date> · Phase: MVP | V1 | V2

## Problem
<what hurts, for whom, evidence>

## Goal and measure
<what changes for the user; how to know it worked>

## Journeys and screens
| Journey | Steps | Screens |
| --- | --- | --- |
| J<nn> | 1. ... 2. ... | S<nn>, S<nn>e (error), S<nn>o (offline) |

## Requirements
| ID | Requirement | Priority |
| --- | --- | --- |
| FR01 | ... | Required |

## Field rules
| Screen | Field | Required | Format/range | Default or example | Error shown |
| --- | --- | --- | --- | --- | --- |

## Edge states
Empty · loading · error · no internet · plan limit · no permission · account being deleted

## Data
Collections/tables touched, who writes each field (app or server), required index.

## Plan rules
What free users see, what paid users see, what happens when paid becomes free.

## Acceptance criteria
- Given <situation>, when <action>, then <result>.

## Tests
Unit: ... · Component: ... · Rules/server: ... · E2E: ...

## Out of scope
<what comes later>

## Related decisions
D<nn>, B<nn>
```
