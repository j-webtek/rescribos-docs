# Provider Implementation Details

### 3.2 Provider Implementation Details

**OpenAI Integration (`src/python/openai_client.py`)**

Core implementation pattern:
```python
class OpenAIClient:
    # Initialize with user's API key (BYOK)
    # Configure model: gpt-4o, text-embedding-3-large
    # generate_completion(messages) -> response with retry logic (3 attempts)
    # Handle rate limits with exponential backoff
    # Support streaming for real-time chat
```

**Features:**
- User-provided API keys (BYOK model)
- Automatic rate limit handling (exponential backoff)
- Streaming support for real-time responses
- Token usage tracking and optimization
- Model version flexibility (GPT-4, GPT-4o, GPT-3.5-turbo)

**Ollama Integration (`src/python/ollama_client.py`)**

Core implementation pattern:
```python
class OllamaClient:
    # Connect to local Ollama server (localhost:11434)
    # is_available() -> health check for service
    # generate(prompt, system_prompt) -> local completion
    # Support models: llama3.1:8b, mistral, nomic-embed-text
```

**Features:**
- Fully local execution (no internet required)
- Zero-cost operation (no API fees)
- Support for multiple models (Llama, Mistral, etc.)
- Privacy-preserving (data never leaves machine)
- Requires ~8GB RAM for 8B parameter models

**Local Fallback Models (`src/python/local_embeddings.py`)**

Core implementation pattern:
```python
class LocalEmbeddingProvider:
    # Use SentenceTransformers: all-MiniLM-L6-v2 (384-dim)
    # Lazy load model on first use
    # encode(texts) -> numpy embeddings array
    # CPU/GPU auto-detection, batch processing
```

**Features:**
- CPU-based operation (GPU optional)
- ~200MB model download (one-time)
- 384-dimensional vectors
- TF-IDF and hash-based alternatives
- No external dependencies

### 3.3 Network-Aware Provider Selection

The `AIProviderManager` class (`src/python/ai_manager.py`) orchestrates intelligent provider selection:

**Selection Logic:**
```python
class AIProviderManager:
    def select_provider(self, task_type: str) -> AIProvider:
        """Intelligent provider selection based on context"""

        # Check network connectivity
        is_online = self.check_network()

        # Priority 1: User has OpenAI key and is online
        if is_online and self.has_openai_key():
            if self.test_openai_connection():
                return self.openai_provider

        # Priority 2: Ollama is running locally
        if self.ollama_available():
            return self.ollama_provider

        # Priority 3: Local fallback models
        if task_type == 'embedding':
            return self.local_embedding_provider
        elif task_type == 'summarization':
            return self.tfidf_summarizer
        else:
            raise NoProviderAvailableError()

    def check_network(self) -> bool:
        """Test internet connectivity"""
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=2)
            return True
        except OSError:
            return False
```

**Decision Matrix:**

| Scenario | Network | OpenAI Key | Ollama | Provider Used |
|----------|---------|------------|--------|---------------|
| Ideal | Online | Yes | N/A | OpenAI API |
| Offline | Offline | Yes | Running | Ollama |
| No Key | Online | No | Running | Ollama |
| Minimal | Offline | No | Not Running | Local Models |
| Emergency | Any | No | Not Running | TF-IDF/Hash |
