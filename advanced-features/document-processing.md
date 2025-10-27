# Document Processing

### 6.1 Document Processing

Rescribos extends beyond web content to process **local documents** (PDF, DOCX, TXT), integrating them seamlessly into the analysis pipeline.

**Supported Formats (default):**
- **PDF** - Research papers, reports, books (via PyMuPDF with PyPDF2 fallback)
- **DOCX** - Word documents, proposals
- **TXT** - Plain text files and notes

Additional extensions can be added through configuration when creating custom workflows.

**Implementation (`scripts/document_processor.py`):**
```python
@dataclass
class DocumentProcessorConfig:
    supported_extensions: List[str] = None
    max_file_size_mb: int = 50
    max_files_per_batch: int = 100
    min_text_length: int = 10
    max_text_length: int = 50000
    chunk_size: int = 5000
    chunk_overlap: int = 200

class DocumentProcessor:
    def extract_text_from_docx(self, file_path: str) -> Tuple[str, Dict]:
        # Multiple extraction strategies (paragraphs, tables, XML fallback)
        ...

    def extract_text_from_pdf(self, file_path: str) -> Tuple[str, Dict]:
        # Uses PyMuPDF when available and falls back to PyPDF2
        ...

    def process_documents(self, paths: List[str]) -> Dict[str, List[Dict]]:
        # Deduplicates via MD5 hashes, chunks large files, and emits progress events
        ...
```

**Features:**
- **Automatic Format Detection:** Based on file extension with a configurable allowlist.
- **Metadata Extraction:** Captures author/title when available and stores file hashes for deduplication.
- **Chunking & Filtering:** Splits long documents and discards files below the relevance threshold.
- **Shared Analysis Pipeline:** Outputs feed directly into `analyzer.py` so summaries, tags, and embeddings are generated alongside web stories.
- **Citation Preservation:** Original file paths and hashes are stored for traceability.

**Usage Flow:**
```
1. Use the UI or `npm run cli -- extract-docs <paths...>` to collect documents.
2. Document processor extracts text, metadata, and hashes while emitting progress updates.
3. The resulting dataset flows into the standard analysis pipeline.
4. Results integrate with web-sourced stories for search, chat, and reporting.
```

**Key CLI flags (see `docs/cli.md` for details):**
- `--output FILE` - Custom destination for the extracted dataset.
- `--max-size MB` / `--max-files N` - Control batch size for large folders.
- `--recursive` - Walk directories to discover nested documents.
- `--include-metadata` - Preserve document metadata in the output payload.
- `--chunk-size N` and `--extensions LIST` - Tune chunking and supported file types.
