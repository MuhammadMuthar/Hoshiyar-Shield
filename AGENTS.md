# AGENTS.md: instructions for AI coding agents

This repo is worked on by **two AI assistants (Claude and ChatGPT/Codex) plus
two humans**. Before changing anything, read
**[`docs/COLLABORATION.md`](docs/COLLABORATION.md)**. It defines who owns
which files, the handoff log, data formats and honesty rules. Live status is
in [`docs/HANDOFF.md`](docs/HANDOFF.md).

## Project in one paragraph
Hoshiyar Shield is an Android app (Expo SDK 57, React Native 0.86,
TypeScript, Expo Router) that warns Pakistani users about financial scam
messages in Roman Urdu, English and Urdu script. The classifier is a
character n-gram TF-IDF + logistic regression model. It is trained in Python
(`ml/`), exported to JSON, and run **on-device** in TypeScript
(`apps/mobile/src/engine/`). No message text leaves the phone.

## Layout
```
apps/mobile/            Expo app (routes in src/app/, engine in src/engine/)
ml/                     dataset generator, training, evaluation, clustering, tests
docs/                   architecture, evaluation, privacy, pitch, collaboration
dashboard/              optional web intelligence dashboard (P2)
.github/workflows/      CI + Android APK build
```

## Commands
```bash
# Python (repo root)
python3 -m venv .venv && .venv/bin/pip install -r ml/requirements.txt
.venv/bin/python ml/training/train.py        # generate data, train, evaluate, export
.venv/bin/python -m pytest ml/tests -q

# App (apps/mobile)
npm install
npm run typecheck && npm run lint && npm test
npx expo start                               # dev server (Expo Go / dev build)
```

## Non-negotiables
- Never hardcode classifier outputs; every message goes through `analyzeMessage()`.
- Python normalisation (`ml/training/textnorm.py`) and TypeScript
  normalisation (`apps/mobile/src/engine/normalize.ts`) must stay identical.
  If you change either, regenerate the model and keep the parity test passing.
- No real personal data. Use placeholder numbers `0399-555xxxx` and `.example` domains.
- Never claim metrics you didn't produce with `ml/training/train.py`.
- Use `npx expo install <pkg>` (or `EXPO_OFFLINE=1 npx expo install`) for native deps.
- Don't edit generated `android/` or `ios/` folders; configure through `app.json`.
