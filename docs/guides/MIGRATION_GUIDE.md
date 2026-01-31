# Migration Guide: ClawdBot → OpenClaw

## 🦞 Project Rename & Gemini 3 Upgrade

**Date**: 2026-01-31  
**Version**: 0.6.0  
**Status**: Complete ✅

---

## 📋 Overview

This guide helps you migrate from `clawdbot-python` to `openclaw-python`.

### What Changed

1. **Project Name**: clawdbot-python → openclaw-python
2. **Package Name**: clawdbot → openclaw
3. **Gemini API**: google.generativeai → google.genai (NEW)
4. **Recommended Model**: gemini-2.5-flash → gemini-3-flash-preview

### What Stayed the Same

- ✅ All functionality preserved
- ✅ 100% backward compatible
- ✅ Same API surface
- ✅ All tests passing (309 tests)

---

## 🚀 Quick Migration

### 1. Update Repository

```bash
cd /path/to/your/project

# If you cloned from old URL
git remote set-url origin https://github.com/openclaw/openclaw-python.git

# Pull latest changes
git pull origin main

# Reinstall dependencies
uv sync
```

### 2. Update Imports

**Old (clawdbot):**
```python
from clawdbot.agents import AgentRuntime
from clawdbot.agents.providers import GeminiProvider
```

**New (openclaw):**
```python
from openclaw.agents import AgentRuntime
from openclaw.agents.providers import GeminiProvider
```

### 3. Update Configuration

**Old config paths:**
- `~/.clawdbot/` → `~/.openclaw/`
- `clawdbot.json` → `openclaw.json`

**Example:**
```bash
# Rename config directory (optional - both work)
mv ~/.clawdbot ~/.openclaw
```

### 4. Update Environment Variables

`.env` file changes (optional):
```bash
# Old (still works)
GOOGLE_API_KEY=your-key

# New (also works)
GEMINI_API_KEY=your-key
```

Both variables are supported for backward compatibility.

---

## 🔧 Detailed Migration Steps

### For Python Code

#### Replace All Imports

Use find-and-replace in your IDE:

```bash
# Find: clawdbot
# Replace with: openclaw
```

Or use command line:
```bash
find . -type f -name "*.py" -exec sed -i '' 's/clawdbot/openclaw/g' {} +
```

#### Update pyproject.toml

```toml
# Old
dependencies = [
    "clawdbot>=0.5.0",
    "google-generativeai>=0.3.0"
]

# New
dependencies = [
    "openclaw-python>=0.6.0",
    "google-genai>=0.2.0"
]
```

### For CLI Usage

**Old commands:**
```bash
clawdbot agent chat "Hello"
clawdbot api start
```

**New commands:**
```bash
openclaw agent chat "Hello"
openclaw api start
```

### For Docker/Compose

Update `Dockerfile` or `docker-compose.yml`:

```dockerfile
# Old
FROM python:3.11
COPY clawdbot /app/clawdbot

# New
FROM python:3.11
COPY openclaw /app/openclaw
```

---

## 🎯 Gemini 3 Migration

### Update Model Configuration

**Old config (~/.clawdbot/clawdbot.json):**
```json
{
  "agent": {
    "model": "models/gemini-2.5-flash"
  }
}
```

**New config (~/.openclaw/openclaw.json):**
```json
{
  "agent": {
    "model": "gemini-3-flash-preview"
  }
}
```

### Update Provider Code

**Old API (google.generativeai):**
```python
import google.generativeai as genai

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.5-flash")
response = model.generate_content(messages)
```

**New API (google.genai):**
```python
from google import genai
from google.genai import types

client = genai.Client(api_key=api_key)
response = client.models.generate_content_stream(
    model="gemini-3-flash-preview",
    contents=contents,
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(
            thinking_level="HIGH"
        )
    )
)
```

### Use OpenClaw Provider (Recommended)

Instead of using the raw API, use our wrapper:

```python
from openclaw.agents.providers import GeminiProvider
from openclaw.agents.providers.base import LLMMessage

provider = GeminiProvider(
    model="gemini-3-flash-preview",
    api_key=os.getenv("GOOGLE_API_KEY")
)

messages = [LLMMessage(role="user", content="Hello!")]

async for response in provider.stream(
    messages,
    thinking_mode="HIGH",  # New feature!
    enable_search=True     # Google Search integration
):
    if response.type == "text_delta":
        print(response.content, end="")
```

