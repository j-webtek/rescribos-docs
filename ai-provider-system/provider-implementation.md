# Provider Implementation Details

Implementation specifics are captured in the Python modules under `scripts/`. This page summarises the interfaces and behaviours that consumers rely on.

## OpenAI (`scripts/providers/openai_provider.py`)

- Accepts user-supplied API keys (stored via Keytar).
- Supports text completion (`gpt-5`, `gpt-4.1`) and embeddings (`text-embedding-3-small`).
- Applies retry logic with exponential backoff and jitter.
- Tracks token usage and exposes metadata for logging.
- Streams responses to the Node.js layer when chat mode is enabled.

## Ollama (`scripts/providers/ollama_provider.py`)

- Connects to the local Ollama daemon (default `http://127.0.0.1:11434`).
- Uses models defined in the environment (commonly `llama3.1:8b` for summaries and `nomic-embed-text` for embeddings).
- Performs health checks before each run to ensure the model is loaded.
- Returns structured payloads that match the OpenAI provider interface for drop-in replacement.

## Local Embeddings (`scripts/providers/local_embeddings.py`)

- Falls back to SentenceTransformers (e.g., `all-MiniLM-L6-v2`) when no external provider is available.
- Lazily loads models to avoid unnecessary startup costs.
- Provides batched encoding methods optimised for CPU execution.

## TF-IDF Summaries (`scripts/providers/tfidf_provider.py`)

- Used as a last resort when no generative provider is available.
- Generates extractive summaries and keyword lists from the source text.
- Ensures the pipeline can still complete with reduced fidelity.

## AI Provider Manager (`scripts/ai_providers/network_aware_manager.py`)

```python
from scripts.ai_providers.network_aware_manager import network_aware_manager

async with network_aware_manager.operation_context("summary"):
    result = await network_aware_manager.generate_text_with_fallback(
        prompt_template,
        model="gpt-5",
    )
```

- Evaluates connectivity, configuration overrides, and provider health before each call.
- Allows separate providers for different task types (text vs embeddings) and automatically falls back when failures occur.
- Emits detailed log entries when falling back or encountering errors.

The decision matrix and complete API reference are available in `docs/AI_PROVIDER_SYSTEM_DOCUMENTATION.md`.
