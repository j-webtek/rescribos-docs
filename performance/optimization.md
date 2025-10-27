# Optimisation Strategies

Rescribos ships with several optimisations to keep large runs responsive. Fine-tuning these settings can significantly reduce runtime and cost.

## Extraction & Analysis

- **Concurrency control** – `EXTRA_FETCH_CONCURRENCY` and `AI_CONCURRENCY` (profile option) limit parallel requests. Increase gradually while monitoring API rate limits.
- **Batch embeddings** – `EMBEDDING_BATCH_SIZE` defaults to 100 to respect provider quotas without sacrificing speed.
- **Keyword filters** – Use `FILTER_KEYWORDS` and `EXCLUDE_KEYWORDS` to minimise irrelevant stories before costly AI analysis.
- **Incremental runs** – `FORCE_REPROCESS=false` skips stories that have already been analysed, saving both time and cost.

## Caching

- Embeddings are cached in `storage/embeddings/embeddings.db`. Remove cached summaries with `npm run cli -- clear-cache` before benchmarking.
- Document processing caches file hashes to avoid re-ingesting unchanged files.
- The chat assistant stores recent prompts and responses locally to speed up follow-up questions.

## Memory Management

- Python scripts process stories in chunks (configurable via `BATCH_SIZE`). Tune this value if you see memory pressure on low-RAM machines.
- The renderer uses virtual scrolling for story lists and carts, so even thousands of entries remain responsive.
- Set `MAX_STORIES_IN_MEMORY` to match available hardware; results beyond this value remain on disk but are streamed when required.

## When to Choose Local Models

- Use Ollama when regulatory requirements forbid cloud inference or when running frequent internal analyses where cost savings outweigh latency.
- Prefer GPT-5 when turnaround time and summarisation quality are critical.
- Hybrid mode (default) automatically tries OpenAI first and falls back to Ollama; override with `FORCE_OFFLINE_MODE` or CLI flags for deterministic behaviour.

## Diagnostics

- Enable verbose logging: `LOG_LEVEL=debug` for granular timings and provider responses.
- Use `logs/performance-*.log` to identify slow stages.
- The automation suite documented in `AUTOMATION_SUITE_OVERVIEW.md` provides a quick regression check after tuning settings.
