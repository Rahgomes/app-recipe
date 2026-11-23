# Explorer tester personas

Each persona is a way of using the app that scripted tests do not cover. Run 3 to 5 per
round, chosen based on what the batch changed. Names and profiles are fictional.

| id | Who they are | Device (web / Android) | Looks for |
| --- | --- | --- | --- |
| `senior-reader` | Age 62, reads everything, unfamiliar with jargon | 360x740 / font 1.3 | Technical text, button that does not explain its action, step that assumes knowledge |
| `in-a-hurry` | Age 24, skips text, taps quickly, goes back midway | 393x852 dark / dark theme | Double tap, going back while saving, lost state, dark theme |
| `low-vision` | Uses huge fonts and contrast | zoom 1.5 / font 2.0 | Cut-off text, button pushed offscreen, contrast, small target |
| `budget-phone` | Cheap phone, small screen, poor network | 360x640, slow network / 720x1280 emulator | Loading without feedback, screen that does not fit, button under the keyboard |
| `tablet` | Opens on a tablet | 800x1280 / tablet emulator | Stretched layout, wasted space, orientation |
| `offline` | Loses the network midway | 393x852 / any | Saving offline, error message, resuming when back online, duplicate data |
| `other-language` | Phone in English, dark theme | en-US dark / app language en-US | Untranslated text, wrong date, number and currency formats |
| `skeptic` | Reads terms, denies permissions, wants to leave | 393x852 / any | Denied permission (notification, camera, location), privacy, delete account, cancel subscription |

Default mission (no brief): complete onboarding to the main screen and accomplish the app's main
goal as this person would. With a brief: the brief's mission, in the persona's style.

Data the persona types: always fictional. Email `test+<persona>@example.com` (reserved domain,
never delivers), invented name and phone number, store test card. A test account created for
this purpose, never yours.
