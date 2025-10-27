# Complete Workflow

The end-to-end pipeline is composed of four stages. Each stage emits structured progress events and writes intermediate artefacts to disk.

1. **Extraction**
   - Pulls from configured sources with concurrency control (`EXTRA_FETCH_CONCURRENCY`) and retry backoff.
   - Filters stories by keyword lists, age (`MAX_STORY_AGE_HOURS`), and duplicate hashes.
   - Saves raw output to `storage/extracted/`.

2. **Analysis**
   - Runs summarisation, relevance scoring, embeddings, and tagging via the active AI provider.
   - Applies deduplication thresholds and discard rules based on score and content quality.
   - Persists analysed data to `storage/analyzed/`.

3. **Organisation**
   - Groups related stories into clusters, ranks results, and prepares them for thematic synthesis.
   - Populates the cart and report builder with curated subsets.

4. **Synthesis and Export**
   - Generates Markdown and JSON reports with executive summaries, sections, and citations.
   - Optional export workers create PDF and DOCX artefacts.
   - Final reports live in `storage/reports/`.

At every step the CLI and UI receive JSON progress updates, allowing cancellation and recovery without losing checkpoints.
