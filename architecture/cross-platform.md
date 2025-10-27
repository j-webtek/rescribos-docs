# Cross-Platform Support

Electron packaging ensures the application runs consistently across Windows, macOS, and Linux. Build targets are defined in `package.json` and use `electron-builder` defaults unless noted.

## Windows

- Creates an NSIS installer (`Rescribos Data Refinement-Setup-<version>.exe`) with optional desktop/start menu shortcuts.
- User data lives under `%APPDATA%\ai-news-extractor\`.
- Supports code signing when certificates are configured via `scripts/build/setup-signing.js`.
- Verified with Windows 10/11; SmartScreen prompts clear once signed binaries are supplied.

## macOS

- Produces a DMG with drag-and-drop install; App bundle contains a universal binary when built on Apple Silicon with `--arch arm64,x64`.
- Application data stored under `~/Library/Application Support/ai-news-extractor/`.
- Hardened runtime and entitlements are provided in `build/entitlements.mac.plist`; notarisation handled outside the repository.

## Linux

- Builds AppImage and Debian packages by default (`electron-builder --linux`).
- Data written to `~/.config/ai-news-extractor/`.
- AppImage supports portable execution, while the DEB artefact integrates with system package managers.

## Headless and Containers

- Docker workflows in `docker/` allow running the CLI and scheduled jobs without spinning up the UI.
- Automation scripts built around the CLI run on any platform that meets the Node.js and Python prerequisites.

Refer to `docs/DEVELOPMENT_SETUP.md` for packaging commands and platform-specific prerequisites.
