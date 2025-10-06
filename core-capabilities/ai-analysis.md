# AI-Powered Analysis

### 2.2 AI-Powered Analysis

Each collected item undergoes sophisticated AI analysis to extract insights and generate actionable intelligence:

**Analysis Components:**

**1. Summarization**
- **Models:** GPT-4o (cloud) or Llama 3.1:8b (local)
- **Length:** Configurable (default: 1000 characters)
- **Quality:** Context-aware with citation preservation
- **Temperature:** 0.7 for creative-yet-factual balance

**2. Relevance Scoring**
- AI-driven content evaluation (0.0-1.0 scale)
- Multi-criteria assessment (novelty, impact, accuracy)
- Threshold-based filtering (default: 0.6)

**3. Embedding Generation**
- **Vector Dimensions:** 1536 (OpenAI), 768 (local), 256 (hash fallback)
- **Providers:** OpenAI, Ollama, SentenceTransformers
- **Batch Processing:** 100 stories per batch for efficiency
- **Storage:** SQLite database with indexed queries

**4. Automated Tagging**
- TF-IDF n-gram extraction (1-2 grams)
- Top-5 tags per story
- Stop word filtering
- Cross-story tag normalization

**5. Clustering**
- **Algorithms:** AgglomerativeClustering, TF-IDF, embedding-based
- **Similarity Metric:** Cosine similarity on vectors
- **Cluster Size:** Dynamic (max 8 stories per cluster)
- **Hierarchy:** Multi-level grouping for complex datasets

**Configuration:**
```env
OPENAI_MODEL=gpt-4o
OPENAI_TEMPERATURE=0.7
SUMMARY_LENGTH=1000
EMBEDDING_MODEL=text-embedding-3-large
EMBEDDING_BATCH_SIZE=100
DEDUP_THRESHOLD=0.85
```

**Analysis Pipeline:**
```
Raw Story → Summarization → Relevance Scoring → Embedding Generation → Tagging → Clustering → Output
    ↓           ↓                ↓                     ↓                ↓          ↓           ↓
  5-10s      2-3s/story      0.5s/story           1s/batch         0.1s      0.5s      JSON/Markdown
```
