# Semantic Search Improvements Plan

## Executive Summary

This document outlines a comprehensive plan to enhance the semantic search system with advanced retrieval, ranking, and explainability features. All improvements are designed to be backward-compatible and will not break existing functionality.

## Current Architecture Overview

- **Database**: Dual backend (SQLite + PostgreSQL with pgvector)
- **Search Method**: Pure cosine similarity on embeddings
- **Ranking**: Simple similarity score ordering
- **Threshold**: Static 0.15 default
- **Metadata**: Available but only used for post-filtering

## Improvement Phases

### Phase 1: Semantic Reranking (HIGH PRIORITY)
**Problem**: Initial retrieval uses only cosine similarity without considering semantic coherence, context relevance, or diversity.

**Solution Components**:
1. **Cross-Encoder Reranking**
   - Use sentence-transformers cross-encoder models (e.g., `cross-encoder/ms-marco-MiniLM-L-12-v2`)
   - Apply to top-50 candidates from initial retrieval
   - More accurate than bi-encoder similarity
   - Scores query-document pairs directly

2. **MMR (Maximal Marginal Relevance) Diversification**
   - Reduce redundancy in results
   - Balance relevance vs diversity
   - Formula: `MMR = λ × Sim(D, Q) - (1-λ) × max(Sim(D, Di))`
   - λ parameter controls relevance/diversity tradeoff (default: 0.7)

3. **LLM-based Relevance Scoring (Optional)**
   - For high-stakes queries, use GPT-4o-mini to score top 10 results
   - Provides semantic understanding beyond embeddings
   - Cached aggressively to minimize API costs

**Implementation**:
- New module: `scripts/embedding/reranking.py`
- Integration point: After initial retrieval, before returning results
- Configuration: `enable_reranking`, `reranking_method`, `mmr_lambda`

**Expected Impact**:
- 15-30% improvement in relevance metrics (NDCG, MRR)
- Better diversity in result sets
- Minimal performance impact (cross-encoder on CPU: ~50ms for 50 docs)

---

### Phase 2: Dynamic Similarity Thresholds (HIGH PRIORITY)
**Problem**: Static 0.15 threshold doesn't adapt to query complexity or specificity.

**Solution Components**:
1. **Query Specificity Detection**
   - Metrics:
     - Query length (longer = more specific)
     - Technical term density (using NER or keyword lists)
     - Embedding entropy/concentration
   - Classification: `low`, `medium`, `high` specificity

2. **Adaptive Threshold Calculation**
   ```python
   base_threshold = 0.15
   if specificity == 'high':
       threshold = 0.25  # More selective for technical queries
   elif specificity == 'low':
       threshold = 0.10  # More permissive for broad queries
   else:
       threshold = base_threshold
   ```

3. **Historical Performance Tracking**
   - Track precision/recall per query type
   - Adjust thresholds based on feedback
   - Store in `embedding_cache.py` with query metadata

**Implementation**:
- Extend `query_embeddings.py` with specificity analyzer
- New function: `calculate_dynamic_threshold(query, embedding)`
- Configuration: `use_dynamic_thresholds`, `threshold_strategy`

**Expected Impact**:
- Reduce false positives for technical queries
- Increase recall for exploratory queries
- Better user experience with context-aware filtering

---

### Phase 3: Hybrid Search (BM25 + Semantic) (HIGH PRIORITY)
**Problem**: Pure semantic search can miss exact keyword matches and relies entirely on embedding quality.

**Solution Components**:
1. **BM25 Index Integration**
   - Use Elasticsearch or lightweight BM25 implementation (rank-bm25)
   - Index story titles, analysis, and snapshots
   - Efficient keyword-based retrieval

2. **Dual Retrieval Pipeline**
   - Parallel execution:
     - Semantic search (existing pgvector/SQLite)
     - BM25 keyword search
   - Retrieve top-50 from each method

