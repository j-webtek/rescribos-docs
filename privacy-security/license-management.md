# License Management

Rescribos includes optional license enforcement logic suited for commercial deployments. The implementation resides in `lib/license-manager.js` and can be disabled for internal builds.

## How It Works

- **Machine binding** – Uses `node-machine-id` to derive a stable hardware identifier. Identifiers are hashed before leaving the device.
- **Activation flow** – Validates licences by calling the configured licensing endpoint (see `.env.example`). Responses contain signed tokens that are cached locally.
- **Offline grace** – Licences remain valid for a configurable period (default 30 days) without contacting the server, enabling air-gapped environments.
- **Audit trail** – Activation attempts, successes, and failures are logged under `logs/license*.log`.

## Privacy Posture

- Only the hashed machine identifier, licence key, and application version are transmitted.
- No usage metrics or telemetry are collected during activation checks.
- The validator code is open and can be inspected or replaced if organisations need bespoke controls.

## Configuration

Relevant environment variables (see `.env.example`):

```
LICENSE_SERVER_URL=https://license.rescribos.com
LICENSE_VALIDATION_INTERVAL_HOURS=24
OFFLINE_GRACE_PERIOD_DAYS=30
```

Set `LICENSE_ENFORCEMENT=false` during development or internal evaluation if licence checks are not required.

For operational guidelines and compliance mapping, refer to `docs/CODE_PROTECTION_GUIDE.md`.
