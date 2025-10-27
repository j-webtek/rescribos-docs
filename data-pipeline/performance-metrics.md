# Performance Metrics

Pipeline benchmarks vary with dataset size and chosen AI provider. Figures below reflect recent runs captured in `docs/AUTOMATION_TESTING_REPORT.md`.

## Extraction

- Sources: up to 500 Hacker News items and 100 arXiv papers per run.
- Throughput: 3–5 minutes with default concurrency (`EXTRA_FETCH_CONCURRENCY=5`).
- Network footprint: roughly 40–80 MB.
- Success rate: typically above 95%; failures are logged under `logs/extraction*.log`.

## Analysis

- Stories processed: 200–500 depending on filters.
- Provider latency: 2–4 seconds per summary with GPT-5; 4–6 seconds using Ollama on modern laptops.
- Embedding batches: 100 items per request; cached results minimise repeated calls.
- Cost: $0.50–$2.00 USD for a full GPT-5 run billed directly to the user’s OpenAI account.
- Resource usage: 20–40% CPU and up to 1 GB RAM on typical development machines.

## Organisation & Synthesis

- Clustering and theme detection: 1–2 minutes leveraging NumPy/SciPy and `hdbscan`.
- Thematic synthesis: 3–8 minutes depending on the number of sections and the prompt profile.
- Output sizes: 0.5–5 MB for JSON, Markdown, and optional PDF/DOCX formats.

## Reliability & Recovery

- All network calls use exponential backoff and three retry attempts.
- Errors are captured in `logs/` and summarised in `AUTOMATION_TESTING_REPORT.md`.
- Pipeline stages are idempotent; rerunning a failed stage will reuse existing inputs and avoid duplicate outputs.
- Provider failover automatically switches to fallback models when cloud services are unavailable.

For profiling guidance and advanced tuning options, see `docs/DEVELOPER_GUIDE_TESTING.md` and `docs/CODE_QUALITY_DETAILED_ANALYSIS.md`.
