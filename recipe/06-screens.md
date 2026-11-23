# 06. Screens

**Goal:** each S## screen has an approved visual reference before code. **Gate:** reference
screens approved by you; the rest checked; navigable flow map.

## Three paths (profile question P4)

| Path | When | Flow |
| --- | --- | --- |
| **AI-generated** | You have Codex (or another generator) and want to explore visuals | Spec → image → check → code |
| **External reference** | You have screenshots of apps you like, Figma, a sketch | Reference attached to spec → code → screenshot comparison |
| **Straight to code** | You want speed, simple visuals | Spec → code → web preview screenshot becomes the image |

In all three, the **screen's `.md` spec is required**: it becomes the implementer's briefing and
the test.

## Pieces

| Piece | What it is |
| --- | --- |
| Base prompt | Block shared by every screen: product, format (390×844, plain background), fictional data, brand, tokens, tabs, status vocabulary, what never to show. Template in `templates/screen.md` |
| Inventory | Single source (script or spreadsheet) with ID, journeys, active tab, content, fictional data. Generates Android and iOS specs |
| Images | `docs/images/{android,ios}/<ID>-<slug>-vN.png`; highest version is current; old ones in `archived/` |
| Flow map | HTML that reads journeys and shows each step with its image; navigates in journey order |

## Sequence ("AI-generated" path)

1. Base prompt with stage 5 tokens.
2. **2 to 4 reference screens per platform** (e.g., sign-in and home), Android first.
   **You approve only these.** Batch consistency comes from them, not the text.
3. Complete inventory, with fictional data fixed per screen.
4. Batch with approved references attached to each generation. With references, batches of 16,
   26 and 52 screens were approved on the first pass (about 1 minute each).
5. Checking: redo only blockers, **at most 2 times**. If still blocked, you decide (proceed with
   a note or change the screen).
6. **Contact sheet**: all journey screens side by side. Catches inconsistencies between screens
   (torn edge, invented floating button) that screen-by-screen checking approved.
7. Logo pasted by script (the generator gets it wrong).
8. Flow map regenerated.

Fixed phrases that solved recurring defects: "no logo" on every screen that does not need one;
"plain light background, no torn edges, no vignette" (a dark frame appeared in 1 out of every 5
iOS screens).

## Without an image generator (Claude-only mode)

- Claude writes the full screen prompt (base prompt + spec) and you paste it into whichever
  generator you have. Bring the image back; Claude checks it against the spec.
- Or: external reference. Claude reads the screenshots and separates **visual language** (color,
  radius, density, typography) from **structure** (what is on the screen). Copy the language,
  never the screen.
- Or: straight to code, and you review through the web preview (`11-seeing-the-app.md`).

## Rules that keep images and code together

- **Image before code**: a screen without an approved reference does not go to implementation.
- **Code follows the image**: the implementer reports every divergence in a line
  `screen divergence: <ID> · <what> · <why>`.
- **Image follows code**: an accepted divergence goes back into the image in the same delivery.
  After implementation, the **real screenshot** replaces the concept image in the documentation.
- **Image without code yet**: a new screen designed when the app already has code opens a B##
  in the same delivery with status "to code", citing the screen and requirement. The implementer
  finds the queue ready.
- A screen closes only with inventory, images (Android and iOS), flow map, code, test and journal
  line **in the same commit**.
- Comparing the **preview screenshot** with the image is the step that catches what component
  tests cannot see.

## Changing an existing screen

| Change | What to redo |
| --- | --- |
| Text only | Inventory and spec; no new image |
| Field, order, state | New image version (Android, then iOS) and code |
| Structure | Same, plus journey contact sheet |
| Global token | `tokens.ts` + base prompt + references; D## |
| Logo | Brand script → all screens with the logo |

## Reference cost

Image: about 1 minute and 19,000 tokens in Codex. Checking: about 80 seconds and 49,000 tokens
in Gemini. A new screen in an app with an inventory costs one inventory line and one journey
in the map.
