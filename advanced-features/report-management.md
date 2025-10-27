# Report Management, CLI, and Automation

This section covers how reports are stored, exported, and automated. The guidance mirrors `cli.js`, Python helpers in `scripts/`, and the Docker assets in `docker/`.

## Report Management

- Reports are written to `storage/reports/` as Markdown and JSON. The analysed datasets that feed them sit in `storage/analyzed/`.
- `src/results-manager.js` and `src/renderer.js` drive the UI for browsing reports, exporting files, and initiating cart analyses.
- `scripts/cart_manager.py` and `scripts/cart_processor.py` allow analysts to persist curated story sets and generate bespoke outputs.

### Export Formats

| Format | Implementation | Notes |
|--------|----------------|-------|
| Markdown | `analyzer.generate_markdown_from_distilled` | Default human-readable output with citations. |
| JSON | Saved alongside Markdown | Retains full metadata, tags, and embeddings. |
| PDF | Node-based exporter (`pdfkit`) | Trigger via the UI or `npm run cli -- export-pdf`. |
| DOCX | Generated through the `docx` package | Handy for collaborative editing (UI driven). |
| XLSX | Optional export when the `xlsx` package is installed | Provides a tabular view through the UI when the dependency is present. |

Exports and timings are logged under `logs/export*.log`.

## Command-Line Interface Highlights

- Entry point: `cli.js`.
- Core commands: `extract`, `analyze`, `thematic`, `pipeline-incremental`, `search`, `combine`, `cart-process`, `export-pdf`, `config`, `profile`, `clear-cache`, `perf`, `wizard`, and validation helpers like `python-check` and `source-check`.
- Offline management: `npm run cli -- offline-status`, `npm run cli -- offline-enable --model all-MiniLM-L6-v2`, `npm run cli -- offline-disable`, and `npm run cli -- offline-generate` prepare the system for air-gapped runs.
- Licensing and resume helpers: `npm run cli -- license-activate`, `npm run cli -- license-status`, `npm run cli -- resume-check`, and `npm run cli -- resume-info` align with the flows documented in `docs/cli.md`.
- Profiles: `npm run cli -- profile list` shows available presets; `npm run cli -- profile default <name>` switches the active profile.
- Environment adjustments: `npm run cli -- config --show` or `npm run cli -- config --set KEY=value`.
- Health checks: `npm run cli -- python-check` validates dependencies and storage paths before a run.

Example workflow:

```bash
# Extract and analyse
npm run cli -- extract --max-stories 250
npm run cli -- analyze --date 2025-10-10
npm run cli -- thematic

# Search analysed stories
npm run cli -- search "open-source LLM licensing" --limit 20

# Export latest report to PDF
npm run cli -- export-pdf storage/reports/ai_report_2025-10-10.json --output ./exports/weekly.pdf
```

See `docs/cli.md` for the complete command catalogue.

## Automation Patterns

- **Scheduled jobs** - Combine CLI commands with cron or Windows Task Scheduler for daily digests.
- **Workspace scripts** - Chain CLI commands in shell scripts or CI workflows for repeatable pipelines.
- **Regression testing** - `AUTOMATION_SUITE_OVERVIEW.md` documents smoke tests that run in CI.

```
0 6 * * 1-5 cd /path/to/ai-news-extractor && \
  npm run cli -- extract --max-stories 200 && \
  npm run cli -- analyze --date $(date +%Y-%m-%d) && \
  npm run cli -- export-pdf storage/reports/ai_report_$(date +%Y-%m-%d).json \
    --output ~/Reports/morning-digest.pdf
```

## Container and Remote Use

- Docker Compose templates under `docker/` build headless environments with persistent volumes.
- Mount `storage/`, `config/`, and `.env` to retain outputs. Launch Ollama in a sidecar container for offline inference.

```bash
# Build images
docker compose build

# Start CLI container and Ollama
docker compose up -d

# Run an extraction inside the container
docker compose exec rescribos npm run cli -- extract --sources hackernews

# Tear down when finished
docker compose down
```

For deployment considerations, refer to the [deployment documentation](../deployment/README.md).
