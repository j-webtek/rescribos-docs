# Privacy & Security

### 4.1 Local-First Architecture

Rescribos is built on a **privacy-first, local-first** philosophy that gives users complete control over their data:

**Core Principles:**
1. **Data Sovereignty** - All data stored locally on user's machine
2. **No Vendor Lock-in** - Standard formats (JSON, Markdown, SQLite)
3. **Transparent Processing** - Open Python scripts, auditable code
4. **User-Controlled Keys** - BYOK model for API access
5. **Minimal Telemetry** - Zero tracking in offline mode

**Data Storage Locations:**
```
C:\Users\[User]\AppData\Roaming\ai-news-extractor\
├── storage/
│   ├── reports/                    # All generated reports
│   │   ├── report_[timestamp].json
│   │   └── report_[timestamp].md
│   ├── rejected/                   # Filtered-out stories
│   │   └── error_stories.jsonl
│   ├── embeddings.db               # SQLite vector database
│   └── cart/                       # User-saved items
│       └── cart_[id].json
├── logs/                           # Application logs
│   ├── extraction_[date].log
│   └── error_[date].log
└── config/                         # User preferences
    └── settings.json
```

**Data Flow:**
```
External Sources → Local Extraction → Local Storage → Local Analysis → Local Database
       ↓                  ↓                  ↓                ↓               ↓
  (Internet)        (Disk Write)       (JSON/MD)     (Python/Node)      (SQLite)
       ↓                  ↓                  ↓                ↓               ↓
  Encrypted          Atomic I/O         Standard       Open Source       No Cloud
  Transport                             Formats
```

## Sections

- [Local-First Architecture](local-first.md)
- [Bring Your Own Keys (BYOK)](byok.md)
- [License Management](license-management.md)
- [Enterprise Compliance](compliance.md)
