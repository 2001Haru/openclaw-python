# Contributing to ClawdBot Python

Thank you for your interest in contributing to ClawdBot Python!

## Development Setup

### Prerequisites

- Python 3.11+
- Poetry or pip
- Git

### Setup

```bash
# Clone repository
git clone https://github.com/yourusername/clawdbot-python.git
cd clawdbot-python

# Install dependencies
poetry install --with dev

# Or with pip
pip install -e ".[dev]"
```

## Development Workflow

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Changes

Follow the project structure:
- Tools: `clawdbot/agents/tools/`
- Channels: `clawdbot/channels/`
- Skills: `skills/`
- Extensions: `extensions/`

### 3. Code Style

```bash
# Format code
black clawdbot/
isort clawdbot/

# Lint
ruff check clawdbot/
mypy clawdbot/
```

### 4. Add Tests

```bash
# Add tests to tests/
# Run tests
pytest
```

### 5. Update Documentation

- Update relevant README sections
- Add docstrings
- Update CHANGELOG.md

### 6. Submit PR

```bash
git add .
git commit -m "Add feature: your feature"
git push origin feature/your-feature-name
```

## Contributing Guidelines

### Code Quality

- Use type hints
- Add docstrings
- Handle errors gracefully
- Log appropriately

### Testing

- Add unit tests for new features
- Ensure existing tests pass
- Test edge cases

### Documentation

- Update README for user-facing changes
- Add inline comments for complex code
- Update CHANGELOG.md

## Adding New Components

### Adding a Tool

1. Create file in `clawdbot/agents/tools/`
2. Inherit from `AgentTool`
3. Implement `get_schema()` and `execute()`
4. Register in `registry.py`
5. Add tests

Example:

```python
from .base import AgentTool, ToolResult

class MyTool(AgentTool):
    def __init__(self):
        super().__init__()
        self.name = "my_tool"
        self.description = "Tool description"
    
    def get_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "param": {"type": "string"}
            }
        }
    
    async def execute(self, params: dict) -> ToolResult:
        # Implementation
        return ToolResult(success=True, content="Result")
```

### Adding a Channel

1. Create file in `clawdbot/channels/`
2. Inherit from `ChannelPlugin`
3. Implement required methods
4. Create extension in `extensions/`
5. Add configuration schema

### Adding a Skill

1. Create directory in `skills/`
2. Create `SKILL.md` with frontmatter
3. Document usage and tools
4. Add examples

## Project Structure

```
clawdbot-python/
├── clawdbot/          # Core package
│   ├── agents/        # Agent runtime and tools
│   ├── channels/      # Channel plugins
│   ├── cli/           # CLI commands
│   ├── config/        # Configuration
│   ├── gateway/       # Gateway server
│   ├── plugins/       # Plugin system
│   ├── skills/        # Skills loader
│   └── web/           # Web UI
├── extensions/        # Extension plugins
├── skills/            # Skill definitions
├── tests/             # Test files
└── docs/              # Documentation
```

## Getting Help

- GitHub Issues: Report bugs and request features
- GitHub Discussions: Ask questions
- Documentation: Check docs/ folder

## Code of Conduct

Be respectful, inclusive, and constructive.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
