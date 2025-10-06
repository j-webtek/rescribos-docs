# Bring Your Own Keys (BYOK)

### 4.2 Bring Your Own Keys (BYOK)

Unlike SaaS platforms that control AI access, Rescribos uses a **BYOK (Bring Your Own Keys)** model:

**Implementation (`src/electron/keyManagement.js`):**
```javascript
const keytar = require('keytar');
const SERVICE_NAME = 'Rescribos';

async function saveOpenAIKey(apiKey) {
    // Validate key format
    if (!apiKey.startsWith('sk-')) {
        throw new Error('Invalid OpenAI key format');
    }

    // Test key validity
    const isValid = await testOpenAIKey(apiKey);
    if (!isValid) {
        throw new Error('OpenAI key authentication failed');
    }

    // Store securely in OS keychain
    await keytar.setPassword(SERVICE_NAME, 'openai_api_key', apiKey);

    // Never log or transmit the key
    console.log('OpenAI key stored securely');
}

async function getOpenAIKey() {
    // Retrieve from OS keychain
    const key = await keytar.getPassword(SERVICE_NAME, 'openai_api_key');
    return key; // Returns null if not set
}

async function deleteOpenAIKey() {
    await keytar.deletePassword(SERVICE_NAME, 'openai_api_key');
}
```

**Security Features:**
- **OS-Level Encryption:** Windows Credential Manager, macOS Keychain, Linux Secret Service
- **Never Transmitted:** Keys stay on user's machine
- **No Storage in Config:** Never written to .env or JSON files
- **Easy Rotation:** Users can update keys anytime
- **Validation:** Keys tested before storage

**BYOK Benefits:**
- **Cost Control:** Users pay OpenAI directly (no markup)
- **Usage Transparency:** Full visibility in OpenAI dashboard
- **Privacy:** Rescribos never sees your API usage
- **Compliance:** Meets enterprise security requirements
- **Flexibility:** Use personal or organizational accounts
