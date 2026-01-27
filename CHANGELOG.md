# Changelog

All notable changes to ClawdBot Python will be documented in this file.

## [0.3.0] - 2026-01-27

### Added - 100% Feature Parity Achieved

#### Final Tools (2 additional tools)
- **apply_patch** - Apply unified diff patches to files
- **whatsapp_actions** - WhatsApp-specific operations

#### Channel Actions - Full Implementation
- **telegram_actions** - Complete implementation (pin, unpin, delete, edit, react, forward)
- **discord_actions** - Complete implementation (pin, delete, edit, react, create_thread)
- **slack_actions** - Complete implementation (pin, delete, edit, react, upload_file)

#### New Channels (9 additional channels)
- **iMessage** - macOS iMessage integration via AppleScript
- **BlueBubbles** - BlueBubbles server for iMessage
- **Microsoft Teams** - Teams Bot Framework integration
- **LINE** - LINE Messaging API integration
- **Zalo** - Zalo messaging (Vietnam)
- **Mattermost** - Mattermost self-hosted chat
- **Nostr** - Nostr decentralized protocol
- **Nextcloud Talk** - Nextcloud Talk integration
- **Tlon** - Urbit/Tlon integration

#### New Skills (38 additional skills)
**Productivity**: 1password, apple-reminders, bear-notes
**Communication**: bluebubbles, imsg, himalaya
**Entertainment**: gog, sonoscli, songsee
**Development**: clawdhub, mcporter, nano-pdf, skill-creator
**System**: camsnap, eightctl, goplaces, local-places, openhue, tmux
**AI/ML**: gemini, openai-image-gen, openai-whisper, sherpa-onnx-tts
**Utility**: bird, blogwatcher, food-order, gifgrep, oracle, ordercli, peekaboo, sag, session-logs, video-frames, voice-call, wacli, nano-banana-pro

### Changed
- Version updated to 0.3.0
- Complete documentation translation to English
- Updated verification scripts for 100% coverage

### Dependencies Added
- line-bot-sdk (LINE integration)
- mattermostdriver (Mattermost)
- botbuilder-core (Teams)
- msgraph-sdk (Teams)
- google-cloud-pubsub (Google Chat)
- google-auth (Google Chat)

---

## [0.2.0] - 2026-01-27

### Added - Major Feature Expansion

#### New Tools (13 additional tools)
- **Sessions Management**: sessions_list, sessions_history, sessions_send, sessions_spawn
- **Analysis & Media**: image (Vision models)
- **Advanced Tools**: browser (Playwright), cron (APScheduler), tts (OpenAI/ElevenLabs), process (psutil)
- **Special Features**: nodes, canvas, voice_call
- **Channel Actions**: message, telegram_actions, discord_actions, slack_actions

#### New Channels (3 additional channels)
- Signal, Matrix, Google Chat

#### New Skills (10 additional skills)
- notion, obsidian, spotify-player, trello, slack, discord-adv, apple-notes, things-mac, summarize, model-usage

#### HTTP API Enhancements
- OpenAI-compatible API: POST /v1/chat/completions
- Tool invocation API: POST /tools/invoke
- Models endpoint: GET /api/models
- Tools endpoint: GET /api/tools

#### Memory System
- LanceDB integration
- Sentence Transformers embeddings
- Semantic search

---

## [0.1.0] - 2026-01-27

### Initial Release

#### Core Features
- Gateway WebSocket server
- Agent runtime (Claude + GPT-4)
- Session management
- Configuration system (Pydantic)
- CLI interface (Typer)
- Web UI (FastAPI)

#### Initial Tools (6)
- read_file, write_file, edit_file
- bash
- web_fetch, web_search

#### Initial Channels (5)
- Telegram, Discord, Slack
- WhatsApp (framework)
- WebChat

#### Initial Skills (4)
- coding-agent, github, weather, web-search

---

## Version History

- **0.3.0** (2026-01-27): 100% Feature Parity - All tools, channels, skills complete
- **0.2.0** (2026-01-27): Major Expansion - Advanced tools and features
- **0.1.0** (2026-01-27): Initial Release - Core functionality
