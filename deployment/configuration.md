# Configuration

### 9.3 CLI Usage

**Installation:**
```bash
# Global installation
npm install -g rescribos-cli

# Verify installation
rescribos --version
# Output: 2.0.0

# View help
rescribos --help
```

**Common Commands:**
```bash
# Initialize configuration
rescribos init

# Configure OpenAI key
rescribos config set OPENAI_API_KEY sk-...

# Run full pipeline
rescribos run --sources hackernews,arxiv --keywords "AI,machine learning"

# Extract only
rescribos extract --sources hackernews --max-stories 100

# Analyze existing data
rescribos analyze --input ./data/raw_stories.json --model gpt-4o

# Generate thematic report
rescribos thematic --report report_20250115

# Search
rescribos search "quantum computing" --limit 10

# Export
rescribos export --report latest --format pdf --output report.pdf

# List reports
rescribos list --sort date --limit 20

# Chat mode (interactive)
rescribos chat --report report_20250115

# Delete old reports
rescribos clean --older-than 30d
```

**Scheduled Execution (Cron):**
```bash
# Edit crontab
crontab -e

# Add daily extraction at 9 AM
0 9 * * * cd /home/user/rescribos && rescribos run --sources hackernews >> logs/daily.log 2>&1

# Weekly full analysis on Sunday at midnight
0 0 * * 0 cd /home/user/rescribos && rescribos run --sources hackernews,arxiv --thematic >> logs/weekly.log 2>&1
```

**CI/CD Integration (GitHub Actions):**
```yaml
name: Daily Research Digest

on:
  schedule:
    - cron: '0 9 * * *'  # 9 AM daily

jobs:
  generate-digest:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install Rescribos
        run: npm install -g rescribos-cli

      - name: Run extraction and analysis
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: |
          rescribos run \
            --sources hackernews,arxiv \
            --keywords "AI,machine learning,LLM" \
            --output ./reports/

      - name: Upload report artifact
        uses: actions/upload-artifact@v3
        with:
          name: daily-digest
          path: ./reports/latest.pdf
```
