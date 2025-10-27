# Executive At-a-Glance

This page distils the Rescribos Data Refinement story into a quick reference for decision makers and onboarding teams.

## What, Why, How, Who

| **What** | **Why choose it** |
|----------|-------------------|
| Privacy-first AI news extraction and analysis for teams that need evidence-backed reporting. | 1. Maintain local control of data and credentials.<br>2. Switch between cloud and offline inference without code changes.<br>3. Collapse multi-source research into repeatable workflows.<br>4. Avoid SaaS lock-in and surprise usage charges. |

| **How it works** | **Who it serves** |
|------------------|-------------------|
| 1. Extract from Hacker News, arXiv, saved document sets, and optional custom connectors.<br>2. Analyse with GPT-5 or Ollama pipelines for summarisation, tagging, and scoring.<br>3. Organise with clustering, deduplication, and embeddings.<br>4. Publish Markdown, JSON, and PDF briefs with citations.<br>5. Explore the corpus through semantic search and chat. | Research analysts, competitive intelligence teams, innovation leads, policy researchers, and security-sensitive organisations that need on-premises tooling. |

## Operating Metrics

| Area | Typical value | Notes |
|------|---------------|-------|
| Extraction throughput | 200–400 stories in 3–5 minutes | Tuned via `MAX_STORIES`, concurrency controls, and source filters. |
| AI analysis latency | 15–25 minutes for 400 stories | Dependent on provider latency and prompt complexity. |
| Storage footprint | ~40 MB per full run | Includes extracted JSON, analysed JSON, and generated Markdown. |
| Embedding lookup | < 150 ms | SQLite vector search with cached nearest-neighbour results. |
| Offline readiness | Fully supported | Toggle in UI or set `FORCE_OFFLINE_MODE=true`. |
| Monitoring | Real-time console + structured logs | Python workers emit JSON progress events consumed by the UI and CLI. |

## Architecture Snapshot

```
[Electron UI] -> IPC -> [Node.js orchestrator] -> IPC -> [Python workers]
      │                      │                          │
  renderer views       secure credential          extraction, analysis,
  report explorer      storage (Keytar)           clustering, export
      │                      │                          │
  semantic search  <------ shared JSON protocol ------> CLI automation
```

Data remains on-device except when cloud providers are explicitly enabled. Offline mode routes inference through Ollama and transformer fallbacks.

## Stack Summary

- Electron 38 renderer with preload bridges that expose typed IPC channels.
- Node.js 18 main process for job orchestration, configuration, and secure storage.
- Python 3.8+ workers handling extraction, document processing, summarisation, and export.
- Optional Docker wrappers for headless automation and CI pipelines.
- SQLite vector store backing semantic search and chat grounding.

## Next Steps

- Review the [value proposition](value-proposition.md) for stakeholder-specific benefits.
- Dive into [system architecture](../architecture/README.md) for component responsibilities.
- See [deployment guidance](../deployment/README.md) to plan installation or packaging.
