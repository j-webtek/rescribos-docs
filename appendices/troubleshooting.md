# Appendix C: Troubleshooting

## Appendix C: Troubleshooting

**Common Issues:**

**1. OpenAI API errors:**
- Verify API key: `rescribos config get OPENAI_API_KEY`
- Check account balance at platform.openai.com
- Test connectivity: `curl https://api.openai.com/v1/models -H "Authorization: Bearer sk-..."`

**2. Ollama not connecting:**
- Check service: `curl http://localhost:11434/api/tags`
- Start service: `ollama serve`
- Verify model: `ollama list`

**3. Out of memory errors:**
- Reduce batch size: `EMBEDDING_BATCH_SIZE=50`
- Limit story count: `MAX_STORIES=250`
- Close other applications

**4. Slow performance:**
- Enable caching: `EMBEDDING_CACHE_TTL_HOURS=24`
- Reduce concurrent requests: `EXTRA_FETCH_CONCURRENCY=3`
- Use local embeddings: `OLLAMA_ENABLED=true`

---
