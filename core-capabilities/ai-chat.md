# Interactive AI Chat

### 2.5 Interactive AI Chat

Engage in natural conversations about your reports, asking questions and receiving context-aware answers:

**Chat Capabilities:**

**1. Context-Aware Responses**
- Automatic inclusion of top-K relevant stories
- Conversation history tracking (6 exchanges)
- Semantic context retrieval

**2. Streaming Responses**
- Real-time token generation
- Progressive UI updates
- <2s time-to-first-token

**3. Multi-Turn Dialogue**
- Conversation memory
- Follow-up questions
- Context refinement

**4. Export Transcripts**
- Save as Markdown
- Timestamp preservation
- Source attribution

**Example Conversation:**
```
User: What are the key AI trends this month?
Assistant: [Detailed response focusing on quantum computing stories with citations]
```

**Configuration:**
```env
CHAT_HISTORY_LENGTH=6
CHAT_USE_STREAMING=true
CHAT_MODEL=gpt-4o
```