3. **Reciprocal Rank Fusion (RRF)**
   - Combines rankings from multiple sources
   - Formula: `RRF(d) = Σ 1/(k + rank_i(d))` where k=60
   - No parameter tuning required
   - Robust to score scale differences

4. **Alternative: Linear Combination**
   - `final_score = α × semantic_score + (1-α) × bm25_score`
   - α parameter tunable (default: 0.7 for semantic emphasis)

**Implementation**:
- New module: `scripts/embedding/hybrid_search.py`
- BM25 index stored in PostgreSQL using `tsvector` or separate index file
- Configuration: `enable_hybrid_search`, `hybrid_fusion_method`, `semantic_weight`

**Expected Impact**:
- Better recall for specific entity/acronym searches (e.g., "GPT-4", "CUDA")
- Improved precision through complementary signals
- Fallback to keywords when embeddings fail

---

### Phase 4: Metadata-Aware Scoring (MEDIUM PRIORITY)
**Problem**: Search doesn't leverage structured metadata for relevance ranking.

**Solution Components**:
1. **Recency Scoring**
   - Exponential decay: `recency_score = exp(-λ × days_old)`
   - λ = 0.01 (half-life ~70 days)
   - Boost recent content without discarding older gems

2. **Source Authority Weighting**
   - Source reputation scores:
     - `arxiv`: 1.2x
     - `hackernews`: 1.0x (baseline)
     - `sam`: 1.1x
   - Configurable per deployment

3. **Engagement Signals** (Future)
   - View counts, click-through rates (CTR)
   - User-provided ratings
   - Implicit feedback (time on page)

4. **Combined Scoring Formula**
   ```python
   final_score = (
       similarity_score * 0.6 +
       recency_score * 0.2 +
       source_authority * 0.1 +
       engagement_score * 0.1
   )
   ```

**Implementation**:
- Extend database schema with `view_count`, `ctr`, `authority_score` columns
- Modify `query_embeddings()` to compute composite scores
- Configuration: `enable_metadata_scoring`, `recency_weight`, `authority_weights`

**Expected Impact**:
- Prioritize timely and authoritative content
- Better user satisfaction through quality signals
- Flexible scoring for different use cases

---

### Phase 5: Query Understanding & Parsing (MEDIUM PRIORITY)
**Problem**: System treats all queries as simple strings without entity extraction or intent detection.

**Solution Components**:
1. **Named Entity Recognition (NER)**
   - Use spaCy or Hugging Face transformers
   - Extract: organizations, technologies, people, locations
   - Example: "OpenAI GPT-4 safety" → entities: ["OpenAI", "GPT-4"]

2. **Intent Classification**
   - Categories:
     - `how_to`: Instructional queries
     - `definition`: Conceptual understanding
     - `comparison`: Comparative analysis
     - `news`: Current events
     - `technical`: Deep technical queries
   - Simple keyword-based classifier or lightweight BERT model

3. **Query Expansion with Entities**
   - Boost documents mentioning detected entities
   - Add synonyms for entities (e.g., "AI" → "artificial intelligence")
   - Use knowledge graphs for entity relationships

4. **Structured Query Parsing** (Advanced)
   - Support operators: AND, OR, NOT
   - Field-specific queries: `title:"GPT-4" AND source:arxiv`
   - Date range syntax: `after:2024-01-01`

**Implementation**:
- New module: `scripts/embedding/query_parser.py`
- Integration before embedding generation
- Configuration: `enable_query_parsing`, `ner_model`, `intent_classifier`

**Expected Impact**:
- Better understanding of user intent
- More targeted retrieval through entity boosting
- Foundation for advanced query syntax

---

### Phase 6: Embedding Validation & Consistency (HIGH PRIORITY)
**Problem**: No enforcement that all embeddings use the same model/dimension.

**Solution Components**:
1. **Embedding Metadata Storage**
   - Add columns to database:
     - `embedding_model`: Model identifier (e.g., "text-embedding-3-small")
     - `embedding_dimension`: Vector dimension (e.g., 1536)
     - `embedding_version`: Versioning for model updates
     - `created_at`: Timestamp for tracking

