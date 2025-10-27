# Multi-Layer Design

The application is composed of three runtime layers plus dedicated adapters for AI providers and storage. Each layer has clear responsibilities and communicates through typed interfaces.

## Renderer Layer (Electron)

- Lives under `src/renderer/` and `src/results/`.
- Renders the report explorer, semantic search, cart management, and chat interface.
- Communicates with the main process using whitelisted IPC channels defined in `src/preload.js`.
- Handles virtualised rendering for large story sets and streams incremental updates from the backend.

## Main Process Layer (Node.js)

- Entry point is `main.js`; supporting modules are under `lib/` and `src/`.
- Loads configuration, merges environment profiles, and resolves secure secrets with Keytar.
- Spawns Python workers via `child_process`, passing a sanitised environment and capturing standard output as structured JSON events.
- Coordinates long-running workflows (extraction, analysis, exports) and updates renderer windows through IPC.

## Processing Layer (Python)

- Core scripts reside in `scripts/` and `jobs/`.
- `extractor.py` handles multi-source story collection with retry policies and deduplication.
- `analyzer.py`, `cart_pipeline.py`, and related modules perform summarisation, tagging, clustering, and report generation.
- `document_processor.py` ingests local PDFs, DOCX files, and text documents and feeds them back into the same pipelines.
- Emit progress through `emit_progress()` which formats JSON messages for the Node.js orchestrator.

## AI Provider Layer

- `scripts/ai_providers/network_aware_manager.py` abstracts OpenAI, Ollama, and local transformer backends.
- Supports mixed-mode execution (e.g., embeddings via OpenAI while summaries run through Ollama).
- Includes automatic fallback logic when rate limits or connectivity issues occur.

## Persistence Layer

- Extracted stories saved under `storage/extracted/`.
- Analysed results and distilled reports under `storage/analyzed/` and `storage/reports/`.
- Embeddings stored in `storage/embeddings/embeddings.db` (SQLite with vector extensions).
- Configuration lives in `config/`, with reusable environment presets stored in `.rescribosrc`.

## IPC Contracts

IPC events follow the definitions documented in `docs/DEVELOPER_GUIDE_IPC_EVENTS.md`. Examples include:

- `pipeline:start`, `pipeline:progress`, and `pipeline:complete` for extraction and analysis jobs.
- `cart:update` for cart state transfers.
- `env:get` and `env:set` for environmental overrides.

These contracts make it possible to extend the platform with new renderer views or automation hooks without breaking existing workflows.
