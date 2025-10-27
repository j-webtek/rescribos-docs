# AI Provider System

Rescribos uses a hybrid provider strategy so teams can switch between cloud-grade models and offline inference without changing workflows. The full specification lives in `docs/AI_PROVIDER_SYSTEM_DOCUMENTATION.md`; this page highlights the essentials.

## Provider Roles

- **OpenAI (cloud)** – Default provider for summarisation and embedding generation when network access and API credits are available.
- **Ollama (local)** – Executes the same prompts using models such as `llama3.1:8b` and `nomic-embed-text`. Ideal for air-gapped or privacy-sensitive deployments.
- **Transformer fallbacks** – SentenceTransformers models offer last-resort embeddings when neither OpenAI nor Ollama is available.

## Selection Logic

1. The orchestrator checks for explicit overrides (`FORCE_OFFLINE_MODE`, `PREFERRED_PROVIDER`).
2. Connectivity and health checks run to confirm provider availability.
3. The AI manager routes summarisation and embedding calls separately, so you can mix providers (for instance, OpenAI summaries with local embeddings).
4. Failures trigger automatic fallback and emit progress events describing the switch.

## Configuration

- `.env` variables such as `OPENAI_API_KEY`, `OLLAMA_HOST`, and `FORCE_OFFLINE_MODE` dictate the default mode.
- Profiles managed in `.rescribosrc` (use `npm run cli -- profile ...`) make it easy to save different provider combinations for teams or environments.
- Override behaviour for ad-hoc runs by supplying environment variables (e.g., `FORCE_OFFLINE_MODE=true`) or loading a profile with `npm run cli -- profile default <name>`.

## Monitoring

- Provider usage and errors are logged in `logs/provider*.log`.
- The UI displays the active provider in the header; CLI output includes the provider per stage.
- Automation reports (`docs/AUTOMATION_TESTING_REPORT.md`) list reliability statistics for each provider.

Continue to learn more about the [hybrid architecture](hybrid-architecture.md) and [offline capabilities](offline-capabilities.md).
