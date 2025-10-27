# Enterprise Compliance

Rescribos provides the controls needed to operate in regulated environments while keeping deployment flexible. The mapping below distils the authoritative information from `docs/SECURITY_ARCHITECTURE.md` and `CODE_PROTECTION_GUIDE.md`.

## Data Handling Pledge

| Rescribos will **not** | Rescribos will **always** |
|------------------------|---------------------------|
| Upload reports or embeddings to vendor infrastructure. | Store data locally in standard formats (JSON, Markdown, SQLite). |
| Track queries, chats, or extraction history. | Let users delete data by removing the storage directory. |
| Bundle shared API keys. | Rely on BYOK and OS keychains for credential storage. |

## Control Mappings

### NIST 800-53 (snapshot)

| Control | Implementation |
|---------|----------------|
| AC-2 / AC-3 | No built-in user accounts; access governed by OS permissions. |
| AU-2 / AU-9 | Extraction, analysis, and export logs stored locally with rotation. |
| IA-5 | Keytar + BYOK enforce secure credential management. |
| SC-8 / SC-13 | TLS 1.3 enforced for outbound calls; certificate pinning optional. |
| SC-28 | At-rest encryption achieved through OS mechanisms (BitLocker, FileVault). |
| SI-7 | Signed installers and integrity checks; repository is openly auditable. |

### SOC 2 (selected criteria)

| Criterion | Implementation |
|-----------|----------------|
| CC6.1 | Local-first architecture limits data exposure. |
| CC6.6 | Credentials managed via secure key storage; never transmitted to Rescribos. |
| CC7.2 | Structured logging provides operational visibility; can be forwarded to SIEM. |
| A1.2 | Offline mode and local providers maintain availability when cloud access is blocked. |

### GDPR Snapshot

| Article | Implementation |
|---------|----------------|
| 5(1)(c) – Data minimisation | Only collects configured sources; no hidden telemetry. |
| 15 / 20 – Access & portability | Data stored in readable JSON/Markdown; direct filesystem access. |
| 17 – Right to erasure | Users delete the application storage directory to remove all data. |
| 32 – Security of processing | TLS for transport and OS-level encryption at rest. |

### HIPAA Considerations

- Operate in offline mode when processing PHI to avoid sending data to external APIs.
- Pair with full-disk encryption policies to satisfy physical safeguards.
- Logs include timestamps and event types for audit controls; forward them to existing monitoring stacks if required.

### Air-Gapped Deployments

- Offline grace period for licence validation (default 30 days) removes the need for constant connectivity.
- Ollama and transformer fallbacks keep summarisation and embeddings on-device.
- Manual update and patching processes are documented in `CODE_PROTECTION_GUIDE.md`.

## Network Posture

| Destination | Purpose |
|-------------|---------|
| `api.openai.com:443` | OpenAI API (optional). |
| `*.hacker-news.firebaseio.com:443` | Hacker News extraction. |
| `export.arxiv.org:443` | arXiv API. |
| `license.rescribos.com:443` | Licence activation (configurable interval). |
| `localhost:11434` | Ollama (when using local inference). |

Disable or proxy endpoints as required; the application honours standard proxy environment variables and `.env` overrides.

## Recommended Settings for Regulated Environments

```dotenv
FORCE_OFFLINE_MODE=true
USE_LOCAL_MODELS_ONLY=true
ENABLE_TELEMETRY=false
ALLOW_INSECURE_CONNECTIONS=false
LICENSE_VALIDATION_INTERVAL_HOURS=720   # 30 days
```

Consult `docs/SECURITY_ARCHITECTURE.md` for a full walkthrough of threat modelling, mitigation strategies, and audit procedures.
