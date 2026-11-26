# 13. Monetization

**Gate:** test purchase (if subscriptions) and test ad (if ads) working in the development
build, with the server knowing each account's plan.

## Who charges, who holds funds, who only notifies

A subscription that unlocks digital features inside the app **is charged through the store** (Google Play
Billing and App Store). A gateway (Stripe, Asaas, Mercado Pago) inside the app gets the version rejected,
except under specific country programs that keep the store option alongside (`recipe/subscriptions.md`,
section 8); for a small app they rarely pay off. Your website and emails can always sell. Gateways
otherwise serve physical goods and services outside the app.

Model, paywall, price, offers and churn: `recipe/subscriptions.md`.

| Role | Who | Holds money? |
| --- | --- | --- |
| Charges, issues receipts, refunds, sales tax | Google Play / Apple | Yes; pays out to the bank account registered **in the store** (Google around the 15th of the following month; Apple up to 45 days after its fiscal month) |
| Says "this person has plan X until this date" | RevenueCat | No. Receives notifications from both stores, combines them into one format and sends a webhook. Free up to a monthly revenue cap |
| Gateway | Only outside the app | Yes |

Why RevenueCat: one API and one webhook for Android and iOS, test purchases without a store (Test
Store), receipts validated by them, refunds by API. Doing it yourself (Play Billing + StoreKit 2 +
validation + notifications from both stores) removes the fee but costs weeks. Adapty and Qonversion
serve the same role.

## Subscription: step by step

1. **Bank and tax details in the store**, not RevenueCat. Apple: Agreements → Paid Apps (bank, country
   tax registration, US tax form). Individuals in Brazil fill out **W-8BEN**;
   Brazil has no treaty with the US, so leave the treaty section blank. Same name in all
   fields. Without an active agreement, even the test purchase does not appear.
2. **Products with the same IDs in both stores**, prefixed with the app and versioned
   (`<app>_pro_monthly_v1`): a deleted Play ID can never be reused, and the prefix keeps the app
   transferable. On Apple, monthly and annual in the **same subscription group** and same level
   (switching becomes a "period change"); two tiers (Pro, Pro+) are different levels of one group.
   Family sharing off, and group purchases off unless the app has seats (on by default since 2026).
   Turn on Billing Grace Period.
3. **RevenueCat**: one app per store, products in the plan's entitlement, `$rc_monthly` and
   `$rc_annual` packages, webhook to the server. Public key through a build variable; test key blocked
   in production builds. The dashboard wizard creates generic entitlements and packages: check them
   against your plan decisions before coding.
4. **Apple**: In-App Purchase key in RevenueCat and server notification URL
   pointing to it. **Google**: service account with financial access and real-time
   notifications (Pub/Sub) configured through RevenueCat.
5. **Server**: SDK behind a port; account ID as `appUserID`; the server **does not trust the
   webhook payload**: fetches state and saves the event version to avoid going back in time.
   A plan may have several sources (store, complimentary access, free trial): combine them, never downgrade.

6. **Events**: `paywall_view` (with trigger and variant), `trial_start` and `purchase` only after the
   store or RevenueCat confirms. Revenue numbers come from RevenueCat and the stores, net of fees and
   refunds; analytics revenue is directional (`recipe/analytics.md`).

Traps: Apple's small business program lowers commission from 30% to 15% and is not
automatic (enroll). Limiting the app to countries where you sell avoids requirements from other markets.
Test these scenarios: subscribe, switch monthly → annual, cancel, refund, restore purchase, new
account on the same device, **trial copy for someone not eligible**, **pending purchase** (Play test
card "slow"), **failed renewal → grace → hold → recovery**, **downgrade deferred to renewal**,
**purchase made outside the app** (offer code, store page). Accelerated clocks: Apple sandbox renews
monthly plans every 5 minutes; Play license testers renew quickly and have cards that decline.

## Ads (AdMob)

For a routine or work app with a free plan:

- **Adaptive banner anchored to the footer**, above the tab bar. Full-screen ads pay 5 to 10 times
  more per thousand impressions, but interrupt people working and lead to uninstalls. Rewarded
  video only makes sense with an in-app "reward".
- **Few screens**: only lists people open often. Never on forms, payments, messages or
  pages seen by your user's end customer.
- **Scale first**: ads rarely pay for an indie app before thousands of daily users; early on, the
  banner mainly gives a reason to subscribe ("remove ads").
- **How much it earns**: Android banner in Brazil, estimated US$0.10 to 0.50 per thousand impressions
  (no official data; actual figures appear in the dashboard). One active user generates hundreds of impressions per month:
  cents. The goal is for the free tier to pay for itself and "ad-free" to become a reason to subscribe.
- **Categories**: you can block them (gambling, dating, politics), but cannot choose advertisers.
- **Required**: consent (UMP) before the first ad, requested when the first screen
  with ads comes into focus (not at app launch); "Contains ads" in the listing; Data Safety covering what the
  SDK collects; **test ad unit in development** (clicking a real ad gets the account suspended).
- SDK behind a port (`AdsPort`), empty web version; check that the SDK is not in the web
  bundle.

## Rough calculations

| Item | How to estimate |
| --- | --- |
| Cost per user | Firebase (reads, writes, Storage, Functions) with expected usage; almost always cents |
| Store fee | Play subscriptions 15% (10% + 5% in US, EEA, UK, JP, AU); Apple 15% (small business or after year one) or 30%; Apple Brazil 26% standard (`recipe/subscriptions.md`) |
| RevenueCat | Free up to a monthly revenue cap; then a percentage |
| EAS | Free plan with a build limit; paid plan when it runs out |
| Fixed costs | Play (one-time fee), Apple (annual), domain |
| Break-even point | Fixed costs ÷ net revenue per paying user |

Launch price as a hypothesis: the closed test checks the purchase flow and willingness to pay;
price is only read after launch, over 1 to 2 renewal cycles. Cooling-off period and refund policy
written in the terms.
