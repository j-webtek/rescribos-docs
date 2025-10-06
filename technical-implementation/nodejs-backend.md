# Node.js Backend

### 7.3 Configuration Management

Rescribos uses **80+ environment variables** for comprehensive configuration:

**Configuration File (`.env.example`):**
```env
# ============================================
# GENERAL SETTINGS
# ============================================
APP_NAME=Rescribos
APP_VERSION=2.0.0
NODE_ENV=production
LOG_LEVEL=info
DATA_DIR=./storage

# ============================================
# AI PROVIDER SETTINGS
# ============================================

# OpenAI Configuration
OPENAI_API_KEY=sk-...                    # User-provided (BYOK)
OPENAI_MODEL=gpt-4o                      # gpt-4o, gpt-4, gpt-3.5-turbo
OPENAI_TEMPERATURE=0.7                   # 0.0-2.0
OPENAI_MAX_TOKENS=4096                   # Max response length
EMBEDDING_MODEL=text-embedding-3-large   # Embedding model
EMBEDDING_DIMENSIONS=1536                # Vector dimensions
EMBEDDING_BATCH_SIZE=100                 # Batch processing size

# Ollama Configuration
OLLAMA_ENABLED=true
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b
OLLAMA_EMBED_MODEL=nomic-embed-text
OLLAMA_TIMEOUT=120000                    # 2 minutes

# Local Models
LOCAL_EMBED_MODEL=all-MiniLM-L6-v2
LOCAL_EMBED_DEVICE=cpu                   # cpu or cuda
FORCE_OFFLINE_MODE=false

# ============================================
# EXTRACTION SETTINGS
# ============================================

# Hacker News
HACKER_NEWS_API_URL=https://hacker-news.firebaseio.com/v0/
MAX_STORIES=500
MAX_STORY_AGE_HOURS=36
MIN_SCORE=10
MIN_COMMENTS=5

# arXiv
ARXIV_API_URL=https://export.arxiv.org/api/query
ARXIV_MAX_RESULTS=100
ARXIV_CATEGORIES=cs.AI,cs.LG,cs.CL        # Computer Science

# Extraction Behavior
EXTRA_FETCH_CONCURRENCY=5                 # Concurrent requests
FETCH_TIMEOUT=30000                       # 30 seconds
RETRY_ATTEMPTS=3
RETRY_BACKOFF=exponential

# Filtering
USE_GPT41_AI_SCREENING=true               # Pre-filter with AI
FILTER_KEYWORDS=AI,machine learning,LLM,GPT,neural,deep learning
EXCLUDE_KEYWORDS=crypto,bitcoin,NFT
DEDUP_ENABLED=true
DEDUP_THRESHOLD=0.85                      # Cosine similarity

# ============================================
# ANALYSIS SETTINGS
# ============================================

# Summarization
SUMMARY_LENGTH=1000                       # Characters
SUMMARY_STYLE=technical                   # technical, general, brief
INCLUDE_CITATIONS=true

# Relevance Scoring
RELEVANCE_THRESHOLD=0.6                   # 0.0-1.0
AUTO_FILTER_LOW_RELEVANCE=true

# Tagging
MAX_TAGS_PER_STORY=5
TAG_MIN_FREQUENCY=2
TAG_NGRAM_RANGE=1,2                       # Unigrams and bigrams

# Clustering
CLUSTERING_ALGORITHM=agglomerative        # agglomerative, hdbscan, tfidf
MAX_CLUSTER_SIZE=8
MIN_CLUSTER_SIZE=2
SIMILARITY_METRIC=cosine

# ============================================
# THEMATIC ANALYSIS
# ============================================
THEMATIC_ENABLED=true
MAX_SECTIONS=10
MIN_STORIES_PER_SECTION=5
INCLUDE_EXECUTIVE_SUMMARY=true
IMPLICATION_DEPTH=3                       # 1st, 2nd, 3rd order
CITATION_STYLE=numbered                   # numbered, inline, footnote

# ============================================
# SEARCH & CHAT
# ============================================
CHAT_ENABLED=true
CHAT_MODEL=gpt-4o
CHAT_TEMPERATURE=0.7
CHAT_MAX_TOKENS=2048
CHAT_HISTORY_LENGTH=6                     # Conversation turns
CHAT_SIMILARITY_THRESHOLD=0.2
CHAT_TOP_STORIES=5                        # Context injection
CHAT_USE_STREAMING=true

SEARCH_TOP_K=20
SEARCH_THRESHOLD=0.3
SEARCH_RERANK=true

# ============================================
# EXPORT SETTINGS
# ============================================
EXPORT_PDF_ENABLED=true
EXPORT_DOCX_ENABLED=true
EXPORT_MD_ENABLED=true
EXPORT_JSON_ENABLED=true
EXPORT_XLSX_ENABLED=true

PDF_PAGE_SIZE=A4
PDF_MARGIN_TOP=20mm
PDF_MARGIN_BOTTOM=20mm
PDF_INCLUDE_TOC=true
PDF_INCLUDE_HEADERS=true

# ============================================
# PERFORMANCE
# ============================================
MAX_CONCURRENT_AI_REQUESTS=10
RATE_LIMIT_RPM=60                         # Requests per minute
EMBEDDING_CACHE_TTL_HOURS=24
ENABLE_GPU=false
MAX_MEMORY_MB=2048

# ============================================
# SECURITY
# ============================================
ALLOW_INSECURE_CONNECTIONS=false
CERTIFICATE_VALIDATION=strict
ENABLE_CORS=false
PROXY_ENABLED=false
PROXY_URL=

# ============================================
# LICENSE
# ============================================
LICENSE_SERVER=https://license.rescribos.com
LICENSE_VALIDATION_INTERVAL_HOURS=24
OFFLINE_GRACE_PERIOD_DAYS=30

# ============================================
# LOGGING & MONITORING
# ============================================
LOG_TO_FILE=true
LOG_TO_CONSOLE=true
LOG_ROTATION_SIZE=10MB
LOG_MAX_FILES=5
PERFORMANCE_MONITORING=true
ERROR_REPORTING=local                     # local, sentry, none
```

