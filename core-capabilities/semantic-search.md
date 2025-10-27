# Semantic Search & Discovery

Semantic search enables analysts to query the document corpus using natural language, receiving context-aware matches ranked by semantic similarity. The system supports both SQLite and high-performance PostgreSQL backends with advanced retrieval features.

## Overview

Rescribos semantic search translates natural language queries into vector embeddings and finds semantically similar documents, even when exact keywords don't match.

**Key Features:**
- **Natural Language Queries**: Search using plain English, no keyword engineering required
- **Cross-Document Search**: Find related content across entire corpus
- **Date Filtering**: Limit results to specific time ranges
- **Relevance Ranking**: Results sorted by semantic similarity
- **Hybrid Search**: Combines semantic and keyword matching (PostgreSQL)
- **Metadata-Aware Scoring**: Boosts results based on document metadata

## Query Experience

**Example Natural Language Queries:**

```
"Recent breakthroughs in LLM efficiency and reduced inference costs"
"Show me papers about AI safety from last month"
"Discussions about GPT-4 alternatives and competitive models"
"Regulatory frameworks for AI governance in Europe"
"Adversarial techniques for bypassing AI content filters"
```

**How It Works:**
1. Query is converted to embedding vector using OpenAI or Ollama
2. Vector similarity search finds semantically related documents
3. Results ranked by cosine similarity (or RRF for hybrid search)
4. UI highlights matching passages with links to source

## Database Backends

### SQLite Backend (Default)

**Best for:**
- Individual users and small teams
- Up to 10,000 documents
- Simple setup and portability
- No additional infrastructure

**Storage:**
- `storage/embeddings/embeddings.db` (SQLite database)
- Vector extensions for similarity search
- Compact, portable, single-file storage

**Performance:**
- Linear scan for small datasets (< 1,000 docs)
- Acceptable latency for most use cases (< 500ms)
- Query caching for repeated searches

### PostgreSQL + pgvector Backend (Recommended for Scale)

**Best for:**
- Enterprise deployments
- 10,000+ documents
- Multi-user environments
- High-performance requirements

**Performance Benefits:**
- **10-100x faster** than SQLite for large datasets
- **HNSW indexing** for logarithmic query time
- **Parallel query execution** for multi-user access
- **Advanced filtering** with metadata indexes

**Setup:**
See [PostgreSQL Quickstart](../../../POSTGRES_QUICKSTART.md) for 5-minute setup guide.

**Migration:**
Existing SQLite embeddings can be migrated to PostgreSQL without data loss.

## Advanced Search Features

### Hybrid Search (PostgreSQL Only)

Combines semantic similarity with traditional keyword matching:

**How It Works:**
1. **Semantic Search**: Finds conceptually similar documents
2. **Keyword Search**: Finds exact term matches
3. **RRF (Reciprocal Rank Fusion)**: Merges results optimally
4. **Configurable Weights**: Balance semantic vs. keyword importance

**When To Use:**
- Searching for specific technical terms or acronyms
- When exact terminology matters (e.g., "GPT-4" vs "GPT-3")
- Combining conceptual search with keyword precision

**Configuration:**
```env
CHAT_ENABLE_HYBRID_SEARCH=true
CHAT_HYBRID_SEMANTIC_WEIGHT=0.7   # 70% semantic, 30% keyword
```

### Metadata-Aware Scoring

Boosts search results based on document metadata:

**Scoring Factors:**
- **Recency**: Newer documents ranked higher
- **Source Reputation**: Trusted sources prioritized
- **Document Type**: Academic papers vs. blog posts
- **View Count**: Popular documents boosted
- **Category Match**: Documents in relevant categories

**Configuration:**
```env
CHAT_ENABLE_METADATA_SCORING=true
CHAT_RECENCY_BOOST=0.2            # 20% boost for recent docs
CHAT_SOURCE_BOOST=0.15            # 15% boost for reputable sources
```

### Semantic Reranking

Improves initial search results using cross-encoder models:

**Process:**
1. Initial retrieval finds top 50 candidates
2. Cross-encoder scores query-document pairs
3. Results reranked by cross-encoder scores
4. More accurate than pure bi-encoder similarity

**Benefits:**
- 15-30% improvement in relevance metrics (NDCG, MRR)
- Better handling of nuanced queries
- Reduced false positives

**Configuration:**
```env
CHAT_ENABLE_RERANKING=true
CHAT_RERANKING_METHOD=cross_encoder
```

### Dynamic Similarity Thresholds

Automatically adjusts relevance thresholds based on query characteristics:

