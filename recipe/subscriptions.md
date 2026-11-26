# Subscriptions in depth: model, paywall, price, offers and churn

Stage 13 wires the purchase. This chapter decides **what** to sell, **when** to ask and **how to keep**
the people who pay. It is tool-agnostic: RevenueCat, Adapty, Qonversion or the store APIs directly
all expose the same store mechanics; where only one vendor has a ready-made feature, it says so.

Store rules here were checked on official pages in November 2026; numbers marked "SOSA" come from
RevenueCat's State of Subscription Apps reports (large sample, but their customers only, and
correlation between different apps, not cause). Check rules again on the day you configure them.

## 1. Decide the model in the PRD (record it as a D##)

| Question | Default for a small app | Why |
| --- | --- | --- |
| Hard paywall or freemium? | Hard paywall at the end of onboarding, unless the app has network effects or value that takes weeks to show | SOSA 2026: download → paid by day 35, median 10.7% hard vs 2.1% freemium; 12-month retention about equal. Freemium needs volume (about 1,000+ free users per useful paying cohort) |
| Free trial? | Yes, with length = **the app's activation window** | Value felt in one session: short or no trial. Value that builds (habit, money, learning): longer trial with onboarding that reaches the "aha". Most apps sit at 3 days; longer trials (17 to 32 days) convert better in the 2026 data |
| Plans | Monthly + annual; annual shown as "R$ X/month, billed yearly (R$ Y)" | Monthly gives fast signal while you learn; annual hides churn for a year. Weekly only for short or seasonal use, with text saying who it is for |
| Price | Start higher than feels safe; it is easier to discount than to raise | Test large jumps (R$ 30 vs R$ 90 per year), not R$ 30 vs R$ 40 |

- **Free-tier charter**: write what will never become paid (a daily limit, N free uses to form the
  habit). Removing free features raises revenue for months and erodes word of mouth. Every new
  feature is classified free or paid against this charter before launch.
- **Changing the model later** (paid → subscription, freemium → trial only): apply it to new
  installs only; existing users keep what they had and get an optional "supporter" purchase.
- **AI or per-call costs** (model tokens, vision, maps, SMS): compute the cost in the "it went viral"
  scenario before launch and have plan B ready. Prefer credits (a quota inside the plan or a
  consumable) debited **on the server before** calling the model, refunded on failure, with an
  idempotency key. Sell in units people understand (minutes, photos), never tokens. A free trial
  with unlimited AI burns money: cap generations in the trial.
- **Apps too simple for a subscription** (timer, utility): a tip jar (2 or 3 consumables) or several
  one-time "supporter" levels unlocking the same thing. A patron plan with no extra features also
  sells for indie apps with a loyal audience.
- **Kids apps**: subscription with trial, no ads, paywall at the start (the parent decides), and one
  touchpoint that shows the parent what the child did.

## 2. Paywall

**Where it appears** (map it in the PRD, `templates/prd.md`): end of onboarding, locked feature or
limit reached, a permanent "Go Pro" entry, campaigns (app open, push). Track **% of new users who saw
the paywall**: most trials start on install day (SOSA 2026: about 89%), and an app where only 40%
of people reach the paywall cannot convert the rest.

**Value before the paywall**: define in the PRD what "value" means for this app (a personalized
result, a projection with a date, the first real output). Ask questions in onboarding only if the
answers come back on screen.

**Content**
- Start plain: big title, 3 benefits, one strong button, solid light background. Add testimonials,
  video or animation only if a test asks for it.
- One plan pre-selected (usually annual), "see all plans" for the rest; judge it by revenue, not
  first conversion (showing all plans can raise conversion and drop annual share).
- **Honest trial**: a timeline ("Today: full access → Day 5: reminder → Day 7: charged") and the
  reminder **really scheduled** (local notification from the expiry date, or better, a server job
  that is cancelled when the trial ends). It reduces day-0 cancellations and justifies asking for
  notification permission. Button says "Start free trial", never "Buy".
