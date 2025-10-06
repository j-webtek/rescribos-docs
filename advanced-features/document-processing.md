# Document Processing

### 6.1 Document Processing

Rescribos extends beyond web content to process **local documents** (PDF, DOCX, TXT), integrating them seamlessly into the analysis pipeline.

**Supported Formats:**
- **PDF** - Research papers, reports, books
- **DOCX** - Word documents, proposals
- **TXT** - Plain text files, notes
- **Markdown** - Documentation, blog posts

**Implementation (`src/python/document_processor.py`):**
```python
class DocumentProcessor:
    """Extract and process local documents"""

    def process_pdf(self, file_path: str) -> dict:
        """Extract text and metadata from PDF"""
        import PyPDF2
        import fitz  # PyMuPDF for better extraction

        doc = fitz.open(file_path)
        text = ""
        metadata = doc.metadata

        for page in doc:
            text += page.get_text()

        return {
            'title': metadata.get('title', os.path.basename(file_path)),
            'author': metadata.get('author', 'Unknown'),
            'content': text,
            'page_count': len(doc),
            'source': 'local_pdf',
            'file_path': file_path
        }

    def process_docx(self, file_path: str) -> dict:
        """Extract text from Word document"""
        from docx import Document

        doc = Document(file_path)
        text = '\n'.join([para.text for para in doc.paragraphs])

        # Extract metadata
        core_props = doc.core_properties

        return {
            'title': core_props.title or os.path.basename(file_path),
            'author': core_props.author or 'Unknown',
            'content': text,
            'created': core_props.created,
            'source': 'local_docx',
            'file_path': file_path
        }

    async def analyze_document(self, document: dict):
        """Apply full analysis pipeline to document"""
        # Same pipeline as web content
        summary = await self.ai_manager.summarize(document['content'])
        embedding = await self.ai_manager.generate_embedding(summary)
        tags = self.extract_tags(document['content'])

        return {
            **document,
            'summary': summary,
            'embedding': embedding,
            'tags': tags
        }
```

**Features:**
- **Automatic Format Detection:** Based on file extension
- **Metadata Extraction:** Title, author, date, page count
- **Full-Text Search:** Document content indexed
- **Same Analysis Pipeline:** Summarization, tagging, clustering
- **Citation Preservation:** Original file paths maintained

**Usage Flow:**
```
1. User uploads document(s) via UI
2. Document processor extracts text and metadata
3. Content enters standard analysis pipeline
4. Results integrated with web-sourced stories
5. Documents appear in search and chat
```
