# 01. Idea and superprompt

**Goal:** turn the idea into a document any agent can use without inventing the product.
**Gate:** you read and approved the superprompt.

## What a superprompt is

A single text you can paste into any AI, describing the whole product: what it is, who it is
for, why someone pays, what goes into each phase, how it should look and what must not happen.
It is the **source** for the PRDs in stage 2. Template in `templates/superprompt.md`.

Required in the superprompt: problem, audience, promise, main journeys, scope by phase
(MVP, V1, V2), billing model, what the app never does. Optional at this stage (the agent can
propose later): name, colors, typography, stack. This recipe's default stack is React Native +
Expo + Firebase; specify another only if you have a reason.

## Three starting points

### No idea

The agent asks about your context (what you do, which routines you know well, who you know who
would pay) and proposes 3 ideas, each with:

| Field | Example answer |
| --- | --- |
| Pain | "Private tutor loses lessons because they schedule through WhatsApp and the student forgets" |
| Who pays and how much | "The professional, R$ 10 to 30 per month, if it saves 1 missed appointment" |
| Why now | "Paper calendars and WhatsApp still dominate the niche" |
| Competitors | 3 names and what they do poorly |
| Main risk | "Professional will not pay for an app; needs a free plan with ads" |
| Smallest version that proves it | "Calendar + WhatsApp reminder, no marketplace" |

You choose one (or combine them) and continue as a "loose idea".

### Loose idea

Interview from `templates/interview.md`, **one question at a time**, with the agent's
recommendation for each (you can simply say "sounds good"). About 15 questions in 4 blocks:
problem and audience, product and journeys, business, constraints. At the end, the agent writes
the superprompt and you review it.

### Ready superprompt

The agent checks it against the template and lists only what is missing and changes a decision.
Examples we caught:

- Superprompt said "first use without an account". Reading where the rule came from (complaints
  about competitors asking for a phone number), the pain was the phone number, not the account.
  Changing it avoided an offline mode without an account that would have cost weeks.
- Superprompt promised parity with competitors "in V1". Separating MVP, public V1 and V2 avoided
  hiding effort inside the word MVP.

**Lesson:** discrepancies appear when **comparing** the superprompt with the recipe and lessons,
not when reading the superprompt alone.

## Validate before spending

Before stage 2, spend an hour on this:

1. **Competitors**: open 3 to 5 in the store; note price, rating, complaints in 1- to 3-star
   reviews. The complaints are your differentiator. Do not copy screens or text: study structure.
2. **Talk to 3 to 5 people in the audience**. Showing 3 or 4 logo concepts to buyers led to a
   choice the owner would not have made (case A).
3. **Back-of-the-envelope calculation**: cost per user (server, store, RevenueCat), revenue per
   paying user, paying users needed to cover costs. Details in `13-monetization.md`.
4. **Name**: shortlist, domain checked (stage 4) before getting attached.
5. **Evidence of payment, not compliments**: ask what people use and pay today for this problem,
   never "would you use it?". When there is an audience, a "painted door" (a buy button that leads
   to a waitlist) or a pre-sale on the website measures intent before building.
6. **The blank-box test** (AI-era apps): type the user's problem into a general AI chat and list what
   the app does that the answer does not (structure, memory, habit, accuracy, community, device).
   If the list is empty, the idea is a prompt, not an app.
7. **Per-call costs** (AI, vision, maps, SMS): cost per active user in the "it went viral" scenario.

## Outputs

- `docs/prd/00-superprompt.md` (version with date at the top; old versions are not deleted).
- Competitor list with what each does and does not do.
- Pricing assumptions marked as **hypotheses**, not decisions.
