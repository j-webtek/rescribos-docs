# Enterprise Compliance

### 4.4 Data Privacy Guarantees

**What Rescribos NEVER Does:**
- ✗ Upload your reports to cloud storage
- ✗ Transmit your research data to Rescribos servers
- ✗ Track your queries or searches
- ✗ Collect analytics on document content
- ✗ Share data with third parties
- ✗ Require account creation or login
- ✗ Store API keys on remote servers

**What Rescribos DOES:**
- ✓ Store 100% of data locally
- ✓ Use your own AI provider credentials
- ✓ Allow complete offline operation
- ✓ Provide full export capabilities
- ✓ Use standard, open formats
- ✓ Enable data deletion anytime
- ✓ Respect user privacy completely

**Compliance Features:**
- **GDPR Compliant:** Data stays on user's machine
- **HIPAA Compatible:** No cloud transmission (when offline)
- **SOC 2 Ready:** Audit logs available
- **Zero Trust:** No server-side data storage
- **Right to Delete:** Full data ownership

### 4.5 Enterprise Compliance Mapping

Rescribos architecture natively aligns with major regulatory frameworks and security standards, making it suitable for federal, healthcare, financial, and enterprise deployments.

#### NIST 800-53 Control Mapping

| NIST Control | Control Family | Rescribos Implementation |
|--------------|----------------|--------------------------|
| **AC-2** | Account Management | Hardware-based licensing with machine ID binding; no user accounts required |
| **AC-3** | Access Enforcement | OS-level keychain for API credentials; local file system permissions |
| **AC-6** | Least Privilege | Application runs in user context; no elevated privileges required |
| **AU-2** | Audit Events | Comprehensive logging (extraction, analysis, errors) in `logs/` directory |
| **AU-9** | Protection of Audit Info | Local log storage with file system access controls; rotation available |
| **CM-2** | Baseline Configuration | Version-controlled settings.json; documented default configurations |
| **CM-7** | Least Functionality | Minimal dependencies; optional AI providers; disable unused sources |
| **IA-5** | Authenticator Management | BYOK model; user-controlled API keys in OS keychain with encryption |
| **SC-8** | Transmission Confidentiality | TLS 1.3 for all external API calls; certificate validation enforced |
| **SC-13** | Cryptographic Protection | OS-native credential storage (DPAPI/Keychain); SHA-256 hashing |
| **SC-28** | Protection of Info at Rest | Local file system encryption (BitLocker/FileVault compatible) |
| **SI-7** | Software Integrity | Signed installers (Windows/macOS); code signing for updates |
| **SI-10** | Information Input Validation | Input sanitization in Python pipeline; Zod validation in Node.js |

#### SOC 2 Trust Service Criteria Mapping

| TSC Category | Criterion | Rescribos Implementation |
|--------------|-----------|--------------------------|
| **CC6.1** | Logical Access - Boundaries | Local-first architecture; no remote access to user data |
| **CC6.6** | Logical Access - Credentials | BYOK with OS keychain; keys never transmitted to Rescribos servers |
| **CC6.7** | Logical Access - Restriction | License-based access control; hardware ID binding |
| **CC7.2** | System Operations - Detection | Application and error logs; structured JSON logging format |
| **CC7.3** | System Operations - Evaluation | Self-contained monitoring; exportable logs for SIEM integration |
| **A1.2** | Availability - Resilience | Offline capability; automatic fallback to local AI models |

#### GDPR Requirements Compliance

| GDPR Article | Requirement | Rescribos Implementation |
|--------------|-------------|--------------------------|
| **Art. 5(1)(a)** | Lawfulness, fairness, transparency | Open-source processing scripts; auditable Python code |
| **Art. 5(1)(c)** | Data minimization | Only collects public data; no PII collection or storage |
| **Art. 5(1)(e)** | Storage limitation | User-controlled retention; manual deletion of reports anytime |
| **Art. 5(1)(f)** | Integrity and confidentiality | Local storage only; TLS for API calls; OS-level encryption |
| **Art. 15** | Right of access | Direct file system access to all data (JSON/Markdown/SQLite) |
| **Art. 16** | Right to rectification | Users can edit reports manually; full control over local data |
| **Art. 17** | Right to erasure | Delete `AppData/Roaming/ai-news-extractor` directory anytime |
| **Art. 20** | Right to data portability | Standard formats (JSON, Markdown, Excel, PDF); easy export |
| **Art. 25** | Data protection by design | Privacy-first architecture; local-first philosophy from inception |
| **Art. 32** | Security of processing | Encryption in transit (TLS 1.3); at-rest encryption via OS |

