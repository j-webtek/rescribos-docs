# Report Management and Exports

### 6.3 Report Management and Exports

**Report Manager (`src/electron/reportManager.js`):**
```javascript
class ReportManager {
    async exportReport(reportId, format) {
        const report = await this.loadReport(reportId);

        switch (format) {
            case 'pdf':
                return await this.exportToPDF(report);
            case 'docx':
                return await this.exportToWord(report);
            case 'md':
                return await this.exportToMarkdown(report);
            case 'json':
                return await this.exportToJSON(report);
            case 'xlsx':
                return await this.exportToExcel(report);
            default:
                throw new Error(`Unsupported format: ${format}`);
        }
    }

    async exportToPDF(report) {
        const marked = require('marked');
        const puppeteer = require('puppeteer');

        // Convert markdown to HTML
        const html = this.generateHTML(report);

        // Launch headless browser
        const browser = await puppeteer.launch();
        const page = await browser.newPage();

        await page.setContent(html, { waitUntil: 'networkidle0' });

        // Generate PDF with professional formatting
        const pdf = await page.pdf({
            format: 'A4',
            margin: {
                top: '20mm',
                right: '15mm',
                bottom: '20mm',
                left: '15mm'
            },
            displayHeaderFooter: true,
            headerTemplate: `
                <div style="font-size:10px; width:100%; text-align:center;">
                    Rescribos Report - ${report.generated_at}
                </div>
            `,
            footerTemplate: `
                <div style="font-size:10px; width:100%; text-align:center;">
                    Page <span class="pageNumber"></span> of <span class="totalPages"></span>
                </div>
            `,
            printBackground: true
        });

        await browser.close();
        return pdf;
    }

    async exportToWord(report) {
        const { Document, Paragraph, TextRun, HeadingLevel } = require('docx');

        const doc = new Document({
            sections: [{
                properties: {},
                children: this.convertReportToWordElements(report)
            }]
        });

        const buffer = await Packer.toBuffer(doc);
        return buffer;
    }
}
```

**Export Formats:**

| Format | Use Case | Features |
|--------|----------|----------|
| PDF | Distribution, archival | Professional layout, TOC, headers/footers |
| DOCX | Editing, collaboration | Editable, style preservation |
| Markdown | Note-taking apps | Obsidian, Notion, GitHub compatible |
| JSON | Programmatic access | Full data structure, embeddings |
| Excel | Data analysis | Filterable, sortable, pivot tables |

**Batch Operations:**
```javascript
// Export multiple reports at once
await reportManager.batchExport({
    reportIds: ['report_1', 'report_2', 'report_3'],
    format: 'pdf',
    outputDir: 'C:/exports/',
    combine: true  // Merge into single file
});
```

## CLI Tool

### 6.4 CLI Tool

Rescribos includes a **command-line interface** for automation and scripting:

**Implementation (`src/cli/rescribos-cli.js`):**
```javascript
#!/usr/bin/env node

const { Command } = require('commander');
const program = new Command();

program
    .name('rescribos')
    .description('Rescribos CLI - AI-Powered Knowledge Management')
    .version('2.0.0');

program
    .command('extract')
    .description('Extract and analyze content from sources')
    .option('-s, --sources <sources>', 'Comma-separated list (hackernews,arxiv)')
    .option('-k, --keywords <keywords>', 'Filter keywords')
    .option('-o, --output <file>', 'Output file path')
    .action(async (options) => {
        const extractor = new ContentExtractor(options);
        const report = await extractor.run();
        console.log(`Report generated: ${report.path}`);
    });

program
    .command('analyze')
    .description('Analyze existing data file')
    .requiredOption('-i, --input <file>', 'Input JSON file')
    .option('-m, --model <model>', 'AI model (gpt-4o, llama3.1)', 'gpt-4o')
    .action(async (options) => {
        const analyzer = new ContentAnalyzer(options);
        await analyzer.run();
    });

program
    .command('search')
    .description('Search across all reports')
    .requiredOption('-q, --query <query>', 'Search query')
    .option('-n, --limit <number>', 'Number of results', '10')
    .action(async (options) => {
        const searcher = new SemanticSearcher();
        const results = await searcher.search(options.query, options.limit);
        console.table(results);
    });

program
    .command('export')
    .description('Export report to various formats')
    .requiredOption('-r, --report <id>', 'Report ID')
    .requiredOption('-f, --format <format>', 'Output format (pdf,docx,md)')
    .option('-o, --output <file>', 'Output file path')
    .action(async (options) => {
        const exporter = new ReportExporter();
        await exporter.export(options);
    });

program.parse();
```

**CLI Usage Examples:**
```bash
# Extract and analyze tech news
rescribos extract --sources hackernews,arxiv --keywords "AI,LLM,machine learning"

# Analyze local documents
rescribos analyze --input ./research_papers/*.pdf --model llama3.1

# Search across reports
rescribos search --query "quantum computing breakthroughs" --limit 20

# Export report to PDF
rescribos export --report report_20250115 --format pdf --output ./report.pdf

# Generate thematic report from cart
rescribos generate --cart research_ai --output ./ai_trends.md

# List all reports
rescribos list --sort date --filter "last 7 days"
```

**Automation Integration:**
```bash
# Cron job: Daily AI news digest
0 9 * * * rescribos extract --sources hackernews --keywords "AI,GPT" && \
          rescribos export --report latest --format pdf --output ~/daily_digest.pdf
```

## Docker Support

### 6.5 Docker Support

Rescribos can run in containerized environments for server deployments:

**Dockerfile (`docker/Dockerfile`):**
```dockerfile
FROM node:18-bullseye

# Install Python and dependencies
RUN apt-get update && apt-get install -y \
    python3.9 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy application files
COPY package*.json ./
COPY src/ ./src/
COPY requirements.txt ./

# Install Node.js dependencies
RUN npm ci --production

# Install Python dependencies
RUN pip3 install -r requirements.txt

# Create data directory
RUN mkdir -p /data/storage

# Set environment variables
ENV NODE_ENV=production
ENV DATA_DIR=/data/storage

# Expose port (if running web interface)
EXPOSE 3000

# Run CLI or server
CMD ["node", "src/cli/rescribos-cli.js"]
```

**Docker Compose (`docker-compose.yml`):**
```yaml
version: '3.8'

services:
  rescribos:
    build: .
    container_name: rescribos
    volumes:
      - ./data:/data/storage
      - ./config:/app/config
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - OLLAMA_BASE_URL=http://ollama:11434
    depends_on:
      - ollama
    command: ["node", "src/server/index.js"]

  ollama:
    image: ollama/ollama:latest
    container_name: ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama-data:/root/.ollama

volumes:
  ollama-data:
```

**Usage:**
```bash
# Build and run
docker-compose up -d

# Extract content
docker-compose exec rescribos rescribos extract --sources hackernews

# View logs
docker-compose logs -f rescribos

# Stop services
docker-compose down
```
