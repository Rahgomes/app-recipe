# 10. Testing and quality

**Goal:** each batch proves what changed without relying on manual clicking. **Gate:** unit,
component, rules (if cloud) and E2E tests green for the flows the batch touched.

## Layers

| Layer | Covers | Tool | Target |
| --- | --- | --- | --- |
| Unit | Pure logic: calculation, time, migration, validation | Jest (jest-expo) | Domain close to 100% |
| Component | Screen + state + persistence, without a device | React Native Testing Library | States: empty, loading, error, offline, pending |
| Rules and server | Who reads and writes what; triggers; callables | Firebase Emulator + rules-unit-testing | Every permissive rule has a test |
| Native E2E | Full journey on Android | Maestro, in CI with an emulator | Critical journeys |
| Web E2E | Journey in the web version, accessibility | Playwright + axe | All journeys, cheaply |

Testing on the web or in Expo Go **does not prove** native behavior (background, audio, notifications,
SVG, large fonts). Record it as **pending device testing**, never as approved.

## Rules learned from bugs

- **Real test database**, not a fake: in-memory SQLite or the Emulator. Catches transactions,
  `INSERT OR IGNORE`, pagination. A fake must fail like the real thing (rejected promise, rejection of
  `undefined` like the native SDK).
- **Run rules and Functions separately**: with the Functions emulator on,
  triggers fire on rule-test writes and lock transactions.
- **New model fields also go into the zod schema**, otherwise the editor saves and the field silently
  disappears. A save-and-reload test catches it; a domain-only test does not.
- **Fixed timezone and language in E2E**: `timezoneId` and `locale: 'pt-BR'` in Playwright (CI runs in
  UTC and English). In Jest, dates in local time.
- **Playwright clock**: a stopped `page.clock` freezes axe and the web database. Freeze only once the
  screen is ready; release it to measure accessibility.
- **Measured touch targets**: a browser loop measures every visible control and fails below
  44×44. It found a 52×32 switch relying on `hitSlop` (ignored on the web).
- **`getByLabel` with `{ exact: true }`**: "Note" matched "Save note".
- **Old screens stay mounted under the stack**: the same button exists hidden; filter for
  visibility. Run the long E2E 4 times in a row before trusting it.
- **Reloading midway kills an in-flight write**: before reloading, leave and return to the screen.
- **Maestro**: `scrollUntilVisible` before tapping anything below the top; disable
  Android autofill in CI (`adb shell settings put secure autofill_service null`);
  dismiss guided tips before any assertion.
- **Stress test before the fix**, and prove it fails without it. Two stress tests
  from the PRD found bugs no function test caught.
- **A test that locks in behavior does not prove it is correct**: an old test guaranteed
  "navigate without saving the draft", which was the bug itself.
- **Map before writing tests**: list each PRD requirement beside the test that already proves it.
  There were few real gaps.

## Accessibility

- Automated test that renders every screen and fails if a touchable has no role or name.
- axe in web E2E. Running E2E in another language found failing contrast.
- Manual on device: TalkBack on (each element says what it is) and maximum system font size
  (nothing gets clipped). Turn TalkBack off: hold both volume buttons for 3 seconds.

## Exploratory testing by agents (unscripted)

The tests above prove what someone thought to test. The `explorer-tester` subagent uses the app
as a **persona** (a senior with large fonts, someone in a hurry using dark mode, offline, a phone in English,
someone who denies permissions) and finds what nobody wrote down: clipped text, a button under the keyboard, missing
translations, a blocking step, an error that disappears from the screen.

| Engine | Where it runs | Good for | Does not prove |
| --- | --- | --- | --- |
| `web` (`tools/explorer/browser.py`) | Any machine, on the web preview | Flow, text, empty and error states, dark mode, small screen, offline | Native: system font, permissions, background |
| `android` (`tools/explorer/device.sh`) | Emulator or phone through adb (requires KVM or your PC) | All of the above + font scales 1.3 and 2.0, app language, permissions, system back | iOS |

When: after a large batch, **before the closed test** (stage 14) and to reproduce a reported
bug. Run 3 to 5 personas in parallel (one subagent per persona, each with its own output
folder), chosen for what the batch changed (`tools/explorer/personas.md`). With the web engine, one
browser at a time per machine: run personas sequentially or set a different `EXPLORER_STATE`
for each.

Then the orchestrator combines the reports: groups identical findings (counting how many personas
hit them), checks screenshots of severe issues and turns them into B## entries in the backlog. A finding becomes a
fix only after its steps are reproduced.

Precautions: test account and data (screenshots go to the AI model you use); never a production
database; token cost grows with personas x actions (start with 3 personas and 30 actions). This does
not replace testing with real people in the closed test.

## CI costs

Native E2E in a private repository uses the free minutes quota quickly (about 35 minutes per
run). Early on, running on every push helps find defects; later, once a night (if main
changed) and on demand.

On a small machine: full suite and build **one at a time**, at most 2 workers. Day to day,
only tests affected by changed files.
