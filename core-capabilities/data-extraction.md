# Intelligent Data Extraction

## Overview

Rescribos provides a flexible, extensible data extraction framework that connects to any information source your organization needs. Unlike rigid tools locked to vendor-defined sources, the platform's connector architecture adapts to YOUR data ecosystem—whether that's internal databases, proprietary APIs, industry-specific feeds, or public repositories.

**Key Principle:** The value of Rescribos lies in its AI-powered analysis pipeline and knowledge management capabilities, not in predefined data sources. Organizations configure the platform to connect to sources relevant to their specific needs.

## Data Source Architecture

### Connector Framework

The platform uses a **plugin-based connector system** that abstracts data source complexity:

- **Source-Agnostic Pipeline**: The analysis engine doesn't care where data comes from—REST API, database query, RSS feed, or file system
- **Standardized Interface**: All connectors implement a common interface, ensuring consistent behavior
- **Hot-Swappable**: Enable, disable, or replace sources without code changes
- **Parallel Execution**: Multiple sources fetch concurrently with intelligent rate limiting
- **Error Isolation**: Source failures don't cascade; the pipeline continues with available data

### Creating Custom Connectors

**Three Approaches:**

1. **Configuration-Based** (No Code Required)
   - Edit `config/data_sources.json` to add REST APIs, RSS feeds, or GraphQL endpoints
   - Specify authentication, rate limits, and filtering rules
   - Platform handles HTTP, pagination, retries, and error recovery

2. **Template-Based** (Minimal Code)
   - Run `python scripts/create_datasource.py` for guided connector generation
   - Answer prompts about your source (API endpoint, auth type, response format)
   - Generated Python class handles 90% of integration work

3. **Custom Implementation** (Full Control)
   - Implement `DataSource` base class for complex sources
   - Custom extraction logic, authentication flows, and data transformation
   - Full access to platform utilities (caching, logging, deduplication)

See [API Data Source Integration Guide](../reference-guides/API_DATASOURCE_INTEGRATION_GUIDE.md) for complete implementation details.

## Included Reference Sources

The platform ships with **example connectors** that demonstrate the framework's capabilities. These are **starting points**, not limitations—organizations typically replace or supplement them with domain-specific sources.

### Pre-Configured Examples

**Hacker News Connector** (Technology News)
- **Purpose**: Demonstrates public REST API integration with content extraction
- **Use Case**: Technology monitoring, developer community trends
- **Replaceability**: Replace with your industry news aggregator, internal news feed, or competitive intel sources
- **Configuration**: Firebase API endpoint, story limits, age filtering, full-text extraction

**arXiv Connector** (Academic Research)
- **Purpose**: Demonstrates research database integration with metadata handling
- **Use Case**: Academic literature monitoring, research trend analysis
- **Replaceability**: Replace with PubMed, IEEE Xplore, SSRN, internal research repositories, or patent databases
- **Configuration**: Category filters, result limits, citation extraction, DOI handling

**USASpending Connector** (Government Contracts)
- **Purpose**: Demonstrates complex API with nested data and context enrichment
- **Use Case**: Government contract monitoring, procurement intelligence
- **Replaceability**: Replace with private sector contract databases, RFP aggregators, or industry-specific procurement feeds
- **Configuration**: Award types, lookback periods, transaction filtering, prime award context

**SAM.gov Connector** (Government Opportunities)
- **Purpose**: Demonstrates authenticated API with keyword filtering and NAICS codes
- **Use Case**: Federal opportunity tracking, solicitation monitoring
- **Replaceability**: Replace with state/local procurement systems, international tenders, or private sector opportunity feeds
- **Configuration**: API authentication, keyword dictionaries, notice types, NAICS filtering

**Key Point:** These connectors demonstrate the platform's capabilities. Most organizations disable or replace them with sources specific to their domain—whether that's financial data feeds, legal databases, healthcare information systems, competitive intelligence sources, or internal document repositories.

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

See [API Data Source Integration Guide](../reference-guides/API_DATASOURCE_INTEGRATION_GUIDE.md) for detailed instructions.

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

## Responsible Data Collection

### Web Scraping Capabilities

Rescribos includes web scraping functionality for extracting content from public websites. This capability uses:

- **HTTP requests** with BeautifulSoup for HTML parsing
- **Browser automation** (Playwright) for JavaScript-heavy sites
- **Domain-specific extractors** optimized for common news sites
- **Anti-bot evasion** techniques for sites with protection mechanisms

**Important:** With these capabilities comes the responsibility to use them ethically and legally.

### Legal and Ethical Considerations

**robots.txt Compliance:**
- The platform does NOT automatically check or enforce robots.txt rules
- **User responsibility**: You must manually verify robots.txt compliance for websites you scrape
- Check `https://example.com/robots.txt` before configuring that domain as a source
- Respect Disallow directives and crawl-delay settings
- Some sites explicitly prohibit automated access—honor these restrictions

