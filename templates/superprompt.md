# Superprompt template

Copy, fill in and paste into any AI. Fields marked **(required)** must be answered
before the PRDs; the agent can propose the rest. Label hypotheses as hypotheses.

````text
SUPERPROMPT · <APP NAME OR "WORKING NAME"> · version <x.y> · <date>

START OF PROMPT

Act as a product lead, mobile designer and senior React Native engineer with business
sense. Develop a React Native (Expo) app with TypeScript for Android <and iOS>,
distributed through Google Play <and App Store>. Question assumptions that seem weak and propose the
cheapest path that proves the idea.

1. VISION (required)
Problem: <the pain, with a concrete everyday example>
Audience: <who uses it; who pays, if different>
Promise in one sentence: <"Record..., organize..., deliver...">
What the app NEVER does: <e.g.: does not issue a professional assessment, replace a professional, store card details>

2. EVIDENCE AND COMPETITORS
<3 to 5 competitors: what they do, public price, complaints in reviews>
Study structure; do not copy screens, text or branding.
Facts with access date; reconfirm before deciding.

3. MAIN JOURNEYS (required)
J01 <name>: <steps from the user's perspective>
J02 <name>: ...
(the 2 most important become the vertical slice)

4. SCOPE BY PHASE (required)
MVP (proves the core): <list>
Public V1: <list>
V2: <list>
Do not hide effort behind the word MVP.

5. MONETIZATION MODEL (required)
<No charge | Ads on free plan | Subscription | Both>
Plans and limits: <Free: ... | Paid: ...>
Price: HYPOTHESIS of R$ <x>/month, to test.

6. DATA AND OFFLINE
Works without internet? <yes/no; what happens to work done offline>
Account required? <yes/no, and why>
Third-party personal data? <e.g.: the user's customers>

7. BRAND AND VISUALS (optional at this point)
Name: <or "propose 5 options with an available domain">
Personality: <e.g.: welcoming, professional, energetic>
Colors: <hex, if available; otherwise "propose a palette with measured AA contrast">
Typography: <if available>
Visual references: <apps or screenshots you admire and why>

8. STACK (optional; default below)
React Native + Expo (current stable SDK), Expo Router, TypeScript strict, Firebase (Auth,
Firestore offline, Functions, Storage, App Check), EAS Build and EAS Update, RevenueCat for
subscriptions, AdMob for ads. Another stack only with a reason: <reason>.

9. CONSTRAINTS
Deadline: <date or "no deadline">
Monthly infrastructure budget: <amount>
Available AI tools: <Claude only | Claude + Codex | + Antigravity/Gemini>
Developing on: <Windows | Linux | Mac> (without a Mac, iOS through EAS in the cloud)
Play account type: <personal | organization> (new personal accounts require a 14-day closed test)

10. SUCCESS CRITERIA
MVP done when: <e.g.: J01 and J02 end to end on Android, E2E green>
Successful launch when: <e.g.: 50 active users, 5 paying users in 60 days>

11. EXPECTED DELIVERABLES
PRDs with IDs (J##, S##, D##, B##), screen inventory, brand, lightweight design system, reference
screens, code with tests, store listings.

END OF PROMPT
````

## Examples of phrases that prevented rework

- "Choosing a name does not confirm the domain or trademark: do not invent a domain, email or store
  URL; use a placeholder until confirmed."
- "Evidence consists of vendors' public descriptions, not tests inside the apps. A feature not
  mentioned on the website must not be marked as nonexistent."
- "'Visually outperforming' is a hypothesis to verify with users, not permission to copy."
- "Do not claim full parity when only screens have been designed."
