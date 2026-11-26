# Fast app: a performance recipe

**What this is for:** a checklist of the technical decisions that make an app feel fast, with
what to do in React Native + Expo + Firebase and the equivalent elsewhere. Read it when you set up
the foundation (stage 8), when you write the brief for a batch (stage 9), and before the closed
test (stage 14). A slow app rarely needs a bigger server. It usually comes down to a few decisions
made early in the code.

Thresholds and tool details were checked on official pages in November 2026. Check again before
relying on them.

## Budgets: decide them in the PRD

Write the targets in the technical review (stage 3) as a D##, so "fast" can be measured.

| What | Target | Store alert threshold |
| --- | --- | --- |
| Cold start (tap to first screen), mid-range Android | Under 2 s; Android's own goal is 500 ms | Android vitals flags 5 s cold, 2 s warm, 1.5 s hot |
| Response to a tap | Visible change within 100 ms (pressed state, skeleton, optimistic update) | |
| Scrolling and animation | 60 fps, no frozen frame (over 700 ms) | Slow and frozen frames in Android vitals and Firebase Performance |
| Screen with data | Cached data on screen at once; fresh data within 1 s on 4G | |
| Web pages (site, public profile) | LCP 2.5 s or less, INP 200 ms or less, CLS 0.1 or less, at the 75th percentile | Core Web Vitals in Search Console |
| App size | Track it per build; justify every jump over a few MB | |

## Measure the right thing

- **Release build on a real mid-range Android phone.** A development build runs in debug mode and
  is several times slower; the web preview and a fast laptop hide every problem.
- **Slow network on purpose**: Chrome DevTools throttling for the web, the Android emulator's
  network profile, Network Link Conditioner on iOS. Also airplane mode: the cached path must work.
- **Measure before and after** each optimization and write the number in the journal. An
  optimization without a number is a guess.
- **Real users beat the lab**: lab tests find problems; field data (vitals, RUM) says which ones
  people actually hit.

## The checklist

Each row: what to do, then how in the reference stack, then the equivalent elsewhere.

### 1. Perceived speed

| Do | React Native + Expo + Firebase | Elsewhere |
| --- | --- | --- |
| **Skeleton while loading**, in the shape of the content, never a lone spinner | A `Skeleton` in the design system (stage 5); only the reads the screen needs hold it | Same idea on web: placeholders with fixed size (no layout shift) |
| **Update the screen without waiting for the server** (optimistic UI) | Firestore writes to the offline cache first and syncs later; show a discreet "syncing" state, roll back on error | TanStack Query `onMutate`, SWR `mutate` |
| **Show cached data first, refresh in the background** | Firestore persistent cache; `fromCache` tells you the data may be stale | Stale-while-revalidate |
| **Stream AI answers token by token** | Streaming callable when your client SDK supports it; otherwise an HTTP function with server-sent events | SSE or a streaming fetch |
| **Debounce search and autocomplete** (250 to 400 ms) and cancel the previous request | `setTimeout` in a hook, or `useDeferredValue` for local filtering | Same; `AbortController` cancels the stale request |
| **A secondary read never blocks the screen** | If the review or the history fails, the main content still shows, with its own retry | |
| **Splash only until the first real frame** | Hold the splash while auth and the first cached read resolve, then hide it; never wait for the network | |

### 2. Images, fonts and static files

| Do | React Native + Expo + Firebase | Elsewhere |
| --- | --- | --- |
| **Resize on the phone before upload**, one size per use, never upscale | `expo-image-manipulator`: e.g. 1600 px for full view, 400 px thumbnail, 512 px logo | Sharp or an image CDN on upload |
| **Modern compression** | JPEG at about 0.75 quality is the safe default on every device and in every browser. WebP saves more; AVIF more still, but check decoding on the oldest OS you support | Serve AVIF or WebP with a JPEG fallback (`<picture>`) |
| **Strip metadata**: EXIF and GPS leak location and add weight | Re-encoding with the manipulator drops it; test it with a photo that has GPS | Same on the server |
| **Cache images on the device** and show a placeholder | `expo-image` with `cachePolicy="memory-disk"`, a blurhash or color placeholder, a short fade (none with "reduce motion") | `loading="lazy"`, `decoding="async"`, width and height set |
| **Lazy load images off screen** | Lists only render what is visible (section 3); prefetch only the next screen's hero image | `loading="lazy"` on everything below the fold |
| **Long cache for static files**, with versioned names | Storage files: set `Cache-Control` metadata on upload; a new file gets a new name instead of being overwritten | `Cache-Control: public, max-age=31536000, immutable` on hashed files |
| **Static files from a CDN** | Firebase Hosting already serves from a CDN | Cloudflare, Vercel, CloudFront |
| **Compression with Brotli or gzip** | Firebase Hosting does it automatically; check the `content-encoding` header | Turn it on in the server or CDN |
| **Few font weights, bundled** | Embed fonts at build time with the `expo-font` config plugin; two or three weights | Self-host with `font-display: swap`, subset, preload the main one |

