# Screen templates: base prompt, inventory and spec

## Base prompt (shared by every screen)

```text
Mobile app screen <Android Material 3 | iOS HIG>, 390x844, plain light background, no frame,
no blur, no glow, no vignette, no torn edges, no surrounding device.
Product: <name>, <promise in one sentence>.
Visual language: <personality>; radius <16>; soft shadows; generous spacing.
Colors by role: primary <#hex>, background <#hex>, surface <#hex>, text <#hex>,
secondary text <#hex>, success <#hex>, warning <#hex>, danger <#hex>.
Typography: <family>; headings <weight>; tabular numbers.
Tabs: <Home · Schedule · Customers · More>.
Status (text + icon + color, never color alone): <Scheduled, Confirmed, Completed, Canceled>.
Fictional data in Brazilian Portuguese, common names, amounts in R$.
No logo (unless the screen calls for it). Never: English text, real data, third-party brands,
a floating button not requested by the spec.
```

## Inventory (single source of truth)

Can be JSON, a spreadsheet or a script. JSON example:

```json
{
  "platform": {
    "android": "Material 3, bottom tab bar, back at top left",
    "ios": "HIG, large title, bottom tabs, back with arrow and label"
  },
  "screens": [
    {
      "id": "S07",
      "slug": "today",
      "jornadas": ["J01", "J02"],
      "aba": "Home",
      "conteudo": "Greeting; daily summary (3 appointments, R$ 180); list by time; Schedule button at the bottom",
      "dados": "Wednesday, November 19; Ana Lima 09:00 Confirmed; Bruno Reis 10:30 Scheduled"
    }
  ]
}
```

It produces: specs per platform, the flow map and the implementation checklist.

## Screen spec (`docs/screens/<platform>/<ID>-<slug>.md`)

```markdown
# S07 Today (Android)

Journeys: J01, J02 · Tab: Home · References: R01, R02
Current image: docs/images/android/S07-today-v2.png

## Content (top to bottom)
1. ...

## States
Empty: ... · Loading: card skeletons · Error: ... · Offline: "Saved on this device" banner

## Fields and rules
(from the PRD field rules table)

## Accessibility
Reading order; icon labels; minimum target 44.

## Fixed fictional data
...
```
