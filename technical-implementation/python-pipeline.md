# Python Pipeline

### 7.2 Dependencies

**Python Dependencies (`requirements.txt`):**
```
# AI/ML Core
openai>=1.0.0              # OpenAI API client
sentence-transformers>=2.2.0  # Local embeddings
transformers>=4.21.0       # Hugging Face transformers
torch>=2.0.0               # PyTorch (CPU version)
tensorflow-cpu>=2.13.0     # TensorFlow (CPU only)

# NLP & Text Processing
tiktoken>=0.5.0            # OpenAI tokenization
beautifulsoup4>=4.11.0     # HTML parsing
lxml>=4.9.0                # XML/HTML parser
playwright>=1.40.0         # Browser automation
nltk>=3.8.0                # Natural language toolkit

# Clustering & Analysis
hdbscan>=0.8.29            # Hierarchical clustering
scikit-learn>=1.3.0        # ML algorithms
scipy>=1.11.0              # Scientific computing
numpy>=1.24.0              # Numerical operations
pandas>=2.0.0              # Data manipulation

# Document Processing
python-docx>=0.8.11        # Word document handling
PyPDF2>=3.0.0              # PDF text extraction
PyMuPDF>=1.23.0            # Advanced PDF processing
python-pptx>=0.6.21        # PowerPoint support

# Async & HTTP
aiohttp>=3.9.0             # Async HTTP client
httpx>=0.25.0              # HTTP client with HTTP/2
requests>=2.31.0           # Synchronous HTTP

# Data Storage
sqlite3                    # Built-in SQLite (vector DB)
pydantic>=2.0.0            # Data validation

# Utilities
python-dotenv>=1.0.0       # Environment management
tqdm>=4.66.0               # Progress bars
loguru>=0.7.0              # Advanced logging
```

**Node.js Dependencies (`package.json`):**
```json
{
  "dependencies": {
    "electron": "^38.0.0",
    "openai": "^4.0.0",
    "node-fetch": "^3.3.0",
    "docx": "^8.5.0",
    "pdfkit": "^0.14.0",
    "puppeteer": "^21.0.0",
    "marked": "^11.0.0",
    "dompurify": "^3.0.0",
    "isomorphic-dompurify": "^2.0.0",
    "zod": "^3.22.0",
    "node-machine-id": "^1.1.12",
    "keytar": "^7.9.0",
    "electron-updater": "^6.1.0",
    "commander": "^11.0.0",
    "exceljs": "^4.4.0",
    "winston": "^3.11.0",
    "dotenv": "^16.0.0"
  },
  "devDependencies": {
    "electron-builder": "^24.9.0",
    "typescript": "^5.4.0",
    "@types/node": "^20.0.0",
    "jest": "^29.7.0",
    "eslint": "^8.56.0"
  }
}
```

**Total Dependencies:**
- Python: 25 packages
- Node.js: 17 production, 5 development
- Combined size: ~2.5 GB (with ML models)
