# Rescribos API Data Source Integration Guide

## 🚀 Quick Start

**New to data source integration?** Start with the [Quick Start Guide](QUICKSTART_DATASOURCE_INTEGRATION.md) to use our automation tools and get started in under 5 minutes!

This detailed guide provides comprehensive technical documentation for integrating new API data sources into Rescribos.

---

## Table of Contents

1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Prerequisites & Requirements](#prerequisites--requirements)
4. [Core Concepts](#core-concepts)
5. [Data Source Implementation](#data-source-implementation)
6. [Schema & Data Mapping](#schema--data-mapping)
7. [Configuration](#configuration)
8. [Testing & Validation](#testing--validation)
9. [Advanced Features](#advanced-features)
10. [Troubleshooting](#troubleshooting)
11. [Examples](#examples)
12. [Automation Tools](#automation-tools)

---

## Overview

The Rescribos system is designed with a modular, plugin-based architecture that allows you to integrate new API data sources without modifying core system code. This guide explains everything you need to know to successfully integrate your API as a data source.

### What This Guide Covers

- **Architecture**: Understanding how the multi-source extraction system works
- **Requirements**: What your API needs to provide
- **Implementation**: Step-by-step guide to creating a data source plugin
- **Schema Mapping**: Converting your API's data format to Rescribos format
- **Configuration**: Setting up authentication, rate limiting, and categorization
- **Best Practices**: Recommendations for robust, production-ready integrations

### Who Should Read This

- Developers integrating new external APIs into Rescribos
- Data engineers working with alternative data sources
- Anyone needing to understand the data ingestion pipeline

---

## System Architecture

### High-Level Data Flow

```
┌─────────────────────┐
│  External API       │
│  (Your Data Source) │
└──────────┬──────────┘
           │
           ↓
┌─────────────────────┐
│  DataSource Plugin  │ ← You implement this
│  - extract()        │
│  - transform()      │
│  - validate()       │
└──────────┬──────────┘
           │
           ↓
┌──────────────────────┐
│ MultiSourceExtractor │ ← System orchestration
│  - Deduplication     │
│  - Categorization    │
│  - Content enhance   │
└──────────┬───────────┘
           │
           ↓
┌──────────────────────┐
│  Analysis Pipeline   │
│  - AI summaries      │
│  - Embeddings        │
│  - Reports           │
└──────────────────────┘
```

### Key Components

1. **DataSource (Base Class)**: Abstract base class that all plugins extend - located in `scripts/data_sources/base_source.py`

2. **MultiSourceExtractor**: Orchestrates extraction from multiple sources - located in `scripts/multi_source_extractor.py`

3. **Configuration File**: JSON file defining all data sources and their settings - located in `config/data_sources.json`

4. **Content Extractor**: Extracts full content from URLs when needed

5. **AI Relevance Checker**: Optional GPT-4 screening for AI-related content

6. **Embeddings Database**: Deduplication and similarity matching

---

## Prerequisites & Requirements

### What Your API Must Provide

At minimum, your API must be able to provide:

1. **Article/Content Listings**: A way to fetch a list of articles, papers, or content items
2. **Unique Identifiers**: Each item must have a unique, stable ID
3. **Metadata**: At least a title and URL for each item
4. **Timestamps**: When the content was published or last updated

### Recommended (But Optional) Features

- **Pagination Support**: For handling large result sets
- **Filtering Options**: To narrow down results (dates, topics, etc.)
- **Full Text/Summaries**: Content text or abstracts
- **Category/Tag Information**: For better classification

### Technical Requirements

- **Python 3.8+**: Your plugin will be written in Python
- **Async Support**: The system uses `asyncio` for concurrent operations
- **JSON/XML Parsing**: Most APIs return data in these formats
- **HTTP Client Library**: System uses `aiohttp` for async HTTP requests

### Authentication Requirements

The system supports:

- **No Authentication**: Public APIs
- **API Keys**: Via environment variables
- **Bearer Tokens**: Via environment variables
- **OAuth**: Custom implementation in your plugin

---

## Core Concepts

### The DataSource Abstract Class

Every data source plugin must extend the `DataSource` base class and implement three core methods:

```python
from scripts.data_sources.base_source import DataSource

class YourSource(DataSource):
    async def extract(self, **kwargs) -> List[Dict[str, Any]]:
        """Fetch raw data from your API"""
        pass

    def transform(self, raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Convert raw data to standard schema"""
        pass

    def validate(self, story: Dict[str, Any]) -> bool:
        """Verify the story meets requirements"""
        pass
```

**Important**: You don't need to implement `process()` - the base class handles calling these three methods in the correct order with rate limiting and error handling.

### The Three-Phase Pipeline

The system automatically orchestrates your plugin through three phases via the base class `process()` method:

1. **EXTRACT**: Your plugin fetches raw data from the external API
2. **TRANSFORM**: Convert the raw data to Rescribos' standard schema
3. **VALIDATE**: Ensure each story has required fields and valid data

The base class `process()` method:

- Checks if the source is enabled
- Enforces rate limiting automatically
- Calls your `extract()` method
- Calls your `transform()` method
- Filters results through your `validate()` method
- Logs progress and errors

**You only need to focus on the three core methods** - the orchestration is handled for you.

### Base Class Helper Methods

The `DataSource` base class provides several helper methods you can use in your implementation:

```python
# Authentication
self._get_auth_headers() -> Dict[str, str]  # Get auth headers based on config
self.get_user_agent() -> str                # Get configured user agent string

# Rate limiting (handled automatically by process())
await self._enforce_rate_limit()            # Check and enforce rate limits

# Configuration access
self.name                                    # Source name from config
self.category                                # Category from config
self.enabled                                 # Whether source is enabled
self.config                                  # Full configuration dictionary
self.rate_limit                              # RateLimit object
self.auth                                    # Auth object
```

**Example using helpers:**

```python
async def extract(self, **kwargs) -> List[Dict[str, Any]]:
    headers = {
        'User-Agent': self.get_user_agent(),
        **self._get_auth_headers()
    }

    async with create_session_context(headers=headers) as session:
        # Make API requests...
        pass
```

### Standard Story Schema

The system expects all stories to conform to this schema:

```python
{
    "id": int or str,              # REQUIRED: Unique identifier
    "title": str,                  # REQUIRED: Article title
    "url": str,                    # REQUIRED: Link to original content
    "time": int,                   # REQUIRED: Unix timestamp
    "content": str,                # RECOMMENDED: Full text or summary
    "source": str,                 # REQUIRED: Source name (e.g., "hackernews")
    "category": str,               # REQUIRED: "arxiv_stories", "other_stories", or "document_stories"

    # Optional but recommended fields
    "summary": str,                # Short summary
    "authors": List[str],          # Author names
    "tags": List[str],             # Relevant tags/keywords
    "metadata": Dict[str, Any]     # Any additional data
}
```

### Category System

Rescribos uses **exactly three categories** for downstream processing:

1. **`arxiv_stories`**: Academic research papers (primarily from arXiv)
2. **`other_stories`**: News, blog posts, HackerNews items, social media
3. **`document_stories`**: Local documents processed separately

**Important**: Your data source will typically use `other_stories` unless it's specifically an academic paper repository.

---

## Data Source Implementation

### Step 1: Create Your Plugin File

Create a new Python file in `scripts/data_sources/` named `{yoursource}_source.py`:

```
scripts/
└── data_sources/
    ├── __init__.py
    ├── base_source.py
    ├── hackernews_source.py
    ├── arxiv_source.py
    └── yoursource_source.py  ← Create this
```

### Step 2: Import Required Dependencies

```python
"""
YourSource data source plugin for extracting content from YourAPI.

This plugin demonstrates how to implement the YourAPI extraction
logic using the Rescribos plugin architecture.
"""

import asyncio
import aiohttp
import logging
import time
from typing import List, Dict, Any, Optional
from datetime import datetime

# Import base class
try:
    from .base_source import DataSource
except ImportError:
    from base_source import DataSource

# Import connection utilities for network handling
try:
    from ..connection_utils import create_session_context
except ImportError:
    # Fallback for different import contexts
    def create_session_context(*args, **kwargs):
        return aiohttp.ClientSession(*args, **kwargs)

logger = logging.getLogger(__name__)
```

### Step 3: Implement Your DataSource Class

```python
class YourSource(DataSource):
    """
    YourSource data source for extracting content from YourAPI.

    Configuration options:
    - api_endpoint: Base URL for the API
    - max_results: Maximum number of items to fetch
    - search_query: Query string for filtering results
    """

    def __init__(self, config: Dict[str, Any]):
        """Initialize with configuration."""
        super().__init__(config)

        # Extract plugin-specific configuration
        self.api_endpoint = config.get('api_endpoint', 'https://api.yourservice.com')
        self.max_results = config.get('max_results', 100)
        self.search_query = config.get('search_query', '')

        logger.info(f"Initialized YourSource with endpoint: {self.api_endpoint}")

    async def extract(self, **kwargs) -> List[Dict[str, Any]]:
        """
        Extract raw data from YourAPI.

        Args:
            **kwargs: Optional parameters to override defaults

        Returns:
            List of raw data dictionaries from the API
        """
        # Allow runtime overrides
        max_results = kwargs.get('max_results', self.max_results)

        # Set up headers
        headers = {
            'User-Agent': self.get_user_agent(),
            **self._get_auth_headers()  # Add authentication if configured
        }

        all_items = []

        # Create HTTP session with timeout
        timeout = aiohttp.ClientTimeout(total=30, connect=10)
        async with create_session_context(headers=headers, timeout=timeout) as session:
            try:
                # Build API request URL
                params = {
                    'limit': max_results,
                    'query': self.search_query
                }

                url = f"{self.api_endpoint}/search"

                # Make API request
                async with session.get(url, params=params) as response:
                    response.raise_for_status()
                    data = await response.json()

                    # Extract items from response
                    # Adapt this to your API's response format
                    items = data.get('items', [])
                    all_items.extend(items)

                    logger.info(f"Fetched {len(items)} items from YourSource")

            except aiohttp.ClientError as e:
                logger.error(f"HTTP error fetching from YourSource: {e}")
                return []
            except Exception as e:
                logger.error(f"Unexpected error in YourSource extraction: {e}")
                return []

        logger.info(f"Total items extracted from YourSource: {len(all_items)}")
        return all_items

    def transform(self, raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Transform raw API data to Rescribos standard schema.

        Args:
            raw_data: List of raw item dictionaries from extract()

        Returns:
            List of stories in standard format
        """
        stories = []

        for item in raw_data:
            try:
                # Map your API's fields to Rescribos schema
                story = {
                    # REQUIRED FIELDS
                    'id': item.get('id'),  # Your API's unique ID
                    'title': item.get('title', '').strip(),
                    'url': item.get('link', item.get('url', '')),
                    'time': self._parse_timestamp(item.get('published_at')),

                    # STANDARD FIELDS
                    'source': self.name,  # Set by base class
                    'category': self.category,  # Set by base class

                    # RECOMMENDED FIELDS
                    'content': item.get('content', item.get('description', '')),
                    'summary': item.get('summary', ''),
                    'authors': item.get('authors', []),
                    'tags': self._extract_tags(item),

                    # METADATA
                    'metadata': {
                        'original_id': item.get('id'),
                        'api_source': 'yoursource',
                        'fetched_at': datetime.now().isoformat()
                    }
                }

                stories.append(story)

            except Exception as e:
                logger.warning(f"Failed to transform item {item.get('id', 'unknown')}: {e}")
                continue

        logger.info(f"Transformed {len(stories)} stories from YourSource")
        return stories

    def _parse_timestamp(self, date_string: str) -> int:
        """Convert date string to Unix timestamp."""
        try:
            # Adapt this to your API's date format
            import dateutil.parser
            dt = dateutil.parser.parse(date_string)
            return int(dt.timestamp())
        except:
            # Fallback to current time if parsing fails
            return int(time.time())

    def _extract_tags(self, item: Dict[str, Any]) -> List[str]:
        """Extract relevant tags from item."""
        tags = []

        # Adapt this to your API's tag/category structure
        if 'tags' in item:
            tags.extend(item['tags'])

        if 'categories' in item:
            tags.extend(item['categories'])

        return list(set(tags))  # Remove duplicates
```

### Step 4: Handle Edge Cases

```python
    def validate(self, story: Dict[str, Any]) -> bool:
        """
        Extended validation for YourSource stories.

        Args:
            story: Transformed story dictionary

        Returns:
            True if valid, False otherwise
        """
        # First run base validation (checks required fields)
        if not super().validate(story):
            return False

        # Add your custom validation rules
        # Example: Check title is not too short
        if len(story.get('title', '')) < 10:
            logger.warning(f"Story title too short: {story.get('id')}")
            return False

        # Example: Verify URL domain
        if 'yourservice.com' not in story.get('url', ''):
            logger.warning(f"Invalid URL domain: {story.get('id')}")
            return False

        return True
```

---

## Schema & Data Mapping

### Understanding Field Mapping

Your API's response structure needs to be mapped to Rescribos' standard schema. Here's a comprehensive mapping reference:

| Rescribos Field | Type      | Required    | Description       | Common API Equivalents                            |
| --------------- | --------- | ----------- | ----------------- | ------------------------------------------------- |
| `id`            | int/str   | Yes         | Unique identifier | `id`, `uid`, `article_id`, `doc_id`               |
| `title`         | str       | Yes         | Article title     | `title`, `headline`, `name`                       |
| `url`           | str       | Yes         | Link to content   | `url`, `link`, `permalink`, `canonical_url`       |
| `time`          | int       | Yes         | Unix timestamp    | `published_at`, `created_at`, `timestamp`, `date` |
| `content`       | str       | Recommended | Full text         | `body`, `content`, `text`, `description`          |
| `source`        | str       | Auto-set    | Source name       | Set automatically by system                       |
| `category`      | str       | Auto-set    | Story category    | Set automatically based on config                 |
| `summary`       | str       | Optional    | Short summary     | `summary`, `abstract`, `excerpt`                  |
| `authors`       | List[str] | Optional    | Author names      | `authors`, `author`, `byline`, `creator`          |
| `tags`          | List[str] | Optional    | Keywords/tags     | `tags`, `categories`, `keywords`                  |

### Timestamp Conversion Examples

```python
def _parse_timestamp(self, date_value: Any) -> int:
    """
    Convert various date formats to Unix timestamp.
    Handles multiple common API date formats.
    """
    import dateutil.parser

    # Already a timestamp
    if isinstance(date_value, (int, float)):
        return int(date_value)

    # ISO 8601 format: "2024-01-15T10:30:00Z"
    if isinstance(date_value, str):
        try:
            dt = dateutil.parser.parse(date_value)
            return int(dt.timestamp())
        except:
            pass

    # RFC 2822 format: "Mon, 15 Jan 2024 10:30:00 GMT"
    if isinstance(date_value, str) and ',' in date_value:
        try:
            from email.utils import parsedate_to_datetime
            dt = parsedate_to_datetime(date_value)
            return int(dt.timestamp())
        except:
            pass

    # Fallback: current time
    logger.warning(f"Could not parse date '{date_value}', using current time")
    return int(time.time())
```

### Content Extraction Strategies

Different APIs provide content in different ways. Here are common patterns:

```python
def _get_content(self, item: Dict[str, Any]) -> str:
    """
    Extract content from API response with multiple fallback strategies.
    """
    content_parts = []

    # Strategy 1: Direct content field
    if 'content' in item and item['content']:
        return item['content'].strip()

    # Strategy 2: Combine multiple fields
    if 'summary' in item:
        content_parts.append(f"Summary: {item['summary']}")

    if 'description' in item:
        content_parts.append(item['description'])

    # Strategy 3: Extract from nested structures
    if 'body' in item and isinstance(item['body'], dict):
        if 'text' in item['body']:
            content_parts.append(item['body']['text'])

    # Strategy 4: HTML content extraction
    if 'html_content' in item:
        content_parts.append(self._strip_html(item['html_content']))

    # Combine all parts
    combined = '\n\n'.join(filter(None, content_parts))

    # If still no content, the system's content extractor
    # will fetch it from the URL later
    return combined.strip()

def _strip_html(self, html: str) -> str:
    """Remove HTML tags from content."""
    import re
    # Simple HTML tag removal
    text = re.sub(r'<[^>]+>', '', html)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    return text.strip()
```

---

## Configuration

### Adding Your Source to data_sources.json

Edit `config/data_sources.json` to register your new data source:

```json
{
  "sources": [
    {
      "_comment": "YourSource - Description of what this source provides",
      "name": "yoursource",
      "enabled": true,
      "category": "other_stories",
      "class_name": "YourSource",

      "config": {
        "api_endpoint": "https://api.yourservice.com",
        "max_results": 100,
        "search_query": "artificial intelligence machine learning",
        "_comment_max_results": "Maximum number of items to fetch per request"
      },

      "rate_limit": {
        "requests": 100,
        "per": "hour",
        "_comment": "API allows 100 requests per hour"
      },

      "auth": {
        "type": "api_key",
        "key_env": "YOURSOURCE_API_KEY",
        "_comment": "API key stored in environment variable YOURSOURCE_API_KEY"
      }
    }
  ],

  "global_config": {
    "concurrent_sources": 5,
    "retry_attempts": 3,
    "timeout": 30,
    "user_agent": "Rescribos-DataRefinement/1.0"
  }
}
```

### Configuration Options Explained

| Field                 | Type    | Required    | Description                                                  |
| --------------------- | ------- | ----------- | ------------------------------------------------------------ |
| `name`                | string  | Yes         | Unique identifier for this source (lowercase, no spaces)     |
| `enabled`             | boolean | Yes         | Whether this source is active                                |
| `category`            | string  | Yes         | One of: `arxiv_stories`, `other_stories`, `document_stories` |
| `class_name`          | string  | Yes         | Python class name (must match your implementation)           |
| `config`              | object  | Yes         | Source-specific configuration parameters                     |
| `rate_limit`          | object  | Recommended | API rate limiting configuration                              |
| `auth`                | object  | Yes         | Authentication configuration                                 |
| `timeout_seconds`     | number  | Optional    | Override default timeout (default: 180s)                     |
| `retry_attempts`      | number  | Optional    | Override default retry attempts (default: 2)                 |
| `retry_delay_seconds` | number  | Optional    | Override default retry delay (default: 5s)                   |

### Authentication Configuration

#### No Authentication

```json
"auth": {
  "type": "none"
}
```

#### API Key (Header)

```json
"auth": {
  "type": "api_key",
  "key_env": "YOURSOURCE_API_KEY"
}
```

This adds header: `X-API-Key: <value from environment>`

#### Bearer Token

```json
"auth": {
  "type": "bearer",
  "token_env": "YOURSOURCE_TOKEN"
}
```

This adds header: `Authorization: Bearer <value from environment>`

#### Custom Authentication

For OAuth or custom auth, implement in your plugin:

```python
def _get_custom_headers(self) -> Dict[str, str]:
    """Override to add custom authentication."""
    headers = super()._get_auth_headers()

    # Add your custom auth logic
    oauth_token = self._get_oauth_token()
    headers['Authorization'] = f'OAuth {oauth_token}'

    return headers
```

### Environment Variables

Add your API credentials to the `.env` file in the project root:

```bash
# YourSource API Configuration
YOURSOURCE_API_KEY=your_api_key_here
YOURSOURCE_API_SECRET=your_secret_here

# Optional: Enable GPT-4 AI screening (requires OpenAI API key)
USE_GPT41_AI_SCREENING=false
OPENAI_API_KEY=your_openai_key_here
```

### Rate Limiting Configuration

Configure rate limits to respect your API's limits:

```json
"rate_limit": {
  "requests": 100,      // Number of requests
  "per": "hour"         // Time period: "second", "minute", "hour", "day"
}
```

The system will automatically throttle requests to stay within these limits.

---

## Testing & Validation

### Step 1: Unit Testing Your Plugin

Create a test file `scripts/data_sources/test_yoursource.py`:

```python
"""
Unit tests for YourSource data source plugin.
"""

import asyncio
import pytest
from yoursource_source import YourSource

@pytest.mark.asyncio
async def test_yoursource_extract():
    """Test that extract() returns data."""
    config = {
        'name': 'yoursource',
        'category': 'other_stories',
        'enabled': True,
        'api_endpoint': 'https://api.yourservice.com',
        'max_results': 10,
        'rate_limit': {'requests': 100, 'per': 'hour'},
        'auth': {'type': 'none'}
    }

    source = YourSource(config)
    results = await source.extract()

    assert isinstance(results, list)
    assert len(results) > 0
    print(f"✓ Extracted {len(results)} items")

@pytest.mark.asyncio
async def test_yoursource_transform():
    """Test that transform() creates valid stories."""
    config = {
        'name': 'yoursource',
        'category': 'other_stories',
        'enabled': True,
        'rate_limit': {'requests': 100, 'per': 'hour'},
        'auth': {'type': 'none'}
    }

    source = YourSource(config)

    # Mock raw data
    raw_data = [
        {
            'id': '123',
            'title': 'Test Article About AI',
            'link': 'https://example.com/article',
            'published_at': '2024-01-15T10:00:00Z',
            'content': 'This is test content about artificial intelligence.'
        }
    ]

    stories = source.transform(raw_data)

    assert len(stories) == 1
    story = stories[0]

    # Verify required fields
    assert story['id'] == '123'
    assert story['title'] == 'Test Article About AI'
    assert story['url'] == 'https://example.com/article'
    assert isinstance(story['time'], int)
    assert story['source'] == 'yoursource'
    assert story['category'] == 'other_stories'

    print(f"✓ Transform created valid story: {story['title']}")

@pytest.mark.asyncio
async def test_yoursource_validate():
    """Test that validation works correctly."""
    config = {
        'name': 'yoursource',
        'category': 'other_stories',
        'enabled': True,
        'rate_limit': {'requests': 100, 'per': 'hour'},
        'auth': {'type': 'none'}
    }

    source = YourSource(config)

    # Valid story
    valid_story = {
        'id': '123',
        'title': 'Valid Test Article',
        'url': 'https://example.com/article',
        'time': 1234567890
    }

    assert source.validate(valid_story) == True
    print("✓ Validation passed for valid story")

    # Invalid story (missing title)
    invalid_story = {
        'id': '456',
        'url': 'https://example.com/article',
        'time': 1234567890
    }

    assert source.validate(invalid_story) == False
    print("✓ Validation correctly rejected invalid story")

if __name__ == "__main__":
    asyncio.run(test_yoursource_extract())
    asyncio.run(test_yoursource_transform())
    asyncio.run(test_yoursource_validate())
```

Run tests:

```bash
cd ai-news-extractor
python scripts/data_sources/test_yoursource.py
```

### Step 2: Integration Testing

Test your source with the full system:

```python
# scripts/test_integration_yoursource.py

import asyncio
import logging
from multi_source_extractor import MultiSourceExtractor

logging.basicConfig(level=logging.INFO)

async def test_integration():
    """Test YourSource with the full extraction pipeline."""

    # Create extractor
    extractor = MultiSourceExtractor()

    # List available sources
    sources = extractor.list_sources()
    print("Available sources:", list(sources.keys()))

    # Ensure your source is enabled
    if 'yoursource' not in sources:
        print("ERROR: YourSource not found in configuration!")
        return

    if not sources['yoursource']['enabled']:
        print("Enabling YourSource...")
        extractor.enable_source('yoursource')

    # Run extraction (only your source)
    print("Starting extraction from YourSource...")
    results = await extractor.extract_all()

    if 'yoursource' in results:
        stories = results['yoursource']
        print(f"\n✓ Extracted {len(stories)} stories from YourSource")

        if stories:
            # Show first story
            first_story = stories[0]
            print("\nFirst story:")
            print(f"  ID: {first_story.get('id')}")
            print(f"  Title: {first_story.get('title')}")
            print(f"  URL: {first_story.get('url')}")
            print(f"  Content length: {len(first_story.get('content', ''))}")
    else:
        print("ERROR: No results from YourSource")

if __name__ == "__main__":
    asyncio.run(test_integration())
```

Run integration test:

```bash
python scripts/test_integration_yoursource.py
```

### Step 3: End-to-End Testing

Run a complete extraction with all sources:

```bash
# Full extraction pipeline
python scripts/multi_source_extractor.py
```

Check the output file in `storage/extracted/` to verify your stories are included.

### Validation Checklist

- [ ] Plugin file created in `scripts/data_sources/`
- [ ] Class extends `DataSource` base class
- [ ] `extract()` method implemented and returns list of dictionaries
- [ ] `transform()` method converts to standard schema
- [ ] All required fields present: `id`, `title`, `url`, `time`
- [ ] Configuration added to `config/data_sources.json`
- [ ] Environment variables set in `.env` (if auth required)
- [ ] Unit tests pass
- [ ] Integration test extracts stories successfully
- [ ] Stories appear in final extraction file
- [ ] No errors in logs during extraction

---

## Advanced Features

### Content Enhancement with Web Search

If your API doesn't provide full content, Rescribos can automatically enhance stories using web search:

```python
# The system will automatically:
# 1. Detect stories with missing/short content
# 2. Search the web for the article
# 3. Extract full content from the original URL
# 4. Add enhanced content to the story

# To enable, ensure OPENAI_API_KEY is set in .env
# The system uses GPT-4 to generate search queries and extract content
```

### AI Relevance Screening

Enable GPT-4 screening to filter for AI-related content:

```python
# In your .env file:
USE_GPT41_AI_SCREENING=true
OPENAI_API_KEY=your_key_here
```

This will:

1. Extract all stories from your API
2. Use GPT-4 to analyze each story's relevance to AI/ML
3. Only keep stories with 45%+ confidence of being AI-related
4. Log confidence scores for debugging

### Async Transform with AI Processing

For compute-intensive transformations (e.g., AI relevance checking), you can implement async transformation. **There are two approaches**:

#### Approach 1: Async Transform with Sync Wrapper (Recommended for AI Filtering)

This approach is used by arXiv and USAspending sources for GPT-4 AI relevance filtering:

```python
async def transform_async(self, raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Async transform with AI processing support.
    """
    candidate_stories = []

    # First pass: Basic transformation
    for item in raw_data:
        story = self._basic_transform(item)
        candidate_stories.append(story)

    # Second pass: AI relevance filtering (if enabled)
    import os
    use_gpt_screening = os.getenv('USE_GPT41_AI_SCREENING', 'false').lower() == 'true'

    if use_gpt_screening:
        from ..ai_relevance_checker import get_ai_relevance_checker
        ai_checker = get_ai_relevance_checker()

        # Prepare for batch checking
        items_to_check = [
            {
                'title': story['title'],
                'content': story.get('content', '')[:1000],
                'context': 'YourSource article'
            }
            for story in candidate_stories
        ]

        # Batch check relevance
        relevance_results = await ai_checker.batch_check_relevance(
            items_to_check,
            concurrency=1
        )

        # Filter based on results
        stories = []
        for story, relevance_result in zip(candidate_stories, relevance_results):
            if relevance_result.is_ai_related and relevance_result.confidence >= 0.45:
                stories.append(story)

        return stories

    return candidate_stories

def transform(self, raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Sync wrapper for transform_async."""
    try:
        loop = asyncio.get_running_loop()
        # Run in thread pool to avoid blocking
        import concurrent.futures

        def run_in_thread():
            new_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(new_loop)
            try:
                return new_loop.run_until_complete(self.transform_async(raw_data))
            finally:
                new_loop.close()

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(run_in_thread)
            return future.result(timeout=300)
    except RuntimeError:
        # No running loop
        return asyncio.run(self.transform_async(raw_data))
```

#### Approach 2: Override process() for Full Async Control (Advanced)

If you need full control over the entire pipeline (extract → transform → validate), you can override `process()` like USAspending does:

```python
async def process(self, **kwargs) -> List[Dict[str, Any]]:
    """
    Override base process to handle async transformation.
    Use this when transform() needs to be async throughout.
    """
    if not self.enabled:
        logger.info(f"Data source '{self.name}' is disabled, skipping")
        return []

    try:
        logger.info(f"Starting processing for {self.name}")

        # Rate limiting check
        await self._enforce_rate_limit()

        # Extract raw data
        raw_data = await self.extract(**kwargs)
        logger.info(f"Extracted {len(raw_data)} raw items from {self.name}")

        # Transform to standard schema (using your async transform method)
        transformed = await self.transform_async(raw_data)
        logger.info(f"Transformed {len(transformed)} items from {self.name}")

        # Validate and filter
        valid_stories = [story for story in transformed if self.validate(story)]
        invalid_count = len(transformed) - len(valid_stories)

        if invalid_count > 0:
            logger.warning(f"Filtered out {invalid_count} invalid items from {self.name}")

        logger.info(f"Successfully processed {len(valid_stories)} stories from {self.name}")
        return valid_stories

    except Exception as e:
        logger.error(f"Error processing data from {self.name}: {e}")
        return []
```

**When to use each approach:**

- **Approach 1**: When you only need async during transformation (e.g., AI filtering)
- **Approach 2**: When you need async operations during transformation AND it's called from `extract()` context (e.g., fetching related data)

### Pagination Handling

For APIs with pagination:

```python
async def extract(self, **kwargs) -> List[Dict[str, Any]]:
    """Extract with pagination support."""
    all_items = []
    page = 1
    max_pages = kwargs.get('max_pages', 10)

    async with create_session_context() as session:
        while page <= max_pages:
            params = {
                'page': page,
                'per_page': 100
            }

            async with session.get(self.api_endpoint, params=params) as response:
                response.raise_for_status()
                data = await response.json()

                items = data.get('items', [])
                if not items:
                    break  # No more pages

                all_items.extend(items)
                page += 1

                # Rate limiting delay
                await asyncio.sleep(1)

    return all_items
```

### Error Handling & Retries

The base class provides rate limiting, but you can add custom retry logic:

```python
async def extract(self, **kwargs) -> List[Dict[str, Any]]:
    """Extract with custom retry logic."""
    max_retries = 3
    retry_delay = 5

    for attempt in range(max_retries):
        try:
            async with create_session_context() as session:
                async with session.get(self.api_endpoint) as response:
                    response.raise_for_status()
                    data = await response.json()
                    return data.get('items', [])

        except aiohttp.ClientError as e:
            logger.warning(f"Attempt {attempt + 1}/{max_retries} failed: {e}")

            if attempt < max_retries - 1:
                await asyncio.sleep(retry_delay * (attempt + 1))
            else:
                logger.error(f"All retry attempts failed for {self.name}")
                return []

        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return []

    return []
```

---

## Troubleshooting

### Common Issues

#### 1. Source Not Found in Configuration

**Error**: `Source 'yoursource' not found`

**Solutions**:

- Verify `name` in `config/data_sources.json` matches your class name (lowercase)
- Check that `class_name` in config matches your Python class name exactly
- Ensure `enabled: true` in configuration
- Restart the application after config changes

#### 2. Import Errors

**Error**: `ModuleNotFoundError: No module named 'yoursource_source'`

**Solutions**:

- Check file is in `scripts/data_sources/` directory
- Ensure `__init__.py` exists in `data_sources/` folder
- Verify Python can find the scripts directory (check PYTHONPATH)
- Use correct import statement in your plugin

#### 3. No Stories Extracted

**Symptoms**: `Extracted 0 stories from yoursource`

**Debug steps**:

1. Check logs for API errors
2. Verify API endpoint is correct
3. Test API credentials/authentication
4. Add print statements in `extract()` to see raw response
5. Check rate limiting isn't blocking requests

```python
# Debug version of extract()
async def extract(self, **kwargs) -> List[Dict[str, Any]]:
    print(f"[DEBUG] Starting extraction from {self.api_endpoint}")

    async with create_session_context() as session:
        print(f"[DEBUG] Making request...")
        async with session.get(self.api_endpoint) as response:
            print(f"[DEBUG] Response status: {response.status}")
            text = await response.text()
            print(f"[DEBUG] Response (first 200 chars): {text[:200]}")

            data = await response.json()
            print(f"[DEBUG] JSON keys: {data.keys()}")

            items = data.get('items', [])
            print(f"[DEBUG] Found {len(items)} items")
            return items
```

#### 4. Validation Failures

**Error**: `Story missing required field 'title'`

**Solutions**:

- Add logging to `transform()` to see what fields are present
- Check your field mapping against API response
- Ensure all required fields are populated
- Add fallback values for missing data

```python
def transform(self, raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    stories = []

    for item in raw_data:
        # Debug: Print available fields
        print(f"[DEBUG] Available fields: {list(item.keys())}")

        # Debug: Print field values
        print(f"[DEBUG] Title: {item.get('title')}")
        print(f"[DEBUG] URL: {item.get('url')}")

        story = {
            'id': item.get('id'),
            'title': item.get('title', 'No title'),  # Fallback
            'url': item.get('url', item.get('link', '')),  # Try multiple fields
            'time': self._parse_timestamp(item.get('published_at', item.get('created_at'))),
            'source': self.name,
            'category': self.category
        }

        stories.append(story)

    return stories
```

#### 5. Authentication Failures

**Error**: `401 Unauthorized` or `403 Forbidden`

**Solutions**:

- Verify environment variable is set: `echo $YOURSOURCE_API_KEY`
- Check API key format is correct (no extra spaces/quotes)
- Ensure auth type in config matches API requirements
- Test API key with curl first:
  ```bash
  curl -H "X-API-Key: YOUR_KEY" https://api.yourservice.com/test
  ```

#### 6. Rate Limiting Issues

**Symptoms**: `429 Too Many Requests` or very slow extraction

**Solutions**:

- Reduce `requests` in rate_limit config
- Increase delay between batches in your code
- Check if API has burst limits vs sustained limits
- Implement exponential backoff

#### 7. Duplicate Stories

**Symptoms**: Same stories appear multiple times

**Solutions**:

- Ensure `id` field is truly unique
- Check that IDs are stable across multiple extractions
- Verify deduplication is enabled in global config
- Look for ID collisions in logs

### Debugging Tools

#### Enable Debug Logging

```python
# In your test script
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

#### Test API Independently

```python
# scripts/test_api_raw.py
import asyncio
import aiohttp

async def test_api():
    """Test your API directly without Rescribos."""
    async with aiohttp.ClientSession() as session:
        url = "https://api.yourservice.com/search"
        headers = {"X-API-Key": "YOUR_KEY"}
        params = {"limit": 5}

        async with session.get(url, headers=headers, params=params) as response:
            print(f"Status: {response.status}")
            print(f"Headers: {response.headers}")

            if response.status == 200:
                data = await response.json()
                print(f"Response keys: {data.keys()}")

                if 'items' in data:
                    print(f"Items count: {len(data['items'])}")
                    print(f"First item: {data['items'][0]}")
            else:
                text = await response.text()
                print(f"Error response: {text}")

asyncio.run(test_api())
```

#### Inspect Extraction Output

```python
# Check what was actually extracted
import json

with open('storage/extracted/ai_stories_extracted_2024-01-15.json', 'r') as f:
    data = json.load(f)

# Find your source's stories
other_stories = data.get('other_stories', [])
yoursource_stories = [s for s in other_stories if s.get('source') == 'yoursource']

print(f"Found {len(yoursource_stories)} stories from yoursource")
if yoursource_stories:
    print(f"Sample story: {json.dumps(yoursource_stories[0], indent=2)}")
```

---

## Examples

### Example 1: Reddit API Integration

```python
"""Reddit data source for extracting posts from AI-related subreddits."""

import asyncio
import aiohttp
from typing import List, Dict, Any
from .base_source import DataSource

class RedditSource(DataSource):
    """Extract posts from Reddit's JSON API."""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.subreddits = config.get('subreddits', ['MachineLearning', 'artificial'])
        self.post_limit = config.get('post_limit', 25)
        self.min_score = config.get('min_score', 10)

    async def extract(self, **kwargs) -> List[Dict[str, Any]]:
        """Extract posts from configured subreddits."""
        all_posts = []

        headers = {'User-Agent': self.get_user_agent()}

        async with aiohttp.ClientSession(headers=headers) as session:
            for subreddit in self.subreddits:
                url = f"https://www.reddit.com/r/{subreddit}/hot.json"
                params = {'limit': self.post_limit}

                try:
                    async with session.get(url, params=params) as response:
                        response.raise_for_status()
                        data = await response.json()

                        posts = data.get('data', {}).get('children', [])
                        all_posts.extend([p['data'] for p in posts])

                        # Reddit rate limit: wait 2 seconds between requests
                        await asyncio.sleep(2)

                except Exception as e:
                    logger.error(f"Failed to fetch r/{subreddit}: {e}")
                    continue

        return all_posts

    def transform(self, raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Transform Reddit posts to standard schema."""
        stories = []

        for post in raw_data:
            # Filter by score
            if post.get('score', 0) < self.min_score:
                continue

            story = {
                'id': post['id'],
                'title': post['title'],
                'url': post.get('url', f"https://reddit.com{post['permalink']}"),
                'time': int(post['created_utc']),
                'content': post.get('selftext', ''),
                'source': self.name,
                'category': self.category,
                'metadata': {
                    'subreddit': post['subreddit'],
                    'score': post['score'],
                    'num_comments': post['num_comments'],
                    'author': post['author']
                }
            }

            stories.append(story)

        return stories
```

Configuration:

```json
{
  "name": "reddit",
  "enabled": true,
  "category": "other_stories",
  "class_name": "RedditSource",
  "config": {
    "subreddits": ["MachineLearning", "artificial", "singularity"],
    "post_limit": 25,
    "min_score": 10
  },
  "rate_limit": {
    "requests": 60,
    "per": "minute"
  },
  "auth": {
    "type": "none"
  }
}
```

### Example 2: RSS Feed Integration

```python
"""Generic RSS feed data source."""

import asyncio
import aiohttp
import xml.etree.ElementTree as ET
from typing import List, Dict, Any
from .base_source import DataSource

class RSSSource(DataSource):
    """Extract articles from RSS/Atom feeds."""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.feed_urls = config.get('feed_urls', [])
        self.max_items_per_feed = config.get('max_items_per_feed', 50)

    async def extract(self, **kwargs) -> List[Dict[str, Any]]:
        """Fetch and parse RSS feeds."""
        all_items = []

        async with aiohttp.ClientSession() as session:
            for feed_url in self.feed_urls:
                try:
                    async with session.get(feed_url) as response:
                        response.raise_for_status()
                        xml_content = await response.text()

                        items = self._parse_rss(xml_content)
                        all_items.extend(items[:self.max_items_per_feed])

                        await asyncio.sleep(1)

                except Exception as e:
                    logger.error(f"Failed to fetch {feed_url}: {e}")
                    continue

        return all_items

    def _parse_rss(self, xml_content: str) -> List[Dict[str, Any]]:
        """Parse RSS XML into item dictionaries."""
        items = []

        try:
            root = ET.fromstring(xml_content)

            # Try RSS 2.0 format
            for item in root.findall('.//item'):
                items.append({
                    'title': self._get_text(item, 'title'),
                    'link': self._get_text(item, 'link'),
                    'description': self._get_text(item, 'description'),
                    'pub_date': self._get_text(item, 'pubDate'),
                    'guid': self._get_text(item, 'guid')
                })

            # Try Atom format if no RSS items found
            if not items:
                ns = {'atom': 'http://www.w3.org/2005/Atom'}
                for entry in root.findall('.//atom:entry', ns):
                    items.append({
                        'title': self._get_text(entry, 'atom:title', ns),
                        'link': entry.find('atom:link', ns).get('href') if entry.find('atom:link', ns) is not None else '',
                        'description': self._get_text(entry, 'atom:summary', ns),
                        'pub_date': self._get_text(entry, 'atom:updated', ns),
                        'guid': self._get_text(entry, 'atom:id', ns)
                    })

        except ET.ParseError as e:
            logger.error(f"XML parsing failed: {e}")

        return items

    def _get_text(self, element, tag, namespace=None):
        """Safely extract text from XML element."""
        if namespace:
            child = element.find(tag, namespace)
        else:
            child = element.find(tag)

        return child.text if child is not None else ''

    def transform(self, raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Transform RSS items to standard schema."""
        import hashlib

        stories = []

        for item in raw_data:
            # Generate numeric ID from GUID/link
            guid = item.get('guid') or item.get('link', '')
            numeric_id = int(hashlib.md5(guid.encode()).hexdigest()[:8], 16)

            story = {
                'id': numeric_id,
                'title': item.get('title', ''),
                'url': item.get('link', ''),
                'time': self._parse_timestamp(item.get('pub_date', '')),
                'content': item.get('description', ''),
                'source': self.name,
                'category': self.category
            }

            stories.append(story)

        return stories
```

### Example 3: REST API with Pagination

```python
"""Example REST API with pagination and authentication."""

import asyncio
import aiohttp
from typing import List, Dict, Any
from .base_source import DataSource

class PaginatedAPISource(DataSource):
    """Extract from paginated REST API."""

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.base_url = config.get('base_url')
        self.max_pages = config.get('max_pages', 10)
        self.per_page = config.get('per_page', 100)

    async def extract(self, **kwargs) -> List[Dict[str, Any]]:
        """Extract with pagination."""
        all_items = []
        page = 1

        headers = {
            'User-Agent': self.get_user_agent(),
            **self._get_auth_headers()
        }

        async with aiohttp.ClientSession(headers=headers) as session:
            while page <= self.max_pages:
                params = {
                    'page': page,
                    'per_page': self.per_page,
                    'sort': 'created_at',
                    'order': 'desc'
                }

                try:
                    async with session.get(self.base_url, params=params) as response:
                        response.raise_for_status()
                        data = await response.json()

                        items = data.get('results', [])

                        if not items:
                            # No more pages
                            break

                        all_items.extend(items)

                        # Check if there are more pages
                        pagination = data.get('pagination', {})
                        if not pagination.get('has_next', False):
                            break

                        page += 1

                        # Rate limiting
                        await asyncio.sleep(1)

                except aiohttp.ClientError as e:
                    logger.error(f"API request failed on page {page}: {e}")
                    break

        logger.info(f"Fetched {len(all_items)} items across {page} pages")
        return all_items

    def transform(self, raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Transform API response to standard schema."""
        stories = []

        for item in raw_data:
            story = {
                'id': item['id'],
                'title': item['title'],
                'url': item['url'],
                'time': self._parse_timestamp(item['created_at']),
                'content': item.get('body', item.get('content', '')),
                'source': self.name,
                'category': self.category,
                'authors': [item['author']['name']] if 'author' in item else [],
                'tags': item.get('tags', [])
            }

            stories.append(story)

        return stories
```

---

## Additional Resources

### Rescribos Documentation

- Main README: `README.md`
- Configuration Guide: `config/data_sources.json` (see inline comments)
- Prompt System: `config/prompts.json`

### Base Classes & Utilities

- `scripts/data_sources/base_source.py` - Base DataSource class
- `scripts/multi_source_extractor.py` - Orchestration logic
- `scripts/connection_utils.py` - Network utilities
- `scripts/content_extractor.py` - Content extraction from URLs

### Reference Implementations

- `scripts/data_sources/hackernews_source.py` - Full-featured example with content extraction
- `scripts/data_sources/arxiv_source.py` - Academic paper integration
- `scripts/data_sources/usaspending_source.py` - Government contracts API

### External Resources

- Python asyncio: https://docs.python.org/3/library/asyncio.html
- aiohttp documentation: https://docs.aiohttp.org/
- API design best practices: https://restfulapi.net/

---

## Summary

Integrating a new API data source into Rescribos involves:

1. **Creating a plugin** that extends the `DataSource` base class
2. **Implementing three methods**: `extract()`, `transform()`, and optionally `validate()`
3. **Mapping your API's data** to Rescribos' standard story schema
4. **Configuring the source** in `config/data_sources.json`
5. **Testing thoroughly** with unit tests and integration tests

The system handles:

- ✅ Parallel extraction from multiple sources
- ✅ Rate limiting and request throttling
- ✅ Deduplication via embeddings database
- ✅ Content enhancement from web search
- ✅ AI relevance screening (optional)
- ✅ Error handling and retries
- ✅ Categorization and storage

Your responsibility:

- ✅ Fetch raw data from your API
- ✅ Transform data to standard schema
- ✅ Handle API-specific authentication
- ✅ Respect API rate limits

For questions or issues, check the troubleshooting section or examine the reference implementations in `scripts/data_sources/`.

---

## Automation Tools

Rescribos provides powerful automation tools to simplify and accelerate data source integration:

### 1. Template Generator (`scripts/create_datasource.py`)

Automatically generates complete data source templates with all boilerplate code, configuration, and tests.

**Features**:

- Interactive wizard for easy setup
- CLI mode for automation pipelines
- Generates plugin file with TODOs at the right places
- Creates test file with pytest examples
- Automatically updates `config/data_sources.json`
- Supports REST, RSS, GraphQL, WebSocket APIs
- Handles all authentication types

**Usage**:

```bash
# Interactive mode
python scripts/create_datasource.py

# CLI mode
python scripts/create_datasource.py --name=myapi --api-type=rest --auth=api_key --category=other_stories
```

**What it generates**:

- `scripts/data_sources/myapi_source.py` - Complete plugin with extract(), transform(), validate()
- `scripts/tests/test_myapi_source.py` - Test file with examples
- Updates to `config/data_sources.json` - Proper configuration entry

**Time saved**: Reduces initial setup from 1-2 hours to 2 minutes!

---

### 2. Validation Debugger (`scripts/validate_datasource.py`)

Tests and debugs data source integrations with detailed validation reporting.

**Features**:

- Tests extract() method execution
- Tests transform() method output
- Validates all required fields (id, title, url, time)
- Checks field types and formats
- Validates optional fields
- Shows exactly why stories fail validation
- Displays sample API responses for debugging
- Configurable verbosity levels

**Usage**:

```bash
# Basic validation
python scripts/validate_datasource.py --source=myapi

# Detailed output
python scripts/validate_datasource.py --source=myapi --verbose

# Show raw API response
python scripts/validate_datasource.py --source=myapi --show-raw

# Validate more stories
python scripts/validate_datasource.py --source=myapi --max-stories=50
```

**Example output**:

```
============================================================
Testing Data Source: myapi
============================================================

✓ Configuration loaded
✓ Class imported successfully
✓ Data source initialized

============================================================
Running Extraction
============================================================

✓ Extraction completed
ℹ Retrieved 25 items

============================================================
Running Transformation
============================================================

✓ Transformation completed
ℹ Generated 25 stories

============================================================
Validation Results
============================================================

✓ Story 1: VALID
  Title: Example Article About AI
  URL: https://example.com/article/123

✗ Story 2: INVALID
  Title: Short
  ✗ Title too short (5 chars, minimum 10)
  ✗ Missing required field: 'time'

============================================================
Summary
============================================================

ℹ Total stories validated: 25
✓ Valid stories: 23 (92.0%)
✗ Invalid stories: 2 (8.0%)
```

**Time saved**: Reduces debugging from hours to minutes with clear error messages!

---

### Quick Start Workflow

For the fastest integration experience:

1. **Generate template** (2 minutes):

   ```bash
   python scripts/create_datasource.py
   ```

2. **Fill in TODOs** (15-30 minutes):

   - Update API endpoint URL
   - Map field names from your API
   - Add any custom logic

3. **Test and debug** (15-30 minutes):

   ```bash
   python scripts/validate_datasource.py --source=myapi --verbose
   ```

4. **Run full integration** (5 minutes):
   ```bash
   python scripts/multi_source_extractor.py
   ```

**Total time: 30-60 minutes** instead of 3-6 hours manually!

---

### Additional Documentation

For a step-by-step quick start guide with common patterns and troubleshooting:

- See [Quick Start Guide](QUICKSTART_DATASOURCE_INTEGRATION.md)

---

**Document Version**: 2.0
**Last Updated**: January 2025
**Rescribos Version**: multi-source-v1.0
