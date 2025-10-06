# Data Schema

### 5.2 Data Schema

**Raw Story Schema (`raw_stories.json`):**
```json
{
  "id": "unique_identifier",
  "title": "Story headline or article title",
  "url": "https://original-source.com/article",
  "source": "hackernews|arxiv|local",
  "timestamp": "2025-01-15T10:30:00Z",
  "score": 125,
  "comments": 42,
  "author": "username",
  "content": "Full article text or abstract",
  "metadata": {
    "doi": "10.1234/example",
    "authors": ["Author Name"],
    "published": "2025-01-10"
  }
}
```

**Analyzed Story Schema (`analyzed_stories.json`):**
```json
{
  "id": "unique_identifier",
  "title": "Original title",
  "url": "https://source.com",
  "source": "hackernews",
  "summary": "AI-generated 500-1000 character summary focusing on key insights...",
  "relevance_score": 0.87,
  "embedding": [0.123, -0.456, 0.789, ...], // 1536 dimensions
  "tags": ["machine-learning", "transformers", "efficiency", "research", "deployment"],
  "cluster_id": 3,
  "timestamp": "2025-01-15T10:30:00Z",
  "analysis_metadata": {
    "model": "gpt-4o",
    "processing_time": 2.34,
    "token_count": 450
  }
}
```

**Thematic Report Schema (`thematic_report.json`):**
```json
{
  "report_id": "report_20250115_103045",
  "generated_at": "2025-01-15T10:30:45Z",
  "statistics": {
    "total_stories_extracted": 847,
    "total_stories_analyzed": 312,
    "total_stories_in_report": 156,
    "processing_time_seconds": 645,
    "ai_provider": "openai-gpt4o"
  },
  "executive_summary": "This week's analysis reveals...",
  "sections": [
    {
      "id": 1,
      "title": "Advances in Large Language Model Efficiency",
      "summary": "Section-level synthesis...",
      "subtopics": [
        {
          "id": "1.1",
          "title": "Quantization and Compression Techniques",
          "stories": [
            {
              "id": "story_123",
              "title": "8-bit Quantization for LLMs",
              "citation_number": 1,
              "implications": {
                "first_order": "Reduces model size by 75%...",
                "second_order": "Enables deployment on edge devices...",
                "third_order": "Democratizes access to AI..."
              }
            }
          ]
        }
      ]
    }
  ],
  "references": [
    {
      "number": 1,
      "title": "8-bit Quantization for LLMs",
      "url": "https://arxiv.org/abs/...",
      "authors": ["Smith et al."],
      "date": "2025-01-10"
    }
  ]
}
```

### 5.3 File Locations and Formats

**Storage Directory Structure:**
```
C:\Users\Jack\AppData\Roaming\ai-news-extractor\storage\
├── reports/                           # All generated reports
│   ├── report_20250115_103045.json   # Structured data
│   ├── report_20250115_103045.md     # Markdown formatted
│   ├── report_20250115_103045.pdf    # PDF export (if generated)
│   └── report_20250115_103045.docx   # Word export (if generated)
│
├── rejected/                          # Filtered-out stories
│   ├── error_stories.jsonl           # Failed extractions
│   ├── low_relevance.jsonl           # Below threshold
│   └── duplicates.jsonl              # Detected duplicates
│
├── cart/                              # User-saved items
│   ├── cart_research_ai.json         # Named cart
│   └── cart_default.json             # Default cart
│
├── embeddings.db                      # SQLite vector database
│   # Tables: stories, embeddings, metadata
│
└── exports/                           # User-initiated exports
    ├── search_results_20250115.xlsx
    ├── thematic_report_20250115.pdf
    └── chat_transcript_20250115.md
```

**File Formats:**

**1. JSON Reports** (`.json`)
- Structured, machine-readable
- Complete metadata preservation
- Embedding vectors included
- Suitable for programmatic analysis
- Size: 500KB - 5MB per report

**2. Markdown Reports** (`.md`)
- Human-readable formatting
- Clickable citations
- Section hierarchy preserved
- Suitable for GitHub, Obsidian, Notion
- Size: 100KB - 1MB per report

**3. PDF Exports** (`.pdf`)
- Professional formatting
- Table of contents with page numbers
- Headers and footers
- Code syntax highlighting
- Suitable for distribution
- Size: 500KB - 3MB per report

**4. Word Documents** (`.docx`)
- Editable format
- Style preservation
- Cross-references maintained
- Suitable for collaboration
- Size: 200KB - 2MB per report

**5. Excel Exports** (`.xlsx`)
- Tabular data format
- Searchable and filterable
- Metadata columns
- Suitable for data analysis
- Size: 300KB - 2MB per export
