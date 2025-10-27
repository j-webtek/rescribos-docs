# Appendix A: File Path Reference

Paths are relative to the project root unless noted.

## Application Runtime

`
main.js                     # Electron entry point
preload.js                  # Secure IPC bridge
lib/workflow-manager.js     # Multi-stage job orchestration
lib/env-loader.js           # Environment/profile merging
lib/license-manager.js      # Optional licence enforcement
cli.js                      # CLI entry point (run with `npm run cli -- <command>`)
`

## Renderer Assets

`
src/index.html              # Core UI layout
src/renderer.js             # Primary renderer controller
src/results-manager.js      # Report loading and cart integration
src/results/cart.js         # Cart UI logic
src/prompt-settings.js      # Prompt configuration interface
`

## Python Pipeline

`
scripts/extractor.py        # Hacker News / arXiv extraction
scripts/analyzer.py         # Summaries, clustering, report generation
scripts/ai_providers/network_aware_manager.py  # Provider selection and fallbacks
scripts/ai_compatibility.py # Provider orchestration helpers and fallbacks
scripts/document_processor.py # Local document ingestion
scripts/cart_processor.py   # Cart to report workflow
scripts/full_context_chat.py # Chat assistant backend
`

## Configuration & Data

`
config/                     # Data sources, prompt profiles, automation presets
.rescribosrc                # Stored environment profiles for CLI usage
storage/                    # Extracted data, analysed data, reports, embeddings
logs/                       # Extraction, analysis, export, provider logs
`

## Documentation & Automation

`
docs/                       # Authoritative Markdown guides
AUTOMATION_TESTING_REPORT.md # End-to-end regression results
CODE_PROTECTION_GUIDE.md     # Secure deployment guidance
`

