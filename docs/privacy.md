# Privacy Model

Hoshiyar Shield handles the most sensitive text people have: messages about their money. The rule is
simple: **analysis happens on the phone, and nothing leaves it.**

## What we collect
**Nothing is sent to us or to anyone.** There is no account, no analytics SDK and no backend in this MVP.

## On-device processing
- The classifier, warning-cue engine and URL analyser are bundled JavaScript plus a JSON model. Analysing a
  message makes **no network request** (tested: `analyze.test.ts` "works offline", and the UI test asserts
  `fetch` is never called during a scan).
- Links are **never opened, fetched or resolved**. Only their text is inspected.

## Permissions
`app.json` explicitly **blocks** READ/RECEIVE/SEND_SMS, READ_CONTACTS, READ_CALL_LOG, READ_PHONE_STATE,
RECORD_AUDIO, CAMERA, location, SYSTEM_ALERT_WINDOW and legacy storage. The generated manifest keeps:
- `INTERNET`: part of the Expo/React Native runtime (used by development tooling). The app's features don't use the network.
- `VIBRATE`: haptic feedback.

The app never reads SMS in the background. The user chooses what to paste.

## What is stored on the phone (AsyncStorage)
| Key | Content | Default |
|---|---|---|
| `hs.prefs.v1` | onboarding done, "save recent checks", "demo mode" | created at onboarding |
| `hs.history.v1` | last 12 checks: type, risk level, **48-character preview** | **off**; only if the user enables "Save recent checks" |
| `hs.reports.v1` | reports the user saves: number/link host, category, optional description, **message text only if the user switches "Attach the analysed message text" on** | empty |

"Delete all data on this phone" (About → Settings) wipes all three keys.
The current message is held in memory only, to show the result screen.

## Reports and accusations
- A report is an **unverified claim**. The UI says so, and the reputation wording is "N reports describe
  suspicious … associated with this number". It never says "fraudster".
- Public/aggregate views mask numbers (`0399-55•••42`).
- Demo reputation records are synthetic and use the fictional `0399-555xxxx` range.
- The report form rejects CNIC/card-like numbers in the free-text description.

## If a backend is added later (not built)
- Upload only **explicitly consented** reports, never by default. Strip or hash message text unless the user opts in.
- Server-side validation, rate limiting and abuse detection. Store only masked or hashed numbers in public aggregates.
- Publish a retention policy. Comply with Pakistan's data-protection requirements once enacted and with bank/regulator rules.