### 3. Lists and rendering

| Do | React Native + Expo + Firebase | Elsewhere |
| --- | --- | --- |
| **Virtualize long lists**: anything that can pass about 30 rows | FlashList (v2 needs the New Architecture and no longer asks for item size estimates) or FlatList; never `ScrollView` + `map` | `react-window`, TanStack Virtual |
| **Paginate**: every query has a `limit` | `limit()` + `startAfter()` cursor; "load more" at the end of the list | Cursor pagination, not offset, on big tables |
| **Avoid needless re-renders** | React Compiler (on by default in new Expo projects since SDK 54; check `experiments.reactCompiler`); zustand selectors instead of one big context; stable `keyExtractor` | Same; measure with the React DevTools Profiler first |
| **Animations off the JS thread** | Reanimated worklets and Gesture Handler; heavy work after the transition finishes | CSS `transform` and `opacity` only |
| **No logs in production** | Strip `console.*` in the release build; they cost time on the bridge and leak data | Same |

### 4. Startup and bundle

| Do | React Native + Expo + Firebase | Elsewhere |
| --- | --- | --- |
| **Remove unused dependencies** | knip in CI (stage 8); one library per job | `depcheck`, bundle analyzer |
| **Look at what the bundle carries** | Expo Atlas (`EXPO_ATLAS=true npx expo start`) shows each module's weight | `source-map-explorer`, the bundler's analyzer |
| **Load heavy modules only when needed** | Import the PDF, chart or camera module inside the screen that uses it; check `inlineRequires` is on in Metro | Split JavaScript per page (route-level code splitting, `import()`) |
| **Do less at startup** | No network call, no large JSON parse and no SDK initialization that can wait before the first frame; Hermes and the New Architecture on | |
| **Third-party scripts after the page** | Ads and analytics SDKs initialize after the first screen and after consent | `defer`/`async`, load after interaction, Partytown |
| **Render on the server or at build time** | For the app's site and public pages: static generation, with a function filling in only what changes | SSG/ISR/SSR (Next, Astro) |
| **Smaller download from the store** | Android App Bundle; `expo-build-properties` with R8 and resource shrinking; images in the right density | |

### 5. Network and API

| Do | React Native + Expo + Firebase | Elsewhere |
| --- | --- | --- |
| **No duplicate calls**: one source per piece of data | One `onSnapshot` listener per feature, in a hook, unsubscribed on unmount (leaked listeners cost reads and battery) | Request deduplication (TanStack Query, SWR) |
| **Fire independent requests in parallel** | `Promise.all` for reads that do not depend on each other; never a chain of awaits | Same |
| **Timeout on every external API** | `AbortSignal.timeout()` in functions; a function timeout shorter than the client's wait; a clear error and a retry | Same, plus a circuit breaker for flaky providers |
| **Ask only for the fields you need** | The Firestore client always reads whole documents: keep list documents small, put heavy fields in a subcollection or a detail document | `SELECT` only the columns used; GraphQL or sparse fieldsets |
| **Count without reading everything** | `getCountFromServer` (and sum or average where your SDK has them) instead of loading the collection | `COUNT(*)` in the database |

### 6. Server and data

