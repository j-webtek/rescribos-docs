# Deployment Models

## Desktop Application

- Build installers with `npm run dist` (platform-specific scripts: `dist:win`, `dist:mac`, `dist:linux`).
- Suited for analysts who prefer a full UI and local storage.
- Auto-update is optional; many teams distribute signed packages manually.

## CLI / Headless

- Use `npm run cli -- …` from the project directory or include the packaged CLI in your PATH.
- Ideal for automation, CI pipelines, and scheduled jobs.
- Combine with cron, Task Scheduler, or GitHub Actions for recurring reports.

## Docker / Container

- Compose files under `docker/` provide headless execution with persistent volumes.
- Pair with an Ollama container when offline inference is required.
- Recommended for shared infrastructure or remote servers.

## Air-Gapped & On-Premises

- Install from offline media, pre-seed Ollama models, and set `FORCE_OFFLINE_MODE=true`.
- Licence validation supports a 30-day offline window by default; longer periods are available via enterprise contracts.
- Bundle documentation from `docs/` for teams operating without internet access.
