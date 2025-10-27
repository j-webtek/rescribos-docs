# Multi-Source Extraction Guide

## Table of Contents

1. [Introduction](#introduction)
2. [Overview of Available Sources](#overview-of-available-sources)
3. [Source: arXiv Research Papers](#source-arxiv-research-papers)
4. [Source: Hacker News](#source-hacker-news)
5. [Source: SAM.gov Government Contracts](#source-samgov-government-contracts)
6. [Source: USASpending](#source-usaspending)
7. [Custom Web Sources](#custom-web-sources)
8. [Rate Limiting and API Keys](#rate-limiting-and-api-keys)
9. [Source Configuration](#source-configuration)
10. [Troubleshooting by Source](#troubleshooting-by-source)
11. [Best Practices](#best-practices)

---

## Introduction

Rescribos Data Refinement is designed as a **multi-source intelligence aggregation system**. Instead of relying on a single data source, it extracts content from multiple complementary sources to provide comprehensive AI/tech coverage.

### Why Multi-Source?

**Single-source limitations**:

- ❌ Incomplete coverage (miss stories from other platforms)
- ❌ Source bias (limited perspective)
- ❌ Dependency risk (if source goes down, you have nothing)

**Multi-source advantages**:

- ✅ **Comprehensive coverage**: Research papers + industry news + government activity
- ✅ **Diverse perspectives**: Academic, commercial, and public sector views
- ✅ **Cross-validation**: Stories appearing in multiple sources are likely important
- ✅ **Resilience**: If one source fails, others continue working

### Supported Sources

| Source          | Type       | Content                                      | Update Frequency                  | API Required            |
| --------------- | ---------- | -------------------------------------------- | --------------------------------- | ----------------------- |
| **arXiv**       | Research   | Academic papers (CS.AI, CS.LG, CS.CL, CS.CV) | Daily (~100-200 papers/day)       | No (public API)         |
| **Hacker News** | News       | Tech industry stories, discussions           | Continuous (~50-100 stories/day)  | No (public API)         |
| **SAM.gov**     | Government | Federal contract opportunities               | Daily (~20-50 relevant/day)       | Yes (free registration) |
| **USASpending** | Government | Federal spending and awards                  | Weekly (~10-30 AI contracts/week) | No (public API)         |
| **Custom Web**  | Various    | RSS feeds, APIs, web scraping                | Configurable                      | Varies                  |

---

## Overview of Available Sources

### Default Configuration

Out of the box, Rescribos extracts from **arXiv** and **Hacker News** (no API keys required).

```bash
# Default extraction includes arXiv + Hacker News
npx rescribos extract

# Output:
# ✓ arXiv: 127 papers
# ✓ Hacker News: 94 stories
# Total: 221 stories extracted
```

### Source Selection

Extract from specific sources only:

```bash
# arXiv only
npx rescribos extract --sources arxiv

# Hacker News only
npx rescribos extract --sources hackernews

# Multiple sources (comma-separated)
npx rescribos extract --sources arxiv,hackernews,sam

# All available sources
npx rescribos extract --sources all
```

### Source Categories

Rescribos organizes extracted stories into three categories:

#### 1. **arxiv_stories** (Research Papers)

- Source: arXiv.org
- Content: Scientific papers from AI/ML/NLP/CV categories
- Strength: Deep technical detail, cutting-edge research
- Use case: Understanding state-of-the-art techniques

#### 2. **other_stories** (News & Discussions)

- Source: Hacker News
- Content: Tech industry news, product launches, discussions
- Strength: Industry trends, practical applications
- Use case: Business intelligence, market awareness

#### 3. **document_stories** (Government Contracts)

- Source: SAM.gov, USASpending
- Content: Federal procurement opportunities and awards
- Strength: Public sector AI adoption, funding signals
- Use case: Business development, market research

---

## Source: arXiv Research Papers

### Overview

**arXiv** (https://arxiv.org) is a free distribution service for scholarly articles in physics, mathematics, computer science, and more. Rescribos focuses on CS (Computer Science) categories related to AI and machine learning.

### What Gets Extracted

Default arXiv categories:

- **cs.AI**: Artificial Intelligence
- **cs.LG**: Machine Learning (includes deep learning)
- **cs.CL**: Computation and Language (NLP)
- **cs.CV**: Computer Vision and Pattern Recognition

**Example papers** (typical daily extraction):

```
1. "Scaling Laws for Neural Language Models" (cs.LG, cs.CL)
2. "YOLO9000: Better, Faster, Stronger" (cs.CV)
3. "AlphaGo Zero: Learning from scratch" (cs.AI, cs.LG)
4. "BERT: Pre-training of Deep Bidirectional Transformers" (cs.CL)
```

### Configuration

#### Default Settings

```json
{
  "name": "arxiv",
  "enabled": true,
  "category": "arxiv_stories",
  "search_queries": ["cat:cs.AI", "cat:cs.LG", "cat:cs.CL", "cat:cs.CV"],
  "max_results": 50,
  "sort_by": "submittedDate",
  "sort_order": "descending"
}
```

#### Customization Options

**1. Change categories**:

Add robotics and human-computer interaction:

```json
{
  "search_queries": [
    "cat:cs.AI",
    "cat:cs.LG",
    "cat:cs.CL",
    "cat:cs.CV",
    "cat:cs.RO", // Robotics
    "cat:cs.HC" // Human-Computer Interaction
  ]
}
```

**2. Increase results per category**:

```json
{
  "max_results": 100 // Up from default 50
}
```

**3. Use keyword queries instead of categories**:

```json
{
  "search_queries": [
    "ti:\"neural networks\" OR ti:\"deep learning\"", // Title contains
    "abs:\"reinforcement learning\"", // Abstract contains
    "au:\"Geoffrey Hinton\"" // Author name
  ]
}
```

**4. Sort by relevance instead of date**:

```json
{
  "sort_by": "relevance",
  "sort_order": "descending"
}
```

### arXiv API Query Syntax

arXiv supports advanced search syntax:

| Prefix | Field      | Example                       |
| ------ | ---------- | ----------------------------- |
| `ti:`  | Title      | `ti:\"attention mechanisms\"` |
| `au:`  | Author     | `au:\"Yann LeCun\"`           |
| `abs:` | Abstract   | `abs:transformer`             |
| `cat:` | Category   | `cat:cs.LG`                   |
| `all:` | All fields | `all:\"language model\"`      |

**Boolean operators**: AND, OR, ANDNOT

**Examples**:

```
# Papers about transformers in NLP
"ti:transformer AND cat:cs.CL"

# Papers by specific authors
"au:\"Yoshua Bengio\" OR au:\"Geoffrey Hinton\""

# Recent GPT papers
"ti:GPT AND cat:cs.LG"
```

### Rate Limiting

**arXiv API limits**:

- **Requests**: No hard limit, but recommends **≥3 second delays** between requests
- **Bulk downloads**: Discouraged (use official bulk data service instead)

Rescribos automatically enforces 3-second delays between arXiv category queries.

### Extracted Fields

Each arXiv paper includes:

```json
{
  "id": "https://arxiv.org/abs/1706.03762",
  "arxiv_id": "1706.03762",
  "title": "Attention Is All You Need",
  "authors": ["Ashish Vaswani", "Noam Shazeer", "..."],
  "summary": "The dominant sequence transduction models...",
  "published": "2017-06-12T17:51:24Z",
  "updated": "2017-06-14T07:32:45Z",
  "categories": ["cs.CL", "cs.LG"],
  "primary_category": "cs.CL",
  "doi": "10.48550/arXiv.1706.03762",
  "url": "https://arxiv.org/abs/1706.03762",
  "pdf_url": "https://arxiv.org/pdf/1706.03762.pdf",
  "comment": "15 pages, 5 figures",
  "source": "arxiv",
  "category": "arxiv_stories"
}
```

### Best Practices

✅ **Use category queries for broad coverage**: `cat:cs.AI` captures all AI papers
✅ **Combine with keyword filters**: Post-process with AI relevance checker
✅ **Run daily**: arXiv updates continuously, daily runs capture new submissions
✅ **Respect rate limits**: Don't reduce the 3-second delay
✅ **Cache results**: Use incremental processing to avoid re-downloading

❌ **Don't**: Query too frequently (more than once per hour)
❌ **Don't**: Use overly broad queries without filtering (e.g., `cat:cs.*`)
❌ **Don't**: Download full PDFs in bulk (use arXiv's bulk data service)

### Troubleshooting

See [Troubleshooting by Source](#troubleshooting-by-source) → arXiv section.

---

## Source: Hacker News

### Overview

**Hacker News** (https://news.ycombinator.com) is a social news website focusing on computer science and entrepreneurship. Rescribos extracts top stories and filters for AI-related content.

### What Gets Extracted

Hacker News extraction focuses on **top stories** with AI/tech relevance:

**Example stories** (typical daily extraction):

```
1. "Show HN: I built a GPT-4 powered code review tool"
2. "Google announces new AI language model"
3. "YC-backed AI startup raises $50M Series A"
4. "Discussion: Future of AI safety and alignment"
```

### Configuration

#### Default Settings

```json
{
  "name": "hackernews",
  "enabled": true,
  "category": "other_stories",
  "max_items": 100,
  "story_types": ["top", "best", "new"],
  "min_score": 10,
  "max_age_hours": 24,
  "fetch_article_content": true
}
```

#### Customization Options

**1. Focus on specific story types**:

```json
{
  "story_types": ["top"] // Only top-ranked stories, not new/best
}
```

**2. Higher quality threshold**:

```json
{
  "min_score": 50 // Only stories with 50+ upvotes
}
```

**3. Faster updates (shorter time window)**:

```json
{
  "max_age_hours": 12 // Last 12 hours instead of 24
}
```

**4. Skip full article content extraction**:

```json
{
  "fetch_article_content": false // Faster, but less context
}
```

### HackerNews API

Rescribos uses the official **Firebase HackerNews API**:

- **Endpoint**: `https://hacker-news.firebaseio.com/v0/`
- **Rate limit**: None officially documented, but be respectful
- **Authentication**: Not required (public API)

**API endpoints used**:

- `/topstories.json`: Top 500 story IDs
- `/beststories.json`: Best stories
- `/newstories.json`: Newest stories
- `/item/{id}.json`: Story details

### AI Relevance Filtering

Not all HackerNews stories are AI-related. Rescribos uses a **relevance checker** to filter:

**AI keywords** (configurable):

```python
ai_keywords = [
    "ai", "artificial intelligence", "machine learning", "ml",
    "deep learning", "neural network", "nlp", "computer vision",
    "gpt", "bert", "transformer", "llm", "large language model",
    "chatgpt", "openai", "anthropic", "ai safety", "agi"
]
```

**Filtering process**:

1. Check title for AI keywords
2. Check HN discussion text (first comment)
3. Check linked article content (if fetched)
4. Score relevance (0-100%)
5. Keep if relevance > threshold (default: 20%)

### Content Extraction

When `fetch_article_content: true`:

1. Follow HN story URL
2. Extract article HTML
3. Convert to clean text (remove ads, nav, etc.)
4. Store as `content` field

**Example**:

```json
{
  "id": "38471234",
  "title": "Show HN: GPT-4 Code Assistant",
  "url": "https://example.com/gpt4-code-assistant",
  "score": 347,
  "by": "username",
  "time": 1697893200,
  "descendants": 89, // Number of comments
  "content": "Full article text extracted...",
  "hn_url": "https://news.ycombinator.com/item?id=38471234",
  "source": "hackernews",
  "category": "other_stories"
}
```

### Rate Limiting

**HackerNews API**:

- No official rate limits
- Rescribos defaults to **1-second delays** between requests
- Can be adjusted via `rate_limit` config

**Respectful usage**:

```json
{
  "rate_limit": {
    "requests": 60,
    "per": "minute" // Max 60 req/min = 1 per second
  }
}
```

### Best Practices

✅ **Enable content extraction for better analysis** (slower but higher quality)
✅ **Use min_score to filter noise** (recommend 10-20 minimum)
✅ **Run 2-4 times per day** for good coverage without duplication
✅ **Combine with arXiv** for comprehensive research + industry coverage

❌ **Don't**: Fetch every single HN story (use top/best only)
❌ **Don't**: Set max_age_hours too low (<6 hours) - causes excessive API calls
❌ **Don't**: Disable AI relevance filtering (you'll get cooking recipes)

### Troubleshooting

See [Troubleshooting by Source](#troubleshooting-by-source) → Hacker News section.

---

## Source: SAM.gov Government Contracts

### Overview

**SAM.gov** (System for Award Management) is the U.S. government's official system for federal procurement and awards. Rescribos extracts AI-related contract opportunities (RFPs, RFQs, solicitations).

### What Gets Extracted

**Contract opportunities** with AI/ML relevance:

**Example solicitations**:

```
1. "Department of Defense - AI/ML Platform Development" ($5M-$15M)
2. "VA Healthcare - Predictive Analytics System" ($2M-$8M)
3. "DHS - Computer Vision for Border Security" ($10M-$25M)
4. "NASA - Machine Learning for Satellite Data Analysis" ($3M-$7M)
```

### Configuration

#### Default Settings

```json
{
  "name": "sam",
  "enabled": false, // Disabled by default (requires API key)
  "category": "document_stories",
  "api_key_env": "SAM_API_KEY",
  "max_items": 100,
  "days_back": 30,
  "notice_types": [], // Empty = all types
  "naics_codes": [],
  "ai_keywords": [
    "artificial intelligence",
    "machine learning",
    "deep learning",
    "neural network",
    "computer vision",
    "natural language",
    "ai",
    "ml",
    "data science",
    "predictive analytics"
  ]
}
```

#### API Key Setup

SAM.gov requires a **free API key**:

1. **Register** at https://sam.gov/
2. **Request API access** at https://open.gsa.gov/api/get-opportunities-public-api/
3. **Get your API key** (delivered via email)
4. **Add to .env file**:

```bash
# In .env
SAM_API_KEY=your-api-key-here
```

5. **Enable in config**:

```json
{
  "name": "sam",
  "enabled": true // Change from false to true
}
```

### Important: Rate Limits

**SAM.gov API rate limits** (as of 2024):

| User Type            | Requests Per Day    |
| -------------------- | ------------------- |
| Non-Federal          | **10 requests/day** |
| Federal (.gov email) | 1,000 requests/day  |

**⚠️ Critical**: Rescribos will **warn you** when approaching the limit and **stop** when hitting 10 requests.

**Best practices**:

```json
{
  "max_items": 100, // Don't go higher (would need multiple pages)
  "limit_per_page": 100, // Max allowed by SAM.gov
  "days_back": 30 // Longer window = fewer daily runs needed
}
```

**Recommended extraction frequency**:

- **Once per day** maximum for non-federal users
- **Best time**: Early morning (6-8 AM) to catch overnight postings

### Notice Types

SAM.gov has various notice types. Common ones for AI contracts:

```json
{
  "notice_types": [
    "o", // Solicitation
    "p", // Pre-solicitation
    "r", // Sources Sought
    "s", // Special Notice
    "i" // Intent to Bundle
  ]
}
```

**Leave empty** to get all types (recommended).

### NAICS Codes

Filter by industry codes (optional):

**AI-relevant NAICS codes**:

```json
{
  "naics_codes": [
    "541511", // Custom Computer Programming Services
    "541512", // Computer Systems Design Services
    "541513", // Computer Facilities Management Services
    "541519", // Other Computer Related Services
    "541715", // Research and Development (Physical, Engineering, Life Sciences)
    "518210", // Data Processing, Hosting Services
    "541690" // Other Scientific and Technical Consulting
  ]
}
```

**Leave empty** to search all NAICS codes (recommended for broader coverage).

### AI Keyword Filtering

SAM.gov returns **all** contract opportunities. Rescribos filters for AI relevance using keyword matching in:

1. **Title**: Contract opportunity title
2. **Description**: Full solicitation description
3. **NAICS description**: Industry category description
4. **Set-aside**: Small business, 8(a), etc. (indirect signal)

**Customize AI keywords**:

```json
{
  "ai_keywords": [
    "artificial intelligence",
    "machine learning",
    "deep learning",
    "computer vision",
    "nlp",
    "natural language processing",
    "neural network",
    "ai",
    "ml",
    "data analytics",
    "predictive modeling",
    "automation",
    "intelligent systems"
  ]
}
```

### Extracted Fields

Each SAM.gov opportunity includes rich metadata:

```json
{
  "id": "abc123def456",
  "notice_id": "DEPT-SOL-2024-001",
  "title": "AI/ML Platform Development and Integration",
  "sol_number": "N00024-24-R-1234",
  "department": "Department of Defense",
  "sub_tier": "Navy",
  "office": "Naval Information Warfare Center",
  "posted_date": "2024-10-15",
  "response_deadline": "2024-11-30",
  "archive_date": "2025-01-15",
  "notice_type": "Solicitation",
  "naics_code": "541512",
  "naics_description": "Computer Systems Design Services",
  "set_aside": "Total Small Business",
  "description": "Full solicitation description...",
  "url": "https://sam.gov/opp/abc123def456",
  "attachments": [
    { "name": "SOW.pdf", "url": "..." },
    { "name": "Requirements.docx", "url": "..." }
  ],
  "place_of_performance": {
    "city": "San Diego",
    "state": "CA",
    "zip": "92101"
  },
  "source": "sam",
  "category": "document_stories"
}
```

### Best Practices

✅ **Run once per day** (non-federal API limit)
✅ **Use broad AI keywords** for maximum coverage
✅ **Set days_back to 30-60** to reduce need for daily runs
✅ **Monitor API request count** (Rescribos logs each request)
✅ **Upgrade to federal API key** if you need higher limits

❌ **Don't**: Run multiple times per day (you'll hit the 10-request limit)
❌ **Don't**: Use overly narrow NAICS filters (you'll miss opportunities)
❌ **Don't**: Ignore rate limit warnings (you'll be blocked for 24 hours)

### Troubleshooting

See [Troubleshooting by Source](#troubleshooting-by-source) → SAM.gov section.

---

## Source: USASpending

### Overview

**USASpending.gov** provides data on federal spending, including contract awards. While SAM.gov shows **pre-award opportunities**, USASpending shows **post-award contracts** that have already been granted.

### What Gets Extracted

**Awarded contracts** related to AI:

**Example awards**:

```
1. "DOD AI Autonomy Research Contract to MIT" ($12.5M, awarded Sep 2024)
2. "VA Predictive Analytics Platform Award" ($8.2M, awarded Oct 2024)
3. "NASA ML Satellite Data Contract to SpaceX" ($15M, awarded Aug 2024)
```

### Configuration

```json
{
  "name": "usaspending",
  "enabled": true, // No API key required
  "category": "document_stories",
  "max_items": 50,
  "months_back": 3,
  "min_award_amount": 1000000, // $1M minimum
  "naics_codes": [
    "541511",
    "541512",
    "541715" // AI-relevant codes
  ],
  "ai_keywords": ["artificial intelligence", "machine learning", "ai", "ml"]
}
```

### API Details

- **Endpoint**: `https://api.usaspending.gov/api/v2/search/spending_by_award/`
- **Rate limit**: None officially documented
- **Authentication**: Not required

### Extracted Fields

```json
{
  "award_id": "CONT_AWD_N00024_9700_SPM30019D0060_9700",
  "award_number": "N00024-19-D-0060",
  "title": "AI/ML Research and Development",
  "description": "Development of machine learning models...",
  "awarding_agency": "Department of Defense",
  "awarding_sub_agency": "Navy",
  "recipient": "Massachusetts Institute of Technology",
  "recipient_uei": "E2NYLCDML6V1",
  "award_amount": 12500000, // $12.5M
  "award_date": "2024-09-15",
  "period_of_performance_start": "2024-10-01",
  "period_of_performance_end": "2027-09-30",
  "naics_code": "541715",
  "naics_description": "Research and Development",
  "place_of_performance": {
    "city": "Cambridge",
    "state": "MA"
  },
  "source": "usaspending",
  "category": "document_stories"
}
```

### Best Practices

✅ **Complement SAM.gov** (pre-award + post-award = full picture)
✅ **Track competitors** (see who's winning AI contracts)
✅ **Run weekly** (awards don't change as frequently as opportunities)
✅ **Set min_award_amount** to filter noise (small purchases)

---

## Custom Web Sources

### Overview

Beyond the built-in sources, you can add **custom web sources** using:

- RSS/Atom feeds
- REST APIs
- Web scraping

### Adding a Custom RSS Feed

Example: Add AI-focused blog RSS feed

**1. Create source plugin** (`scripts/data_sources/custom_rss_source.py`):

```python
from .base_source import DataSource
import feedparser

class CustomRSSSource(DataSource):
    def __init__(self, config):
        super().__init__(config)
        self.feed_url = config.get('feed_url')

    async def extract(self, **kwargs):
        feed = feedparser.parse(self.feed_url)
        return feed.entries

    def transform(self, raw_data):
        stories = []
        for entry in raw_data:
            stories.append({
                'id': entry.get('id', entry.link),
                'title': entry.title,
                'url': entry.link,
                'summary': entry.get('summary', ''),
                'published': entry.get('published', ''),
                'source': self.name,
                'category': self.category
            })
        return stories
```

**2. Add to config** (`config/data_sources.json`):

```json
{
  "sources": [
    {
      "name": "openai_blog",
      "plugin": "custom_rss_source.CustomRSSSource",
      "enabled": true,
      "category": "other_stories",
      "feed_url": "https://openai.com/blog/rss.xml",
      "max_items": 20
    }
  ]
}
```

**3. Register and use**:

```bash
npx rescribos extract --config config/data_sources.json
```

### Custom API Source

Similar pattern for REST APIs - implement `extract()` and `transform()` methods.

See `scripts/data_sources/base_source.py` for the full interface.

---

## Rate Limiting and API Keys

### Summary Table

| Source      | API Key Required | Rate Limit                   | Recommended Frequency |
| ----------- | ---------------- | ---------------------------- | --------------------- |
| arXiv       | No               | 3 sec between requests       | Daily                 |
| Hacker News | No               | ~1 req/sec (unofficial)      | 2-4 times/day         |
| SAM.gov     | Yes (free)       | **10 req/day** (non-federal) | Once/day              |
| USASpending | No               | None documented              | Weekly                |

### Setting Up API Keys

All API keys are stored in the `.env` file:

```bash
# SAM.gov API Key
SAM_API_KEY=your-sam-api-key-here

# Future sources (examples)
NEWS_API_KEY=your-news-api-key
TWITTER_BEARER_TOKEN=your-twitter-token
```

### Monitoring Rate Limits

Rescribos logs all API requests:

```
[09:00:15] Making SAM.gov API request #1 (Daily limit: 10 requests)
[09:00:18] Making SAM.gov API request #2 (Daily limit: 10 requests)
...
[09:01:05] Making SAM.gov API request #10 (Daily limit: 10 requests)
[09:01:08] ⚠️ Approaching SAM.gov daily limit (10 requests used)
```

If you hit the limit:

```
[09:01:10] ❌ SAM.gov daily API limit exceeded (retry_after: 86400s)
[09:01:10] Try again tomorrow. Non-federal users limited to 10 requests/day.
```

### Rate Limit Configuration

Customize per source:

```json
{
  "name": "hackernews",
  "rate_limit": {
    "requests": 30,
    "per": "minute" // 30 requests per minute
  }
}
```

---

## Source Configuration

### Global Configuration File

Create `config/data_sources.json`:

```json
{
  "sources": [
    {
      "name": "arxiv",
      "plugin": "data_sources.arxiv_source.ArxivSource",
      "enabled": true,
      "category": "arxiv_stories",
      "search_queries": ["cat:cs.AI", "cat:cs.LG", "cat:cs.CL", "cat:cs.CV"],
      "max_results": 50,
      "sort_by": "submittedDate",
      "sort_order": "descending"
    },
    {
      "name": "hackernews",
      "plugin": "data_sources.hackernews_source.HackerNewsSource",
      "enabled": true,
      "category": "other_stories",
      "max_items": 100,
      "story_types": ["top"],
      "min_score": 10,
      "max_age_hours": 24,
      "fetch_article_content": true
    },
    {
      "name": "sam",
      "plugin": "data_sources.sam_source.SamSource",
      "enabled": true,
      "category": "document_stories",
      "api_key_env": "SAM_API_KEY",
      "max_items": 100,
      "days_back": 30,
      "ai_keywords": ["ai", "machine learning", "artificial intelligence"]
    }
  ],
  "global_settings": {
    "ai_relevance_threshold": 0.2,
    "dedup_threshold": 0.85,
    "max_concurrent_requests": 10
  }
}
```

### Using Custom Config

```bash
# Extract with custom config
npx rescribos extract --config config/data_sources.json

# Incremental with custom config
npx rescribos extract-incremental --config config/data_sources.json
```

### Environment-Based Configuration

Override config with environment variables:

```bash
# In .env
ARXIV_MAX_RESULTS=100
HACKERNEWS_MIN_SCORE=50
SAM_DAYS_BACK=60
```

---

## Troubleshooting by Source

### arXiv Issues

#### Problem: No papers extracted

**Causes**:

1. Categories too narrow
2. Network issues
3. arXiv API down

**Solutions**:

```bash
# Test arXiv connectivity
curl "http://export.arxiv.org/api/query?search_query=cat:cs.AI&max_results=1"

# Broaden categories
# In config: ["cat:cs.AI", "cat:cs.LG", "cat:cs.CL", "cat:cs.CV", "cat:cs.*"]

# Check logs
grep "arXiv" logs/extraction.log
```

#### Problem: Duplicate papers

**Cause**: Overlapping category queries (e.g., paper in both cs.AI and cs.LG)

**Solution**: Rescribos automatically deduplicates by arXiv ID. No action needed.

#### Problem: Missing recent papers

**Cause**: arXiv updates continuously, but there may be a processing delay

**Solution**: Run extraction 2-4 hours after target time (e.g., 8 AM for papers posted since midnight)

### Hacker News Issues

#### Problem: Too many irrelevant stories

**Cause**: AI relevance threshold too low

**Solutions**:

```json
{
  "ai_relevance_threshold": 0.5 // Up from default 0.2
}
```

Or increase min_score:

```json
{
  "min_score": 50 // Only highly upvoted stories
}
```

#### Problem: Content extraction failing

**Cause**: Paywalls, JavaScript-heavy sites

**Solution**: Disable content extraction or use better extraction library

```json
{
  "fetch_article_content": false // Faster, but less context
}
```

#### Problem: Rate limit errors

**Cause**: Too many concurrent requests

**Solution**: Reduce concurrency or increase delays

```json
{
  "rate_limit": {
    "requests": 30,
    "per": "minute" // Slower
  }
}
```

### SAM.gov Issues

#### Problem: "Daily API limit exceeded"

**Cause**: Non-federal users limited to 10 requests/day

**Solutions**:

1. **Wait 24 hours** (limit resets daily)
2. **Upgrade to federal API key** (requires .gov email)
3. **Reduce extraction frequency** (once per day maximum)
4. **Increase days_back** to capture more per run:

```json
{
  "days_back": 60 // Up from 30
}
```

#### Problem: No opportunities found

**Causes**:

1. AI keywords too narrow
2. Date range too short
3. No relevant opportunities posted

**Solutions**:

```json
{
  "ai_keywords": [...],  // Expand keyword list
  "days_back": 90,       // Longer window
  "naics_codes": []      // Remove NAICS filter
}
```

#### Problem: API key not working

**Cause**: Invalid or expired API key

**Solutions**:

1. Verify API key in .env:
   ```bash
   grep SAM_API_KEY .env
   ```
2. Test API key directly:
   ```bash
   curl "https://api.sam.gov/opportunities/v2/search?api_key=YOUR_KEY&limit=1"
   ```
3. Request new API key at https://open.gsa.gov/api/get-opportunities-public-api/

### USASpending Issues

#### Problem: Old awards, no recent ones

**Cause**: Awards take time to appear in USASpending (processing delay)

**Solution**: Expect 1-2 month lag. Use SAM.gov for current opportunities.

#### Problem: Too many results

**Cause**: min_award_amount too low

**Solution**:

```json
{
  "min_award_amount": 5000000 // $5M minimum (up from $1M)
}
```

---

## Best Practices

### 1. Use Complementary Sources

**Recommended combination**:

- **arXiv**: Research trends (daily)
- **Hacker News**: Industry news (2-4x/day)
- **SAM.gov**: Government opportunities (1x/day)

This gives you research + industry + public sector coverage.

### 2. Optimize Extraction Frequency

| Source      | Recommended Frequency   | Reason                      |
| ----------- | ----------------------- | --------------------------- |
| arXiv       | Once per day (6-8 AM)   | Papers posted overnight     |
| Hacker News | 2-4 times per day       | Stories update continuously |
| SAM.gov     | Once per day (early AM) | API limit (10 req/day)      |
| USASpending | Once per week           | Awards don't change daily   |

### 3. Use Incremental Processing

Always use `extract-incremental` for daily runs:

```bash
# Good: Only extracts new stories
npx rescribos extract-incremental

# Wasteful: Re-extracts everything
npx rescribos extract
```

See [Incremental Processing Guide](INCREMENTAL_PROCESSING_GUIDE.md).

### 4. Monitor API Costs and Limits

Track usage:

```bash
# Check SAM.gov request count
grep "SAM.gov API request" logs/extraction.log | wc -l

# Should be ≤10 per day for non-federal users
```

### 5. Filter Aggressively

Better to filter early than store irrelevant data:

```json
{
  "ai_relevance_threshold": 0.3, // Moderate filtering
  "min_score": 20, // HN quality threshold
  "min_award_amount": 1000000 // Serious contracts only
}
```

### 6. Customize for Your Use Case

**Use case**: AI safety research

```json
{
  "arxiv": {
    "search_queries": [
      "ti:\"ai safety\" OR ti:\"alignment\"",
      "abs:\"interpretability\" OR abs:\"explainable\""
    ]
  },
  "hackernews": {
    "ai_keywords": ["ai safety", "alignment", "interpretability", "xai"]
  }
}
```

**Use case**: Business development (government contracts)

```json
{
  "sources": ["sam", "usaspending"], // Only government sources
  "sam": {
    "days_back": 90,
    "min_award_amount": 500000
  }
}
```

**Use case**: Academic research monitoring

```json
{
  "sources": ["arxiv"], // Research only
  "arxiv": {
    "max_results": 200, // More coverage
    "search_queries": ["cat:cs.AI", "cat:cs.LG", "cat:cs.CL", "cat:cs.CV", "cat:cs.RO", "cat:cs.HC"]
  }
}
```

### 7. Keep Logs Clean

Regularly review and clean logs:

```bash
# Archive old logs
mv logs/extraction.log logs/archive/extraction-2024-10-21.log

# Monitor errors
grep "ERROR" logs/extraction.log

# Check rate limits
grep "limit" logs/extraction.log
```

---

## Related Documentation

- **[Incremental Processing Guide](INCREMENTAL_PROCESSING_GUIDE.md)**: Optimize for daily multi-source runs
- **[CLI Reference](cli.md)**: Full command-line documentation
- **[Troubleshooting FAQ](TROUBLESHOOTING_FAQ.md)**: General troubleshooting
- **[Cost Tracking Guide](COST_TRACKING_GUIDE.md)**: Monitor API usage costs

---

## Summary

Multi-source extraction is the foundation of comprehensive AI intelligence gathering. Key takeaways:

✅ **Use multiple complementary sources** (arXiv + HN + SAM.gov)
✅ **Respect rate limits** (especially SAM.gov: 10 req/day)
✅ **Run incremental updates** (not full extractions every time)
✅ **Filter aggressively early** (AI relevance, scores, amounts)
✅ **Customize for your use case** (research vs business vs government focus)
✅ **Monitor API usage** (track requests, check logs)
✅ **Test individually first** (verify each source works before combining)

Master multi-source extraction to build a powerful AI intelligence pipeline! 🚀
