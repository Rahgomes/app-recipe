# 12. Build or over the air (EAS Update)

**Rule:** OTA updates are the default way to deliver changes to phones. A new build costs
EAS credit (about US$1 per Android build on the paid plan), takes 15 to 30 minutes and forces
testers to reinstall. One of our apps used 11 builds before getting EAS Update.

**`expo-updates` goes into the first build of every app**, not "at launch".

## Which path

| What changed | Path |
| --- | --- |
| Screen, text, logic, new route, image used by code, font loaded at runtime (`useFonts`) | **OTA** |
| New library with native code, plugin, permission, icon, splash, name, `app.config`, Firebase config, SDK version, font embedded by the `expo-font` plugin | **New build** |
| App `package.json` or lockfile | New build, even if it looks like tooling only |
| Only Functions, rules, site, Remote Config | Neither: separate deployment |

## Configuration

- Channels linked to `eas.json` profiles (`preview`, `production`).
- `runtimeVersion`: two policies that work.
  - `appVersion` (the one we use): runtime is the app's `version` (`expo.version`, e.g. 1.2.0).
    EAS `autoIncrement` only raises `versionCode`/`buildNumber` and **does not change the runtime**. So:
    for every build with a native change, bump `expo.version`; and the **guard** below refuses OTA
    publishing when something native has changed since the last build.
  - `fingerprint`: runtime is a hash of native inputs and changes when they change. It protects
    without relying on remembering to bump the version; a build without native changes keeps the same runtime.
- EAS Update code signing enabled before launch.
- Rollback documented (`eas update:rollback` or republish the previous update).
- Backend always compatible with the previous app version: people take time to update.

## The guard

Tag each build's commit (`preview-build-<n>` or `android-build-<versionCode>`).
Before publishing OTA, compare changes since the tag against the list of native paths. Ready-made script
in `tools/ota-or-build.sh`:

```bash
tools/ota-or-build.sh --check     # OK for OTA, or BUILD REQUIRED with the list
```

The script should also check that the exported bundle has the correct environment settings
(e.g. the production OAuth client ID) before publishing.

## In practice

- Do not generate builds "just in case". The first sets up the foundation; from then on, use OTA until
  a native change appears.
- Unavoidable build: combine pending changes in the same build.
- Updating dependencies changes the lockfile and requires a build: group it with the next planned build.
- On the phone: the app downloads on opening and applies on the next launch (fully close and reopen).
- **About** screen with version, build number (`expo-application`, not `app.config`), active
  update ID and channel, with a copy button for support. This distinguishes two people "on
  1.0.0".
- New-version notice: Remote Config with the latest store build compared against the installed one.

## Generate the build

```bash
eas build --profile development --platform android   # dev, once
eas build --profile preview --platform android       # testers
eas build --profile production --platform android    # store (AAB)
```

Production: `"appVersionSource": "remote"` and `"autoIncrement": true` in `eas.json`.