**Query Specificity Detection:**
- **Technical queries**: Higher threshold (0.25) for precision
- **Broad queries**: Lower threshold (0.10) for recall
- **Medium queries**: Standard threshold (0.15)

**Benefits:**
- Technical queries get fewer, more relevant results
- Broad queries get comprehensive coverage
- Optimal precision/recall balance per query type

**Configuration:**
```env
CHAT_USE_DYNAMIC_THRESHOLDS=true
CHAT_BASE_THRESHOLD=0.15
```

## Search Configuration

### Basic Settings

```env
# Similarity thresholds
CHAT_SIMILARITY_THRESHOLD=0.3      # Minimum similarity score (0.0-1.0)
CHAT_TOP_STORIES=20                # Max results to return

# Database backend
EMBEDDING_BACKEND=sqlite           # Options: sqlite, postgresql
POSTGRES_HOST=localhost            # PostgreSQL connection (if using postgres)
POSTGRES_PORT=5432
POSTGRES_DB=ai_news_embeddings
```

### Advanced Settings

```env
# Hybrid search (PostgreSQL only)
CHAT_ENABLE_HYBRID_SEARCH=true
CHAT_HYBRID_SEMANTIC_WEIGHT=0.7

# Metadata scoring
CHAT_ENABLE_METADATA_SCORING=true
CHAT_RECENCY_BOOST=0.2

# Reranking
CHAT_ENABLE_RERANKING=true
CHAT_RERANKING_MODEL=cross-encoder/ms-marco-MiniLM-L-12-v2

# Performance
CHAT_QUERY_CACHE_TTL=3600          # Cache duration (seconds)
CHAT_MAX_PARALLEL_QUERIES=5        # Concurrent queries
```

## Integration Points

### Chat Grounding

Semantic search powers the chat system's context retrieval:

- Queries automatically generate embeddings
- Top-K relevant documents added to chat context
- Configurable similarity threshold
- Dynamic context based on conversation

See [Interactive AI Chat](ai-chat.md) for chat integration details.

### Document Library

Document Library uses semantic search for document discovery:

- Natural language search across all documents
- Category and tag filtering combined with semantic search
- Adjustable relevance thresholds in UI
- Real-time search as you type

See [Document Library](../advanced-features/document-library.md) for UI details.

### Export & API

**UI Export:**
- Copy results in Markdown format
- Includes source citations and similarity scores
- Formatted for reports and documentation

**CLI Export:**
```bash
npm run cli -- search "query text" --format json
```

**Output Format:**
```json
{
  "query": "AI safety research",
  "results": [
    {
      "story_id": "abc123",
      "title": "Anthropic's Constitutional AI",
      "similarity": 0.87,
      "snippet": "...",
      "metadata": {...}
    }
  ]
}
```

## Performance Optimization

### Query Caching

- Recent queries cached for instant retrieval
- Configurable TTL (default: 1 hour)
- Automatic cache invalidation on new documents
- LRU eviction for memory management

### Index Optimization

**SQLite:**
- Automatic vacuum on startup
- Periodic index rebuilding
- Query plan optimization

**PostgreSQL:**
- HNSW index for vector similarity
- B-tree indexes on metadata fields
- Automatic statistics updates
- Parallel query execution

## Troubleshooting

**Slow searches:**
- Consider migrating to PostgreSQL for large datasets (>10K docs)
- Enable query caching
- Reduce `CHAT_TOP_STORIES` value
- Check database indexes

**Irrelevant results:**
- Increase `CHAT_SIMILARITY_THRESHOLD`
- Enable metadata-aware scoring
- Try hybrid search (PostgreSQL)
- Use more specific queries

**No results found:**
- Lower `CHAT_SIMILARITY_THRESHOLD`
- Verify embeddings are generated
- Check if documents match query domain
- Try keyword search as fallback

**Migration issues:**
- See [PostgreSQL Migration Guide](../../../PGVECTOR_MIGRATION_GUIDE.md)
- Backup SQLite database before migration
- Test connection before starting migration
- Monitor progress logs during migration

## Related Documentation

- [Semantic Search Improvements](../../../SEMANTIC_SEARCH_IMPROVEMENTS.md) - Technical deep dive
- [Semantic Search Usage](../../../SEMANTIC_SEARCH_USAGE.md) - Complete usage guide
- [PostgreSQL Quickstart](../../../POSTGRES_QUICKSTART.md) - PostgreSQL setup
- [Document Library](../advanced-features/document-library.md) - UI integration
- [Interactive AI Chat](ai-chat.md) - Chat integration