2. **Pre-Search Validation**
   - Check query embedding matches database embeddings
   - Prevent dimension mismatches
   - Warning logs for mixed embedding models

3. **Multiple Embedding Space Support**
   - Separate indexes per embedding model
   - Table structure: `story_embeddings_{model_name}`
   - Query routing based on selected model

4. **Migration Tools**
   - Script to re-embed existing data with new models
   - Batch processing with progress tracking
   - Validation of migration completeness

**Implementation**:
- Schema migration: Add metadata columns to all embedding tables
- Validation in `embedding_db.py` and `embedding_db_pg.py`
- Migration script: `scripts/embedding/migrate_embeddings.py`

**Expected Impact**:
- Prevent silent failures from dimension mismatches
- Enable safe model upgrades
- Support for multi-model deployments

---

### Phase 7: Feedback Loop & Continuous Improvement (MEDIUM PRIORITY)
**Problem**: System doesn't learn from user behavior or collect implicit feedback.

**Solution Components**:
1. **Click-Through Rate (CTR) Tracking**
   - Log user interactions:
     - Query → Results shown
     - Results clicked
     - Time spent on clicked articles
   - Store in `user_feedback` table

2. **Implicit Feedback Collection**
   - Signals:
     - Position of clicked results (higher position = weaker signal)
     - Dwell time (longer = more relevant)
     - Bounce rate (quick return = not relevant)
   - Privacy-preserving: No personal data stored

3. **Relevance Score Adjustment**
   - Use feedback to boost/demote results
   - Formula: `adjusted_score = base_score × (1 + β × ctr_score)`
   - β = 0.2 (configurable)

4. **Learning-to-Rank (LTR) Integration** (Advanced)
   - Train lightweight ranking model on feedback data
   - Features: similarity score, metadata, feedback signals
   - Model: LambdaMART, RankNet, or simple gradient boosting

**Implementation**:
- New module: `scripts/embedding/feedback_tracker.py`
- Database tables: `query_logs`, `click_logs`, `feedback_scores`
- Background job to compute feedback-adjusted scores
- Configuration: `enable_feedback_tracking`, `feedback_weight`

**Expected Impact**:
- Continuous improvement of ranking quality
- Personalization opportunities (future)
- Data-driven optimization

---

### Phase 8: Enhanced Query Expansion (MEDIUM PRIORITY)
**Problem**: Current expansion uses expensive GPT-4o-mini calls and lacks effective caching.

**Solution Components**:
1. **Local Query Expansion**
   - WordNet synonyms for common terms
   - Word embedding similarity (Word2Vec, GloVe)
   - Domain-specific thesaurus (AI/ML terms)
   - Fast and cost-free

2. **Cached Expansion Results**
   - Store expansions in `embedding_cache.py`
   - TTL: 7 days (expansions stable over time)
   - Semantic deduplication of expanded terms

3. **Query Reformulation**
   - Transform queries for better results:
     - "best practices" → "how to", "guide", "tutorial"
     - "what is X" → definitions and explanations
     - "X vs Y" → comparisons and differences
   - Rule-based or template-based

4. **Smart Expansion Triggering**
   - Only expand when:
     - Initial query yields <5 results
     - Query is very short (<3 words)
     - User explicitly requests broader search
   - Avoid unnecessary API calls

**Implementation**:
- Extend `query_embeddings.py` with local expansion methods
- Add expansion cache to `embedding_cache.py`
- Configuration: `expansion_strategy`, `use_local_expansion`, `expansion_cache_ttl`

**Expected Impact**:
- Reduce API costs for query expansion
- Faster expansion (local models)
- Better recall for underspecified queries

---

### Phase 9: Explainability & Debugging (LOW PRIORITY - HIGH VALUE)
**Problem**: Users/developers can't see why a result was returned or debug poor results.

**Solution Components**:
1. **Match Explanation**
   - For each result, provide:
     - Similarity score breakdown (title, content, analysis)
     - Matched keywords (from BM25)
     - Entity matches
     - Metadata boosts applied

