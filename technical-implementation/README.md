# Technical Implementation

This section provides an engineering-centric view of the codebase. It complements the deep dives in `docs/DEVELOPER_GUIDE_IPC_EVENTS.md`, `docs/DEVELOPER_GUIDE_TESTING.md`, and related guides.

## Repository Layout

| Path | Purpose |
|------|---------|
| `src/` | Electron renderer assets, preload scripts, and UI logic. |
| `lib/` | Node.js orchestration utilities (workflow manager, environment loader, secure storage). |
| `scripts/` | Python processing pipeline (extraction, analysis, document processing, chat). |
| `config/` | Data source definitions, prompt templates, and automation presets (CLI profiles are stored in `.rescribosrc`). |
| `docker/` | Container definitions for headless and remote execution. |
| `tests/` | Jest suites for JavaScript and pytest suites for Python. |
| `storage/` | Generated outputs (extracted data, analysed data, reports, embeddings). |

## Runtime Processes

1. **Renderer** - Runs in the Chromium context. Files `src/renderer.js`, `src/index.html`, and the resources under `src/results/` handle UI state, search, and cart interactions.
2. **Main process** - Entry point `main.js` loads user configuration, wires IPC handlers, and launches Python workers via `child_process.spawn`.
3. **Python workers** - Scripts in `scripts/` perform extraction (`extractor.py`), analysis (`analyzer.py`), chat (`full_context_chat.py`), and document processing (`document_processor.py`).

IPC interactions between renderer and main are defined in `src/preload.js` and documented in `docs/DEVELOPER_GUIDE_IPC_EVENTS.md`.

## Key Modules

- `lib/workflow-manager.js` - Coordinates multi-stage jobs and ensures progress updates reach the UI.
- `lib/env-loader.js` - Merges `.env`, profile files, and runtime overrides before launching Python processes.
- `scripts/ai_providers/network_aware_manager.py` - Centralises provider selection and error handling for OpenAI, Ollama, and transformer fallbacks.
- `scripts/ai_compatibility.py` - Helper utilities that normalise provider behaviour and expose shared fallbacks.
- `scripts/cart_manager.py` / `scripts/cart_processor.py` - Persist and process cart selections into full analyses.
- `scripts/document_processor.py` - Adds local PDF/DOCX/TXT ingestion.
- `cli.js` - Exposes the automation interface (`npm run cli -- <command>`).

## Testing & Quality

- JavaScript tests run with `npm test` (Jest). Coverage focuses on configuration loaders, IPC validation, and CLI utilities.
- Python tests run with `pytest` under the `tests/` directory and cover extraction, analysis, and AI manager behaviours.
- Automation reports (`AUTOMATION_TESTING_REPORT.md`) track end-to-end reliability, while `CODE_QUALITY_DETAILED_ANALYSIS.md` documents linting and static analysis.

Proceed to the following pages for component-specific details:

- [Electron Frontend](electron-frontend.md)
- [Node.js Backend](nodejs-backend.md)
- [Python Pipeline](python-pipeline.md)
