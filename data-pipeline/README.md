# Data Processing Pipeline

The pipeline converts raw stories into structured intelligence. It mirrors the behaviour described in `docs/data-pipeline.md` and `docs/SYSTEM_ARCHITECTURE.md`.

```
Stage 1: Extraction  -> Stage 2: Analysis -> Stage 3: Organisation -> Stage 4: Synthesis
    Raw API + files          AI summaries + embeddings      Clustered themes         Markdown & JSON reports
```

1. **Extraction**
   - Sources: Hacker News, arXiv, saved documents, scripted web captures.
   - Controls: concurrency limits, retries, age filters, keyword whitelists, deduplication.
   - Output: `storage/extracted/<timestamp>.json`.

2. **Analysis**
   - Applies summarisation, relevance scoring, tagging, and embedding generation.
   - Supports OpenAI, Ollama, or transformer fallbacks.
   - Output: `storage/analyzed/<timestamp>.json`.

3. **Organisation**
   - Groups stories into logical clusters, ranks them, and prepares them for thematic synthesis.
   - Feeds the cart workflow for analyst review.

4. **Synthesis**
   - Produces Markdown and JSON reports with multi-order implications and citations.
   - Generates export artefacts (PDF, DOCX) when enabled.

Downstream steps such as semantic search, chat, and automation reuse the same analysed dataset to guarantee consistency.

## Related Guides

- [Detailed Workflow](workflow.md)
- [Data Schema](data-schema.md)
- [Performance Metrics](performance-metrics.md)
