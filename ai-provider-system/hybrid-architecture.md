# Hybrid Architecture

The AI manager orchestrates multiple providers so the pipeline can balance quality, latency, and privacy.

## Control Flow

1. **Connectivity check** – Detects whether outbound network calls are possible. When offline, the manager immediately selects the local stack.
2. **Provider health probes** – Lightweight requests confirm that OpenAI and Ollama are reachable before they are assigned to a job.
3. **Task routing** – Summaries and embeddings can be split across providers. For example, keep embeddings local while using GPT-5 for narrative quality.
4. **Fallbacks** – Transient errors trigger retries; repeated failures switch to the next available provider with detailed log entries.

## Why It Matters

- **Cost control** – Use OpenAI only when necessary; run exploratory or internal-only work through local models.
- **Resilience** – Avoid downtime when APIs are rate limited or when working from restricted networks.
- **Compliance** – Route sensitive workloads through offline providers to keep data within regulated boundaries.

The implementation sits in `scripts/ai_providers/network_aware_manager.py` and the provider modules. Each provider exposes a consistent interface (`summarize`, `embed`, `healthcheck`), making it straightforward to add new backends.
