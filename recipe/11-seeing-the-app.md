# 11. Seeing the app during development

| Option | Shows | Data | Requires | When |
| --- | --- | --- | --- | --- |
| **1. Browser (Expo Web)** | Layout and navigation | Fictional, in memory | Nothing | Every day, new screen. The fastest |
| **1b. Published preview** | The same, through a link | Fictional | Nothing | Show someone, view on a phone |
| 2. Expo Go | The app on a phone | | Expo Go app | **Only before the first native module** |
| **3. Dev build + Firebase Emulator** | The real app | Local test database | Dev build installed once; emulator or phone over USB | Feel touch, keyboard, performance without a Firebase account |
| 4. Dev build + Firebase dev | Same | Real dev project | Dev project created | Phone on any network |
| 5. Test build (preview) | Standalone app, no dev server | Firebase dev | | Send to testers |

## Step by step

### 1. Browser

```bash
pnpm -C apps/mobile web          # opens on port 8081
```

When developing on a remote machine (VS Code Remote-SSH), the **Ports** tab forwards automatically.
Open `http://localhost:8081`, F12, mobile mode.

### 1b. Published preview

```bash
cd apps/mobile && npx expo export --platform web && eas deploy --alias preview
```

An alias keeps the link fixed. The link is public: **fictional data only**, never real Firebase.
A tip that helped a lot: `?demo` in the URL opens a ready account with months of fictional data,
for reviewing screens that depend on history (finances, reports).

### 3. Development build with the Emulator

Once: install the APK from the EAS link. Each session:

```bash
pnpm emulators                              # Firebase Emulator
pnpm -C apps/mobile start --dev-client      # Metro
```

With a phone connected over USB (USB debugging) or the Android Studio emulator:

```bash
adb reverse tcp:8081 tcp:8081      # Metro
adb reverse tcp:<port> tcp:<port> # one per Emulator service (Firestore, Auth, Functions)
```

Check that another project is not using the Emulator ports before starting.

## What each option does not show

- The web does not show: blur, haptics, background behavior, SVG with percentage width (on Android
  it rendered only halfway), large system fonts. Web background images need explicit 100%
  `width`/`height`.
- A new dev build is needed only when a **native library** is added. Screen changes arrive through Metro.
- EAS free build queue: minutes to an hour. Request it ahead of time.

## Check the screen

Before showing someone: 375×667, 412×915 and 430×932. A full-page screenshot hides clipping at the
fold. A Playwright spec just for screenshots (outside the suite) revealed an invisible ring in dark
mode and content hidden under the footer.
