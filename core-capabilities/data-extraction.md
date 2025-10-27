# Intelligent Data Extraction

## Overview

Rescribos automatically collects content from diverse sources, applying AI-driven filtering to ensure relevance. The multi-source extraction system provides a flexible, configurable architecture for gathering AI-related content from news sources, research repositories, government databases, and local documents.

## Supported Data Sources

### Built-in Sources

**1. Hacker News** (Enabled by default)
- Real-time technology news and AI discussions
- Firebase API integration for story retrieval
- Configurable story limits (default: 30 per request)
- Age-based filtering (default: 36 hours)
- Full article content extraction from linked URLs
- Rate limit: 100 requests/hour

**2. arXiv** (Enabled by default)
- Academic research papers in AI/ML categories
- Categories: cs.AI, cs.LG, cs.CL, cs.CV
- Full metadata: DOI, authors, citations, abstracts
- Configurable result limits (default: 50 per category)
- Sort by submission date or relevance
- Rate limit: 50 requests/hour

**3. USASpending.gov** (Enabled by default)
- Federal government contract awards and transactions
- AI-related contract opportunities and spending data
- Award types: contracts, grants, loans, direct payments
- Context enrichment with prime award information
- Configurable lookback periods (default: 7 days)
- Rate limit: 1000 requests/hour

**4. SAM.gov** (Disabled by default, configurable)
- System for Award Management procurement data
- Government contract opportunities and solicitations
- NAICS code filtering for tech/AI sectors
- AI keyword matching with 300+ term dictionary
- Notice types: Presolicitation, Solicitation, Combined Synopsis
- Rate limit: 1000 requests/day
- Requires API key (register at SAM.gov)

### Additional Content Sources

- **Local Documents** - PDF, DOCX, and TXT files via Document Library
- **Folder Watch** - Automatic monitoring of directories for new documents
- **Custom Data Sources** - Generate REST/RSS/GraphQL connectors with `scripts/create_datasource.py`
- **Web Content** - Article scraping for extracted URLs with BeautifulSoup4
- **Browser Automation** - Playwright for JavaScript-heavy sites

## Extraction Features

### Core Capabilities

- **Multi-Source Orchestration** - Fetches from all enabled sources in parallel
- **Concurrent Processing** - 5-10 simultaneous requests with semaphore control (configurable)
- **Smart Filtering** - Multi-layer filtering with keywords, domains, and content rules
- **AI-Powered Relevance** - Optional GPT pre-screening for precision filtering
- **Age-Based Filtering** - Configurable time windows (default: 36 hours)
- **Duplicate Detection** - Embedding-based deduplication across all sources (0.85 similarity threshold)
- **Error Recovery** - Exponential backoff with configurable retry attempts (default: 3)
- **Progress Tracking** - Real-time UI updates via JSON protocol with detailed statistics
- **Content Extraction** - Full article text extraction with timeout protection
- **Rate Limiting** - Per-source rate limits with automatic throttling

### Advanced Filtering System

The extraction pipeline includes multiple filtering layers configured in `config/data_sources.json`:

**Title Filtering:**
- Minimum length: 10 characters
- Maximum length: 200 characters
- Removes incomplete or spam titles

**Domain Filtering:**
- Blocked domains list to avoid low-quality sources
- Configurable domain blacklist
- Per-source domain restrictions

**Keyword Filtering:**
- 300+ AI-related required keywords
- Case-insensitive matching
- Excluded keywords to filter spam/clickbait
- Customizable keyword dictionaries per source

**Content Quality:**
- Minimum content length requirements (default: 220 characters)
- Content refresh for articles below threshold
- Automatic retry queue for failed extractions

### Categorization System

Stories are automatically categorized based on source and content:

**Categories:**
- `arxiv_stories` - Academic research papers from arXiv
- `other_stories` - News, discussions, and government data
- Configurable rules in `config/data_sources.json`

**Categorization Rules:**
- Source-based: Stories inherit category from their source
- Keyword-based: Content analysis for ambiguous sources
- Custom rules: Define your own categories and matching logic

## Configuration

### Environment Variables

Configure extraction behavior in `.env`:

```env
# API Endpoints
HACKER_NEWS_API_URL=https://hacker-news.firebaseio.com/v0/
ARXIV_API_URL=https://export.arxiv.org/api/query

# Extraction Limits
MAX_STORIES=500              # Total stories to extract per run
MAX_STORY_AGE_HOURS=36      # Only fetch recent content
MAX_CONCURRENT_REQUESTS=5    # Parallel request limit

# AI Screening (Optional)
CHECK_SUMMARY_FOR_AI=true   # Enable GPT-based relevance check

# Retry Behavior
RETRY_COUNT=3               # Failed request retry attempts
RETRY_BACKOFF_BASE=2        # Exponential backoff multiplier

# Content Extraction
EXTRA_FETCH_CONCURRENCY=5   # Parallel content extraction
SKIP_NETWORK_CHECK=false    # Skip connectivity check before extraction
```

### Data Source Configuration

Enable/disable and configure sources in `config/data_sources.json`:

```json
{
  "sources": [
    {
      "name": "hackernews",
      "enabled": true,
      "category": "other_stories",
      "config": {
        "max_stories": 30,
        "max_age_hours": 36,
        "extract_content": true
      }
    },
    {
      "name": "usaspending",
      "enabled": true,
      "config": {
        "max_items": 30,
        "discover_days": 7,
        "enable_prime_context": true
      }
    }
  ],
  "global_config": {
    "concurrent_sources": 5,
    "retry_attempts": 3,
    "timeout": 30,
    "enable_deduplication": true,
    "deduplication_similarity_threshold": 0.85
  }
}
```

### Custom Data Sources

Create custom connectors for proprietary or specialized sources:

**Using the Data Source Generator:**
```bash
# Interactive wizard
python scripts/create_datasource.py

# Command-line
python scripts/create_datasource.py \
  --name "MySource" \
  --type rest \
  --endpoint "https://api.example.com/articles"
```

**Manual Configuration:**
1. Edit `config/data_sources.json`
2. Add new source with required fields:
   - `name`: Unique identifier
   - `enabled`: true/false
   - `category`: Story categorization
   - `class_name`: Python class implementing source
   - `config`: Source-specific settings
   - `rate_limit`: Request throttling
   - `auth`: Authentication configuration

**Supported Source Types:**
- REST APIs with JSON/XML responses
- RSS/Atom feeds
- GraphQL endpoints
- Custom Python implementations

See [API Data Source Integration Guide](../docs/API_DATASOURCE_INTEGRATION_GUIDE.md) for detailed instructions.

## Performance Metrics

**Typical Extraction Performance:**
- 200-500 stories in 2-5 minutes
- Network bandwidth: ~50MB per full extraction
- Memory usage: 200-400MB during extraction
- CPU usage: Moderate (content extraction is I/O bound)

**Storage Locations:**
- Extracted data: `storage/extracted/`
- Failed extractions: `storage/rejected/error_stories.jsonl`
- Retry queue: `storage/extraction_retry_queue.json`
- Deduplication database: `storage/embeddings.db`

## Monitoring and Troubleshooting

**Progress Tracking:**
- Real-time console output with source-by-source progress
- JSON protocol messages for UI integration
- Detailed statistics: fetched, filtered, deduplicated, errors

**Common Issues:**

**Network Timeouts:**
- Increase `NETWORK_CHECK_TIMEOUT` in `.env`
- Check firewall/proxy settings
- Use `SKIP_NETWORK_CHECK=true` for offline testing

**Rate Limit Errors:**
- Reduce `concurrent_sources` in data_sources.json
- Decrease `MAX_CONCURRENT_REQUESTS`
- Adjust per-source rate limits

**Content Extraction Failures:**
- Check `storage/rejected/error_stories.jsonl` for details
- Increase `content_extraction_timeout` in data_sources.json
- Verify target sites are accessible

**Duplicate Stories:**
- Adjust `deduplication_similarity_threshold` (0.0-1.0)
- Lower values = stricter deduplication
- Default: 0.85 (85% similar)

## See Also

- [Multi-Source Extraction Guide](../docs/MULTI_SOURCE_EXTRACTION_GUIDE.md) - Advanced multi-source configuration
- [API Data Source Integration](../docs/API_DATASOURCE_INTEGRATION_GUIDE.md) - Custom connector development
- [Data Pipeline Workflow](../data-pipeline/workflow.md) - Complete extraction → analysis flow
- [Configuration Guide](../deployment/configuration.md) - All configuration options