- **Copy depends on eligibility**: a trial or intro price is valid once per subscription group on
  Apple; show "7 days free" only to eligible people (StoreKit and the subscription SDKs expose the
  check; Play returns only eligible offers). Otherwise the store charges full price and you get
  refunds.
- **Required on screen** (Apple, Play similar): subscription name, period, price for the period
  charged (and per-unit price if you show one), when it renews and how to cancel, "Restore
  purchases", links to Terms and Privacy. Apple has no Terms field: put the Terms link at the end
  of the store description.
- **Errors**: user cancellation is not an error (no "Purchase failed" toast). Log the low-level
  store message, not just the code. Check **active** entitlements, never "all entitlements".
  If the store does not return a plan, hide it and log; never break the screen.

**Rules and ethics**
- iOS: developers report rejections of the "free trial on/off" toggle paywall since January 2026
  (guideline 3.1.2 asks for a clear offer; the toggle is not named in it). Safer: the trial as an
  explicit separate plan.
- iOS: a second paywall with a discount when closing the first ("exit offer") gets rejected under
  5.6 inconsistently; on Android there are no reports. Never switch one on remotely after approval.
- Anything changed remotely (Remote Config, offerings, EAS Update) must be something that would pass
  review in that build: components already in the reviewed binary, no new screens or features.
  Hard vs soft paywall by flag breaks guideline 2.3.1 when the listing promises a free app.
- Declare running A/B tests in the review notes and keep all variants reachable in the build sent.
- The "would I accept this done to my grandmother?" test, using South Korea's banned patterns as a
  checklist: hidden renewal, price revealed in steps, pre-checked options, huge buy button with a
  hidden close, cancellation in many steps, repeated pop-ups to reverse a cancellation, fake
  countdowns.
- Check the paywall on a small screen, a foldable, large fonts, TalkBack/VoiceOver, and the longest
  translation.

**After the purchase** (most trial cancellations happen on day 0): a screen that confirms, reminds
what was unlocked and the person's goal, and gives **one** next step. Then a 7-day path to the first
"premium win" (push or email on day 0, 1 to 2, about 5).

## 3. Price

- **Set the main country's price by hand**: stores convert by exchange rate and tax, not purchasing
  power. Round to local patterns (R$ 49,90, not R$ 52,37); compare with the top 5 local competitors.
- **Annual in instalments**: Apple's monthly plan with a 12-month commitment (worldwide except the
  US and Singapore, iOS 26.4+, since May 2026) and Play installment plans (Brazil, France, Italy,
  Spain). The paywall shows the instalment and the total commitment. Apple's grace period does not
  apply to it.
- **Do not add the store fee** to the app price unless each user has a direct variable cost.
- **Raising price**: only with good retention and together with a concrete gain, announced as value.
  Google Play keeps existing subscribers on the old price (a legacy cohort) until you end it;
  increases are opt-in by default (users who do not accept are cancelled; you get 7 days to tell
  them first), and opt-out increases, allowed only in some places with limits, require an in-app
  notice. Apple has its own consent rules. Lowering is simple.
- **Testing price**: read results after 1 to 2 renewal cycles, by cohort revenue in the subscription
  service or your server. Firebase A/B Testing can split users, but its revenue counts devices and
  misses renewals with the app closed. The closed test validates the purchase flow, not the price.
- Pre-launch research: Van Westendorp (4 questions, 100+ answers per platform) and interviews that ask
  what people use and pay today, never "would you pay X?".
- Signs the price is low: trial start and trial conversion far above the norm. Retest every 6 months.

## 4. Offers, promotions and campaigns

