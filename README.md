# ClawdBot Python

**Personal AI Assistant Platform - Complete Python Implementation**

This is a complete Python clone of [ClawdBot](https://github.com/badlogic/clawdbot), ported from TypeScript.

ClawdBot is a local-first AI assistant platform that connects to multiple messaging channels (WhatsApp, Telegram, Discord, Slack, etc.) and provides AI assistant services through these channels.

## About This Project

- **Original Project**: [ClawdBot (TypeScript)](https://github.com/badlogic/clawdbot)
- **Python Implementation**: Feature-complete port
- **Created**: 2026-01-27
- **Version**: 0.3.0
- **License**: MIT
- **Feature Completeness**: 100% (compared to TypeScript version)

## Highlights (v0.3.0)

- ✅ **24 Tools** - Complete tool parity including Browser, Cron, TTS, Image, Memory, Patch
- ✅ **17 Channels** - Full channel support: Telegram, Discord, Slack, WhatsApp, Signal, Teams, LINE, iMessage, Matrix, Mattermost, and more
- ✅ **52 Skills** - Complete skills library: Notion, Obsidian, Spotify, Trello, 1Password, Apple Notes, Tmux, and many more
- ✅ **OpenAI-Compatible API** - `/v1/chat/completions` endpoint
- ✅ **LanceDB Memory** - Full vector search
- ✅ **Playwright Automation** - Browser control and testing

## Features

- **Multi-Channel Support**: WhatsApp, Telegram, Discord, Slack, WebChat, and more
- **Local-First**: Runs on your hardware, keeps your data private
- **Gateway Architecture**: Single WebSocket control plane for all clients
- **Agent Runtime**: Streaming LLM responses with tool calling
- **58+ Skills**: Pre-built capabilities for common tasks
- **Plugin System**: Extensible architecture for custom channels and tools
- **Web UI**: Control panel and WebChat interface

## Quick Start

### Installation

```bash
# Install with poetry
poetry install

# Or with pip
pip install -e .
```

### Setup

```bash
# Run onboarding wizard
clawdbot onboard

# Start gateway
clawdbot gateway start
```

### Usage

```bash
# Run agent turn
clawdbot agent --message "Hello!"

# Manage channels
clawdbot channels list
clawdbot channels login telegram

# Check status
clawdbot status
```

## Architecture

```
Messaging Channels → Gateway (WebSocket) → Agent Runtime → LLM
                                ↓
                            CLI/Web UI
```

## Development

```bash
# Install dev dependencies
poetry install --with dev

# Run tests
pytest

# Format code
black clawdbot/
ruff check clawdbot/
```

## License

MIT License
