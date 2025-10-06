# AI Provider System

### 3.1 Hybrid Architecture Overview

Rescribos implements a sophisticated **hybrid AI architecture** that seamlessly combines cloud-based and local AI models, providing users with unprecedented flexibility and reliability. The system automatically adapts to network conditions, user preferences, and operational requirements.

**Architecture Diagram:**
```
┌──────────────────────────────────────────────────────────────┐
│              Network-Aware AI Manager                         │
│  • Connectivity detection (online/offline)                   │
│  • Provider health monitoring                                │
│  • Automatic failover logic                                  │
│  • Performance metrics tracking                              │
└──────────────────────────────────────────────────────────────┘
                          ↓ (Provider Selection)
        ┌─────────────────┼─────────────────┐
        ↓                 ↓                  ↓
┌───────────────┐  ┌──────────────┐  ┌─────────────────┐
│  OpenAI API   │  │    Ollama    │  │  Local Models   │
│  (Primary)    │  │  (Secondary) │  │   (Fallback)    │
├───────────────┤  ├──────────────┤  ├─────────────────┤
│ • GPT-4o      │  │ • Llama 3.1  │  │ • Sentence-     │
│ • GPT-4       │  │ • Mistral    │  │   Transformers  │
│ • text-       │  │ • nomic-     │  │ • TF-IDF        │
│   embedding   │  │   embed      │  │ • Hash-based    │
│ • BYOK        │  │ • Local      │  │ • Always        │
│ • Requires    │  │   hosting    │  │   available     │
│   internet    │  │ • No API key │  │ • No network    │
└───────────────┘  └──────────────┘  └─────────────────┘
```

## Sections

- [Hybrid Architecture](hybrid-architecture.md)
- [Provider Implementation](provider-implementation.md)
- [Offline Capabilities](offline-capabilities.md)
