# Rescribos Data Refinement

Rescribos Data Refinement is a cross-platform desktop application that transforms how organizations collect, analyze, and synthesize information from any source. The platform combines an Electron front end, a Node.js orchestration layer, and a Python processing pipeline to deliver curated reports, semantic search, and interactive analysis—all without handing data to third-party services.

## Platform Highlights

**Your Data, Your Sources, Your Control:**
- **Flexible Data Ingestion** – Connect to any data source: APIs, RSS feeds, databases, document repositories, web scraping, or custom connectors
- **Local-First Architecture** – All content, analysis, and reports stored on your infrastructure with optional cloud AI processing
- **Bring-Your-Own-Keys Model** – Complete cost control and credential ownership; pay AI providers directly at cost
- **Hybrid AI Execution** – Switch seamlessly between OpenAI GPT-5, Ollama Llama 3.1, or transformer-based fallbacks
- **AI-Powered Analysis Pipeline** – Automated summarization, relevance scoring, deduplication, clustering, and tag generation
- **Semantic Knowledge Management** – Vector search, conversational AI assistant, and intelligent document discovery
- **Enterprise Automation** – CLI tools, scheduling, and integration hooks for systematic workflows

**Included Example Data Sources:**
The platform includes pre-configured connectors for Hacker News, arXiv, USASpending.gov, and SAM.gov as reference implementations. These demonstrate the platform's capabilities and can be easily replaced or supplemented with your organization's specific data sources using the extensible connector framework.

## How the System Works

1. **Connect** - Configure data sources relevant to your organization (news feeds, research databases, internal documents, APIs, etc.)
2. **Extract** - Automated collection with concurrency control, retry policies, and intelligent deduplication
3. **Analyze** - AI-powered summarization, relevance scoring, tagging, and impact assessment
4. **Organize** - Thematic grouping, duplicate collapse, and semantic embedding generation
5. **Synthesize** - Generate reports in multiple formats (Markdown, JSON, PDF, DOCX) with executive summaries
6. **Explore** - Query your knowledge base through semantic search, interactive AI chat, or the desktop interface

The entire pipeline is accessible through both the desktop UI and CLI, enabling automated workflows, scheduled jobs, and CI/CD integration.

## Responsible Use Notice

Rescribos includes web scraping capabilities for content extraction. **Users are responsible for ensuring legal and ethical use** of these features:

- ✅ Verify authorization to access configured data sources
- ✅ Respect robots.txt directives and website Terms of Service
- ✅ Configure appropriate rate limits to avoid server overload
- ✅ Be aware that aggressive scraping may result in IP bans
- ✅ Prefer official APIs over scraping when available

See [Responsible Data Collection](core-capabilities/data-extraction.md#responsible-data-collection) for comprehensive guidelines on ethical scraping practices.

## Documentation Map

- **Orientation** - [Executive Summary](introduction/README.md), [At a Glance](introduction/at-a-glance.md), and [Value Proposition](introduction/value-proposition.md).
- **Architecture** - [System Architecture](architecture/README.md), [Multi-Layer Design](architecture/multi-layer-design.md), [Technology Stack](architecture/technology-stack.md), and [Cross-Platform Support](architecture/cross-platform.md).
- **Core Capabilities** - [Overview](core-capabilities/README.md) plus deep dives on [Extraction](core-capabilities/data-extraction.md), [AI Analysis](core-capabilities/ai-analysis.md), [Thematic Analysis](core-capabilities/thematic-analysis.md), [Semantic Search](core-capabilities/semantic-search.md), and [Chat](core-capabilities/ai-chat.md).
- **AI Providers & Security** - [Hybrid Provider System](ai-provider-system/README.md), [Offline Mode](ai-provider-system/offline-capabilities.md), [Privacy Controls](privacy-security/README.md), and [Compliance Notes](privacy-security/compliance.md).
- **Pipeline & Features** - [Data Pipeline](data-pipeline/README.md), [Document Processing](advanced-features/document-processing.md), [Cart Workflow](advanced-features/cart-workflow.md), and [Report Management](advanced-features/report-management.md).
- **Implementation Reference** - [Technical Implementation](technical-implementation/README.md) with breakouts for frontend, backend, and Python services.
- **Operations** - [Deployment](deployment/README.md), [Configuration](deployment/configuration.md), [Performance](performance/README.md), and [Troubleshooting](appendices/troubleshooting.md).
- **Business Support** - [Licensing Overview](licensing/README.md), [Pricing Tiers](licensing/tiers.md), and [Frequently Asked Questions](licensing/faqs.md).

## Current Release Snapshot

- **Application version**: `1.0.0`
- **Node.js requirement**: 18+
- **Python requirement**: 3.8+ with virtual environment support
- **Primary storage**: `storage/` (reports), `logs/`, `config/`, and `coverage/`
- **Supported distributions**: packaged installers via `electron-builder`, CLI usage, or containerised deployment
- **Key commands**:
  - `npm install` and `npm run install-python` for full environment setup
  - `npm start` for the desktop application
  - `npm run cli -- extract --max-stories 200` for CLI-driven extraction
  - `npm run cli -- validate` for environment verification

## Need a Starting Point?

- Developers should begin with [Deployment & Setup](deployment/installation.md) and the [Technical Implementation](technical-implementation/README.md).
- Analysts can review [Core Capabilities](core-capabilities/README.md) and the [Report Management](advanced-features/report-management.md) guide.
- Operations teams can focus on [AI Provider System](ai-provider-system/README.md) and [Privacy & Security](privacy-security/README.md).

All sections are kept in sync with the Markdown documentation under `docs/`. Whenever the codebase evolves, the GitBook pages here are updated to match the authoritative guides.
