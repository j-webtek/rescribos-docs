# AI-Powered Analysis

The analysis stack turns extracted stories into decision-ready insights. It mirrors the behaviour documented in `docs/AUTOMATION_SUITE_OVERVIEW.md` and `docs/AI_PROVIDER_SYSTEM_DOCUMENTATION.md`.

## Pipeline Components

1. **Summarisation**
   - Models: OpenAI GPT-5 by default, Ollama Llama 3.1 when offline, or transformer fallbacks.
   - Length: Controlled via `SUMMARY_LENGTH` (defaults to approximately 1,000 characters).
   - Prompts: Context-aware templates defined in `config/prompts/`.

2. **Relevance Scoring**
   - Multi-factor evaluation that combines keyword hit rate, novelty, and model-generated impact scoring.
   - Threshold controlled by `MIN_RELEVANCE_SCORE` (see `docs/DEVELOPER_GUIDE_TESTING.md` for calibration guidance).

3. **Embedding Generation**
   - Uses OpenAI `text-embedding-3-small` or `nomic-embed-text` via Ollama.
   - Batch size tuned with `EMBEDDING_BATCH_SIZE` (default 100 per batch).
   - Stored in `storage/embeddings/embeddings.db` with vector search backed by SQLite.

4. **Automated Tagging**
   - Combines TF-IDF analysis with keyword heuristics to assign up to five tags per story.
   - Normalises tags across the dataset to support grouping and filtering in the UI.

5. **Clustering and Theme Detection**
   - Clustering algorithms include `hdbscan` and agglomerative clustering depending on the dataset size.
   - Themes feed both the report structure and the cart-based workflow for follow-up analysis.

## Configuration Highlights

```dotenv
OPENAI_MODEL=gpt-5
OPENAI_TEMPERATURE=0.6
SUMMARY_LENGTH=1000
EMBEDDING_MODEL=text-embedding-3-small
EMBEDDING_BATCH_SIZE=100
DEDUP_THRESHOLD=0.85
```

- Set `FORCE_OFFLINE_MODE=true` to enforce use of local summarisation and embedding models.
- Use `PROMPT_PROFILE=<name>` to switch between preset prompt templates stored under `config/prompt-profiles/`.

## Outputs

- Summaries, relevance scores, tags, and embeddings are stored in the analysed JSON files under `storage/analyzed/`.
- Distilled Markdown reports in `storage/reports/` contain executive summaries, key takeaways, and citation references for each theme.
- The chat assistant and semantic search consume the same analysed dataset, guaranteeing consistent answers across interfaces.