**Configuration Loading (`src/shared/config.js`):**
```javascript
const dotenv = require('dotenv');
const path = require('path');
const fs = require('fs');

class ConfigManager {
    constructor() {
        this.config = {};
        this.loadEnvironment();
        this.validateConfig();
    }

    loadEnvironment() {
        // Load from multiple sources (priority order)
        const envFiles = [
            '.env.local',           // User overrides
            '.env',                 // Default config
            '.env.production'       // Production defaults
        ];

        for (const file of envFiles) {
            const filePath = path.join(process.cwd(), file);
            if (fs.existsSync(filePath)) {
                dotenv.config({ path: filePath });
            }
        }

        this.config = process.env;
    }

    get(key, defaultValue = null) {
        return this.config[key] || defaultValue;
    }

    getInt(key, defaultValue = 0) {
        return parseInt(this.config[key]) || defaultValue;
    }

    getBool(key, defaultValue = false) {
        const value = this.config[key];
        if (value === undefined) return defaultValue;
        return value === 'true' || value === '1';
    }

    validateConfig() {
        // Ensure critical settings are present
        const required = [
            'APP_NAME',
            'APP_VERSION',
            'DATA_DIR'
        ];

        for (const key of required) {
            if (!this.config[key]) {
                throw new Error(`Missing required config: ${key}`);
            }
        }
    }
}

module.exports = new ConfigManager();
```

### 7.4 System Requirements

**Minimum Requirements:**
```
Operating System: Windows 10/11, macOS 11+, Ubuntu 20.04+
Processor: Intel Core i3 / AMD Ryzen 3 (2.0 GHz)
Memory: 4 GB RAM
Storage: 5 GB available space
Display: 1280x720 resolution
Network: Internet connection (for cloud AI)
```

**Recommended Requirements:**
```
Operating System: Windows 11, macOS 13+, Ubuntu 22.04+
Processor: Intel Core i7 / AMD Ryzen 7 (3.0 GHz+)
Memory: 16 GB RAM
Storage: 20 GB SSD
Display: 1920x1080 resolution
Network: High-speed internet (10 Mbps+)
GPU: Optional (for local model acceleration)
```

**For Ollama (Local AI):**
```
Additional Memory: +8 GB RAM (8B models)
Storage: +10 GB (model weights)
Processor: 4+ cores recommended
```

**Network Requirements:**
```
Firewall Ports (Outbound):
- 443 (HTTPS): OpenAI API, Hacker News, arXiv
- 11434 (Local): Ollama service

Bandwidth Estimate:
- Extraction: 50-100 MB per run
- AI API calls: 1-5 MB per run
- Total monthly: 500 MB - 2 GB (typical usage)
```
