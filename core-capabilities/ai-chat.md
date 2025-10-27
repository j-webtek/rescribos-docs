# Interactive AI Chat

### 2.5 Interactive AI Chat

Engage in natural conversations about your reports and documents, asking questions and receiving context-aware answers with intelligent context management.

## Core Chat Capabilities

**1. Context-Aware Responses**
- Automatic inclusion of top-K relevant stories
- Conversation history tracking (6 exchanges)
- Semantic context retrieval
- Dynamic context switching

**2. Streaming Responses**
- Real-time token generation
- Progressive UI updates
- <2s time-to-first-token
- Markdown rendering during streaming

**3. Multi-Turn Dialogue**
- Conversation memory
- Follow-up questions
- Context refinement
- History-aware responses

**4. Export Transcripts**
- Save as Markdown
- Timestamp preservation
- Source attribution
- Conversation threading

## Context Management

The chat system features **intelligent context management** that allows you to control which content is included in your conversations.

### Context Modes

The chat interface displays a **context indicator** showing the current analysis scope:

#### 1. Full Report Context (Default)

**Label:** `📰 Full Report Context`

**When Active:**
- No specific stories have been added to chat
- Questions are answered using the entire report
- AI searches all stories for relevant information

**Use Cases:**
- Initial exploration and discovery
- Broad trend analysis
- Topic searching across all content
- Overview questions

**Example Questions:**
```
"What are the main themes in this report?"
"Which companies are mentioned most frequently?"
"Summarize AI developments this month"
"Find stories about quantum computing"
```

#### 2. Single Story Context

**Label:** `📄 Story: [story title]`

**When Active:**
- Exactly one story has been added to chat
- Questions focus exclusively on that story
- Detailed, precise answers about specific content

**Use Cases:**
- Deep dive into specific article
- Extracting detailed information
- Understanding technical specifics
- Quote extraction and verification

**Example Questions:**
```
"What is the main finding of this paper?"
"Who are the authors and their affiliations?"
"What methodology was used?"
"What are the limitations mentioned?"
```

#### 3. Multi-Story Context

**Label:** `📚 2 Stories in Context` (or 3, 4, etc.)

**When Active:**
- Multiple stories have been added to chat
- Questions analyze across selected stories
- Comparative and relational analysis

**Use Cases:**
- Comparing related articles
- Finding connections between stories
- Building narrative across documents
- Analyzing specific subset

**Example Questions:**
```
"How do these papers relate to each other?"
"What are the common themes across these stories?"
"Compare the approaches in these articles"
"Create a timeline from these stories"
```

### Adding Stories to Context

**From Results Viewer:**
1. Browse stories in the main results panel
2. Find story you want to analyze
3. Click **"Add to Chat"** or **💬** button on story card
4. Context label updates immediately
5. Add more stories to build multi-story context

**Visual Feedback:**
- Context label updates in real-time
- Notification appears in chat: "Added Story to Context"
- Icon changes based on mode (📰/📄/📚)

### Managing Story Context

**Removing Stories:**
- **Single story**: Click **[×]** button next to context label
- **All stories**: Click **"Remove All"** to return to full report context
- **Individual management**: Use **[▼]** dropdown to see and remove specific stories

**Context Label States:**
```
No stories selected:
┌─────────────────────────────┐
│ 📰 Full Report Context      │
└─────────────────────────────┘

One story selected:
┌─────────────────────────────┐
│ 📄 Story: GPT-5 Released   │
│    [×] Remove               │
└─────────────────────────────┘

Multiple stories selected:
┌─────────────────────────────┐
│ 📚 3 Stories in Context     │
│    [▼] Manage  [×] Remove   │
└─────────────────────────────┘
```

### Context Switching

**Automatic Notifications:**
When context changes, the chat displays a system message:
- "Added Story to Context"
- "2 Stories in Context"
- "Returned to Full Report Context"

**Best Practices:**
- **Start broad**: Use Full Report Context for discovery
- **Narrow down**: Add specific stories for detailed analysis
- **Compare**: Use Multi-Story Context for comparative questions
- **Clean up**: Remove stories when switching topics

## Document Library Integration

Chat seamlessly integrates with the [Document Library](../advanced-features/document-library.md):

**Adding Documents to Chat:**
1. Open Document Library
2. Select documents you want to analyze
3. Click "Add to Chat"
4. Chat context updates to include documents
5. Ask questions about the documents

**Documents-Only Mode:**
- Works even without a loaded report
- Label shows: "Documents Only" or "N Documents in Context"
- Same context management as stories

## Advanced Features

### Semantic Grounding

Every chat response is grounded in actual document content:
- **Relevance Ranking**: AI automatically finds most relevant stories
- **Citation Links**: Responses include links back to source stories
- **Passage Highlighting**: Key passages are highlighted in context
- **Confidence Scoring**: System indicates certainty of answers

### Conversation History

**History Management:**
- Last 6 exchanges preserved in memory
- Enables follow-up questions
- Context-aware clarifications
- Thread continuity

**Clear History:**
- Reset conversation at any time
- Useful when switching topics
- Starts fresh conversation
- Preserves current story context

### Export Capabilities

**Save Conversations:**
- Export as Markdown file
- Includes timestamps
- Preserves source attributions
- Maintains formatting

## Example Conversations

**Discovery (Full Report Context):**
```
User: What are the main AI trends this month?
Assistant: [Analyzes all stories, identifies top trends with citations]

User: Tell me more about the quantum computing stories
Assistant: [Filters to quantum computing, provides details]
```

**Deep Dive (Single Story Context):**
```
User: [Adds specific paper to context]
User: What methodology did they use?
Assistant: [Detailed answer specific to that paper]

User: What were the limitations?
Assistant: [Precise extraction from that paper]
```

**Comparative Analysis (Multi-Story Context):**
```
User: [Adds 3 papers about LLM optimization]
User: How do their approaches differ?
Assistant: [Compares methodologies across the 3 papers]

User: Which achieved better results?
Assistant: [Performance comparison with metrics]
```

## Configuration

```env
# Chat behavior
CHAT_HISTORY_LENGTH=6              # Conversation memory depth
CHAT_USE_STREAMING=true            # Enable streaming responses
CHAT_MODEL=gpt-5                   # AI model selection

# Context retrieval
CHAT_SIMILARITY_THRESHOLD=0.3      # Relevance threshold
CHAT_TOP_STORIES=20                # Max stories for full report context
CHAT_MAX_TOKENS=4000               # Response length limit

# Performance
CHAT_TIMEOUT=30000                 # Response timeout (ms)
CHAT_RETRY_ATTEMPTS=3              # Retry failed requests
```

## Troubleshooting

**Chat not responding:**
- Verify API key is configured
- Check internet connection (for cloud AI)
- Ensure AI model is available
- Check logs for error messages

**Irrelevant answers:**
- Narrow context by adding specific stories
- Lower similarity threshold
- Rephrase question more specifically
- Verify relevant stories are in report

**Context not updating:**
- Refresh the page
- Check console for errors
- Verify story was successfully added
- Try clearing and re-adding stories

## Related Documentation

- [Chat User Guide](../../../CHAT_USER_GUIDE.md) - Complete chat documentation
- [Chat Context Switching](../../../CHAT_CONTEXT_SWITCHING.md) - Technical implementation
- [Document Library](../advanced-features/document-library.md) - Document management
- [Semantic Search](semantic-search.md) - Search capabilities
