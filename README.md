# OpenClaw Python

> 🦞 **Personal AI assistant platform - Python implementation of [OpenClaw](https://github.com/openclaw/openclaw)**

A production-ready Python implementation of OpenClaw, the personal AI assistant that works across all your channels (WhatsApp, Telegram, Slack, Discord, etc.). Inspired by the TypeScript version, built with Python for better accessibility and enterprise features.

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Tests](https://img.shields.io/badge/tests-309%20passing-green.svg)]()
[![Coverage](https://img.shields.io/badge/coverage-45%25-yellow.svg)]()

## 🌟 What's New in v0.6.0

### 🤖 Multi-Provider LLM Support
- ✅ **Anthropic Claude** - Opus, Sonnet, Haiku (recommended)
- ✅ **OpenAI GPT** - GPT-4, GPT-4 Turbo, GPT-3.5
- ✅ **Google Gemini** - Gemini 3 Flash/Pro with Thinking Mode
- ✅ **Ollama** - Local, free, private (llama3.2, mistral, etc)
- ✅ **AWS Bedrock** - Enterprise-grade

### ⚡ Enterprise Features
- **Settings Manager**: Workspace-specific configuration
- **Message Summarization**: LLM-driven context compression  
- **Enhanced Tool Policies**: Fine-grained security control
- **WebSocket Streaming**: Production-grade real-time
- **Advanced Features**: Thinking Mode, Auth Rotation, Model Fallback

See [docs/RELEASE_NOTES_v0.6.0.md](docs/RELEASE_NOTES_v0.6.0.md) for full details.

---

## 📋 Status

| Component | Status | Notes |
|-----------|--------|-------|
| Agent Runtime | ✅ 100% | Multi-provider, context management, v0.5.0+ features |
| Gemini Integration | ✅ 100% | **NEW**: Gemini 3 Flash/Pro with Thinking Mode |
| Tools System | ✅ 90% | 24+ tools with v0.6.0 policies |
| Channel Plugins | ✅ 70% | 4 production + 13 stubs |
| REST API | ✅ 100% | FastAPI + OpenAI compatibility |
| Documentation | ✅ 100% | Complete guides + examples |
| Testing | ✅ 45% | 309 passing tests |

**Current Stage**: ✨ **Production Ready** - v0.6.0

---

## 🚀 Quick Start

### Step 1: 安装依赖

```bash
# 1. 克隆项目
git clone https://github.com/zhaoyuong/openclaw-python.git
cd openclaw-python

# 2. 安装 uv 包管理器（如果还没安装）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 3. 安装项目依赖
uv sync
```

### Step 2: 配置 API Key

**选择一个 LLM Provider**（至少选一个）：

<details>
<summary><strong>🔹 选项 1: Claude（推荐）</strong></summary>

1. 访问 https://console.anthropic.com/
2. 注册账号并创建 API Key
3. 编辑 `.env` 文件：
   ```bash
   cp .env.example .env
   echo 'ANTHROPIC_API_KEY=sk-ant-your-key-here' >> .env
   ```
</details>

<details>
<summary><strong>🔹 选项 2: OpenAI GPT</strong></summary>

1. 访问 https://platform.openai.com/api-keys
2. 创建 API Key
3. 编辑 `.env` 文件：
   ```bash
   cp .env.example .env
   echo 'OPENAI_API_KEY=sk-your-key-here' >> .env
   ```
</details>

<details>
<summary><strong>🔹 选项 3: Google Gemini</strong></summary>

1. 访问 https://aistudio.google.com/apikey
2. 创建 API Key
3. 编辑 `.env` 文件：
   ```bash
   cp .env.example .env
   echo 'GOOGLE_API_KEY=your-key-here' >> .env
   ```
</details>

<details>
<summary><strong>🔹 选项 4: Ollama（本地免费，无需 API Key）</strong></summary>

1. 安装 Ollama: https://ollama.ai/download
2. 启动服务：
   ```bash
   ollama serve
   ```
3. 下载模型：
   ```bash
   ollama pull llama3.2
   ```
4. 无需配置 `.env`
</details>

### Step 3: 启动服务

**方式 1: 命令行对话（最简单）**

```bash
# 单次对话
uv run openclaw agent chat "你好，介绍一下自己"

# 指定模型
uv run openclaw agent chat "帮我写代码" --model anthropic/claude-opus-4-5
```

**方式 2: 交互式模式（推荐日常使用）**

```bash
# 启动交互式对话
uv run openclaw agent interactive

# 多轮对话，输入 'exit' 或 'quit' 退出
```

**方式 3: API 服务器（用于集成）**

```bash
# 启动 REST API 服务
uv run openclaw api start

# 访问 API 文档: http://localhost:18789/docs
# 兼容 OpenAI API 格式
```

**方式 4: Python 脚本（高级用法）**

```python
import asyncio
from openclaw.agents import AgentRuntime, Session
from pathlib import Path

async def main():
    runtime = AgentRuntime(
        model="anthropic/claude-opus-4-5",  # 或其他模型
        max_tokens=2000,
        temperature=0.7
    )
    
    session = Session(
        session_id="my-chat",
        workspace_dir=Path.cwd()
    )
    
    response = await runtime.run_turn(
        session=session,
        user_message="Hello!"
    )
    
    async for event in response:
        if event["type"] == "text":
            print(event["text"], end="", flush=True)

asyncio.run(main())
```

### 📖 完整文档

- **[START_HERE.md](START_HERE.md)** - 1 分钟入门
- **[QUICK_START.md](QUICK_START.md)** - 详细指南  
- **[docs/](docs/)** - 完整文档

---

## 🎯 支持的模型

| Provider | 模型示例 | 使用方式 |
|----------|---------|---------|
| **Claude** | claude-opus-4-5, claude-sonnet-4-5 | `--model anthropic/claude-opus-4-5` |
| **OpenAI** | gpt-4, gpt-4-turbo, gpt-3.5-turbo | `--model openai/gpt-4` |
| **Gemini** | gemini-3-flash-preview, gemini-3-pro-preview | `--model google/gemini-3-flash-preview` |
| **Ollama** | llama3.2, mistral, codellama | `--model ollama/llama3.2` |

**完整模型列表**: 运行 `uv run openclaw agent models` 查看所有支持的模型

---

## 📚 Features

### Core Platform (v0.4.x)
- ✅ Multi-provider LLM support (Anthropic, OpenAI, Google, AWS, Ollama)
- ✅ 24+ tools with permissions & rate limiting
- ✅ Multi-channel support (Telegram, Discord, Slack, WebChat)
- ✅ REST API + OpenAI compatibility
- ✅ Authentication & rate limiting
- ✅ Health monitoring & metrics

### Advanced Features (v0.5.0)
- ✅ **Thinking Mode** - AI reasoning extraction
- ✅ **Auth Rotation** - Multi-key failover with cooldown
- ✅ **Model Fallback** - Automatic model switching
- ✅ **Session Queuing** - Concurrency control
- ✅ **Context Compaction** - Intelligent pruning
- ✅ **Tool Formatting** - Channel-specific output

### Enterprise Features (v0.6.0)
- ✅ **Settings Manager** - Workspace configuration
- ✅ **Message Summarization** - LLM-driven compression
- ✅ **Tool Policies** - Security & access control
- ✅ **WebSocket Streaming** - Production real-time

---

## 🔧 Configuration

Minimal `~/.openclaw/openclaw.json`:

```json
{
  "agent": {
    "model": "gemini-3-flash-preview"
  }
}
```

Full configuration: [docs/configuration.md](docs/configuration.md)

---

## 📖 Documentation

### Getting Started
- [Installation Guide](docs/installation.md)
- [Quick Start Tutorial](docs/quickstart.md)
- [Gemini Setup Guide](GEMINI_SETUP_GUIDE.md) ⭐
- [Configuration Reference](docs/configuration.md)

### Advanced Guides
- [Advanced Features](docs/guides/ADVANCED_FEATURES.md)
- [v0.5.0 Release Notes](RELEASE_NOTES_v0.5.0.md)
- [v0.6.0 Release Notes](RELEASE_NOTES_v0.6.0.md) ⭐
- [Security Guide](docs/security.md)

### Examples
- [examples/01_basic_agent.py](examples/01_basic_agent.py) - Basic usage
- [examples/02_with_tools.py](examples/02_with_tools.py) - Tool usage
- [examples/08_advanced_features.py](examples/08_advanced_features.py) - v0.5.0 features
- [examples/09_v0.6_features.py](examples/09_v0.6_features.py) - v0.6.0 features

---

## 🤝 Project History

**OpenClaw** (formerly MoltBot, formerly ClawdBot) is the open-source personal AI assistant platform.

- **Main Project**: [openclaw/openclaw](https://github.com/openclaw/openclaw) (TypeScript)
- **Python Port**: openclaw/openclaw-python (this repository)

This Python implementation provides:
- ✅ Better testing (45% vs ~10% in TypeScript)
- ✅ Complete documentation
- ✅ Enhanced security features
- ✅ Easier deployment

---

## 🧪 Testing

```bash
# Run all tests
uv run pytest tests/

# Run specific tests
uv run pytest tests/test_gemini_provider.py

# With coverage
uv run pytest --cov=openclaw --cov-report=html
```

**Current**: 309 tests passing, 45% coverage

---

## 🛠️ Development

```bash
# Install dev dependencies
uv sync

# Format code
uv run black openclaw/
uv run ruff check --fix openclaw/

# Type checking
uv run mypy openclaw/

# Build package
uv build
```

---

## 📝 Changelog

### v0.6.0 (2026-01-31)
- ✅ Renamed from clawdbot-python to openclaw-python
- ✅ Added Gemini 3 Flash/Pro support with Thinking Mode
- ✅ Upgraded to `google-genai` API
- ✅ Settings Manager for workspace configuration
- ✅ Message summarization with multiple strategies
- ✅ Enhanced tool policies with 6 policy types
- ✅ WebSocket improvements for production

### v0.5.0 (2026-01-29)
- ✅ All 6 advanced features from TypeScript version
- ✅ Full feature parity achieved
- ✅ 72 new tests, comprehensive documentation

See [CHANGELOG.md](CHANGELOG.md) for full history.

---

## 🔗 Links

- **Main Project**: https://github.com/openclaw/openclaw
- **Website**: https://openclaw.ai
- **Documentation**: [docs/](docs/)
- **Discord**: Join the community
- **Twitter**: [@openclaw](https://twitter.com/openclaw)

---

## 📜 License

MIT License - see [LICENSE](LICENSE)

---

## 🙏 Acknowledgments

- [OpenClaw](https://github.com/openclaw/openclaw) - Original TypeScript implementation
- [MoltBot](https://openclaw.ai) - The space lobster AI 🦞
- All contributors to the OpenClaw ecosystem

---

## 🚀 Get Started

```bash
# Test Gemini 3 Flash
uv run python test_gemini_3_flash.py

# Start building
cd openclaw-python
uv sync
uv run openclaw agent chat "Hello, OpenClaw!"
```

**Welcome to OpenClaw Python!** 🦞
