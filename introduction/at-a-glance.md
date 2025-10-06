# Executive At-a-Glance

**Rescribos Data Refinement** transforms information chaos into strategic intelligence through privacy-first AI analysis.

## What | Why | How | Who

| **What is Rescribos?** | **Why Choose Rescribos?** |
|------------------------|---------------------------|
| Enterprise AI knowledge management platform that automates content extraction, analysis, and synthesis from multiple sources into actionable intelligence reports. | - 100% local data storage (GDPR/HIPAA ready)<br>- User-controlled AI costs (BYOK model)<br>- Hybrid cloud/local processing<br>- 10-20 hours saved per week<br>- Zero vendor lock-in |

| **How Does It Work?** | **Who Is It For?** |
|-----------------------|--------------------|
| 1. **Extract** from 10+ sources (APIs, PDFs, web)<br>2. **Analyze** with GPT-4o or local models<br>3. **Organize** via ML clustering & embeddings<br>4. **Synthesize** thematic reports with citations<br>5. **Query** via semantic search & AI chat | - Research analysts & consultants<br>- Competitive intelligence teams<br>- Academic researchers<br>- Technology strategists<br>- Enterprise knowledge workers<br>- Federal/regulated industries |

## Key Performance Metrics

| Metric | Value | Details |
|--------|-------|---------|
| **Processing Speed** | 500 articles in 23 min | Full pipeline: extract → analyze → synthesize |
| **Accuracy** | 95%+ relevance | AI-driven filtering with configurable thresholds |
| **Supported Formats** | 8 input / 6 output | Input: HN, arXiv, PDF, DOCX, web, APIs<br>Output: PDF, DOCX, MD, JSON, Excel, HTML |
| **Embedding Dimensions** | 1536 (cloud) / 768 (local) | OpenAI text-embedding-3-large / local models |
| **Cost Efficiency** | $0.50-$2.50 per run | User-controlled via BYOK (500-1000 stories) |
| **Memory Footprint** | 1.2 GB peak | Scales to 2,500 stories under 4 GB RAM |
| **Offline Capability** | 100% functional | Complete local processing with Ollama/local models |
| **Security** | Zero-trust architecture | Local storage, OS-level key encryption, no telemetry |

## Architecture at a Glance

```
┌─────────────────────────────────────────────────────────────────┐
│                    RESCRIBOS PLATFORM                           │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   Electron   │  │   Node.js    │  │    Python    │         │
│  │   Frontend   │◄─┤ Orchestrator │◄─┤   Pipeline   │         │
│  │              │  │              │  │              │         │
│  │ • Reports UI │  │ • Workflows  │  │ • Extraction │         │
│  │ • Search     │  │ • File I/O   │  │ • AI Analysis│         │
│  │ • Chat       │  │ • Licensing  │  │ • Embeddings │         │
│  └──────────────┘  └──────────────┘  └──────┬───────┘         │
│                                              │                 │
│  ┌───────────────────────────────────────────▼──────────────┐  │
│  │              AI PROVIDER LAYER (Hybrid)                  │  │
│  │  ┌──────────┐    ┌──────────┐    ┌─────────────┐       │  │
│  │  │  OpenAI  │    │  Ollama  │    │   Local     │       │  │
│  │  │ (Cloud)  │◄───┤ (Local)  │◄───┤  Fallback   │       │  │
│  │  │  GPT-4o  │    │ Llama3.1 │    │ Transformers│       │  │
│  │  └──────────┘    └──────────┘    └─────────────┘       │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │           DATA PERSISTENCE (100% Local)                  │  │
│  │  • JSON reports • SQLite vectors • Markdown exports      │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## The Rescribos Workflow

### Step 1: Extract
Multi-source data collection from Hacker News, arXiv, local documents, and web content with concurrent processing and smart filtering.

### Step 2: Analyze
AI-powered summarization, relevance scoring, embedding generation, and automated tagging using GPT-4o or local models.

### Step 3: Organize
ML-based clustering, hierarchical grouping, and semantic organization to identify themes and relationships.

### Step 4: Synthesize
Thematic analysis with multi-order implications, executive summaries, and comprehensive citations.

### Step 5: Query
Semantic search and interactive AI chat for natural language exploration of your intelligence reports.

## Technology Stack Summary

- **Frontend**: Electron 38.0 with modern JavaScript
- **Backend**: Node.js 18+ with IPC communication
- **Processing**: Python 3.8+ with AsyncIO
- **AI**: OpenAI GPT-4o, Ollama Llama 3.1, SentenceTransformers
- **Storage**: JSON files, SQLite vector database, Markdown exports
- **Deployment**: Desktop installers, Docker containers, CLI tools

## Next Steps

- Review the detailed [value proposition](value-proposition.md)
- Explore [system architecture](../architecture/README.md)
- Check [core capabilities](../core-capabilities/README.md)
- See [deployment options](../deployment/README.md)
