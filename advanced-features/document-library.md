# Document Library

The Document Library provides a centralized, searchable interface for managing all processed documents in Rescribos. It features semantic search, category organization, and folder watch integration for automatic document monitoring.

## Overview

The Document Library serves as the hub for all document management operations:

- **Browse & Search**: Find documents using semantic search or category filters
- **Organize**: Auto-categorization based on content and source
- **Monitor**: Integrate with folder watches for automatic document ingestion
- **Analyze**: Preview documents and access full analysis
- **Export**: Batch operations on selected documents

## Key Features

### Semantic Search

Search documents using natural language queries:

```
"Recent papers about transformer architecture improvements"
"Regulatory compliance documents from Q3"
"Security research on adversarial AI"
```

**Search Configuration:**
- **Top K**: Number of results (1-100, default: 10)
- **Threshold**: Minimum similarity score (0.0-1.0, default: 0.3)
- **Date Filters**: Search within specific time ranges
- **Category Filters**: Limit search to specific categories

### Category Organization

Documents are automatically organized into categories:

- **Auto-categorization**: Based on content analysis
- **Custom categories**: Manual categorization available
- **Category statistics**: Document counts per category
- **Hierarchical browsing**: Navigate by category structure

### Tag Management

Multi-dimensional document organization:

- **Auto-tagging**: AI-generated tags based on content
- **Tag filtering**: Filter by multiple tags simultaneously
- **Tag cloud**: Visual representation of tag frequency
- **Tag search**: Find documents by tag keywords

### Document Preview

Quick access to document information:

- **Metadata display**: Type, size, dates, source
- **Content snippets**: Key passages and summaries
- **Analysis preview**: Quick view of AI analysis
- **Full analysis**: One-click access to complete analysis

## Folder Watch Integration

### What are Folder Watches?

Folder Watches automatically monitor specified directories for new or modified documents, processing them and adding them to the Document Library without manual intervention.

**Use Cases:**
- **Research Teams**: Auto-import papers dropped into shared folders
- **Business Intelligence**: Monitor downloads folder for reports
- **Compliance**: Track regulatory documents in designated folders
- **Content Aggregation**: Automatically process incoming documents

### Viewing Folder Watches

The Document Library sidebar displays all configured folder watches as **list-style cards**:

**Card Layout:**
```
┌────────────────────────────────────────────┐
│ 📁 Research Papers      ✓  🔄  ⚙️  🗑️    │
│                                            │
│ 📄 42    ⚠️ 0    ⏰ 60m                   │
│                                            │
│ Checked 15m ago                            │
└────────────────────────────────────────────┘
```

**Card Elements:**
- **Header**: Folder icon, name, status indicator, action buttons
- **Statistics**: File count, error count, check interval
- **Footer**: Last check timestamp

**Status Indicators:**
- ✓ (Green check) = Enabled and actively monitoring
- ⏸ (Orange pause) = Disabled or paused

**Action Buttons:**
- 🔄 **Sync** - Trigger immediate folder scan
- ⚙️ **Settings** - Modify watch configuration
- 🗑️ **Delete** - Remove folder watch

### Adding Folder Watches

**Via Document Library:**
1. Click the **"+"** button next to "FOLDER WATCHES" section
2. Browse to select the directory to monitor
3. Configure options:
   - **Folder Name**: Auto-detected or custom
   - **Check Interval**: Scan frequency (default: 60 minutes)
   - **File Types**: Extensions to monitor (PDF, DOCX, PPTX, TXT, MD)
   - **Include Subdirectories**: Recursive scanning option
4. Click **"Start Watching"**

**Supported File Types:**
- PDF - Research papers, reports, documentation
- DOCX - Word documents, proposals
- PPTX - PowerPoint presentations
- TXT - Plain text files
- MD - Markdown documents

### Folder Watch Automation

**Automatic Processing:**
1. **Detection**: Folder watch scans directory at configured interval
2. **Filtering**: Only processes new or modified files (SHA-256 hash checking)
3. **Extraction**: Text and metadata extraction
4. **Analysis**: AI analysis and summarization
5. **Categorization**: Auto-assigned to category based on folder name or content
6. **Indexing**: Document added to library with searchable embeddings