**Rate Limiting and Server Load:**
- **Default settings** use concurrent requests which can stress servers
- **Configure responsibly**: Reduce `concurrent_sources` and `MAX_CONCURRENT_REQUESTS` for smaller sites
- **Add delays**: Use rate limits in `config/data_sources.json` to space requests appropriately
- **Monitor errors**: High error rates may indicate you're overwhelming the target server
- **Consider off-peak hours**: Schedule extractions during low-traffic periods when possible

**IP Blocking Risks:**
- Aggressive scraping can result in **temporary or permanent IP bans**
- Sites with anti-bot protection may block your IP, VPN, or entire subnet
- **Corporate/institutional users**: IP bans may affect your entire organization
- **Residential users**: ISP may flag or restrict your connection
- **No workaround support**: The platform does not provide proxy rotation or ban circumvention

### Best Practices for Responsible Scraping

**1. Prefer Official APIs**
- Always use official APIs when available (even if paid)
- APIs are explicitly authorized, documented, and rate-limited appropriately
- Scraping should be a last resort, not the first choice

**2. Review Terms of Service**
- Read and comply with website Terms of Service before scraping
- Some sites explicitly prohibit automated access, even if robots.txt allows it
- Commercial use of scraped data may require licensing or permission

**3. Configure Conservative Defaults**
```json
{
  "global_config": {
    "concurrent_sources": 2,        // Reduce concurrent requests
    "timeout": 30,                  // Generous timeout
    "retry_attempts": 1,            // Limit retries
    "content_extraction_timeout": 15
  }
}
```

**4. Implement Polite Delays**
- Add delays between requests to the same domain
- Use rate_limit configuration to enforce request spacing
- Consider `User-Agent` headers that identify your organization

**5. Cache Aggressively**
- Enable content caching to avoid repeated requests for same content
- Use deduplication to prevent re-fetching known articles
- Store extracted content locally rather than re-scraping

**6. Monitor and Respond**
- Watch logs for HTTP 429 (Too Many Requests) or 403 (Forbidden) responses
- If you receive rate limit errors, **immediately reduce your request rate**
- Persistent errors may indicate you're not welcome—respect that

**7. Consider Legal Implications**
- Some jurisdictions have laws against unauthorized data access (e.g., CFAA in US)
- Scraping copyrighted content may have legal implications
- Consult legal counsel if using scraped data commercially
- Be aware of GDPR, CCPA, and other privacy regulations

### Configuration for Responsible Use

**Recommended Settings for Public Web Scraping:**

```env
# Conservative extraction settings
MAX_CONCURRENT_REQUESTS=2           # Limit parallel requests
RETRY_COUNT=1                       # Reduce retry attempts
EXTRA_FETCH_CONCURRENCY=2           # Limit content extraction concurrency
NETWORK_CHECK_TIMEOUT=15            # Generous timeout

# Content extraction
CONTENT_EXTRACTION_TIMEOUT=15       # Allow sites time to respond
```

**Per-Source Rate Limits in data_sources.json:**

```json
{
  "name": "custom_news_site",
  "config": {
    "max_items": 10,               // Limit items per fetch
    "request_delay_seconds": 2     // Delay between requests
  },
  "rate_limit": {
    "requests": 30,                // Conservative limit
    "per": "hour"                  // Spread requests over time
  }
}
```

### When to Avoid Web Scraping

**Do NOT scrape if:**
- robots.txt explicitly disallows your use case
- Terms of Service prohibit automated access
- Site provides an official API (use that instead)
- Content is behind authentication/paywall (likely unauthorized)
- Site displays anti-scraping measures (CAPTCHAs, rate limiting)
- You lack authorization for commercial use of the data

**Alternative Approaches:**
- Request API access from the site owner
- Use licensed data providers or aggregators
- Partner with the content owner for authorized access
- Focus on sources that explicitly allow automated access

### User Responsibility Statement

**The Rescribos platform provides web scraping as a technical capability. The responsibility for legal, ethical, and authorized use rests entirely with the user/organization deploying the platform.**

- Verify you have authorization to access and collect data from configured sources
- Ensure compliance with applicable laws and regulations in your jurisdiction
- Respect website terms of service, robots.txt directives, and rate limits
- Monitor for and respond to blocking or rate limiting signals
- Accept liability for any IP bans, legal issues, or other consequences of scraping activities

**The platform developers assume no liability for user-configured data sources or scraping activities. Users must exercise due diligence and good faith in configuring data collection.**

## See Also

- [Multi-Source Extraction Guide](../reference-guides/MULTI_SOURCE_EXTRACTION_GUIDE.md) - Advanced multi-source configuration
- [API Data Source Integration](../reference-guides/API_DATASOURCE_INTEGRATION_GUIDE.md) - Custom connector development
- [Data Pipeline Workflow](../data-pipeline/workflow.md) - Complete extraction → analysis flow
- [Configuration Guide](../deployment/configuration.md) - All configuration options
