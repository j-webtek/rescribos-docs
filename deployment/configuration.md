# Configuration & Automation

## Environment Management

- `.env.example` lists every supported variable. Copy it to `.env` and adjust as needed.
- Profiles stored in `.rescribosrc` override subsets of variables for specific workflows (for example, offline mode or staging credentials).
- Inspect or edit values via the CLI:

```bash
npm run cli -- config --show
npm run cli -- config --set MAX_STORIES=250
npm run cli -- profile list
npm run cli -- profile default offline
```

- Configuration is merged in this order: Configuration is merged in this order: CLI overrides -> selected profile -> `.env.local` -> `.env`..

## CLI Highlights

```bash
# Extract + analyse + thematic report
npm run cli -- extract --max-stories 200
npm run cli -- analyze --date 2025-10-10
npm run cli -- thematic

# Extract only
npm run cli -- extract --sources hackernews,arxiv --max-stories 150

# Analyse a saved dataset
npm run cli -- analyze --file ./storage/extracted/documents_20251010.json

# Export to PDF
npm run cli -- export-pdf storage/reports/ai_report_2025-10-10.json --output ./exports/weekly.pdf

# Search across analysed stories
npm run cli -- search "foundation model licensing" --limit 15
```

See `docs/cli.md` for the full command reference.

## Scheduling Examples

- **Cron (Linux/macOS)**

```
0 7 * * 1-5 cd /opt/ai-news-extractor && \
  npm run cli -- extract --max-stories 200 && \
  npm run cli -- analyze --date $(date +\%Y-\%m-\%d) && \
  npm run cli -- export-pdf storage/reports/ai_report_$(date +\%Y-\%m-\%d).json \
    --output /reports/daily.pdf
```

- **Windows Task Scheduler**
  - Action: `powershell.exe`
  - Arguments: `-Command "cd C:\ai-news-extractor; npm run cli -- extract --sources hackernews; npm run cli -- analyze --date (Get-Date -Format yyyy-MM-dd); npm run cli -- export-pdf storage/reports/ai_report_((Get-Date).ToString('yyyy-MM-dd')).json --output C:\reports\daily.pdf"`

- **GitHub Actions (headless)**

```yaml
name: Daily Digest

on:
  schedule:
    - cron: '0 9 * * *'

jobs:
  digest:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '18'
      - name: Install dependencies
        run: |
          npm install
          npm run install-python
      - name: Generate report
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: |
          npm run cli -- extract --max-stories 150
          npm run cli -- analyze --date $(date +%Y-%m-%d)
          npm run cli -- export-pdf storage/reports/ai_report_$(date +%Y-%m-%d).json --output ./reports/daily.pdf
      - uses: actions/upload-artifact@v4
        with:
          name: daily-report
          path: reports/
```

## Monitoring & Logs

- Logs live under `logs/` (e.g., `extraction-*.log`, `analysis-*.log`, `provider-*.log`).
- Tail logs with your preferred shell command (`tail -f logs/extraction-*.log` or `Get-Content -Wait`).
- Automation results in `AUTOMATION_TESTING_REPORT.md` provide sample timings and failure signatures to monitor.
