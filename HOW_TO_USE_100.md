# How to Use All 100% Features

Quick guide to using all features of ClawdBot Python v0.3.0

---

## All 24 Tools

### File Operations
```bash
# Read file
clawdbot agent run "Read the contents of package.json"

# Write file
clawdbot agent run "Create a new file called hello.txt with 'Hello World'"

# Edit file
clawdbot agent run "Replace 'foo' with 'bar' in app.py"

# Apply patch
clawdbot agent run "Apply this patch to the code: [paste diff]"
```

### Execution
```bash
# Bash command
clawdbot agent run "List all Python files in current directory"

# Process management
clawdbot agent run "Start a background process to run the server"
```

### Web
```bash
# Web fetch
clawdbot agent run "Fetch the content from https://example.com"

# Web search
clawdbot agent run "Search for Python async tutorial"
```

### Sessions
```bash
# List sessions
clawdbot agent run "Show me all my conversation sessions"

# Get history
clawdbot agent run "Show me the history of session-123"

# Send message
clawdbot agent run "Send 'hello' to session-456"

# Spawn new session
clawdbot agent run "Create a new session for project planning"
```

### Advanced
```bash
# Browser automation
clawdbot agent run "Open google.com and take a screenshot"

# Scheduled tasks
clawdbot agent run "Remind me every day at 9am to check emails"

# Text-to-speech
clawdbot agent run "Convert this text to speech: Hello World"

# Memory search
clawdbot agent run "Search my conversation history for 'Python tutorial'"

# Image analysis
clawdbot agent run "Analyze this image: ~/photo.jpg"
```

### Channel Actions
```bash
# Send message
clawdbot agent run "Send 'Hello' to Telegram chat 123456"

# Telegram actions
clawdbot agent run "Pin message 42 in Telegram chat 123456"

# Discord actions
clawdbot agent run "Create a thread on Discord message 789"

# Slack actions
clawdbot agent run "React with :thumbsup: to Slack message"
```

---

## All 17 Channels

### Setup Channels

```bash
# Configure in ~/.clawdbot/clawdbot.json
{
  "channels": {
    "telegram": {"enabled": true, "botToken": "..."},
    "discord": {"enabled": true, "botToken": "..."},
    "slack": {"enabled": true, "botToken": "..."},
    "line": {"enabled": true, "channelAccessToken": "...", "channelSecret": "..."},
    "mattermost": {"enabled": true, "url": "...", "token": "..."}
  }
}
```

### Start Gateway with Channels

```bash
clawdbot gateway start
```

All configured channels will start automatically.

---

## All 52 Skills

Skills are automatically loaded from `skills/` directory. Use them naturally:

```bash
# Notion
clawdbot agent run "Search my Notion for project notes"

# Obsidian
clawdbot agent run "Create an Obsidian note about the meeting"

# Spotify
clawdbot agent run "Play my Discover Weekly playlist"

# Trello
clawdbot agent run "Add a card to my TODO board"

# Apple Notes (macOS)
clawdbot agent run "Create a note in Apple Notes"

# And 47 more skills...
```

---

## OpenAI-Compatible API

### Use with OpenAI SDK

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8080/v1",
    api_key="dummy"  # Not validated
)

response = client.chat.completions.create(
    model="claude-opus-4",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

### Direct HTTP

```bash
curl -X POST http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "claude-opus-4",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

---

## Direct Tool Invocation

```bash
curl -X POST http://localhost:8080/tools/invoke \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "web_search",
    "params": {"query": "Python tutorials"}
  }'
```

---

## Web UI

1. Start web server:
```bash
uvicorn clawdbot.web.app:app --port 8080
```

2. Open browser: http://localhost:8080

3. Features:
   - Dashboard with status
   - WebChat interface
   - Session management

---

## Advanced Usage

### Memory System

```bash
# Searches use LanceDB automatically
clawdbot agent run "What did we discuss about Python last week?"
```

### Browser Automation

```bash
clawdbot agent run "Go to github.com/trending and screenshot it"
```

### Scheduled Tasks

```bash
clawdbot agent run "Set up a daily reminder at 2pm"
```

### Multi-Channel

```bash
clawdbot agent run "Send a message to both Telegram and Discord"
```

---

## Tips

### Performance
- Use streaming for long responses
- Enable memory for context retention
- Use appropriate model for task

### Best Practices
- Set up error notifications
- Monitor gateway logs
- Regular session cleanup
- Backup configuration

---

**All 100% features are now accessible!** ✅

For detailed documentation, see:
- [ALL_FEATURES.md](ALL_FEATURES.md) - Complete list
- [ARCHITECTURE.md](ARCHITECTURE.md) - System design
- [QUICKSTART.md](QUICKSTART.md) - Getting started
