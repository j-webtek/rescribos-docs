# Installation Guide

### 9.1 Desktop Installers

**Windows Installation:**
```
rescribos-setup-2.0.0.exe
Size: 145 MB
Installer: NSIS (Nullsoft Scriptable Install System)
Features:
  • Silent install: rescribos-setup.exe /S
  • Custom install directory
  • Start Menu shortcuts
  • Desktop shortcut (optional)
  • Auto-launch on startup (optional)
  • Uninstaller included

Install Location:
  C:\Program Files\Rescribos\

User Data:
  C:\Users\[User]\AppData\Roaming\ai-news-extractor\

Code Signing: DigiCert EV Certificate
SmartScreen: Microsoft-approved
```

**macOS Installation:**
```
Rescribos-2.0.0.dmg
Size: 152 MB
Format: Apple Disk Image
Features:
  • Drag-and-drop installation
  • Gatekeeper-approved
  • Notarized by Apple
  • Universal binary (Intel + Apple Silicon)
  • Retina display optimized

Install Location:
  /Applications/Rescribos.app

User Data:
  ~/Library/Application Support/ai-news-extractor/

Code Signing: Apple Developer Certificate
Notarization: Apple-notarized
```

**Linux Installation:**
```
AppImage (Recommended):
  rescribos-2.0.0-x86_64.AppImage
  Size: 148 MB
  Usage: chmod +x rescribos*.AppImage && ./rescribos*.AppImage
  No installation required, fully portable

DEB Package (Debian/Ubuntu):
  rescribos_2.0.0_amd64.deb
  Install: sudo dpkg -i rescribos*.deb
  Dependencies: Auto-resolved via apt

RPM Package (Fedora/RHEL):
  rescribos-2.0.0-1.x86_64.rpm
  Install: sudo rpm -i rescribos*.rpm

Install Location:
  /opt/rescribos/

User Data:
  ~/.config/ai-news-extractor/
```

**Auto-Update System:**
```javascript
// Electron-updater configuration
const { autoUpdater } = require('electron-updater');

autoUpdater.setFeedURL({
    provider: 'github',
    owner: 'rescribos',
    repo: 'rescribos-app'
});

autoUpdater.on('update-available', (info) => {
    dialog.showMessageBox({
        type: 'info',
        title: 'Update Available',
        message: `Version ${info.version} is available. Download now?`,
        buttons: ['Download', 'Later']
    });
});

autoUpdater.checkForUpdatesAndNotify();
```

### 9.2 Docker Deployment

**Docker Hub:**
```bash
# Pull pre-built image
docker pull rescribos/rescribos:latest

# Run with volume mounting
docker run -d \
  --name rescribos \
  -v $(pwd)/data:/data/storage \
  -v $(pwd)/config:/app/config \
  -e OPENAI_API_KEY=sk-... \
  rescribos/rescribos:latest
```

**Docker Compose (Full Stack):**
```yaml
version: '3.8'

services:
  rescribos:
    image: rescribos/rescribos:latest
    container_name: rescribos
    restart: unless-stopped
    volumes:
      - ./data:/data/storage
      - ./config:/app/config
      - ./logs:/app/logs
    environment:
      - NODE_ENV=production
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - OLLAMA_BASE_URL=http://ollama:11434
      - DATA_DIR=/data/storage
      - LOG_LEVEL=info
    ports:
      - "3000:3000"  # Web UI (if enabled)
    depends_on:
      - ollama
    networks:
      - rescribos-net

  ollama:
    image: ollama/ollama:latest
    container_name: ollama
    restart: unless-stopped
    ports:
      - "11434:11434"
    volumes:
      - ollama-models:/root/.ollama
    environment:
      - OLLAMA_HOST=0.0.0.0
    networks:
      - rescribos-net

volumes:
  ollama-models:

networks:
  rescribos-net:
    driver: bridge
```

**Kubernetes Deployment:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rescribos
spec:
  replicas: 1
  selector:
    matchLabels:
      app: rescribos
  template:
    metadata:
      labels:
        app: rescribos
    spec:
      containers:
      - name: rescribos
        image: rescribos/rescribos:latest
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: rescribos-secrets
              key: openai-api-key
        - name: DATA_DIR
          value: /data/storage
        volumeMounts:
        - name: data
          mountPath: /data/storage
        - name: config
          mountPath: /app/config
      volumes:
      - name: data
        persistentVolumeClaim:
          claimName: rescribos-data
      - name: config
        configMap:
          name: rescribos-config
```
