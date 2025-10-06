# Offline Capabilities

### 3.4 Offline Capabilities

Rescribos maintains full functionality even without internet connectivity:

**Offline Features:**
- **Data Extraction:** Disabled (requires network sources)
- **Analysis:** Enabled via Ollama or local models
- **Summarization:** Enabled (Ollama or extractive summarization)
- **Embeddings:** Enabled (SentenceTransformers)
- **Search:** Enabled (local vector database)
- **Chat:** Enabled (Ollama required)
- **Export:** Enabled (all formats)

**Offline Configuration:**
```env
# Force offline mode
FORCE_OFFLINE_MODE=true

# Ollama settings
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b
OLLAMA_EMBED_MODEL=nomic-embed-text

# Local embedding fallback
LOCAL_EMBED_MODEL=all-MiniLM-L6-v2
LOCAL_EMBED_DEVICE=cpu
```

**Performance Comparison:**

| Operation | OpenAI (Online) | Ollama (Offline) | Local (Offline) |
|
