# Installation Guide

This guide mirrors the steps in `docs/DEVELOPMENT_SETUP.md` and highlights platform nuances.

## Prerequisites

- Node.js 18 or newer.
- Python 3.8 or newer (ensure it is available on your PATH).
- Git, make, and a C++ build toolchain for native modules (Windows users can install Microsoft Build Tools).
- Optional: Ollama for offline AI models.

## First-Time Setup

```bash
git clone https://github.com/rescribos/data-refinement.git ai-news-extractor
cd ai-news-extractor
npm install
npm run install-python
```

`npm run install-python` upgrades `pip`, removes conflicting TensorFlow versions, installs PyTorch CPU wheels, installs project requirements, and registers Playwright (for automated browser tasks).

## Running the Desktop App

```bash
npm start
```

- The first launch prompts for configuration paths and API keys.
- Data is stored under the Electron user data directory (`%APPDATA%` on Windows, `~/Library/Application Support` on macOS, `~/.config` on Linux).

## Packaging Installers

```bash
npm run dist           # Build platform-specific artefacts
npm run dist:win       # Windows NSIS installer
npm run dist:mac       # macOS DMG
npm run dist:linux     # Linux AppImage + DEB
```

Outputs are written to `dist-final/`. Configure signing certificates via `scripts/build/setup-signing.js` if required.

## CLI-Only Environments

```bash
npm run cli -- extract --max-stories 200
npm run cli -- analyze --date 2025-10-10
npm run cli -- thematic
npm run cli -- export-pdf storage/reports/ai_report_2025-10-10.json --output ./exports/latest.pdf
```

- Profiles managed via `.rescribosrc` can be activated with `npm run cli -- profile default <name>`.
- Use cron, Task Scheduler, or CI pipelines to schedule repeated runs.

## Containerised Deployment

- Dockerfiles and compose samples are located in `docker/`.
- Mount `storage/`, `config/`, and `.env` to keep outputs persistent:

```bash
docker compose up -d rescribos
docker compose exec rescribos npm run cli -- extract --sources hackernews
docker compose exec rescribos npm run cli -- analyze --date $(date +%Y-%m-%d)
```

- Run Ollama in a sidecar container if offline summarisation is required.

## Updating

```bash
git pull
npm install
npm run install-python
```

- Re-run packaging commands if you distribute installers.
- Review `CHANGELOG.md` for migration notes between releases.
