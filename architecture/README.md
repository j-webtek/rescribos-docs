# System Architecture

The Rescribos platform follows a layered architecture that separates presentation, orchestration, and heavy processing concerns while keeping communication deterministic and auditable. This page mirrors the authoritative details in `docs/SYSTEM_ARCHITECTURE.md`.

## Layer Overview

1. **Electron renderer** – Provides the desktop UI, semantic search explorer, report viewer, and chat assistant. All communication with the backend goes through a secure preload bridge that exposes only vetted IPC channels.
2. **Node.js main process** – Orchestrates background work, coordinates configuration, manages secure credential storage via Keytar, and spawns Python workers with sanitised environment variables.
3. **Python workers** – Execute extraction, analysis, clustering, document processing, and export jobs. Workers emit structured JSON messages for progress, logging, and error reporting.
4. **AI provider adapters** – Map the analysis pipeline to OpenAI, Ollama, or transformer-based fallbacks. Provider selection is dynamic and can change mid-run if a service is unavailable.
5. **Persistence layer** – Reports, logs, embeddings, and configuration data are stored under the project’s `storage/`, `logs/`, and `config/` directories to ensure everything remains on-device.

```
[Renderer UI] --IPC--> [Node.js main] --child process--> [Python pipeline]
      │                       │                               │
  report explorer       config + secrets                 extraction, analysis,
  chat + search         job scheduling                   clustering, export
      │                       │                               │
  user actions     <---- JSON progress ---->      CLI, automation, scheduled jobs
```

## Cross-Cutting Principles

- **Local-first storage** – Reports, embeddings, and raw data remain on the user’s filesystem by default.
- **Deterministic IPC** – Renderer-to-main and main-to-Python communications use well-defined schemas documented in `docs/DEVELOPER_GUIDE_IPC_EVENTS.md`.
- **Security guardrails** – The preload script exposes whitelisted operations, command-line tools validate environment variables, and secrets never transit the renderer.
- **Recovery friendly** – Long-running operations write checkpoints and use atomic file writes so restarts can pick up without data loss.

## Related Documentation

- [Multi-Layer Design](multi-layer-design.md)
- [Technology Stack](technology-stack.md)
- [Cross-Platform Support](cross-platform.md)
- [AI Provider System](../ai-provider-system/README.md)
