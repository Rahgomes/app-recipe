# 09. Vertical slice and building in batches

**Goal:** prove the core before expanding, then deliver one batch at a time without breaking what
already works. **Vertical slice gate:** the 2 core journeys end to end with green E2E on
Android. **Gate for each batch:** three test layers green for the affected flows, screenshots checked
against the images, journal updated.

## Vertical slice

Choose **the most-used journey and the riskiest one**. In a scheduling app: create an account and book with
payment. In a timer: a reliable counter. In a reporting app: from photo to PDF.

If the product risk is native (camera, files, PDF, background audio), run a **technical
proof on a real device before stage 8 ends**. Do not discover in batch 6 that the camera cannot
handle it.

What the vertical slice found in our cases that the web preview hid: a configuration key
in the wrong format, an `undefined` field rejected by the native SDK, a tap swallowed by Android's "save
password" dialog, an incorrect outstanding amount on a canceled appointment with a refund.

## Batch: the cycle

1. Choose the batch from the plan (stage 2): a few screens from the same area.
2. Batch screens have approved images (or specs, according to P4).
3. Pure logic first, with tests, in `shared`/domain.
4. Batch backend (rules, Function) with Emulator tests. New backend code goes to
   another agent for review, if available.
5. Screens: a briefing per screen (`templates/briefing.md`) for Codex, or direct implementation.
   Component tests for states (empty, loading, error, offline, pending) in the same round.
6. Review: the full diff, project-wide typecheck, affected tests.
7. Screenshot of the web preview (and the device when native code is affected) compared with the image.
8. E2E if the journey gained or lost a step.
9. Deliver: OTA or build (stage 12).
10. Same commit: code, tests, updated images, journal entry.

## Review: what caught the most defects

- **Backend cross-review**: almost every round found a real concurrency or edge-case bug
  (a race between two trigger executions, an audit record written outside the transaction,
  an item cap within a period). Sync goes to review **with the entire file**: a review
  truncated at 600 lines caught 2 of 12 gaps.
- **Full typecheck during review**: the implementing agent said "passed" after running only tests;
  the typecheck caught the wrong form type.
- **Verify what the briefing claims**: a contract the orchestrator said was ready
  was not (the edit did not match after Prettier). `grep` before making a claim.
- **Briefing contradicts the image = briefing error.** The agent follows the briefing literally.
- **Size cap**: without a limit in the briefing, we got a 680-line file. "No file over
  ~250 lines" in the agent instructions file.
- Each agent call is a new session: "implement the approved plan" without pasting the plan makes it
  return without doing anything.

## Audit before merging into main

Once per delivery (not per commit): scan for secrets, dead code, `console.log`, old TODOs,
unauthenticated routes, queries assembled from user text. Good work to delegate:
it is mechanical and reads the whole repository.

## When an agent gets stuck

If the same test fails twice with one agent, the other takes over. A third round costs more
than starting over.
