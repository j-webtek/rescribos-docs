# Privacy & Security

Rescribos adopts a local-first design so teams can control data residency, credentials, and operational risk. This page summarises the approach described in `docs/SECURITY_ARCHITECTURE.md` and `CODE_PROTECTION_GUIDE.md`.

## Core Principles

1. **Data stays local** – Reports, embeddings, logs, and configuration live on the operator’s machine unless explicitly exported.
2. **Transparent processing** – Python and Node.js sources are included in the repository, enabling audits and custom reviews.
3. **Bring your own keys** – API credentials are never bundled with the application; they are supplied by the user and stored securely on-device.
4. **Minimal telemetry** – No usage analytics are collected. Network requests occur only when contacting chosen AI providers or data sources.
5. **Configurable compliance** – Features such as offline mode and air-gapped licensing support regulated environments.

## Default Storage Layout

```
<user-app-data>/ai-news-extractor/
├─ storage/        # Extracted data, analysed results, reports, embeddings
├─ logs/           # Rolling log files (setup, extraction, analysis, exports)
├─ config/         # User preferences, profiles, cached settings
└─ backups/        # Optional backups of key configuration files
```

All write operations use atomic saves to prevent corruption and leave an audit trail via timestamped files.

## Threat Mitigations

- Secrets handled by Keytar are never exposed to the renderer or written to disk.
- IPC channels enforce validation using Zod schemas before commands execute.
- Python processes strip environment variables that are not whitelisted before launching.
- The document processing pipeline sanitises file paths and enforces size and extension allowlists.

## Related Reading

- [Local-First Architecture](local-first.md)
- [Bring Your Own Keys](byok.md)
- [License Management](license-management.md)
- [Enterprise Compliance](compliance.md)
