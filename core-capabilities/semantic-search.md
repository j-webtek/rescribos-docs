# Semantic Search & Discovery

### 2.4 Semantic Search & Discovery

Vector-based search enables natural language queries across all collected content:

**Search Features:**

**1. Natural Language Queries**
```
"What are recent breakthroughs in LLM efficiency?"
"Show me papers about AI safety from last month"
"Find discussions about GPT-4 alternatives"
```

**2. Similarity-Based Ranking**
- Cosine similarity on embeddings
- Configurable threshold (0.0-0.6)
- Top-K result retrieval (default: 20)

**3. Temporal Filtering**
- Date range constraints
- Recency boosting
- Historical trend analysis

**4. Multi-Index Search**
- SQLite vector database
- In-memory caching for speed
- Index optimization for <100ms queries

**5. Export Results**
- JSON with scores
- Markdown with citations
- Excel with metadata

**Search Architecture:**
```
User Query → Embedding Generation → Vector Search → Ranking → Presentation
     ↓              ↓                     ↓            ↓           ↓
  "AI trends"   [1536d vector]      SQLite query   Cosine   Interactive UI
```

**Configuration:**
```env
CHAT_SIMILARITY_THRESHOLD=0.2
CHAT_TOP_STORIES=5
EMBEDDING_CACHE_TTL_HOURS=24
```
