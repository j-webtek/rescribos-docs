# Deployment Options

Rescribos can be deployed as a desktop application, run headless through the CLI, or automated inside containers. This page summarises the processes described in `docs/DEVELOPMENT_SETUP.md` and `docs/DEPLOYMENT_GUIDE.md`.

## Desktop Builds

- Install dependencies: `npm install` followed by `npm run install-python`.
- Launch in development: `npm start`.
- Package installers: `npm run dist` (generates binaries under `dist-final/`).
  - Windows: NSIS installer (`Rescribos Data Refinement-Setup-<version>.exe`).
  - macOS: DMG with drag-and-drop install (`Rescribos Data Refinement-<version>.dmg`).
  - Linux: AppImage and DEB packages.
- User data paths follow the Electron defaults (`%APPDATA%` on Windows, `~/Library/Application Support` on macOS, `~/.config` on Linux).

## Headless / CLI

- `npm run cli --` exposes the full pipeline without launching the UI.
- Run from scheduled tasks or CI to generate daily digests.
- Profiles allow environment-specific overrides without editing `.env`.

## Containers

- Docker assets in `docker/` include compose files and helper scripts.
- Mount `storage/`, `config/`, and `.env` for persistence when running in containers.
- Optional Ollama container provides offline models for headless environments.

## Configuration Management

- `.env` contains defaults; additional profiles are stored in `.rescribosrc` and can be activated via CLI or UI.
- `npm run cli -- config --set KEY=value` updates environment variables safely.
- For multi-user deployments, store per-user `.env.local` files or rely on secure environment injection at launch time.

Continue with the detailed [installation steps](installation.md) and [configuration guidance](configuration.md).
