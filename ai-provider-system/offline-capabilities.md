# Offline Capabilities

Rescribos is designed to keep the core analysis workflow running even when no outbound network connection is available.

## What Works Offline

- **Analysis pipeline** – Summaries, tagging, and clustering via Ollama or TF-IDF fallbacks.
- **Embeddings and search** – Local embeddings feed the same SQLite vector index used online.
- **Chat assistant** – Runs against the analysed dataset using the selected offline model.
- **Exports** – Markdown, PDF, DOCX, XLSX output continue to function.
- **Automation** – CLI commands and scheduled scripts work with local providers.

## What Requires Connectivity

- **Source extraction** – Fetching from Hacker News, arXiv, and other online feeds demands internet access. You can still analyse previously extracted datasets or local documents.
- **OpenAI usage** – Any call that depends on GPT-5 or OpenAI embeddings needs network access and valid credentials.

## Configuration

```dotenv
FORCE_OFFLINE_MODE=true
OLLAMA_HOST=http://127.0.0.1:11434
OLLAMA_SUMMARY_MODEL=llama3.1:8b
OLLAMA_EMBED_MODEL=nomic-embed-text
LOCAL_EMBED_MODEL=all-MiniLM-L6-v2
```

- Use `scripts/setup-ollama.ps1` or `.sh` to install models ahead of time.
- Profiles can pin offline settings so team members inherit the same configuration.

## Performance Notes

| Operation | GPT-5 (cloud) | Ollama Llama 3.1 | Local TF-IDF |
|-----------|----------------|------------------|--------------|
| Summary latency | ~3 s/story | 4–7 s/story (depends on hardware) | < 1 s/story |
| Embedding latency | < 1 s/100 stories | ~2 s/100 stories | ~4 s/100 stories |
| Cost | Billed per token | Free (local compute) | Free |
| Fidelity | Highest | High with tuned prompts | Extractive only |

Offline runs still emit the same progress events and logs, making it easy to mix offline and online workflows in automation pipelines.