**Performance:**
- **Background Operation**: Runs silently without UI interruption
- **Smart Deduplication**: Prevents reprocessing unchanged files
- **Error Handling**: Failed files tracked separately
- **Progress Tracking**: Real-time statistics in sidebar

## Multi-Select Operations

### Selecting Documents

- **Hover to select**: Checkboxes appear on hover
- **Click checkbox**: Select/deselect individual documents
- **Cross-category selection**: Select documents from different categories
- **Selection counter**: Shows count in footer

### Bulk Actions

**Available Operations:**
- **Load Selected**: Load multiple documents for batch processing
- **Export Selected**: Export documents in various formats
- **Delete Selected**: Remove multiple documents (with confirmation)
- **Clear Selection**: Deselect all documents

## Document Storage

**Storage Structure:**
```
storage/
├── documents/
│   ├── processed/          # Analyzed documents
│   │   ├── index.json     # Document catalog
│   │   └── *.json         # Individual documents
│   ├── raw/               # Pre-analysis extracts
│   └── originals/         # Original file copies (optional)
└── embeddings/
    └── embeddings.db      # Semantic search index (SQLite or PostgreSQL)
```

**Index Management:**
- **Automatic Updates**: Refreshed on each processing run
- **Fast Lookup**: Optimized for quick document retrieval
- **Metadata Caching**: Pre-computed statistics for instant UI updates

## Integration with Other Features

### Chat Integration

Documents from the library can be added to chat context:

1. Select document(s) in library
2. Click "Add to Chat"
3. Chat context label updates to show selected documents
4. Ask questions specifically about those documents

See [Interactive AI Chat](../core-capabilities/ai-chat.md) for details on context management.

### Semantic Search

The Document Library uses the same semantic search engine as chat:

- **Shared embeddings**: Documents indexed once, searched everywhere
- **Cross-document search**: Find related content across entire library
- **Relevance ranking**: Results sorted by semantic similarity

See [Semantic Search](../core-capabilities/semantic-search.md) for technical details.

### Report Generation

Documents can be included in generated reports:

1. Select documents in library
2. Click "Generate Report"
3. Choose report format
4. Documents compiled into comprehensive report

## Configuration

**Environment Variables:**
```env
# Document Library settings
DOC_LIBRARY_MAX_PREVIEW=500  # Max preview length (words)
DOC_LIBRARY_PAGE_SIZE=50     # Documents per page
DOC_LIBRARY_CACHE_TTL=3600   # Cache duration (seconds)

# Folder Watch settings
FOLDER_WATCH_DEFAULT_INTERVAL=60  # Default scan interval (minutes)
FOLDER_WATCH_MAX_FILE_SIZE=100    # Max file size (MB)
FOLDER_WATCH_PARALLEL_SCANS=3     # Concurrent folder scans
```

## Best Practices

### Organization

- **Use descriptive folder names**: Folder watch categories match folder names
- **Hierarchical structure**: Organize watched folders by topic/project
- **Regular cleanup**: Remove outdated documents periodically

### Performance

- **Adjust scan intervals**: Reduce frequency for rarely-updated folders
- **File size limits**: Configure max file size to prevent oversized processing
- **Selective monitoring**: Only watch folders with relevant content

### Security

- **Permission management**: Ensure Rescribos has read access to watched folders
- **Sensitive content**: Use separate folders for classified/sensitive documents
- **Audit trail**: Document source tracking for compliance

## Troubleshooting

**Documents not appearing:**
- Check folder watch status (enabled/disabled)
- Verify file extensions are supported
- Check logs for processing errors
- Ensure folder permissions allow read access

**Search not finding documents:**
- Verify embeddings are generated (check `embeddings.db`)
- Lower similarity threshold for broader results
- Check if document was successfully processed
- Try exact keyword search vs. semantic search

**Folder watch not scanning:**
- Verify watch is enabled (green check icon)
- Check last scan timestamp
- Manually trigger sync using 🔄 button
- Check logs for folder access errors

## Related Documentation

- [Folder Watch User Guide](../../../FOLDER_WATCH_USER_GUIDE.md) - Complete folder watch documentation
- [Document Processing](document-processing.md) - Technical implementation details
- [Semantic Search](../core-capabilities/semantic-search.md) - Search capabilities
- [Interactive AI Chat](../core-capabilities/ai-chat.md) - Chat integration
