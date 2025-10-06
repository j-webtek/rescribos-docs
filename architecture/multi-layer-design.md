# Multi-Layer Design

### 1.1 Multi-Layer Design

Rescribos employs a sophisticated multi-layer architecture that separates concerns while maintaining tight integration:

```
┌─────────────────────────────────────────────────────┐
│           Electron Frontend Layer                   │
│  • Rich interactive UI (HTML5/JavaScript)          │
│  • Advanced virtual rendering for large datasets   │
│  • Real-time progress tracking                     │
│  • Multi-tab interface (reports, chat, search)     │
└─────────────────────────────────────────────────────┘
                        ↕ IPC
┌─────────────────────────────────────────────────────┐
│        Node.js Orchestration Layer                  │
│  • Workflow coordination and state management      │
│  • File system operations with atomic writes       │
│  • License validation and activation tracking      │
│  • Performance monitoring and metrics              │
│  • Error recovery and retry mechanisms             │
└─────────────────────────────────────────────────────┘
                        ↕ Child Process
┌─────────────────────────────────────────────────────┐
│         Python Processing Pipeline                  │
│  • Async data extraction (10+ sources)            │
│  • AI-powered analysis and summarization           │
│  • ML-based clustering and categorization          │
│  • Embedding generation and similarity search      │
│  • Natural language chat interface                 │
└─────────────────────────────────────────────────────┘
                        ↕ API/Local
┌─────────────────────────────────────────────────────┐
│              AI Provider Layer                      │
│  • OpenAI (GPT-4o, text-embedding-3-large)        │
│  • Ollama (Llama 3.1:8b, nomic-embed-text)        │
│  • Local Models (SentenceTransformers)             │
│  • Automatic fallback and provider selection       │
└─────────────────────────────────────────────────────┘
                        ↕
┌─────────────────────────────────────────────────────┐
│            Data Persistence Layer                   │
│  • JSON reports (structured, versioned)            │
│  • SQLite vector database (embeddings.db)          │
│  • Markdown summaries (human-readable)             │
│  • Local file system storage                       │
└─────────────────────────────────────────────────────┘
```
