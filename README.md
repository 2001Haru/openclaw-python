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

## 🚀 快速开始 (Quick Start)

### 第一步：安装

```bash
# 1. 克隆仓库
git clone https://github.com/zhaoyuong/openclaw-python.git
cd openclaw-python

# 2. 安装 uv 包管理器
curl -LsSf https://astral.sh/uv/install.sh | sh

# 3. 安装依赖
uv sync
```

### 第二步：配置 .env 文件（⚠️ 重要）

```bash
# 复制示例配置文件
cp .env.example .env

# 编辑 .env 文件（使用任意编辑器）
nano .env   # 或者 vim .env, code .env 等
```

**至少配置以下一个 LLM API Key：**

```bash
# ========== LLM API Keys（至少选择一个）==========

# 选项 1: Anthropic Claude（推荐，最稳定）
ANTHROPIC_API_KEY=sk-ant-your-key-here
# 获取地址: https://console.anthropic.com/

# 选项 2: OpenAI GPT
OPENAI_API_KEY=sk-your-key-here
# 获取地址: https://platform.openai.com/api-keys

# 选项 3: Google Gemini（支持 Gemini 3）
GOOGLE_API_KEY=your-google-api-key
# 获取地址: https://makersuite.google.com/app/apikey

# 选项 4: 本地 Ollama（免费，无需 API Key）
# 只需安装并启动: ollama serve

# ========== Telegram Bot（可选）==========
# 如果你想通过 Telegram 使用
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
# 获取方式: 
# 1. 在 Telegram 搜索 @BotFather
# 2. 发送 /newbot 创建机器人
# 3. 复制获得的 token

# ========== 其他设置（可选）==========
CLAWDBOT_PORT=18789           # API 服务器端口
CLAWDBOT_LOG_LEVEL=INFO       # 日志级别
```

**⚠️ 安全提醒：**
- `.env` 文件已在 `.gitignore` 中，不会被提交到 Git
- 永远不要分享你的 API Keys
- 生产环境建议使用密钥管理服务

### 第三步：启动服务

---

## ⭐ 推荐方式：通过 Telegram Bot 使用（最实用）

**这是最方便的使用方式！** 在手机或电脑上通过 Telegram 直接与 AI 对话。

### 前提条件
确保已配置：
- ✅ 至少一个 LLM API Key（步骤二）
- ✅ Telegram Bot Token（步骤二中的 Telegram 配置）

### 启动 Telegram Bot 服务

```bash
# 🚀 启动 Telegram Bot（推荐）
uv run python tests/manual/test_telegram_restricted.py

# 看到以下输出表示启动成功：
# ✅ Telegram Bot 启动成功！
# Bot 用户名: @你的bot用户名
# 现在可以在 Telegram 中搜索并开始对话了
```

**⚠️ 重要：这是一个持续运行的服务**
- 启动后会一直运行，等待 Telegram 消息
- 需要保持终端窗口打开
- 按 `Ctrl+C` 可以停止服务

### 在 Telegram 中使用

1. 打开 Telegram（手机或电脑）
2. 搜索你的 bot 用户名（例如：`@myopenclaw_bot`）
3. 点击 **Start** 开始对话
4. 直接发送消息，AI 会回复你！

**示例对话：**
```
你: 你好，能帮我写个 Python 函数吗？
Bot: 当然可以！你需要什么样的函数？

你: 一个计算斐波那契数列的函数
Bot: [AI 生成代码并回复]

你: 谢谢！
Bot: 不客气！还有其他问题吗？
```

---

## 其他使用方式

### 方式 1️⃣：命令行单次对话（快速测试）

```bash
# 单次对话（不是服务，命令执行完就结束）
uv run openclaw agent chat "你好，请介绍一下自己"

# 指定模型
uv run openclaw agent chat "帮我写个 Python 函数" --model anthropic/claude-opus-4-5
```

**特点：**
- ❌ 不是服务，执行完就结束
- ✅ 适合快速测试
- ❌ 不支持多轮对话

### 方式 2️⃣：交互式终端模式（在终端对话）

```bash
# 启动交互式对话（持续运行，直到输入 /quit）
uv run openclaw agent interactive

# 然后你可以：
# - 多轮对话
# - 输入 /help 查看命令
# - 输入 /quit 退出
```

**特点：**
- ❌ 不是网络服务，只是终端界面
- ✅ 支持多轮对话
- ✅ 适合在服务器上使用

### 方式 3️⃣：HTTP API 服务器（应用集成）⭐

