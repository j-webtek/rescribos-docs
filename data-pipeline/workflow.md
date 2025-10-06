# Complete Workflow

### 5.1 Complete Workflow Overview

The Rescribos data pipeline consists of four primary stages, each with distinct responsibilities:

```
┌─────────────────────────────────────────────────────────────────────┐
│                     STAGE 1: EXTRACTION                             │
│  • Multi-source data collection (Hacker News, arXiv, local docs)   │
│  • Concurrent fetching with rate limiting                          │
│  • Basic filtering (keywords, age, duplicates)                     │
│  • Optional AI pre-screening                                       │
│  • Output: raw_stories.json (500-1000 items)                       │
│  • Duration: 2-5 minutes                                            │
└─────────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────────┐
│                     STAGE 2: ANALYSIS                               │
│  • AI summarization (GPT-4o or Llama 3.1)                          │
│  • Relevance scoring and filtering                                 │
│  • Embedding generation (vector representations)                   │
│  • Automated tagging (TF-IDF + AI)                                 │
│  • Initial clustering (similarity-based)                           │
│  • Output: analyzed_stories.json (200-500 items)                   │
│  • Duration: 5-15 minutes                                           │
└─────────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────────┐
│                     STAGE 3: ORGANIZATION                           │
│  • Advanced clustering (hierarchical)                              │
│  • Category identification                                         │
│  • Story grouping and ranking                                      │
│  • Section structure creation                                      │
│  • Output: organized_report.json                                   │
│  • Duration: 1-2 minutes                                            │
└─────────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────────┐
│                   STAGE 4: THEMATIC SYNTHESIS                       │
│  • Multi-order implications analysis                               │
│  • Executive summary generation                                    │
│  • Cross-section insights                                          │
│  • Citation management                                             │
│  • Output: thematic_report.md + .json                              │
│  • Duration: 3-8 minutes                                            │
└─────────────────────────────────────────────────────────────────────┘
                            ↓
                    [Final Report + Exports]
```
