# Deployment Options

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

## Sections

- [Installation Guide](installation.md)
- [Configuration](configuration.md)
