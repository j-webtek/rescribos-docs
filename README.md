# Rescribos Data Refinement (AI News Extractor)

Rescribos Data Refinement is a cross-platform desktop application that automates the collection, analysis, and synthesis of AI-related news. The platform combines an Electron front end, a Node.js orchestration layer, and a Python processing pipeline to deliver curated reports, semantic search, and interactive analysis without handing data to third-party services.

## Platform Highlights

- Local-first storage for reports, logs, and configuration with optional cloud calls only for selected AI providers
- Bring-your-own-keys model that keeps cost control and credentials in the hands of the operator
- Hybrid AI execution that can switch between OpenAI GPT-5, Ollama Llama 3.1, or transformers-based fallbacks
- Multi-source extraction covering Hacker News, arXiv, optional US public procurement feeds, and local document ingestion. Additional connectors can be generated with the data source template for REST/RSS/GraphQL APIs.
- Rich analysis pipeline with summarisation, relevance scoring, deduplication, clustering, and tag generation
- Semantic vector search, cart-based batching, and a conversational assistant backed by the analysed corpus
- CLI and automation hooks for scheduled jobs, smoke tests, and integration into existing workflows

## How the System Works

1. **Extract** - Collect stories from configured sources with concurrency limits, retry policies, and deduplication.
2. **Analyse** - Execute Python-based summarisation, tagging, and impact scoring through the selected AI provider.
3. **Organise** - Group stories into themes, collapse duplicates, and generate embeddings for semantic lookup.
4. **Synthesize** - Produce Markdown, JSON, and PDF outputs with executive summaries and streamlined citations.
5. **Explore** - Use the desktop UI, semantic search, or chat assistant to interrogate the generated knowledge base.

The same pipeline is exposed through the CLI (`npm run cli -- <command>`) and can be orchestrated from scheduled jobs or CI environments.

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
