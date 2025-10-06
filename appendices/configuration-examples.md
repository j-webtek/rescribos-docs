# Appendix B: Configuration Examples

## Appendix B: Configuration Examples

**Research Use Case:**
```env
# Optimized for academic research
FILTER_KEYWORDS=machine learning,deep learning,neural networks,AI,transformers
ARXIV_CATEGORIES=cs.AI,cs.LG,cs.CL,stat.ML
MAX_STORY_AGE_HOURS=168
USE_GPT41_AI_SCREENING=true
RELEVANCE_THRESHOLD=0.7
THEMATIC_ENABLED=true
IMPLICATION_DEPTH=3
```

**Competitive Intelligence:**
```env
# Track specific companies/products
FILTER_KEYWORDS=CompanyA,CompanyB,ProductX,IndustryTrend
USE_GPT41_AI_SCREENING=true
RELEVANCE_THRESHOLD=0.8
CHAT_ENABLED=true
EXPORT_PDF_ENABLED=true
```

**Offline Operation:**
```env
# Fully local operation with Ollama
FORCE_OFFLINE_MODE=true
OLLAMA_ENABLED=true
OLLAMA_MODEL=llama3.1:8b
LOCAL_EMBED_MODEL=all-MiniLM-L6-v2
```

---
