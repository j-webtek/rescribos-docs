# Technical Implementation

### 7.1 Code Statistics

**Project Overview:**
```
Language                Files        Lines         Code     Comments       Blanks
─────────────────────────────────────────────────────────────────────────────────
JavaScript                 42        12,847       10,234        1,205        1,408
Python                     28        18,562       14,892        2,108        1,562
TypeScript                  8         3,421        2,845          312          264
JSON                       12         1,847        1,847            0            0
Markdown                    6         2,105            0        1,842          263
YAML                        4           342          298           22           22
Dockerfile                  2            98           72           18            8
Shell                       3           267          198           35           34
─────────────────────────────────────────────────────────────────────────────────
Total                     105        39,489       30,386        5,542        3,561
```

**Source Code Distribution:**
```
src/
├── electron/              # Electron main process (Node.js)
│   ├── main.js           # 847 lines - Application entry point
│   ├── ipcHandlers.js    # 1,234 lines - IPC communication
│   ├── licenseManager.js # 423 lines - License validation
│   ├── keyManagement.js  # 198 lines - Secure key storage
│   └── reportManager.js  # 567 lines - Report operations
│
├── renderer/              # Electron renderer process (frontend)
│   ├── index.html        # 342 lines - Main UI structure
│   ├── app.js            # 2,156 lines - UI logic and interactions
│   ├── search.js         # 678 lines - Search interface
│   ├── chat.js           # 892 lines - Chat UI and streaming
│   └── styles.css        # 1,234 lines - Application styling
│
├── python/                # Python processing pipeline
│   ├── extract.py        # 1,847 lines - Multi-source extraction
│   ├── analyze.py        # 2,341 lines - AI analysis pipeline
│   ├── organize.py       # 1,156 lines - Clustering and organization
│   ├── thematic.py       # 3,421 lines - Thematic analysis engine
│   ├── chat.py           # 892 lines - Interactive chat system
│   ├── search.py         # 567 lines - Vector search
│   ├── embeddings.py     # 743 lines - Embedding generation
│   ├── ai_manager.py     # 1,234 lines - AI provider orchestration
│   ├── openai_client.py  # 456 lines - OpenAI integration
│   ├── ollama_client.py  # 378 lines - Ollama integration
│   └── local_models.py   # 289 lines - Local fallback models
│
├── cli/                   # Command-line interface
│   └── rescribos-cli.js  # 892 lines - CLI implementation
│
└── shared/                # Shared utilities
    ├── config.js         # 234 lines - Configuration management
    ├── logger.js         # 156 lines - Logging system
    └── utils.py          # 421 lines - Python utilities
```

**Test Coverage:**
```
tests/
├── unit/                  # 34 test files
│   ├── test_extract.py   # 456 lines
│   ├── test_analyze.py   # 623 lines
│   └── test_ai_manager.py # 389 lines
│
└── integration/           # 12 test files
    ├── test_pipeline.py  # 892 lines
    └── test_exports.py   # 567 lines

Total Test Lines: 4,567
Code Coverage: 78%
```

## Sections

- [Electron Frontend](electron-frontend.md)
- [Node.js Backend](nodejs-backend.md)
- [Python Pipeline](python-pipeline.md)
