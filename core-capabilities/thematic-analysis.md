# Thematic Analysis Engine

The thematic analysis stage assembles related stories into coherent sections, produces subtopic summaries, and generates an executive narrative with citations.

## Key Capabilities

1. **Multi-order implications** – Prompts guide the model to identify immediate impacts, downstream consequences, and long-term strategic considerations for each cluster.
2. **Dynamic taxonomy** – Sections are generated from the data itself; there is no fixed category list. Story grouping adapts to the content uncovered in each run.
3. **Hierarchical clustering** – Embedding similarity feeds clustering algorithms (HDBSCAN and agglomerative clustering) to form major themes with optional subtopics.
4. **Citation management** – Every statement references a story via footnotes. Markdown exports maintain numbered citations that link back to the source URLs.
5. **Executive synthesis** – A top-level briefing summarises the most important developments, risks, and opportunities across the analysed set.

## Processing Flow

1. Build a cosine-similarity matrix from embeddings.
2. Identify clusters and optimise distribution so sections stay balanced.
3. Generate subtopics when clusters span multiple independent narratives.
4. Run targeted prompts to produce section summaries and implications.
5. Compile an executive summary referencing the section insights.
6. Emit Markdown and JSON representations with structured citations.

## Output Structure

```markdown
# Executive Summary
Key findings with references [1], [2], ...

## Section 1: Theme Name
Section summary paragraph with citations.

### Subtopic 1.1: Specific Focus
- Story reference with short insight and link.
- Story reference with follow-up implications.

## Section 2: Another Theme
...

## References
[1] Article title — URL
[2] Article title — URL
```

## Performance Notes

- Typical run time: 5–15 minutes for 100–500 stories, depending on provider latency.
- Offline mode produces comparable structure but may require longer generation windows on lower-powered hardware.
- Thematic prompts are configurable via `config/prompt-profiles/`. Adjust or add profiles when tailoring the tone for executives, researchers, or technical teams.