2. **Content Highlighting**
   - Identify matching segments in documents
   - Use attention weights or simple token overlap
   - Show top-3 matching sentences

3. **Similarity Visualization**
   - Compare query embedding to document embedding
   - Show dimension-wise contributions
   - Visualize as heatmap or bar chart (CLI-friendly format)

4. **Debug Mode**
   - `--debug` flag in query_embeddings.py
   - Verbose output:
     - Pre-filter candidate count
     - Post-filter result count
     - Threshold applied
     - Time per stage (retrieval, reranking, scoring)
   - Export results to JSON for analysis

5. **Similar Documents**
   - "More like this" functionality
   - Show top-5 similar documents for any result
   - Helps users explore related content

**Implementation**:
- New module: `scripts/embedding/explainer.py`
- CLI flag: `--explain` for detailed output
- JSON output format with explanation metadata
- Configuration: `enable_explanations`, `explanation_depth`

**Expected Impact**:
- Improved developer debugging
- Better user trust and transparency
- Insights for system optimization

---

### Phase 10: Integration Testing & Optimization (CRITICAL)
**Ensuring No System Breakage**

**Testing Strategy**:
1. **Unit Tests**
   - Test each new component in isolation
   - Mock external dependencies
   - Coverage target: 80%+

2. **Integration Tests**
   - End-to-end query flow with new features enabled
   - Backward compatibility tests (disable new features)
   - Performance regression tests

3. **A/B Testing Framework**
   - Compare new ranking vs old ranking
   - Metrics: NDCG, MRR, user satisfaction
   - Gradual rollout with feature flags

4. **Fallback Mechanisms**
   - If reranking fails → fall back to basic similarity
   - If hybrid search fails → fall back to semantic only
   - If dynamic thresholds fail → use static threshold
   - Graceful degradation for all new features

**Performance Optimization**:
1. **Caching at Every Level**
   - Query embeddings
   - BM25 scores
   - Reranking results
   - Metadata scores

2. **Batch Processing**
   - Batch embedding generation
   - Batch reranking
   - Parallel query execution

3. **Lazy Loading**
   - Load reranking models only when needed
   - Initialize BM25 index on first use
   - Defer expensive operations

4. **Profiling & Monitoring**
   - Track query latency (p50, p95, p99)
   - Monitor cache hit rates
   - Alert on performance degradation

**Implementation**:
- Test suite: `tests/test_semantic_search_improvements.py`
- Benchmark suite: `scripts/benchmark_search.py`
- Feature flag configuration: `enable_*` settings in config
- Monitoring dashboard integration

---

## Configuration Schema Extensions

### New Configuration Options

```python
class EmbeddingChatConfig:
    # Existing fields...

    # Reranking
    enable_reranking: bool = True
    reranking_method: str = "cross_encoder"  # "cross_encoder" | "llm" | "mmr"
    mmr_lambda: float = 0.7  # Relevance vs diversity tradeoff
    cross_encoder_model: str = "cross-encoder/ms-marco-MiniLM-L-12-v2"

    # Dynamic thresholds
    use_dynamic_thresholds: bool = True
    threshold_strategy: str = "adaptive"  # "adaptive" | "static"
    min_threshold: float = 0.05
    max_threshold: float = 0.40

    # Hybrid search
    enable_hybrid_search: bool = True
    hybrid_fusion_method: str = "rrf"  # "rrf" | "linear"
    semantic_weight: float = 0.7  # For linear fusion
    bm25_k1: float = 1.5
    bm25_b: float = 0.75

    # Metadata scoring
    enable_metadata_scoring: bool = True
    recency_weight: float = 0.2
    recency_decay_rate: float = 0.01  # Daily decay
    authority_weights: Dict[str, float] = {
        "arxiv": 1.2,
        "hackernews": 1.0,
        "sam": 1.1
    }

    # Query understanding
    enable_query_parsing: bool = True
    ner_model: str = "en_core_web_sm"  # spaCy model
    intent_classifier: str = "keyword"  # "keyword" | "bert"

    # Embedding validation
    enforce_embedding_consistency: bool = True
    allow_multiple_embedding_models: bool = False

    # Feedback tracking
    enable_feedback_tracking: bool = False  # Opt-in for privacy
    feedback_weight: float = 0.2

    # Query expansion
    expansion_strategy: str = "local"  # "local" | "llm" | "hybrid"
    use_local_expansion: bool = True
    expansion_cache_ttl: int = 604800  # 7 days in seconds

    # Explainability
    enable_explanations: bool = False  # Performance impact
    explanation_depth: str = "basic"  # "basic" | "detailed"

    # Performance
    reranking_batch_size: int = 50
    hybrid_search_timeout: float = 5.0  # seconds
    max_parallel_queries: int = 3
```

