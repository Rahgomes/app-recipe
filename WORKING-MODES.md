# Working modes: which agents you have

The recipe is the same in all three modes. What changes is who does each task and, above all,
**how screens are created** (stage 6), because Claude does not generate images.

## Comparison

| Task | Claude only | Claude + Codex | Claude + Codex + Antigravity |
| --- | --- | --- | --- |
| Talk, decide, orchestrate | Claude | Claude | Claude |
| PRDs and superprompt | Claude | Claude (or Codex on the web for a long draft) | Same |
| Logo concepts | You generate externally (see below) or SVG through code | Codex generates images | Codex generates |
| Final brand kit (SVG, icons) | Claude, by script | Claude, by script | Claude, by script |
| Reference screens | Ready prompt from Claude for you to paste into a generator, Figma, or straight to code | Codex generates | Codex generates |
| Check generated screen | Claude looks at the image | Claude | Gemini checks, Claude reviews the contact sheet |
| Read long document, video, PDF | Claude | Claude | Gemini summarizes, Claude decides |
| Implement a bounded screen task | Claude | Codex | Codex |
| Backend, rules, E2E | Claude | Claude | Claude |
| Review code | Claude (you review the diff) | Cross-review: Claude reviews Codex, Codex reviews Claude's backend | Same |

Antigravity is Google's agent environment (Gemini). If you use another agent with vision
(image reading), it fills the same role.

## Mode 1: Claude only

The simplest mode, and it works well. What changes:

- **Screens without an image generator**, three paths (choose in the profile, question P4):
  1. **External reference**: you bring screenshots of apps you like, a Figma design or a photo
     of a sketch. Claude reads the image, separates visual language (color, radius, density)
     from structure (what is on the screen) and writes the screen spec.
  2. **External generator**: Claude writes the screen prompt (with the base prompt from
     `templates/screen.md`) and you paste it into whichever generator you have (ChatGPT,
     Gemini, Midjourney, Figma AI). Bring the image back; Claude checks it against the spec.
  3. **Straight to code**: skip the image. The screen's `.md` spec is still required (it becomes
     the test and briefing). You review through the web preview in the browser. Faster, with
     less visual exploration.
- **Logo**: concepts can start as SVG through code (Claude draws simple geometry very well) or
  come from an external generator; the final kit is always SVG produced by script.
- **Review**: without a second agent, you are the second pair of eyes. Ask Claude to review its
  own diff "as if it were someone else's", run typecheck and the full tests, and list the risks
  before the commit.

## Mode 2: Claude + Codex

Claude decides and reviews; Codex executes bounded tasks and generates images.

- **Image**: Codex generates logo concepts, screens and supporting photos (site, store listing).
  An image takes about 1 minute.
- **Implementation**: Claude writes the **briefing** (`templates/briefing.md`) and Codex implements
  only the listed files, with the screen's component test in the same round.
- **Protocol**: (1) Codex plans and stops; (2) Claude reads the plan and adjusts the scope;
  (3) Codex implements; (4) Claude reviews `git diff`, runs typecheck and tests; (5) Claude
  commits. Codex never commits.
- **Cross-review**: new backend code from Claude (Function, rule, webhook, synchronization) goes
  to Codex for read-only review. In case A, this review found real concurrency bugs in almost
  every round.
- **When not to delegate**: architecture decisions, schema, anything involving secrets, deploys,
  changes under ~10 lines (the round trip costs more than doing it).

## Mode 3: Claude + Codex + Antigravity (Gemini)

Same as mode 2, plus an agent with good vision and a long context window:

- **Screen checking**: Gemini compares the generated image with the spec and returns a VERDICT
  (APPROVE/BLOCK), blockers and notes. At most 2 redos per screen; after that, you decide.
- **Long reading**: store rules PDF, competitor video, 50-page document. It summarizes, Claude
  decides.
- **Observed caveat**: Gemini approved screens with the wrong logo and torn edges. Claude's
  visual review of the contact sheet (all screens side by side) is still required.

## Briefing: the biggest way to reduce cost

Every call to another agent starts from scratch and explores the repo unless you say where to
look. We measured it: with a briefing (stack, reference file to follow, 4 to 6 relevant files,
what not to inspect, "done" command), cost fell by about a third. The most influential field is
**"Pattern to follow"**: if you cannot point to a similar file, you do not yet understand the task.

Template in `templates/briefing.md`.

## Parallel work without a mess

- Two agents run in parallel only if they change **different files**.
- Heavy work (installing dependencies, full test suite, build) runs one at a time, and tests use
  at most 2 workers on a small machine. Three suites together take down a 4-vCPU VPS.
- Long background work: one job per batch, checked on disk, never "wait for the batch and start
  the next" in a loop (it dies without warning if the session drops).