| Need | How | Watch out |
| --- | --- | --- |
| Seasonal sale (Black Friday, New Year, the audience's own dates) | Apple: scheduled intro offer (one current and one future per storefront). Play: offers switched on and off by hand. Paywall variant switched by Remote Config with start and end dates | Never lower the product price (it lowers it for current subscribers). If a trial is eligible, it wins over the discount: pause it during the sale. Target the old free base too, with a no-discount control |
| Influencer, flyer, partner | Store offer codes distributed by URL or QR | Play subscription codes give a free trial (3 to 90 days); Apple offer codes follow the offer you configure. Neither is a coupon for "30% off" any plan |
| Bring back people who left | Apple win-back offers (shown in the App Store and Settings); Play offers for previous subscribers | Eligibility is configured in the store; the purchase may happen without opening the app (listen for it) |
| Reward current subscribers | Apple promotional offers (signed on the server with the subscription key) | The key downloads once: vault it on day one |
| Lifetime | Non-consumable at 5 to 12× the annual, as a one-off promotion or upsell | No trial, no price increases; on iOS it does not cancel an active subscription by itself: say so |
| Every campaign | Its own offer ID (`bf-2026`) | Clean cohorts; reuse by switching on and off |

Discount math before testing: 50% off that brings 20 extra buyers can lose more than it gains on the
100 who would pay full price. Aim discounts at people past the first days who have stopped
converting.

## 5. Involuntary churn: failed payments

Failed payments are a large share of cancellations, worse on Google Play (SOSA 2026: about 32% on
Play, 15% on the App Store). It is mostly configuration:

- **Apple**: turn on Billing Grace Period in App Store Connect (opt-in; 3, 16 or 28 days).
- **Google Play**: grace period is on by default and account hold lasts 60 days minus the grace
  period (since December 2025); for low-risk payments Play may keep access while it retries in the
  background. Call the Play in-app message (`showInAppMessages`, transactional category) on every
  app open: it shows the "fix your payment" snackbar. Some SDKs do it for you; check.
- **Model the states on the server**: active, in grace (keep access, show "update your payment"),
  on hold (no access, show the store's manage link), cancelled (access until expiry: cancelling is
  not expiring), expired, refunded. A subscription on hold disappears from the device's purchase
  query; only server notifications know it exists.
- **Pending purchases** (cash, bank transfer, Pix for one-time products on Play, some carriers): do
  not unlock, show "payment processing", unlock when the server confirms. Index by purchase token.
  Play Billing 8+ requires enabling pending one-time purchases explicitly.
- **Store hygiene** (only if you call the stores directly; the subscription SDKs do it): acknowledge
  Play purchases within 3 days or they are refunded; on every app open, reprocess unacknowledged
  purchases; treat "item already owned" as "restore", not as an error.
- A **global listener** for subscription changes, not only the return of the "Subscribe" button:
  purchases complete outside the flow (pending, bank authentication, "ask to buy", store-page offers,
  plan change in Settings).
- Track the **purchase failure rate** (started vs completed, by error code) before optimizing price.

## 6. Voluntary churn and win-back

- **"My subscription" screen**: plan, price, next charge, change plan, restore, support, cancel (deep
  link to the store's manage page) in at most 4 to 6 taps. Hard cancellation becomes 1-star reviews.
  Account deletion warns that the store subscription keeps charging and links to manage it.
- **One-question survey** before sending to the store, each answer mapped to an action: "don't need it
  now" → pause (Play) or reminder; "too expensive" → cheaper or annual plan; "didn't see the value" →
  guided setup; "technical problem" → support. Check usage in the 30 days before: if it had already
  collapsed, a discount will not fix a habit problem.
- **Apple retention messaging** (App Store Connect, no code; up to 10 messages per app): shown in
  the cancellation flow. The text cannot mention offers, discounts or prices; an attached offer
  needs a minimum paid duration you configure. Start with a value message: in early data,
  discounts were accepted rarely and brought less revenue per saved subscriber.
- **Play**: pause is enabled by default (1 to 4 weeks on weekly plans, 1 to 3 months on others):
  the natural answer to "I don't need it now". Add up to 4 subscription benefits (40 characters
  each) in the Play Console; Play shows them in the purchase and cancellation flows.
- **Refund requests (Apple)**: when the store sends a consumption request, answer within 12 hours
  with usage data (only with the customer's consent, stated in your terms). On Play, users can ask
  Google within 48 hours; after that, refunds are yours to grant. Never configure "always decline": it pushes
  people to bank chargebacks, which threaten the developer account.
- **Win-back timing**: right when auto-renew is switched off (the store notifies your server even if
  done in Settings), and again near expiry; for annual plans, find the day people typically switch
  off and act about 10 days before. In-app messages at that moment beat push and email.
- **Email with consent from day one**: the only channel that reaches people who uninstalled. A link
  to a web checkout **from email or your site** is allowed; from inside the app it depends on the
  country and store program (section 8).
- **Cancelled but still active**: show what they built and what they will lose, in context.
- **Annual**: about a third of annual subscribers switch off renewal in the first month; plan the
  first-month experience and a reminder before the yearly charge.

## 7. Server-side truth and security

- Entitlement decided by the server: the purchase webhook updates the account document and a custom
  claim; Firestore and Storage rules check the claim; paid files go out by short-lived signed URLs.
  App Check proves the request came from your app, not that the user paid.
- Signed responses from the subscription service (where available) instead of certificate pinning,
  against devices with a proxy that fakes "premium".
- Anonymous sign-in plus purchase is a trap: reinstalling creates a new user and the subscription
  "disappears". Either require a stable account before buying, or show "Restore purchases" and link
  the anonymous user to the account when it is created.
- Cache the last offer and entitlement with its expiry so the paywall and the gate work offline.
- The production server must accept **sandbox** purchases: Apple reviewers buy in sandbox.
- Apple (WWDC 2026): selling a subscription to groups and organizations is **on by default** for
  StoreKit 2 subscriptions without Family Sharing. Turn it off unless the app models seats.

## 8. Fees, countries and store programs

| Topic | Rule (check the day you decide) |
| --- | --- |
| Google Play subscriptions | Brazil and most countries: 15% from the first day. US, EEA, UK, Japan, Australia (since mid-2026): 10% + 5% billing fee |
| Apple, most countries | 30%; 15% in the Small Business Program (enroll) or after a subscriber's first paid year |
| Apple, Brazil (from iOS 26.5, mid-2026) | In-app purchase 26% (21% + 5% processing); 15% for small business or after year one. Alternative processor inside the app: 21% (10%). Link to web checkout: 15% (10%) on sales within 7 days of the tap. Both alternatives keep Apple's purchase shown at the same time and at least as prominently |
| Google Play, Brazil | No alternative billing program today; Pix only for one-time products |
| Selling outside the app | Website and email can always sell; linking or charging from **inside** the app depends on country and program (US link-outs, EU terms, Apple in Brazil, Google's billing choice in US, EEA, UK, Japan, Australia). Each keeps the store purchase alongside and adds reporting and fees |
| Small app | Stay on in-app purchase: in a public test, adding a web button returned less money per user (conversion drops more than the fee saves) and refunds grew |
| EU | Under the Digital Services Act, a trader's address, phone and email are shown on the EU product page (individuals may use a P.O. box). Without a trader status the app is not distributed in the EU |
| Product IDs | `<app>_<plan>_<period>_v1` in both stores: Play never lets you reuse a deleted ID, and the app prefix lets you transfer or sell the app later |
| Market restrictions | When a country restricts trials or renewals, serve a country-specific offer instead of removing the trial for everyone; watch revenue by country |

## 9. Metrics for a subscription app

Add to the weekly review in `recipe/15-after-launch.md` and the event plan:

- **Realized revenue per cohort** (paid per user at D7, D30, D90, D365) and payback, instead of a
  single LTV formula; churn is not constant (the curve flattens after year one).
- **First renewal rate by plan duration**: the biggest loss happens there; blended renewal hides it.
- **Trial → paid**, **refund rate** and **cancellations in the first hours** as guardrails on every
  paywall or price test: a "winner" that raises trials and refunds more is a loser.
- % of new users who saw the paywall; purchase failure rate; payment recovery rate.
- Hybrid apps (ads + subscription): one blended ARPU (ad ARPU × % free + paying ARPU × % paying).
- Cash: Apple pays within 45 days of the end of its fiscal month, Google around the 15th of the
  following month; a sale can take two months to reach the bank. Plan with the payment report.
