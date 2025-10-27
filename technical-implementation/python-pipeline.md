# Python Pipeline

The Python scripts under `scripts/` power extraction, document processing, analysis, and automation. They are designed to run both from the Electron application and the CLI.

## Core Modules

| Module | Responsibility |
|--------|----------------|
| `extractor.py` | Fetches stories from Hacker News, arXiv, and configured sources; applies filtering, deduplication, and progress reporting. |
| `analyzer.py` | Runs summarisation, relevance scoring, clustering, and report synthesis; delegates provider calls to the network-aware manager. |
| `ai_providers/network_aware_manager.py` | Orchestrates OpenAI, Ollama, and local fallbacks; exposes unified interfaces for summaries and embeddings. |
| `ai_compatibility.py` | Helper utilities that normalise provider behaviour and manage feature fallbacks. |
| `document_processor.py` | Processes local PDF, DOCX, and TXT files and feeds them into the same analysis workflow. |
| `cart_processor.py` | Turns saved cart selections into full thematic reports. |
| `full_context_chat.py` | Supports the chat assistant by answering questions grounded in analysed reports. |

## Execution Model

- Scripts are invoked by Node.js using `child_process.spawn` with JSON-based stdout messages (progress, warnings, errors).
- `asyncio` enables concurrent network calls during extraction.
- Errors are propagated with structured payloads so the UI and CLI can present meaningful diagnostics.
- Configuration is injected via environment variables prepared by `lib/env-loader.js`.

## Dependencies

Key packages declared in `requirements.txt` include:

- **Networking**: `aiohttp`, `requests`, `beautifulsoup4`, `tqdm`
- **AI providers**: `openai`, `sentence-transformers`, `transformers`, `hf_xet`
- **Local inference**: `torch`, `torchvision`, `tensorflow-cpu`
- **ML & clustering**: `scikit-learn`, `hdbscan`, `numpy`, `scipy`
- **Document handling**: `python-docx`, `PyPDF2`, `PyMuPDF`
- **Utilities**: `python-dotenv`, `portalocker`, `colorama`, `tiktoken`

Installation is handled by `npm run install-python`, which upgrades `pip`, removes conflicting TensorFlow packages, installs PyTorch CPU wheels from the official index, and then installs project dependencies.

## Testing

- Python unit and integration tests live alongside JavaScript suites under `tests/`.
- After installing dependencies (`npm run install-python`), run `pytest` from the project root.
- Automation suites documented in `AUTOMATION_SUITE_OVERVIEW.md` exercise the pipeline end-to-end.

For implementation specifics, consult the individual scripts or the deep-dive documentation in `docs/` (e.g., `DOCUMENT_PROCESSING.md`, `CHAT_ARCHITECTURE.md`).