---

## Migration Plan

### Rollout Strategy

**Phase 1-3 (Weeks 1-2)**: Core Retrieval Improvements
- Reranking, dynamic thresholds, hybrid search
- High impact, moderate risk
- Feature flags: default OFF, enable progressively

**Phase 4-6 (Weeks 3-4)**: Metadata & Validation
- Metadata scoring, query parsing, embedding validation
- Medium impact, low risk
- Can run in parallel with Phase 1-3

**Phase 7-9 (Weeks 5-6)**: Advanced Features
- Feedback tracking, enhanced expansion, explainability
- Lower priority, high value for power users
- Optional features, default OFF

**Phase 10 (Ongoing)**: Testing & Optimization
- Continuous throughout all phases
- Performance benchmarking after each phase
- User feedback collection and iteration

### Backward Compatibility

- All new features behind feature flags (default OFF)
- Existing API unchanged (new parameters optional)
- Database schema migrations backward compatible
- Fallback to original behavior if new features fail

---

## Success Metrics

### Performance Metrics
- **Query Latency**: <500ms p95 (currently varies)
- **Throughput**: 10+ queries/second
- **Cache Hit Rate**: >60%

### Relevance Metrics
- **NDCG@10**: >0.7 (normalized discounted cumulative gain)
- **MRR**: >0.6 (mean reciprocal rank)
- **Recall@25**: >0.8

### User Satisfaction
- **Click-Through Rate**: Track and improve over baseline
- **Zero-Result Rate**: <5%
- **User Feedback**: Positive sentiment trend

---

## Risk Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| Performance degradation | High | Caching, lazy loading, feature flags |
| Breaking existing functionality | Critical | Extensive testing, backward compatibility |
| Model loading time | Medium | Lazy initialization, model caching |
| API cost increase (LLM reranking) | Medium | Local models default, LLM opt-in only |
| Database migration issues | High | Staged migrations, rollback procedures |
| Increased complexity | Medium | Modular design, comprehensive docs |

---

## Implementation Order (Prioritized)

1. **Phase 6**: Embedding validation (prevents future issues)
2. **Phase 2**: Dynamic thresholds (quick win, high impact)
3. **Phase 1**: Semantic reranking (highest relevance improvement)
4. **Phase 3**: Hybrid search (complementary to reranking)
5. **Phase 4**: Metadata scoring (leverages existing data)
6. **Phase 8**: Enhanced expansion (cost reduction)
7. **Phase 5**: Query understanding (foundation for advanced features)
8. **Phase 9**: Explainability (debugging and trust)
9. **Phase 7**: Feedback tracking (long-term improvement)

Phase 10 (Testing) runs continuously throughout.

---

## Next Steps

1. Review and approve this plan
2. Set up feature flag infrastructure
3. Create test suite for backward compatibility
4. Begin Phase 6 implementation (embedding validation)
5. Parallel workstreams for Phase 1-3 after validation complete

---

## Document Version
- **Version**: 1.0
- **Date**: 2025-10-23
- **Author**: Claude (AI Assistant)
- **Status**: Proposed - Pending Approval
