# Briefing template for another agent

Place this at the top of the prompt, before the task. We measured about one-third fewer tokens with it.

```text
BRIEFING
Stack: Expo SDK <n> + Expo Router + TS strict; styling with StyleSheet + tokens
Pattern to follow: src/app/(tabs)/<similar-screen>.tsx      <- REQUIRED
Image: docs/images/android/<ID>-<slug>-vN.png (spec alongside it)
Relevant files (4 to 6):
  src/app/<route>.tsx: route
  src/features/<x>/<Screen>.tsx: component
  src/features/<x>/use<Data>.ts: data hook
  src/schemas/<x>.ts: zod
  src/test/<x>/<Screen>.test.tsx: test
No need to look at: functions/, docs/ (except the spec), apps/site/
Limits: no file over ~250 lines; kit components cannot use arbitrary color styles
Done when: npx eslint <files> && npx jest --findRelatedTests <files> --maxWorkers=2
Report: every divergence from the image as "screen divergence: <ID> · <what> · <why>"

TASK
<what to do, in 3 to 8 lines>
```

## Rules

- **Pattern to follow** saves the most. Without a similar file to point to, you do not yet
  understand the task.
- **4 to 6 files**. With 1 to 3, the agent fills the gaps by exploring; with 7 or more, it reads everything.
- Two-call protocol: (1) "plan and stop"; (2) paste the approved plan and ask "implement
  only the listed files". Each call is a new session: without pasting the plan, it does not know which one.
- The approved plan for the first slice becomes the example for the next ones ("follow slice 1").
- The orchestrator reviews the diff, runs the full project typecheck and commits. The executor never
  commits.
