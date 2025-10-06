# Intelligent Data Extraction

### 2.1 Intelligent Data Extraction

Rescribos automatically collects content from diverse sources, applying AI-driven filtering to ensure relevance:

**Supported Sources:**
- **Hacker News** - Real-time tech news and discussions
- **arXiv** - Academic papers with full metadata (DOI, authors, citations)
- **Local Documents** - PDF, DOCX, TXT files
- **Web Content** - Custom URL scraping with BeautifulSoup4
- **Browser Automation** - Playwright for JavaScript-heavy sites

**Extraction Features:**
- **Concurrent Processing** - 5-10 simultaneous requests with semaphore control
- **Smart Filtering** - Keyword-based relevance with regex patterns
- **Optional AI Screening** - GPT-4o pre-filtering for precision
- **Age-Based Filtering** - Configurable time windows (default: 36 hours)
- **Duplicate Detection** - Hash-based deduplication across sources
- **Error Recovery** - Exponential backoff with 3 retry attempts
- **Progress Tracking** - Real-time UI updates via JSON protocol

**Configuration Example:**
```env
HACKER_NEWS_API_URL=https://hacker-news.firebaseio.com/v0/
ARXIV_API_URL=https://export.arxiv.org/api/query
MAX_STORIES=500
MAX_STORY_AGE_HOURS=36
EXTRA_FETCH_CONCURRENCY=5
USE_GPT41_AI_SCREENING=true
```

**Performance:**
- Average extraction: 200-500 stories in 2-5 minutes
- Network bandwidth: ~50MB per full extraction
- Rejected story tracking: `storage/rejected/error_stories.jsonl`