```bash
# 🚀 启动 HTTP API 服务（真正的网络服务）
uv run openclaw api start

# 服务启动后：
# - API 文档: http://localhost:18789/docs
# - Health check: http://localhost:18789/health
# - 支持 OpenAI 兼容接口
```

**特点：**
- ✅ 真正的网络服务，持续运行
- ✅ 其他程序可以通过 HTTP 调用
- ✅ 适合集成到应用中
- ⚠️ 需要保持终端运行，按 `Ctrl+C` 停止

### 📱 如何创建 Telegram Bot（首次使用）

如果你还没有创建 Telegram Bot，按以下步骤操作：

**步骤 1：在 Telegram 中创建 Bot**
```bash
1. 打开 Telegram，搜索 @BotFather
2. 点击开始对话，发送命令：
   /newbot

3. 按照提示操作：
   问题：What's your bot's name?
   回答：My OpenClaw Bot（你的 bot 名称）
   
   问题：What's your bot's username?
   回答：myopenclaw_bot（必须以 bot 结尾）

4. 创建成功后，@BotFather 会给你一个 token：
   1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
   
   ⚠️ 保存好这个 token！
```

**步骤 2：配置 Token 到 .env**
```bash
# 编辑 .env 文件
nano .env

# 添加或修改这一行：
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
#                  ↑ 替换成你从 @BotFather 获得的 token

# 保存并退出
```

**步骤 3：启动 Bot 服务（重要）**
```bash
# 启动 Telegram Bot 服务
uv run python tests/manual/test_telegram_restricted.py

# ✅ 看到以下输出表示成功：
# Telegram Bot 启动成功！
# Bot 用户名: @myopenclaw_bot
#
# ⚠️ 保持这个终端窗口打开！
# Bot 需要持续运行才能接收和回复消息
```

**步骤 4：在 Telegram 中开始对话**
```bash
1. 在 Telegram 搜索你的 bot 用户名（@myopenclaw_bot）
2. 点击 "Start" 或发送 /start
3. 现在可以直接发消息了！

示例：
你: 你好
Bot: 你好！我是 OpenClaw 助手，有什么可以帮你的？

你: 帮我写个 Python 函数
Bot: [AI 生成并回复代码]
```

**⚠️ 重要提示：**
- Bot 服务需要**持续运行**才能接收消息
- 不要关闭启动 Bot 的终端窗口
- 如果关闭了，重新运行 `uv run python tests/manual/test_telegram_restricted.py`
- 生产环境建议使用 `screen`、`tmux` 或 `systemd` 保持后台运行

### 使用本地 Ollama（免费方案）

```bash
# 1. 安装 Ollama（如果还没安装）
# macOS/Linux:
curl -fsSL https://ollama.ai/install.sh | sh

# 2. 启动 Ollama 服务
ollama serve

# 3. 下载模型（新终端）
ollama pull llama3.2

# 4. 使用 OpenClaw（新终端）
cd openclaw-python
uv run openclaw agent chat "Hello" --model ollama/llama3.2

# 无需任何 API Key！完全本地运行
```

---

## 📖 更多文档

- **[START_HERE.md](START_HERE.md)** - 1分钟超快速入门
- **[QUICK_START.md](QUICK_START.md)** - 5分钟完整指南
- **[docs/](docs/)** - 完整技术文档

---

## 💻 Usage Examples

### Command-Line Usage

```bash
# Basic chat
uv run openclaw agent chat "What is Python?"

# With specific model
uv run openclaw agent chat "Write a function" --model anthropic/claude-opus-4-5

# Interactive mode (multi-turn conversation)
uv run openclaw agent interactive
```

### Python Script

```python
import asyncio
from openclaw.agents import AgentRuntime, Session
from pathlib import Path

async def main():
    # Create runtime (choose your provider)
    runtime = AgentRuntime(
        model="anthropic/claude-opus-4-5",  # or any model
        max_tokens=2000,
        temperature=0.7
    )
    
    # Create session
    session = Session(
        session_id="my-chat",
        workspace_dir=Path.cwd()
    )
    
    # Send message
    response = await runtime.run_turn(
        session=session,
        user_message="Hello! Introduce yourself."
    )
    
    # Stream output
    async for event in response:
        if event["type"] == "text":
            print(event["text"], end="", flush=True)

asyncio.run(main())
```

### API Server

```bash
# Start API server
uv run openclaw api start

# Access API docs at http://localhost:18789/docs
```

See [QUICK_START.md](QUICK_START.md) for more examples.

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
