# Technology Stack

### 1.2 Technology Stack

**Frontend Technologies:**
- **Electron 38.0.0** - Cross-platform desktop framework
- **Modern JavaScript/ES6+** - Async/await, modules, fetch API
- **TypeScript 5.4.0** - Type-safe development (optional)
- **HTML5 & CSS3** - Responsive, accessible interface

**Backend Coordination:**
- **Node.js 18+** - Runtime with native fetch support
- **IPC Protocol** - Bidirectional Electron communication
- **Child Process Management** - Python script orchestration
- **File System APIs** - Atomic writes, locking, streaming

**Python Processing:**
- **Python 3.8+** - Core processing engine
- **AsyncIO** - Concurrent request handling
- **Type Hints** - Runtime validation with Pydantic/Zod

**Key Dependencies:**

*Python (25+ packages):*
```
AI/ML: openai>=1.0.0, sentence-transformers>=2.2.0, transformers>=4.21.0
Deep Learning: torch>=2.0.0 (CPU), tensorflow-cpu>=2.13.0
NLP: tiktoken, beautifulsoup4, playwright
Clustering: hdbscan, scikit-learn, scipy
Documents: python-docx, PyPDF2, PyMuPDF
Async: aiohttp, asyncio
```

*Node.js (17 production):*
```
Core: electron, openai>=4.0.0, node-fetch
Documents: docx, pdfkit
Parsing: marked, dompurify
Validation: zod
Security: node-machine-id, keytar
```
