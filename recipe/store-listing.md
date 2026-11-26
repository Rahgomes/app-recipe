# Store listing: get found and turn views into downloads

Part of stage 14, but start early: screenshots depend on finished screens and good fictional
data, and the listing changes conversion without changing a line of app code. In one public case, the same app
went from 700 to 5200 installs just by changing screenshots (a designer's account, without a methodology;
use it as inspiration, not a promise).

Store rules change: the facts below were checked on official pages in November 2026.
Check again on submission day.

## 1. Before visuals: where the funnel loses people

Address the right stage, in this order:

| Symptom | Problem | Action |
| --- | --- | --- |
| Broken link, app unavailable in a country or on a device, wrong price | Availability | Fix in the console |
| Few people see the listing | Discoverability (ASO) | Section 2 |
| Many visits, few installs | Listing does not convince | Sections 3 to 6 |
| Installs and leaves, or does not pay | First experience | Stages 9 and 13; screenshots cannot save poor onboarding |

Measurement: Apple only shows data from 5 first-time downloads in the period (missing data
is not zero); on Play, the listing report counts **clicks** (install, open, pre-register),
not completed installs.

## 2. Get found (ASO)

| | App Store | Google Play |
| --- | --- | --- |
| What search reads | Title, subtitle, keyword field, primary category; then behavior (downloads, ratings, reviews) | Title, short description and full description |
| Limits | Title 30, subtitle 30, keywords 100 **bytes** (an accented character counts as 2) | Title 30, short description 80, full description 4000 |
| Useful techniques | Comma-separated words without spaces; do not repeat what is already in the title, subtitle, company name or category; singular or plural, just one | Natural keyword wording in the short description and the beginning of the full description |
| Page by search | Custom Product Page with its own keywords appears instead of the default (up to 70) | Custom store listing by keyword, country or campaign (up to 50) |

- **Research how users search**: autocomplete in both stores, competitors from stage 1 and
  their reviews (the words people use when complaining). A list with estimated volume and difficulty
  helps; paid tools are optional.
- **Title**: brand + what it does, if it fits ("Routine: daily habits"). No "#1", "best",
  price or promotion: both stores reject them.
- **Localization affects ranking**: each language has its own keyword list; do not translate the list, research
  it again. Apple indexes metadata by country.
- Apple generates **AI tags** from metadata: clear text about what the app does helps.
- Rating and review volume affect ranking and decisions: see section 7.

## 3. Convert: the first screenshots decide

Apple search shows up to **3 screenshots or videos** before any tap; Play asks you to
prioritize the interface in the **first 3**. Only a minority scroll the gallery (older market studies
put it at ~13%). So:

1. **Contrast that stops scrolling**: first and last screenshot in a strong brand color, a dark one in
   the middle. Next to competitors on light backgrounds, the block of color catches the eye.
2. **Title readable in half a second**: 2 to 4 words, a benefit rather than a feature, with the keyword
   highlighted (another font, italics, color). A large number ("21 days", "30 s") works as a title.
3. **A story, not isolated cards**: screenshots form a panorama; an element crosses the
   edge and draws the eye to the next. The app extends outside the frame: tilted phone, a piece of the
   interface (button, card, sticker) floating above it.
4. **People see themselves using it**: a screen with realistic fictional data for the audience ("Walk 20 min"), not
   an empty screen, login or splash.
5. **Suggested order**: promise → how it works → proof (number, result) → distinguishing
   feature → offer (plan, free trial in text, no price in the image).

Always read the **thumbnail** (1/4 size): if the title is unreadable there, it is unreadable in search.

## 4. What each store rejects

| Rule | App Store | Google Play |
| --- | --- | --- |
| App in use | More than half the screenshots show the app in use (2.3.3); text overlays are allowed if they do not obscure the app | Prioritize the interface in the first 3 |
| Price and promotion | Prices and terms prohibited in screenshots (2.3.7) | No "Free", "Sale", "Discount", "#1", "Best", "New" in the feature graphic; no ranking or price in the icon and title |
| Call to action | Avoid making the whole screenshot a CTA or award | "Download now", "Install now", "Try now" prohibited |
| Device frame | Allowed (generic) | Avoid devices and hands holding devices: they age quickly |
| Text in the image | Readable | Up to 20% of the image; no small fonts or backgrounds that compete with text |
| Other platforms | No Android status bar, name or icon (2.3.10) | No other store brands |
| Data | Fictional account, never a real person's data (2.3.9) | Same (privacy) |
| In-app purchase | Indicate what is paid for separately (2.3.2) | Consistent with the listing |

## 5. Sizes and counts

