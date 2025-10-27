# Technology Stack

The platform blends web, desktop, and data tooling to deliver a hybrid workflow. Versions listed here are aligned with `package.json` and `requirements.txt`.

## Frontend

- **Electron 38** for cross-platform windows and menu integration.
- **HTML/CSS/JavaScript** renderer code under `src/renderer/` and `src/results/`.
- **TypeScript 5.x** for shared models and IPC type definitions compiled into `dist-ts/`.
- **Font Awesome**, custom CSS modules, and Chart.js for visuals.

## Main Process & Services

- **Node.js 18** runtime with native `fetch` support.
- **Keytar** for secure storage of OpenAI and Ollama credentials.
- **dotenv** and custom loaders for environment profile management.
- **electron-store** for persisted application preferences.
- **pdfkit** and **docx** for export formatting.
- **p-limit** and custom queues for throttling parallel tasks.

## Python Pipeline

- **Python 3.8+** running in virtual environment managed by `npm run install-python`.
- **aiohttp** for asynchronous requests to Hacker News, arXiv, and other APIs.
- **openai>=1.42** for GPT-5 integration.
- **ollama-python** helpers in the AI manager for local inference.
- **sentence-transformers**, **scikit-learn**, and **hdbscan** for embeddings and clustering.
- **PyMuPDF (fitz)** and **python-docx** for document ingestion.
- **playwright** optional dependency for scripted web extractions.

## Data & Storage

- **SQLite (with vector extensions)** for embedding search stored at `storage/embeddings/embeddings.db`.
- **JSON** outputs under `storage/extracted/` and `storage/analyzed/` for raw and processed data.
- **Markdown** reports in `storage/reports/` for human-readable summaries.
- **Log files** under `logs/` with rotation handled by custom utilities.

## Tooling & Quality

- **Jest** and **Playwright** for JavaScript testing.
- **Pytest** for Python unit and integration tests.
- **ESLint**, **Prettier**, and **Flake8** for code consistency.
- **Semantic Release** for automated changelog generation.

For dependency installation steps and troubleshooting, refer to `docs/DEVELOPMENT_SETUP.md`.