| Do | React Native + Expo + Firebase | Elsewhere |
| --- | --- | --- |
| **Fix N+1 queries** | Copy what a list shows into the document when it is written (the name on the appointment), so one read serves the list | Joins or batch loading (DataLoader) |
| **Precompute what screens filter on** | A trigger writes a derived field on each write (e.g. `amountDue`), so the app queries `amountDue > 0` instead of scanning history; heavy counts in a nightly job | Materialized views, counters |
| **Indexes for the common queries** | `firestore.indexes.json` in the repo, deployed with the rules; the query error names the missing index | `EXPLAIN` the slow query, then index |
| **Slow work goes to a queue** | Return at once and let a trigger, Cloud Tasks or Pub/Sub do the email, the PDF or the AI call; the app watches the status document | BullMQ, SQS, Celery |
| **Cache what everyone reads** | A summary document the server rebuilds; globals in the function instance for config | Redis in front of the hot queries |
| **Reuse connections** | Create SDK clients at module scope in functions, not per call | A connection pool (PgBouncer, the driver's pool) |
| **Server close to the database** | Functions in the same region as Firestore and Storage, near the users | App server and database in the same region |
| **Cold starts and load** | `minInstances` only for the function on the critical path, and only if the cost is worth it; functions scale out by themselves | Several instances behind a load balancer; autoscaling |

### 7. Measure in production

| Do | React Native + Expo + Firebase | Elsewhere |
| --- | --- | --- |
| **Monitor real users' speed** | Firebase Performance Monitoring (app start, screen rendering, network) plus Android vitals and Xcode Organizer | Sentry, Datadog RUM; `web-vitals` library for the site |
| **Trace slow requests end to end** | Cloud Trace for functions; custom traces around the slowest journeys | OpenTelemetry to Jaeger, Grafana Tempo or Honeycomb |
| **Alert on regressions** | Compare each release with the previous one before the next rollout step (stage 15) | Performance budgets in CI |

## Tools that help, in parallel

| Tool | Measures | Cost |
| --- | --- | --- |
| React Native DevTools (Profiler, Performance panel) | Renders, slow components, JS thread | Free |
| Expo Atlas | Bundle contents and weight per module | Free |
| Android Studio profiler, Perfetto | CPU, memory, startup, jank on a real device | Free |
| Xcode Instruments | Time Profiler, Hangs, Allocations on iOS | Free |
| Flashlight | A performance score for Android apps, also in CI | Free, open source |
| Reassure | Render time regressions in component tests | Free, open source |
| Maestro | Repeatable journeys to time before and after | Free CLI |
| Firebase Performance Monitoring | Field data: startup, screens, network | Free |
| Lighthouse, PageSpeed Insights, WebPageTest | Web pages: Core Web Vitals, waterfall | Free |
| k6 | Load on your API or functions before a launch | Free, open source |
| OpenTelemetry | Traces across app, API and database | Free standard; the backend may cost |
| Sentry | Errors and performance in one place | Free developer tier |

## Directives to give your agent

Paste this into the brief of every batch (stage 9) or the project's agent instructions:

```text
Performance rules for this app:
- Every screen that loads data shows a skeleton in the content's shape and cached data first.
- Writes update the screen at once (optimistic) and show a sync state; errors roll back.
- Every query has a limit; lists that can pass 30 rows are virtualized and paginated by cursor.
- Images are resized and compressed before upload, cached on the device, with a placeholder.
- No duplicate requests: one listener or query per piece of data, cleaned up on unmount.
- Independent requests run in parallel; every external call has a timeout and a retry.
- Search and autocomplete are debounced and cancel the previous request.
- Slow work (email, PDF, AI) goes to a background job; AI answers stream.
- Heavy modules load inside the screen that needs them; nothing slow runs before the first frame.
- New dependency only if nothing in the project already does it; report its size.
- Report the before and after numbers for anything you optimized.
```

## Where it fits in the recipe

| Stage | Performance work |
| --- | --- |
| 2 PRDs | Budgets per journey; which lists can grow without limit |
| 3 Technical review | Budgets as D##; regions; which work goes to a queue |
| 5 Design system | Skeleton, placeholder and pressed states as components |
| 8 Foundation | Persistent cache, image helper with sizes, list component, knip, React Compiler, Performance Monitoring |
| 9 Batches | The directives above in each brief; the reviewer checks limits, listeners and lists |
| 10 Tests | Release build on a mid-range phone and slow network for the batch's journeys |
| 14 Stores | Pre-launch report and vitals read before the closed test |
| 15 After launch | Field data each week; a release that got slower does not advance in the rollout |
