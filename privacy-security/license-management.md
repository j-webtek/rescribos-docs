# License Management System

### 4.3 License Management System

Rescribos uses a **hardware-based licensing system** that protects user privacy while preventing piracy:

**License Architecture:**
```
┌─────────────────────────────────────────────────────┐
│              License Server (Cloud)                 │
│  • License generation and activation                │
│  • Machine ID validation                            │
│  • No user data collection                          │
│  • Minimal metadata (activation count only)         │
└─────────────────────────────────────────────────────┘
                        ↕ HTTPS
┌─────────────────────────────────────────────────────┐
│         Client License Validator (Local)            │
│  • Hardware ID generation (machine-id library)      │
│  • License signature verification                   │
│  • Offline grace period (30 days)                   │
│  • No telemetry or tracking                         │
└─────────────────────────────────────────────────────┘
```

**Implementation (`src/electron/licenseManager.js`):**

Core license validation logic:
```javascript
class LicenseManager {
    // getMachineId() -> SHA-256 hash of hardware ID (stable, unique)
    // activateLicense(key) -> POST to server, verify signature, save locally
    // isLicenseValid() -> check: signature, expiration, machine binding
    // Offline grace: 30-day cached validation period
}
```

**Privacy Guarantees:**
- **No User Identification:** Only hardware ID sent (hashed)
- **No Usage Tracking:** License server doesn't log activity
- **Offline Grace Period:** 30-day validation cache
- **Transparent:** Open-source license validator code
- **Minimal Data:** Only license key, machine ID, app version

**License Types:**
- **Rescribos Complete:** Single-user, 1 device per seat ($150/year, or $129/year for 5+ seats)
- **Enterprise:** Unlimited users, custom deployment
