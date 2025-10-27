# Performance & Scalability

Benchmarking results are tracked in `AUTOMATION_TESTING_REPORT.md` and the built-in performance monitor (`lib/performance-monitor.js`). This section summarises typical behaviour and offers tuning tips.

## Typical Pipeline Timing (reference run)

| Stage | Stories | Duration | Notes |
|-------|---------|----------|-------|
| Extraction | 300 | ~3 minutes | Dominated by network latency to Hacker News and arXiv. |
| Analysis | 300 | ~12 minutes | GPT-5 latency; include retries for transient errors. |
| Organisation | 300 | ~90 seconds | CPU-bound clustering and ranking. |
| Synthesis | 150 | ~6 minutes | Depends on prompt profile and provider. |

Peak memory stays under 1.5 GB for runs up to 500 stories on a modern laptop when embeddings are cached to SQLite.

## Influencing Factors

- **Provider latency** – Local models (Ollama) trade cost savings for longer processing times. Expect 1.5–2x slower analysis compared to GPT-5.
- **Concurrency** – `EXTRA_FETCH_CONCURRENCY` and provider rate limits define how quickly extraction and AI calls complete.
- **Caching** – Embedding caches reduce repeated costs for the same stories; disable them for pure benchmarking.
- **Hardware** – SSD storage and 8+ GB RAM minimise contention during large runs.

## Monitoring Tools

- `npm run cli -- perf` or the developer tools performance monitor show stage timings in real time.
- `logs/performance-*.log` summarises run durations, provider usage, and cache hits.
- `AUTOMATION_TESTING_REPORT.md` records end-to-end regression runs used in CI.

For detailed measurements and reproducibility notes, see [Benchmarks](benchmarks.md). To tune performance further, continue to [Optimisation](optimization.md).
