# Deployment Models

### 11.3 Deployment Models

#### Desktop Application (All Tiers)

**Installation:**
- Windows: NSIS installer (`.exe`)
- macOS: DMG installer (`.dmg`)
- Linux: AppImage (`.AppImage`) or DEB package

**Characteristics:**
- Single-user, local installation
- Data stored in user's AppData/home directory
- Auto-update capability
- No server required

**Best For:** Individual users, small teams with independent workflows

---

#### CLI/Headless Mode (Professional+)

**Installation:**
```bash
npm install -g rescribos-cli

# Or via pip
pip install rescribos-cli
```

**Usage:**
```bash
# Run extraction and analysis
rescribos run --sources hackernews,arxiv --keywords "AI,ML" --output ./reports/

# Schedule daily reports (cron)
0 8 * * * rescribos run --config ~/rescribos-config.json --email report@company.com
```

**Best For:** Automation, CI/CD pipelines, scheduled reporting

---

#### Docker Deployment (Professional+)

**Installation:**
```bash
docker pull rescribos/rescribos:latest

# Run with mounted volumes
docker run -v $(pwd)/storage:/app/storage \
           -v $(pwd)/config:/app/config \
           -e OPENAI_API_KEY=$OPENAI_API_KEY \
           rescribos/rescribos:latest run
```

**Characteristics:**
- Containerized environment
- Reproducible deployments
- Easy scaling via orchestration
- Isolated dependencies

**Best For:** Cloud deployments, microservices architecture, team environments

---

#### On-Premises Server (Enterprise)

**Installation:**
- Custom deployment package
- Ansible/Terraform scripts provided
- Database migration tools
- Load balancer configuration

**Architecture:**
```
┌─────────────────────────────────────────────────────┐
│              Corporate Network                      │
│                                                     │
│  ┌──────────────┐      ┌──────────────┐            │
│  │ Web Frontend │◄────►│  API Server  │            │
│  │  (Nginx)     │      │  (Node.js)   │            │
│  └──────────────┘      └───────┬──────┘            │
│                                 │                   │
│                        ┌────────▼────────┐          │
│                        │ Processing Pool │          │
│                        │  (Python workers)│         │
│                        └────────┬────────┘          │
│                                 │                   │
│  ┌──────────────┐      ┌───────▼─────────┐         │
│  │  PostgreSQL  │◄────►│     Redis       │         │
│  │  (pgvector)  │      │  (Task queue)   │         │
│  └──────────────┘      └─────────────────┘         │
│                                                     │
│  Optional: Ollama server for local AI              │
└─────────────────────────────────────────────────────┘
```

**Best For:** Large organizations, compliance-sensitive environments, high-volume processing

---

#### Air-Gapped Deployment (Enterprise)

**Requirements:**
- No internet connectivity required
- Local AI models (Ollama) pre-installed
- Manual license transfer protocol
- Offline documentation package

**Setup Process:**
1. Install Rescribos package from USB/DVD media
2. Copy pre-downloaded AI models to local directory
3. Transfer license file via secure media
4. Configure for offline mode in `config/settings.json`

**Configuration:**
```json
{
  "offline_mode": true,
  "ai_provider": "ollama",
  "ollama_base_url": "http://localhost:11434",
  "license_offline_grace_days": 365,
  "disable_telemetry": true,
  "disable_update_check": true
}
```

**Best For:** Federal agencies, classified environments, highly regulated industries
