# Node.js Backend

The Electron main process and supporting libraries live under `main.js`, `lib/`, and parts of `src/`. They manage configuration, secure storage, job orchestration, and IPC.

## Configuration Loading

- `.env` provides defaults; `.env.local` and profiles stored in `.rescribosrc` overlay environment-specific values.
- `lib/env-loader.js` merges configuration, validates keys, and exposes helper methods for retrieving typed values.
- Sensitive secrets (e.g., `OPENAI_API_KEY`) are stored via Keytar using `secure-key-manager.js`. The renderer never receives plaintext credentials.

## Workflow Management

- `lib/workflow-manager.js` defines multi-step jobs (extract → analyse → report → export) and coordinates retries.
- Each job stage spawns Python scripts using `child_process.spawn` with a dedicated working directory and sanitized environment.
- Structured progress events are pushed to the renderer through IPC (`pipeline:progress`, `pipeline:error`, `pipeline:complete`).

## IPC Handlers

- Defined in `main.js` and modularised under `lib/ipc-handlers/`.
- Cover operations such as launching pipelines, exporting reports, accessing environment variables, and reading logs.
- All channels are documented with payload schemas in `docs/DEVELOPER_GUIDE_IPC_EVENTS.md`.

## Logging & Telemetry

- `lib/logger.js` wraps `electron-log` to output to both console and rolling files under `logs/`.
- Runtime metrics (timings, provider usage) are appended to automation reports to aid regression analysis.
- No telemetry is sent externally; all data remains local unless the user opts into external providers.

## System Requirements (Practical)

- **Node.js**: 18+
- **Python**: 3.8+ (installed via `npm run install-python`)
- **Storage**: ~5 GB free for models, logs, and reports
- **Memory**: 8 GB recommended for comfortable Ollama usage

For a complete index of environment variables and default values, see `docs/ENVIRONMENT_REFERENCE.md` and `.env.example`.