#### HIPAA Compliance Considerations

| HIPAA Requirement | Implementation Guidance |
|-------------------|-------------------------|
| **Administrative Safeguards** | Use in offline mode; document security policies for organizational deployment |
| **Physical Safeguards** | Desktop application inherits device physical security controls |
| **Technical Safeguards** | Encryption in transit (TLS 1.3); local storage with disk encryption |
| **Access Control** | Machine-specific licensing; no multi-user access without OS controls |
| **Audit Controls** | Comprehensive logging to `logs/` directory; timestamp all operations |
| **Integrity Controls** | File-based storage with atomic writes; version control for reports |
| **Transmission Security** | TLS 1.3 mandatory; certificate validation; no insecure fallback |

**Note for HIPAA Users:** When processing Protected Health Information (PHI), operate Rescribos in **fully offline mode** using local AI models (Ollama) to avoid transmitting data to third-party APIs. Configure `USE_LOCAL_MODELS_ONLY=true` in environment settings.

#### Federal & Air-Gapped Deployment

**FedRAMP Considerations:**
- Deploy in **offline mode** with local models for IL-2+ environments
- Hardware-based licensing (no cloud callback with offline grace period)
- Auditable open-source codebase for security review
- Standard installation packages (no containers required)

**Air-Gap Compatibility:**
- Full functionality with Ollama or local embedding models
- No internet requirement after initial installation
- License validation: 30-day offline grace period
- Manual license transfer protocol available for classified environments

**Recommended Configuration for Federal Use:**
```env
USE_LOCAL_MODELS_ONLY=true
OLLAMA_MODEL=llama3.1:8b
OLLAMA_EMBED_MODEL=nomic-embed-text
ENABLE_TELEMETRY=false
OFFLINE_MODE=true
LICENSE_OFFLINE_GRACE_DAYS=30
```

### 4.5 Enterprise Compliance Mapping

Rescribos architecture natively aligns with major regulatory frameworks and security standards, making it suitable for federal, healthcare, financial, and enterprise deployments.

#### NIST 800-53 Control Mapping

| NIST Control | Control Family | Rescribos Implementation |
|--------------|----------------|--------------------------|
| **AC-2** | Account Management | Hardware-based licensing with machine ID binding; no user accounts required |
| **AC-3** | Access Enforcement | OS-level keychain for API credentials; local file system permissions |
| **AC-6** | Least Privilege | Application runs in user context; no elevated privileges required |
| **AU-2** | Audit Events | Comprehensive logging (extraction, analysis, errors) in `logs/` directory |
| **AU-9** | Protection of Audit Info | Local log storage with file system access controls; rotation available |
| **CM-2** | Baseline Configuration | Version-controlled settings.json; documented default configurations |
| **CM-7** | Least Functionality | Minimal dependencies; optional AI providers; disable unused sources |
| **IA-5** | Authenticator Management | BYOK model; user-controlled API keys in OS keychain with encryption |
| **SC-8** | Transmission Confidentiality | TLS 1.3 for all external API calls; certificate validation enforced |
| **SC-13** | Cryptographic Protection | OS-native credential storage (DPAPI/Keychain); SHA-256 hashing |
| **SC-28** | Protection of Info at Rest | Local file system encryption (BitLocker/FileVault compatible) |
| **SI-7** | Software Integrity | Signed installers (Windows/macOS); code signing for updates |
| **SI-10** | Information Input Validation | Input sanitization in Python pipeline; Zod validation in Node.js |

#### SOC 2 Trust Service Criteria Mapping

