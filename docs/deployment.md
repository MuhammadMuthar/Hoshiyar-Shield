# Deployment & Build Guide

## 1. Run in development (Expo Go)
```bash
cd apps/mobile
npm install
npx expo start          # scan the QR with Expo Go on Android (same Wi-Fi), or press "a" for an emulator
```
Every dependency is part of Expo Go (no custom native modules), so the full app runs in Expo Go.
Behind a restrictive proxy, use `EXPO_OFFLINE=1 npx expo start`.

## 2. Release APK from GitHub Actions (recommended for the demo)
Workflow: `.github/workflows/android-apk.yml`. It runs on pushes that touch `apps/mobile/**`, or manually
(Actions → *Android APK* → *Run workflow*).
1. `npm ci` → unit tests
2. `npx expo prebuild --platform android --clean` (generates `android/`, which is not committed)
3. `./gradlew assembleRelease -PreactNativeArchitectures=arm64-v8a,armeabi-v7a` (JDK 17)
4. Upload artifact **`hoshiyar-shield-apk`** (kept 30 days)

Install: download the artifact zip → extract the `.apk` → copy to the phone → enable "Install unknown apps" for
your file manager → open it. The APK is signed with the Expo template's **debug keystore**. Android will show
it as from an unknown developer. That's fine for a demo, not for the Play Store.

## 3. EAS Build (official Expo cloud build; needs an Expo account)
```bash
npm install --global eas-cli
cd apps/mobile
eas login                                            # HUMAN STEP: Expo account credentials
eas init                                             # links the project (adds extra.eas.projectId to app.json)
eas build --platform android --profile preview       # .apk, internal distribution (eas.json)
```
`eas.json` profiles: `preview` → APK, `production` → AAB (Play Store). EAS manages a proper keystore.

## 4. Local Gradle build
Needs the Android SDK (API 36 platform + build tools), NDK 27.1.12297006 and JDK 17:
```bash
cd apps/mobile && npm run apk:local     # = expo prebuild --clean && cd android && ./gradlew assembleRelease
# → android/app/build/outputs/apk/release/app-release.apk
```

## 5. Verification done in the build container
| Check | Result |
|---|---|
| `npx expo export --platform android` (Metro → Hermes bytecode) | ✅ 5.5 MB bundle, 8 MB total export |
| `npx expo prebuild --platform android` | ✅ `pk.hoshiyar.shield`, `hoshiyar://` scheme, sensitive permissions removed |
| Gradle build in the container | ❌ not possible: `dl.google.com` (Android SDK/Maven) is blocked by the network policy, so the APK is built on GitHub Actions instead |
| GitHub Actions `android-apk.yml`, run [38011938779](https://github.com/MuhammadMuthar/Hoshiyar-Shield/actions/runs/38011938779) (commit `7b4010f`) | ✅ tests → prebuild → `assembleRelease` (≈16 min) → artifact `hoshiyar-shield-apk` (32.3 MB zip, expires 2026-11-09) |
| Installing and running that APK on a real phone | ⏳ **not done yet**: needs a human with an Android device (the container cannot download the artifact) |

## 6. Optional future backend (not built)
A reports API (FastAPI or Supabase) would accept **consented** reports only, with server-side validation, rate
limiting, masked numbers in aggregates, and an analyst dashboard over clustered campaigns. Set
`EXPO_PUBLIC_REPORTS_API_URL` (see `.env.example`). Never put service-role keys in `EXPO_PUBLIC_*` variables.

## 7. Model updates
`ml/training/train.py` regenerates the model and copies it into `apps/mobile/assets/model/`. Ship by rebuilding
the app. The model version appears in About → "AI model on this phone" and in every result's technical details.
