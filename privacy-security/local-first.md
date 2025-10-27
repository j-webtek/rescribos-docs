# Local-First Architecture

Rescribos keeps every artefact of the workflow on the operator’s machine unless explicitly exported.

## Storage Layout

```
<user-app-data>/ai-news-extractor/
├─ storage/
│  ├─ extracted/    # Raw story dumps
│  ├─ analyzed/     # Summaries, scores, embeddings
│  ├─ reports/      # Markdown + JSON exports
│  ├─ embeddings/   # SQLite vector index
│  └─ cart/         # Saved cart selections
├─ logs/            # Extraction, analysis, and export logs
└─ config/          # Preferences, profiles, cached settings
```

- All directories are created on first run; paths can be overridden via environment variables documented in `docs/ENVIRONMENT_REFERENCE.md`.
- Exports are generated beside the source files so teams can back them up or version them with standard tooling.

## Processing Guarantees

- Atomic file writes and `.bak` fallbacks prevent corruption.
- Pipelines append metadata (timestamps, provider names, configuration hashes) so audits can reproduce results.
- Sensitive values (API keys, prompts) never leave the local machine unless the user shares them manually.

## Benefits

| Goal | Implementation |
|------|----------------|
| Data sovereignty | No third-party storage or telemetry. |
| Portability | JSON/Markdown/SQLite formats import easily into other systems. |
| Auditability | Open Python scripts and detailed logs allow full traceability. |
| Compliance | Offline workflows support regulated and air-gapped deployments. |