| TSC Category | Criterion | Rescribos Implementation |
|--------------|-----------|--------------------------|
| **CC6.1** | Logical Access - Boundaries | Local-first architecture; no remote access to user data |
| **CC6.6** | Logical Access - Credentials | BYOK with OS keychain; keys never transmitted to Rescribos servers |
| **CC6.7** | Logical Access - Restriction | License-based access control; hardware ID binding |
| **CC7.2** | System Operations - Detection | Application and error logs; structured JSON logging format |
| **CC7.3** | System Operations - Evaluation | Self-contained monitoring; exportable logs for SIEM integration |
| **A1.2** | Availability - Resilience | Offline capability; automatic fallback to local AI models |

#### GDPR Requirements Compliance

| GDPR Article | Requirement | Rescribos Implementation |
|--------------|-------------|--------------------------|
| **Art. 5(1)(a)** | Lawfulness, fairness, transparency | Open-source processing scripts; auditable Python code |
| **Art. 5(1)(c)** | Data minimization | Only collects public data; no PII collection or storage |
| **Art. 5(1)(e)** | Storage limitation | User-controlled retention; manual deletion of reports anytime |
| **Art. 5(1)(f)** | Integrity and confidentiality | Local storage only; TLS for API calls; OS-level encryption |
| **Art. 15** | Right of access | Direct file system access to all data (JSON/Markdown/SQLite) |
| **Art. 16** | Right to rectification | Users can edit reports manually; full control over local data |
| **Art. 17** | Right to erasure | Delete `AppData/Roaming/ai-news-extractor` directory anytime |
| **Art. 20** | Right to data portability | Standard formats (JSON, Markdown, Excel, PDF); easy export |
| **Art. 25** | Data protection by design | Privacy-first architecture; local-first philosophy from inception |
| **Art. 32** | Security of processing | Encryption in transit (TLS 1.3); at-rest encryption via OS |

#### HIPAA Compliance Considerations

| HIPAA Requirement | Implementation Guidance |
|-------------------|-------------------------|
| **Administrative Safeguards** | Use in offline mode; document security policies for organizational deployment |
| **Physical Safeguards** | Desktop application inherits device physical security controls |
| **Technical Safeguards** | Encryption in transit (TLS 1.3); local storage with disk encryption |
| **Access Control** | Machine-specific licensing; no multi-user access without OS controls |
| **Audit Controls** | Comprehensive logging to `logs/` directory; timestamp all operations |
| **Integrity Controls** | File-based storage with atomic writes; version control for reports |
| **Transmission Security** | TLS 1.3 mandatory; certificate validation; no insecure fallback |

**Note for HIPAA Users:** When processing Protected Health Information (PHI), operate Rescribos in **fully offline mode** using local AI models (Ollama) to avoid transmitting data to third-party APIs. Configure `USE_LOCAL_MODELS_ONLY=true` in environment settings.

#### Federal & Air-Gapped Deployment

**FedRAMP Considerations:**
- Deploy in **offline mode** with local models for IL-2+ environments
- Hardware-based licensing (no cloud callback with offline grace period)
- Auditable open-source codebase for security review
- Standard installation packages (no containers required)

**Air-Gap Compatibility:**
- Full functionality with Ollama or local embedding models
- No internet requirement after initial installation
- License validation: 30-day offline grace period
- Manual license transfer protocol available for classified environments

**Recommended Configuration for Federal Use:**
```env
USE_LOCAL_MODELS_ONLY=true
OLLAMA_MODEL=llama3.1:8b
OLLAMA_EMBED_MODEL=nomic-embed-text
ENABLE_TELEMETRY=false
OFFLINE_MODE=true
LICENSE_OFFLINE_GRACE_DAYS=30
```

### 4.6 Network Security

**Encrypted Connections:**
- All API calls use TLS 1.3
- Certificate validation enforced
- No insecure HTTP fallback

**Configuration Example:**
```env
# Security settings
ALLOW_INSECURE_CONNECTIONS=false
CERTIFICATE_VALIDATION=strict
PROXY_SUPPORT=true
PROXY_URL=http://corporate-proxy:8080
```

**Firewall Rules:**
Required outbound access (when using cloud AI):
- `api.openai.com:443` - OpenAI API
- `*.hacker-news.firebaseio.com:443` - Hacker News
- `export.arxiv.org:443` - arXiv API
- `license.rescribos.com:443` - License validation (once per 30 days)

Optional outbound access:
- `localhost:11434` - Ollama (local)
