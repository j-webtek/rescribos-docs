# Data Schema

This summary reflects the canonical formats documented in `docs/data-schema.md` and used throughout the pipeline.

## Raw Extraction (`storage/extracted/*.json`)

```json
{
  "id": "hackernews-42012345",
  "title": "Story headline",
  "url": "https://news.ycombinator.com/item?id=42012345",
  "source": "hackernews",
  "created_at": "2025-10-10T12:34:56Z",
  "score": 128,
  "comment_count": 42,
  "author": "username",
  "content": "Full article text or abstract",
  "metadata": {
    "doi": "10.1234/example",
    "authors": ["Author Name"],
    "tags": ["ai", "research"]
  }
}
```

## Analysed Stories (`storage/analyzed/*.json`)

```json
{
  "id": "hackernews-42012345",
  "title": "Story headline",
  "summary": "AI-generated synthesis focusing on the insight...",
  "relevance_score": 0.87,
  "embedding": [0.123, -0.456, 0.789, "..."],
  "tags": ["machine-learning", "deployment"],
  "cluster_id": 3,
  "provider": "openai-gpt4o",
  "analysis": {
    "token_count": 480,
    "processing_seconds": 2.4
  },
  "original": {
    "url": "https://source/article",
    "source": "hackernews",
    "captured_at": "2025-10-10T12:34:56Z"
  }
}
```

## Thematic Reports (`storage/reports/*.json`)

```json
{
  "report_id": "ai_report_2025-10-10",
  "generated_at": "2025-10-10T13:30:00Z",
  "statistics": {
    "stories_extracted": 420,
    "stories_analyzed": 260,
    "themes": 6,
    "provider": "openai-gpt4o"
  },
  "executive_summary": "This week's analysis highlights...",
  "sections": [
    {
      "slug": "llm-efficiency",
      "title": "Large Language Model Efficiency",
      "summary": "Key developments around compression and inference speed.",
      "stories": [
        {
          "id": "hackernews-42012345",
          "title": "8-bit quantisation for LLMs",
          "citation": 1,
          "implications": {
            "first_order": "Reduces inference cost by 60%.",
            "second_order": "Enables deployment on edge devices.",
            "third_order": "Wider access to private deployments."
          }
        }
      ]
    }
  ],
  "references": [
    {
      "number": 1,
      "title": "8-bit quantisation for LLMs",
      "url": "https://arxiv.org/abs/...",
      "published": "2025-10-08"
    }
  ]
}
```

## File Locations

```
storage/
├─ extracted/        # Raw stories by timestamp
├─ analyzed/         # Summaries, scores, embeddings
├─ reports/          # Markdown + JSON reports
├─ embeddings/       # SQLite database for semantic search
├─ cart/             # Saved analyst carts
├─ rejected/         # Duplicates, low relevance, errors
└─ exports/          # User-triggered exports (PDF, DOCX, XLSX)
```

## Export Formats

- **JSON** – Machine-readable, includes full metadata and embeddings.
- **Markdown** – Human-friendly narrative with citations and sections.
- **PDF/DOCX** – Optional exports triggered from the UI or CLI.
- **XLSX** – Tabular snapshots for analysis in spreadsheet tools.
- **Chat transcripts** – Markdown files capturing question-answer sessions with references.
