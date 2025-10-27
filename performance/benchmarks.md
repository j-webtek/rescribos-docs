# Benchmark Results

Benchmarking focuses on repeatable measurements that mirror real-world usage. The figures below were captured on a 2024 14" MacBook Pro (M3 Pro, 18 GB RAM) and a Windows 11 workstation (Ryzen 7 5800X, 32 GB RAM). Detailed logs are saved by `scripts/optimization/benchmark_performance.py` (output written to `scripts/optimization/benchmark_results.json`) and summarised in `AUTOMATION_TESTING_REPORT.md`.

## MacBook Pro (M3 Pro, 18 GB RAM)

| Scenario | Stories | Provider | Duration | Peak RAM | Notes |
|----------|---------|----------|----------|----------|-------|
| Full pipeline | 250 | GPT-5 | 14m 20s | 1.1 GB | `MAX_STORIES=250`, default prompts. |
| Extraction only | 400 | – | 3m 05s | 420 MB | Hacker News + arXiv; concurrency 5. |
| Analysis only | 250 | Llama 3.1 (Ollama) | 24m 10s | 1.4 GB | Offline mode enabled. |

## Windows 11 (Ryzen 7 5800X, 32 GB RAM)

| Scenario | Stories | Provider | Duration | Peak RAM | Notes |
|----------|---------|----------|----------|----------|-------|
| Full pipeline | 300 | GPT-5 | 18m 45s | 1.6 GB | Includes document ingestion (25 PDFs). |
| Automation suite | 200 | GPT-5 | 11m 32s | 1.2 GB | CLI pipeline replayed via the automation test plan. |
| Cart report | 60 | GPT-5 | 4m 18s | 780 MB | Generated from saved cart. |

## Cost Snapshot (GPT-5)

- 250-story run: ~$1.70 USD (summaries + embeddings + synthesis).
- 300-story run with document enrichment: ~$2.10 USD.
- Offline runs: $0 (electricity only) but 1.5–2× slower depending on hardware.

## Reproducing Benchmarks

1. Set `BENCHMARK_MODE=true` to disable caches.
2. Run `python scripts/optimization/benchmark_performance.py`.
3. Review `scripts/optimization/benchmark_results.json` and the console summary for detailed metrics.
4. Optionally cross-reference timings with `AUTOMATION_TESTING_REPORT.md` for regression context.

Refer to `AUTOMATION_TESTING_REPORT.md` for raw metrics, percentile breakdowns, and historical trends.
