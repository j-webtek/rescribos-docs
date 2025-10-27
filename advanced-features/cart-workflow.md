# Cart Workflow

The cart system lets analysts curate subsets of stories for focused analysis or reusable briefs.

## Where It Lives

- UI logic: `src/results/cart.js`, `src/results-manager.js`, and supporting markup in `src/index.html`.
- Persistence: selections are stored in `localStorage` and mirrored to JSON files under `storage/cart/` when processed.
- Backend: `scripts/cart_manager.py` and `scripts/cart_processor.py` handle saving carts and generating dedicated reports.

## Workflow

1. **Collect stories** – Add items from the report explorer, search results, or automation outputs.
2. **Review & annotate** – Use the cart modal to reorder stories, add notes, and preview the resulting brief.
3. **Generate report** – Trigger the cart analysis, which reuses the Python pipeline to create Markdown/JSON outputs scoped to the selected stories.
4. **Export** – Download PDF, DOCX, Markdown, or JSON versions, or feed the cart into scheduled CLI runs.

## CLI Integration

```bash
# Process a saved cart into a bespoke brief
npm run cli -- cart-process ./storage/cart/ai-weekly.json --instructions "Highlight funding signals" --tone technical --audience "AI researchers"

# Re-analyse an exported cart file directly
npm run cli -- analyze --file ./storage/cart/ai-weekly.json
```

Key options for `cart-process`:
- `--instructions` – Additional guidance for the summariser.
- `--important` – Must-cover talking points emphasised in the brief.
- `--tone` and `--audience` – Tailor the narrative for stakeholders.

## Tips

- Maintain multiple carts for recurring deliverables (e.g., weekly digest, competitor watch).
- Version-control exported cart JSON to track how coverage evolves over time.
- Pair carts with prompt profiles to tailor tone and depth for different audiences.
