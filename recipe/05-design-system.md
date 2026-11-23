# 05. Lightweight design system

**Goal:** the same values in images and code. **Gate:** `tokens.ts`, `DESIGN-SYSTEM.md` and the
screen base prompt have the same values; contrast measured in a test.

## Why lightweight and why before code

Tokens + about 10 components + one document. Storybook and a full catalog only when a second
app or team uses the kit. This comes before code because if the image and token diverge, the
implementer copies the image and the token becomes decoration.

## Tokens (`src/theme/tokens.ts`)

| Group | Content | Rule |
| --- | --- | --- |
| Color by **role** | `primary`, `onPrimary`, `background`, `surface`, `text`, `textMuted`, `border`, `success`, `warning`, `danger`, `focus` | Never a bare hex in a component; lint blocks fixed colors |
| Dark theme | Same roles, different values | Starts with roles even if dark mode comes later |
| Typography | `display`, `title`, `body`, `label`, `caption`; numbers with `tabular-nums` | Respect large system fonts |
| Spacing | Scale of 4: 4, 8, 12, 16, 24, 32, 48 | Side margin 16 or 20 |
| Radius | `sm 8`, `md 16`, `lg 24`, `pill 999` | |
| Touch | Minimum target 44 to 48 | `hitSlop` does not count on the web: measure the actual target |
| Status | Fixed vocabulary: text + icon + color | Never color alone; the same words in the prompt, code and tests |

**Contrast in an automated test** (`theme.test.ts`): normal text at least 4.5:1, target 7:1;
field borders and icons 3:1. Test every palette if users can choose a color. A gradient glow
effect dropped white text contrast to 3.2:1 in three palettes; lightening was changed to stop
automatically at the limit.

## Base components

`Text`, `Button` (primary, secondary, text; loading), `IconButton`, `TextField` (label, help,
error, counter), `Select`, `Chip`, `Card`, `ListRow`, `StatusPill`, `Avatar`, `Banner` (offline,
info, error), `EmptyState`, `Sheet`, custom `Switch`, `Screen` with fixed footer, loading skeleton.

Rules that came from bugs:
- Kit components **do not accept arbitrary color `style`**, only variants. An agent passed
  `style` to a button and it became a strip.
- Default text in the kit is neutral (hardcoded "or" in a divider became a bug on every new screen).
- Custom `Switch`: the native one looks different across platforms and lacks contrast when off.
- A heading is also an accessibility role (`accessibilityRole="header"`).
- On the web, `accessibilityState` does not become `aria-checked`/`aria-pressed`: switches and
  chips need explicit `aria-*` attributes.
- Always place an icon in a box matching its size: the icon font arrives later and the layout
  jumps (the test clicked where the button used to be).

## Screen sizes

- Main action pinned to the footer (`Screen` with `footer`): the button disappeared on short phones.
- `useCompact()` for height < 720.
- Check at 375×667, 412×915 and 430×932, and with the **system font at maximum size**.
- Tab bar on edge-to-edge Android: height **adds** `useSafeAreaInsets().bottom`, or it sits
  underneath the gesture bar.

## Styling: which library

| Option | When |
| --- | --- |
| **StyleSheet + typed tokens** | Default: zero native dependencies, easy migration |
| Unistyles | Many screens with a dark theme, tablet, or measured stuttering during theme changes |
| NativeWind | Team that thinks in Tailwind, **if** support for the current Expo SDK is confirmed |
| Tamagui | Universal web + native app with a full design system |

## Third-party component library

Worth it for what it improves in the task. Evaluate component by component: many use blur
(expensive on Android) and do not respect "reduce motion". Decide adjustments once (motion hook,
solid background on Android) and copy only what the screen uses.