| | App Store | Google Play |
| --- | --- | --- |
| Screenshots | 1 to 10 per screen size and language | 2 to 8 per device type |
| Size | iPhone 6.9": 1320 x 2868 (Apple scales down for smaller sizes); iPad 13": 2064 x 2752 if it runs on iPad | 9:16 recommended; side length from 320 to 3840 px; at least **4 screenshots at 1080 px** to qualify for large placements |
| Format | PNG or JPEG, **no transparency** | PNG or JPEG, up to 8 MB |
| Extras | Icon comes from the binary | 512 x 512 icon and 1024 x 500 feature graphic required; alt text up to 140 characters per screenshot |
| Video | Up to 3, 15 to 30 s each, app recordings only, plays muted | 1 from YouTube, no ads; first 30 s play muted |

## 6. How to produce them (recipe workflow)

1. **Real screenshots** of screens with good fictional data (demo account or
   Emulator seed). Clean status bar:
   ```bash
   # Android (emulator or device)
   adb shell settings put global sysui_demo_allowed 1
   adb shell am broadcast -a com.android.systemui.demo -e command enter
   adb shell am broadcast -a com.android.systemui.demo -e command clock -e hhmm 0941
   adb shell am broadcast -a com.android.systemui.demo -e command battery -e level 100 -e plugged false
   adb shell am broadcast -a com.android.systemui.demo -e command notifications -e visible false
   adb exec-out screencap -p > screens/pt-BR/01.png
   # iOS (simulator, requires a Mac)
   xcrun simctl status_bar booted override --time 9:41 --batteryLevel 100 --cellularBars 4
   xcrun simctl io booted screenshot screens/pt-BR/01.png
   ```
   Without a Mac: screenshots from a real iPhone, or crop the status bar from Android screenshots and check that
   the screen has no Android elements (2.3.10). Maestro (`takeScreenshot`) automates the sequence.
2. **Stickers** (character, sticker, object, background): AI-generated (Codex or another tool) with a transparent
   background, or cut from the interface itself. AI **does not** draw the interface or screenshot
   text: an invented interface fails review (2.3.3) and AI text comes out with errors.
3. **Assembly through code**: `tools/store-listing/listing.py listing.json` assembles the panorama, crops
   to both stores' sizes, generates the Play feature graphic, alt text and thumbnail
   preview, and warns about contrast below 4.5:1, titles over 20% on Play and words the stores
   reject. Ready-made example in `tools/store-listing/example/` (fictional app). New language = text
   in the JSON + screenshots in `screens/{language}/`.
4. **Check**: `screen-checker` in store listing mode on the thumbnail preview (criteria in the
   agent). Adjust the JSON and run again; do not edit PNGs by hand.
5. **Submission**: Play through the API (service account, `recipe/automation-by-api.md`); Apple through App
   Store Connect or `eas metadata` (listing text and configuration in a versioned file).
6. **Version** `listing.json` and screenshots in the repository (`docs/store/`): changing a sentence becomes
   a commit, and an A/B test variant becomes another JSON.

## 7. What the code needs (plan in stage 9)

- **Review request** (`expo-store-review`) right after a task succeeds
  (saved, finished, received the result). It can be in the first session, after the first valuable
  action. Not at launch or inside onboarding (Apple's guidance; developers report rejections), never
  after an error or failed purchase, and only through the system prompt: Apple disallows custom
  review prompts (5.6.1) and Google's in-app review guidelines forbid asking questions before it. The system limits display (iOS: 3 times per year); record when you
  asked and do not ask again too soon.
- **Reply to reviews** in both stores, negative ones first; the reason becomes a B## in the backlog.
- **Funnel events** in analytics: first open, first valuable action (activation), paywall
  viewed, purchase started and completed. Without these, you cannot tell whether the problem is the listing or the app.
- **Direct link** to custom pages (Apple: Custom Product Page URL; Play: `&listing=`)
  leading to the right app screen when appropriate.

## 8. After publishing

Listing A/B tests, pages by audience and review routine: `recipe/15-after-launch.md`,
"Improve conversion" section.

## Official sources (checked in 11/2026)

- Apple: screenshot and preview specifications (App Store Connect Help), Product page, Search,
  Product Page Optimization, Custom Product Pages, App Review Guidelines 2.3 and reference 2.3.3,
  Asset best practices. At developer.apple.com/app-store/ and developer.apple.com/help/.
- Google: Store listing graphic assets (Play Console Help 9866151), Metadata policy (9898842),
  Asset best practices (13393723), Store listing experiments (6227309), Custom store listings
  (9867158). At support.google.com/googleplay/android-developer/.
