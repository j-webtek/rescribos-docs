# Electron Frontend

The renderer delivers the desktop experience and is implemented primarily in `src/index.html`, `src/renderer.js`, and supporting modules under `src/results/`.

## Responsibilities

- Render the report explorer, semantic search, cart UI, and chat assistant.
- Display live pipeline progress and error notifications streamed from the backend.
- Manage local UI state (layout preferences, filters) using browser storage.
- Bridge to the main process through the secure preload API defined in `src/preload.js`.

## Key Modules

| File | Description |
|------|-------------|
| `src/index.html` | Root HTML template that loads renderer bundles and modal markup. |
| `src/renderer.js` | Primary UI controller covering navigation, event handling, and IPC listeners. |
| `src/results-manager.js` | Handles report loading, cart integration, and export triggers. |
| `src/results/cart.js` | Manages cart state, modal interactions, and checkout workflows. |
| `src/prompt-settings.js` | Exposes prompt editing and saving capabilities for analysts. |
| `src/preload.js` | Whitelists IPC channels and exposes typed APIs to the renderer. |

## IPC Usage

Renderer calls look like:

```javascript
const jobId = await window.rescribos.startPipeline({
  profile: 'daily-digest',
  maxStories: 250
});

window.rescribos.onPipelineProgress(jobId, (event) => {
  updateProgressBar(event.progress);
});
```

- All IPC channels are documented in `docs/DEVELOPER_GUIDE_IPC_EVENTS.md`.
- Sensitive operations (e.g., environment access, file exports) go through dedicated preload functions to keep the renderer sandboxed.

## Testing

- Jest tests target the preload bridge and renderer utilities.
- UI regression coverage is supplemented by Playwright scripts launched via `npm run install-python` (installs the browser binaries).