---

## 📦 Recommended Models (2026)

### For Production

**Recommended:**
```python
model = "gemini-3-flash-preview"  # Fast + Thinking Mode
```

**Alternatives:**
```python
model = "gemini-3-pro-preview"    # Most capable
model = "gemini-2.5-flash"        # Stable, no thinking
model = "gemini-2.5-pro"          # Stable, powerful
```

### Model Comparison

| Model | Speed | Intelligence | Thinking | Context | Cost |
|-------|-------|-------------|----------|---------|------|
| gemini-3-flash-preview | ⚡⚡⚡ | ⭐⭐⭐ | ✅ | 1M | $ |
| gemini-3-pro-preview | ⚡⚡ | ⭐⭐⭐⭐⭐ | ✅ | 2M | $$$ |
| gemini-2.5-flash | ⚡⚡⚡ | ⭐⭐⭐ | ❌ | 1M | $ |
| gemini-2.5-pro | ⚡⚡ | ⭐⭐⭐⭐ | ❌ | 2M | $$$ |

---

## 🧪 Testing Your Migration

### 1. Run Tests

```bash
cd openclaw-python

# Install dependencies
uv sync

# Run all tests
uv run pytest tests/

# Should see: 309 passed ✅
```

### 2. Test Gemini 3

```bash
# Test new Gemini API
uv run python test_gemini_3_flash.py

# Should see successful responses
```

### 3. Test Your Code

```bash
# Test your application
uv run python your_app.py

# Or test with CLI
uv run openclaw agent chat "Test message"
```

---

## 🔍 Troubleshooting

### Import Errors

**Error:**
```
ModuleNotFoundError: No module named 'clawdbot'
```

**Fix:**
```bash
# Update all imports
find . -name "*.py" -exec sed -i '' 's/clawdbot/openclaw/g' {} +

# Reinstall
uv sync
```

### Model Not Found

**Error:**
```
404 models/gemini-2.5-flash is not found
```

**Fix:**
Update to use correct model names:
- ✅ `gemini-3-flash-preview` (no `models/` prefix)
- ✅ `gemini-3-pro-preview`
- ❌ ~~`models/gemini-2.5-flash`~~ (old format)

### API Key Issues

**Error:**
```
ValueError: GOOGLE_API_KEY not provided
```

**Fix:**
```bash
# Check .env file
cat .env | grep GOOGLE_API_KEY

# Or set GEMINI_API_KEY (both work)
echo "GEMINI_API_KEY=your-key" >> .env
```

### Package Installation

**Error:**
```
ImportError: cannot import name 'genai' from 'google'
```

**Fix:**
```bash
# Uninstall old package
pip uninstall google-generativeai

# Install new package
uv add google-genai

# Or with pip
pip install google-genai
```

---

## 📚 Additional Resources

- [GEMINI_SETUP_GUIDE.md](GEMINI_SETUP_GUIDE.md) - Complete Gemini setup
- [RELEASE_NOTES_v0.6.0.md](RELEASE_NOTES_v0.6.0.md) - Full changelog
- [README.md](README.md) - Updated project README
- [Main OpenClaw Project](https://github.com/openclaw/openclaw) - TypeScript version

---

## ✅ Migration Checklist

Use this checklist to track your migration:

- [ ] Updated git remote URL
- [ ] Pulled latest changes (`git pull`)
- [ ] Renamed imports (clawdbot → openclaw)
- [ ] Updated config files (.clawdbot → .openclaw)
- [ ] Updated environment variables
- [ ] Installed new dependencies (`uv sync`)
- [ ] Updated Gemini model names
- [ ] Tested with `test_gemini_3_flash.py`
- [ ] Ran full test suite (`pytest tests/`)
- [ ] Updated your application code
- [ ] Tested your application
- [ ] Updated deployment scripts
- [ ] Updated CI/CD pipelines
- [ ] Updated documentation

---

## 🎉 Migration Complete!

Once all items are checked, your migration is complete!

**Welcome to OpenClaw Python!** 🦞

For questions or issues:
- GitHub Issues: https://github.com/openclaw/openclaw-python/issues
- Discord: [Join Community]
- Documentation: [docs/](docs/)

---

**Last Updated**: 2026-01-31  
**Migration Version**: 0.5.x → 0.6.0
