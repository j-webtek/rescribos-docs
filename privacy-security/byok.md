# Bring Your Own Keys (BYOK)

Rescribos never ships with embedded credentials. Users supply their own API keys and the application stores them securely on-device.

## Implementation

- `secure-key-manager.js` wraps Keytar and exposes async helpers for saving, retrieving, and deleting credentials.
- Keys are validated (format and connectivity) before being persisted.
- If Keytar is unavailable (e.g., some headless environments), the manager falls back to encrypted local storage with clear warnings.
- Secrets are injected into Python workers just before execution and removed from the environment once the process exits.

```javascript
await secureKeyManager.save({
  keyName: 'OPENAI_API_KEY',
  keyValue: userInput,
  metadata: { provider: 'openai', updatedAt: new Date().toISOString() }
});
```

## Operational Guidance

- Rotate keys regularly through the desktop Settings panel or by rerunning `npm run cli -- wizard` / `npm run cli -- config --set OPENAI_API_KEY=...`.
- Use separate keys for staging and production environments and manage them via profiles.
- Keep `.env` files free of credentials; rely on secure storage or environment variables injected at runtime.

## Benefits

| Benefit | Description |
|---------|-------------|
| Cost control | Users pay providers directly with no markup. |
| Transparency | API usage can be monitored in provider dashboards. |
| Compliance | Supports organisational policies that forbid shared keys. |
| Flexibility | Switch providers or accounts without reinstalls. |
