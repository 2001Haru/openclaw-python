# OpenClaw 工具与 Skills 系统对比分析

## 🎯 概述

本文档分析 TypeScript OpenClaw 的工具加载和 Skills 系统架构，对比 Python 版本的实现现状，并提供完整的实现建议。

**分析日期**: 2026-02-06  
**用户需求**: "看一下之前项目如何加载工具调用skills及其他用法，看一下现在我们的项目是否有类似实现。要完整理解整个流程"

## 📚 TypeScript OpenClaw 架构

### 1. 工具系统 (Tools System)

#### 1.1 工具定义层次

```typescript
// src/agents/tools/common.ts
export type AnyAgentTool = AgentTool<any, unknown>;

// 工具基础接口 (from @mariozechner/pi-agent-core)
interface AgentTool<TParams, TResult> {
  name: string;
  description: string;
  parameters: TypeSchema;
  execute: (toolCallId: string, params: TParams) => Promise<AgentToolResult<TResult>>;
}
```

#### 1.2 工具注册机制

**TypeScript Plugin Registry** (`src/plugins/registry.ts`):

```typescript
export type PluginToolRegistration = {
  pluginId: string;
  factory: OpenClawPluginToolFactory;
  names: string[];        // 工具别名
  optional: boolean;      // 可选工具
  source: string;         // 来源标识
};

export type PluginRegistry = {
  plugins: PluginRecord[];
  tools: PluginToolRegistration[];
  hooks: PluginHookRegistration[];
  channels: PluginChannelRegistration[];
  providers: PluginProviderRegistration[];
  gatewayHandlers: GatewayRequestHandlers;
  httpHandlers: PluginHttpRegistration[];
  httpRoutes: PluginHttpRouteRegistration[];
  cliRegistrars: PluginCliRegistration[];
  services: PluginServiceRegistration[];
  commands: PluginCommandRegistration[];
  diagnostics: PluginDiagnostic[];
};
```

**工具工厂模式**:

```typescript
export type OpenClawPluginToolFactory = (
  ctx: OpenClawPluginToolContext,
) => AnyAgentTool | AnyAgentTool[] | null | undefined;

export type OpenClawPluginToolContext = {
  config?: OpenClawConfig;
  workspaceDir?: string;
  agentDir?: string;
  agentId?: string;
  sessionKey?: string;
  messageChannel?: string;
  agentAccountId?: string;
  sandboxed?: boolean;
};
```

#### 1.3 核心工具列表

TypeScript 版本包含的工具 (`src/agents/tools/`):

1. **文件操作**: `read_file`, `write_file`, `edit_file`, `patch`
2. **执行**: `bash`, `process`
3. **Web**: `web_fetch`, `web_search`, `readability`
4. **会话**: `sessions_list`, `sessions_send`, `sessions_spawn`, `sessions_history`
5. **浏览器**: `browser` (自动化)
6. **图片**: `image` (视觉模型)
7. **语音**: `tts`, `voice_call`
8. **定时**: `cron`
9. **平台动作**: `telegram_actions`, `discord_actions`, `slack_actions`, `whatsapp_actions`
10. **其他**: `canvas`, `nodes`, `message`, `gateway`

### 2. Skills 系统 (Skills System)

#### 2.1 Skills 定义

**Skill 结构** (from `@mariozechner/pi-coding-agent`):

```typescript
export type Skill = {
  name: string;
  description: string;
  location: string;      // SKILL.md 文件路径
};

export type SkillEntry = {
  skill: Skill;
  frontmatter: ParsedSkillFrontmatter;  // YAML frontmatter
  metadata?: OpenClawSkillMetadata;      // OpenClaw 元数据
  invocation?: SkillInvocationPolicy;    // 调用策略
};
```

#### 2.2 Skill Metadata

**OpenClawSkillMetadata** (`src/agents/skills/types.ts`):

```typescript
export type OpenClawSkillMetadata = {
  always?: boolean;           // 总是包含
  skillKey?: string;          // 唯一标识
  primaryEnv?: string;        // 主要环境变量
  emoji?: string;             // 图标
  homepage?: string;          // 主页
  os?: string[];              // 支持的操作系统
  requires?: {
    bins?: string[];          // 需要的二进制文件
    anyBins?: string[];       // 需要任一二进制文件
    env?: string[];           // 需要的环境变量
    config?: string[];        // 需要的配置
  };
  install?: SkillInstallSpec[];  // 安装说明
};
```

#### 2.3 Skills 加载流程

**核心流程** (`src/agents/skills/workspace.ts`):

```typescript
export function loadWorkspaceSkillEntries(
  workspaceDir: string,
  opts?: {
    config?: OpenClawConfig;
    managedSkillsDir?: string;
    bundledSkillsDir?: string;
  },
): SkillEntry[]
```

**加载源优先级**:

1. **Workspace Skills** (`{workspace}/skills/`) - 最高优先级
2. **Managed Skills** (`~/.openclaw/skills/`) - 用户安装的 skills
3. **Plugin Skills** - 插件提供的 skills
4. **Extra Dirs** - 配置的额外目录
5. **Bundled Skills** - 内置 skills

**合并策略**:
- Workspace skills 优先于 managed skills
- 同名 skill，后加载的覆盖先加载的
- 支持 skill 过滤（通过配置）

#### 2.4 Skills 目录结构

```
skills/
├── skill-name/
│   ├── SKILL.md           # Skill 定义（必须）
│   ├── package.json       # Node.js 依赖（可选）
│   ├── pyproject.toml     # Python 依赖（可选）
│   └── scripts/           # 辅助脚本（可选）
└── another-skill/
    └── SKILL.md
```

**SKILL.md 格式**:

```markdown
---
name: skill-name
description: Skill description
openclaw:
  always: false
  emoji: "🔧"
  requires:
    bins: ["git"]
  install:
    - kind: brew
      formula: git
---

# Skill Name

## Usage

Instructions for the AI agent...
```

#### 2.5 Skills 在 Prompt 中的使用

**System Prompt 集成** (`src/agents/system-prompt.ts`):

```typescript
const skillsSection = [
  "## Available Skills",
  "",
  "Skills are located in the workspace `skills/` directory:",
  "",
  skillsList,
  "",
  "Usage:",
  "- If exactly one skill clearly applies: read its SKILL.md at <location> with `Read`, then follow it.",
  "- If multiple skills might apply: ask user which to use.",
  "- If none clearly apply: do not read any SKILL.md.",
].join("\n");
```

**Skills Snapshot** (`src/agents/skills/types.ts`):

```typescript
export type SkillSnapshot = {
  prompt: string;                              // 格式化后的 prompt
  skills: Array<{ name: string; primaryEnv?: string }>;
  resolvedSkills?: Skill[];                    // 解析后的 skills
  version?: number;                            // 快照版本
};
```

#### 2.6 Skill Command Dispatch

**命令分发** (`src/agents/skills/types.ts`):

```typescript
export type SkillCommandSpec = {
  name: string;              // 命令名（如 /skill-name）
  skillName: string;         // 对应的 skill 名称
  description: string;       // 描述
  dispatch?: {
    kind: "tool";           // 分发到工具
    toolName: string;       // 工具名称
    argMode?: "raw";        // 参数模式
  };
};
```

**用例**: 将聊天命令 `/summarize` 分发到 `summarize` skill，再调用特定工具。

### 3. Plugin 系统

#### 3.1 Plugin 类型

```typescript
export type PluginKind = "memory";

export type PluginRecord = {
  id: string;
  name: string;
  version?: string;
  description?: string;
  kind?: PluginKind;
  source: string;              // 插件来源
  origin: PluginOrigin;        // internal | workspace | remote
  workspaceDir?: string;
  enabled: boolean;
  status: "loaded" | "disabled" | "error";
  toolNames: string[];         // 提供的工具
  hookNames: string[];         // 注册的钩子
  channelIds: string[];        // 提供的频道
  providerIds: string[];       // 提供的 provider
  gatewayMethods: string[];    // Gateway 方法
  cliCommands: string[];       // CLI 命令
  services: string[];          // 服务
  commands: string[];          // 命令
  httpHandlers: number;        // HTTP handlers
  hookCount: number;
  configSchema: boolean;
  configUiHints?: Record<string, PluginConfigUiHint>;
  configJsonSchema?: Record<string, unknown>;
};
```

#### 3.2 Plugin API

```typescript
export type OpenClawPluginApi = {
  // 工具注册
  registerTool(
    factory: OpenClawPluginToolFactory,
    options?: OpenClawPluginToolOptions,
  ): void;
  
  // 钩子注册
  registerHook(
    handler: InternalHookHandler,
    options?: OpenClawPluginHookOptions,
  ): void;
  
  // 频道注册
  registerChannel(
    plugin: ChannelPlugin,
    options?: OpenClawPluginChannelRegistration,
  ): void;
  
  // Provider 注册
  registerProvider(provider: ProviderPlugin): void;
  
  // Gateway 方法注册
  registerGatewayMethod(
    method: string,
    handler: GatewayRequestHandler,
  ): void;
  
  // HTTP 路由注册
  registerHttpRoute(
    path: string,
    handler: OpenClawPluginHttpRouteHandler,
  ): void;
  
  // CLI 命令注册
  registerCli(registrar: OpenClawPluginCliRegistrar): void;
  
  // 服务注册
  registerService(service: OpenClawPluginService): void;
  
  // 命令注册
  registerCommand(command: OpenClawPluginCommandDefinition): void;
};
```

### 4. 工具策略系统

#### 4.1 工具别名和分组

**从 TypeScript `tool_policy.py` 对应**:

```typescript
const TOOL_NAME_ALIASES = {
  'Read': 'read_file',
  'Write': 'write_file',
  // ... more aliases
};

const TOOL_GROUPS = {
  'file_ops': ['read_file', 'write_file', 'edit_file'],
  'web': ['web_fetch', 'web_search', 'readability'],
  'sessions': ['sessions_list', 'sessions_send', 'sessions_spawn'],
  // ... more groups
};
```

#### 4.2 工具配置文件

**Tool Profiles** (`tool_policy.py` 已实现):

- `minimal`: 最小工具集
- `coding`: 编码工具集
- `messaging`: 消息工具集
- `full`: 完整工具集

#### 4.3 Owner-Only 工具

```typescript
const OWNER_ONLY_TOOL_NAMES = [
  'bash',
  'process',
  'cron',
  'browser',
  'voice_call',
  // ... dangerous tools
];
```

## 📊 Python 版本现状对比

### ✅ 已实现功能

#### 1. 基础工具系统

**Python Implementation** (`openclaw/agents/tools/`):

✅ **工具基类** (`base.py`):
```python
class AgentTool(ABC):
    name: str
    description: str
    required_permissions: set[ToolPermission]
    
    @abstractmethod
    def get_schema(self) -> dict[str, Any]:
        pass
    
    async def execute(self, params: dict[str, Any]) -> ToolResult:
        pass
```

✅ **工具注册表** (`registry.py`):
```python
class ToolRegistry:
    def register(self, tool: AgentTool) -> None
    def get(self, name: str) -> AgentTool | None
    def list_tools(self) -> list[AgentTool]
    def get_tools_by_profile(self, profile: str) -> list[AgentTool]
```

✅ **已实现的工具**:
- ✅ 文件操作: `read_file`, `write_file`, `edit_file`
- ✅ 执行: `bash`
- ✅ Web: `web_fetch`, `web_search`
- ✅ 图片: `image`
- ✅ 会话: `sessions_list`, `sessions_send`, `sessions_spawn`, `sessions_history`
- ✅ 浏览器: `browser`
- ✅ 定时: `cron`
- ✅ 语音: `tts`, `voice_call`
- ✅ 平台动作: `telegram_actions`, `discord_actions`, `slack_actions`, `whatsapp_actions`
- ✅ 其他: `canvas`, `nodes`, `process`, `patch`

#### 2. 工具策略系统

✅ **Tool Policy** (`security/tool_policy.py`):
- ✅ 工具别名映射
- ✅ 工具分组
- ✅ 工具配置文件
- ✅ Owner-only 限制
- ✅ 工具策略解析

#### 3. 权限和安全

✅ **Permission System** (`tools/base.py`):
```python
class ToolPermission(str, Enum):
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    NETWORK = "network"
    FILESYSTEM = "filesystem"
    DANGEROUS = "dangerous"
```

✅ **安全特性**:
- ✅ 超时控制
- ✅ 权限检查
- ✅ 速率限制
- ✅ 输出大小限制
- ✅ 执行指标

### ❌ 缺失功能

#### 1. Skills 系统（完全缺失）

❌ **Skills 加载**:
- ❌ 从目录加载 SKILL.md 文件
- ❌ Frontmatter 解析（YAML）
- ❌ Skill metadata 提取
- ❌ Skill 优先级和合并
- ❌ Skill 过滤和资格检查

❌ **Skills 管理**:
- ❌ Managed skills 目录 (`~/.openclaw/skills/`)
- ❌ Bundled skills 支持
- ❌ Plugin skills 集成
- ❌ Skill 安装规范

❌ **Skills Prompt 生成**:
- ❌ `formatSkillsForPrompt` 等价实现
- ❌ Skills snapshot 生成
- ❌ System prompt 中的 skills 部分

❌ **Skill Commands**:
- ❌ Skill command dispatch
- ❌ 聊天命令到 skill 的映射

#### 2. Plugin 系统（部分缺失）

❌ **Plugin Registry**:
- ❌ 完整的 plugin 注册机制
- ❌ Plugin 工具工厂
- ❌ Plugin 钩子系统
- ❌ Plugin HTTP handlers
- ❌ Plugin CLI registrars

⚠️ **部分实现**:
- ✅ Channel plugins (基础)
- ❌ Provider plugins
- ❌ Service plugins

#### 3. 工具上下文（部分缺失）

⚠️ **ToolContext**:
```python
# TypeScript 有完整的上下文
OpenClawPluginToolContext = {
  config, workspaceDir, agentDir, agentId,
  sessionKey, messageChannel, agentAccountId, sandboxed
}

# Python 缺少统一的上下文传递机制
```

#### 4. 动态工具加载（缺失）

❌ **Tool Factory Pattern**:
- ❌ 工具工厂函数
- ❌ 基于上下文的工具创建
- ❌ 可选工具机制

## 🚀 实现建议

### Phase 1: Skills 核心系统

#### 1.1 创建 Skills 模块结构

```python
openclaw/agents/skills/
├── __init__.py
├── types.py              # Skill 类型定义
├── loader.py             # Skill 加载器
├── frontmatter.py        # YAML frontmatter 解析
├── workspace.py          # Workspace skills 管理
├── bundled.py            # Bundled skills
├── metadata.py           # OpenClaw metadata
└── prompt.py             # Skills prompt 生成
```

#### 1.2 核心类型定义

```python
# openclaw/agents/skills/types.py
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

@dataclass
class Skill:
    """Skill definition (matches pi-coding-agent)."""
    name: str
    description: str
    location: str  # Path to SKILL.md

@dataclass
class SkillInstallSpec:
    """Installation specification."""
    kind: str  # brew | node | go | uv | download
    id: str | None = None
    label: str | None = None
    bins: list[str] | None = None
    os: list[str] | None = None
    formula: str | None = None
    package: str | None = None
    module: str | None = None
    url: str | None = None

@dataclass
class OpenClawSkillMetadata:
    """OpenClaw-specific metadata."""
    always: bool = False
    skill_key: str | None = None
    primary_env: str | None = None
    emoji: str | None = None
    homepage: str | None = None
    os: list[str] | None = None
    requires: dict[str, list[str]] | None = None
    install: list[SkillInstallSpec] | None = None

@dataclass
class SkillEntry:
    """Skill with metadata."""
    skill: Skill
    frontmatter: dict[str, Any]
    metadata: OpenClawSkillMetadata | None = None
```

#### 1.3 Skill 加载器

```python
# openclaw/agents/skills/loader.py
from pathlib import Path

def load_skills_from_dir(
    directory: Path,
    source: str = "workspace"
) -> list[Skill]:
    """
    Load skills from directory (matches pi-coding-agent).
    
    Scans for SKILL.md files in subdirectories.
    """
    skills = []
    
    if not directory.exists():
        return skills
    
    for skill_dir in directory.iterdir():
        if not skill_dir.is_dir():
            continue
        
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            continue
        
        try:
            content = skill_file.read_text(encoding="utf-8")
            skill = parse_skill_file(skill_file, content, source)
            if skill:
                skills.append(skill)
        except Exception as e:
            logger.warning(f"Failed to load skill from {skill_dir}: {e}")
    
    return skills

def parse_skill_file(
    file_path: Path,
    content: str,
    source: str
) -> Skill | None:
    """Parse SKILL.md file."""
    # Extract frontmatter and description
    frontmatter, body = parse_frontmatter(content)
    
    name = frontmatter.get("name", file_path.parent.name)
    description = frontmatter.get("description", "")
    
    # Extract first paragraph if no description
    if not description and body:
        first_para = body.split("\n\n")[0].strip()
        description = first_para[:200]  # Limit length
    
    return Skill(
        name=name,
        description=description,
        location=str(file_path)
    )
```

#### 1.4 Frontmatter 解析

```python
# openclaw/agents/skills/frontmatter.py
import re
import yaml

def parse_frontmatter(content: str) -> tuple[dict[str, Any], str]:
    """
    Parse YAML frontmatter from markdown (matches TS parseFrontmatterBlock).
    
    Returns:
        (frontmatter_dict, body_content)
    """
    # Match ---\n...\n---
    pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)$'
    match = re.match(pattern, content, re.DOTALL)
    
    if not match:
        return {}, content
    
    yaml_content = match.group(1)
    body = match.group(2)
    
    try:
        frontmatter = yaml.safe_load(yaml_content) or {}
    except yaml.YAMLError as e:
        logger.warning(f"Failed to parse YAML frontmatter: {e}")
        return {}, content
    
    return frontmatter, body

def parse_openclaw_metadata(
    frontmatter: dict[str, Any]
) -> OpenClawSkillMetadata | None:
    """Extract OpenClaw metadata from frontmatter."""
    openclaw = frontmatter.get("openclaw", {})
    
    if not openclaw or not isinstance(openclaw, dict):
        return None
    
    return OpenClawSkillMetadata(
        always=openclaw.get("always", False),
        skill_key=openclaw.get("skillKey"),
        primary_env=openclaw.get("primaryEnv"),
        emoji=openclaw.get("emoji"),
        homepage=openclaw.get("homepage"),
        os=openclaw.get("os"),
        requires=openclaw.get("requires"),
        install=parse_install_specs(openclaw.get("install", []))
    )
```

#### 1.5 Workspace Skills 管理

```python
# openclaw/agents/skills/workspace.py
from pathlib import Path

def load_workspace_skill_entries(
    workspace_dir: Path,
    config: Any | None = None,
    managed_skills_dir: Path | None = None,
    bundled_skills_dir: Path | None = None,
) -> list[SkillEntry]:
    """
    Load skills from all sources (matches TS loadWorkspaceSkillEntries).
    
    Priority (highest first):
    1. Workspace skills ({workspace}/skills/)
    2. Managed skills (~/.openclaw/skills/)
    3. Plugin skills
    4. Extra dirs
    5. Bundled skills
    """
    all_entries = []
    
    # Load from different sources
    bundled = load_bundled_skills(bundled_skills_dir)
    extra = load_extra_skills(config)
    managed = load_managed_skills(managed_skills_dir)
    workspace = load_workspace_skills(workspace_dir)
    
    # Merge with priority (workspace overrides managed overrides bundled)
    entries_by_name = {}
    
    for entry in bundled + extra + managed + workspace:
        entries_by_name[entry.skill.name] = entry
    
    return list(entries_by_name.values())

def format_skills_for_prompt(skills: list[Skill]) -> str:
    """
    Format skills for system prompt (matches pi-coding-agent).
    
    Returns formatted string like:
    - skill-name: Description (location: /path/to/SKILL.md)
    """
    lines = []
    for skill in skills:
        line = f"- {skill.name}: {skill.description}"
        if skill.location:
            line += f" (location: {skill.location})"
        lines.append(line)
    
    return "\n".join(lines)
```

### Phase 2: Skills Prompt 集成

#### 2.1 System Prompt 集成

```python
# openclaw/agents/system_prompt_sections.py
def build_skills_section(
    workspace_dir: Path,
    config: Any | None = None,
    read_tool_name: str = "read_file"
) -> str:
    """Build skills section for system prompt."""
    skill_entries = load_workspace_skill_entries(workspace_dir, config)
    
    if not skill_entries:
        return ""
    
    skills = [entry.skill for entry in skill_entries]
    skills_list = format_skills_for_prompt(skills)
    
    return f"""## Available Skills

Skills are located in the workspace `skills/` directory:

{skills_list}

Usage:
- If exactly one skill clearly applies: read its SKILL.md at <location> with `{read_tool_name}`, then follow it.
- If multiple skills might apply: ask user which to use.
- If none clearly apply: do not read any SKILL.md.
"""
```

### Phase 3: Plugin 系统增强

#### 3.1 Plugin Registry

```python
# openclaw/plugins/registry.py
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable

@dataclass
class PluginToolRegistration:
    """Tool registration from plugin."""
    plugin_id: str
    factory: Callable[[ToolContext], AgentTool | list[AgentTool] | None]
    names: list[str]
    optional: bool = False
    source: str = ""

@dataclass
class PluginRegistry:
    """Central registry for all plugins."""
    plugins: list[PluginRecord] = field(default_factory=list)
    tools: list[PluginToolRegistration] = field(default_factory=list)
    channels: list[PluginChannelRegistration] = field(default_factory=list)
    
    def register_tool(
        self,
        plugin_id: str,
        factory: Callable[[ToolContext], AgentTool | None],
        names: list[str] | None = None,
        optional: bool = False
    ) -> None:
        """Register a tool factory."""
        self.tools.append(PluginToolRegistration(
            plugin_id=plugin_id,
            factory=factory,
            names=names or [],
            optional=optional,
            source=f"plugin:{plugin_id}"
        ))
    
    def create_tools(
        self,
        context: ToolContext
    ) -> list[AgentTool]:
        """Create all tools from factories."""
        tools = []
        
        for registration in self.tools:
            try:
                result = registration.factory(context)
                if result:
                    if isinstance(result, list):
                        tools.extend(result)
                    else:
                        tools.append(result)
            except Exception as e:
                if not registration.optional:
                    raise
                logger.warning(f"Optional tool failed: {e}")
        
        return tools
```

#### 3.2 Tool Context

```python
# openclaw/agents/tools/context.py
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

@dataclass
class ToolContext:
    """Context for tool creation (matches OpenClawPluginToolContext)."""
    config: Any | None = None
    workspace_dir: Path | None = None
    agent_dir: Path | None = None
    agent_id: str | None = None
    session_key: str | None = None
    message_channel: str | None = None
    agent_account_id: str | None = None
    sandboxed: bool = False
```

### Phase 4: Skill Commands

#### 4.1 Command Dispatch

```python
# openclaw/agents/skills/commands.py
from __future__ import annotations

from dataclasses import dataclass

@dataclass
class SkillCommandSpec:
    """Skill command specification."""
    name: str              # Command name (e.g., /summarize)
    skill_name: str        # Skill name
    description: str
    dispatch: SkillCommandDispatch | None = None

@dataclass
class SkillCommandDispatch:
    """Dispatch configuration."""
    kind: str = "tool"     # Currently only "tool"
    tool_name: str = ""    # Tool to invoke
    arg_mode: str = "parsed"  # "raw" | "parsed"

def build_skill_commands(
    skill_entries: list[SkillEntry]
) -> list[SkillCommandSpec]:
    """Build command specs from skills."""
    commands = []
    
    for entry in skill_entries:
        # Extract commands from skill metadata
        frontmatter = entry.frontmatter
        commands_spec = frontmatter.get("commands", [])
        
        for cmd_spec in commands_spec:
            commands.append(SkillCommandSpec(
                name=cmd_spec.get("name", entry.skill.name),
                skill_name=entry.skill.name,
                description=cmd_spec.get("description", entry.skill.description),
                dispatch=parse_dispatch(cmd_spec.get("dispatch"))
            ))
    
    return commands
```

## 📋 实现路线图

### Stage 1: Skills 基础 (高优先级)

1. ✅ 创建 `openclaw/agents/skills/` 模块
2. ✅ 实现 `types.py` - 核心类型
3. ✅ 实现 `frontmatter.py` - YAML 解析
4. ✅ 实现 `loader.py` - 基础加载
5. ✅ 实现 `workspace.py` - Workspace 管理
6. ✅ 实现 `prompt.py` - Prompt 格式化

### Stage 2: Skills 集成 (高优先级)

7. ✅ 集成到 `system_prompt_sections.py`
8. ✅ 添加 skills 配置到 `OpenClawConfig`
9. ✅ 实现 skill 过滤和资格检查
10. ✅ 测试完整流程

### Stage 3: Plugin 系统增强 (中优先级)

11. ✅ 创建 `openclaw/plugins/` 模块
12. ✅ 实现 `registry.py` - Plugin registry
13. ✅ 实现 `ToolContext` 和工具工厂
14. ✅ 重构现有工具使用工厂模式

### Stage 4: Skill Commands (中优先级)

15. ✅ 实现 command dispatch
16. ✅ 集成到聊天命令系统
17. ✅ 测试命令分发

### Stage 5: 高级特性 (低优先级)

18. ⏳ Skill installation 支持
19. ⏳ Bundled skills 打包
20. ⏳ Skill scanning 和验证
21. ⏳ Remote skills 支持

## 📊 对比总结

| 功能 | TypeScript | Python | 状态 |
|------|-----------|--------|------|
| **工具系统** | ✓ | ✓ | ✅ 基本对齐 |
| 工具注册 | ✓ | ✓ | ✅ 完成 |
| 工具策略 | ✓ | ✓ | ✅ 完成 |
| 工具权限 | ✓ | ✓ | ✅ 完成 |
| 工具工厂 | ✓ | ✗ | ❌ 缺失 |
| **Skills 系统** | ✓ | ✗ | ❌ 完全缺失 |
| SKILL.md 加载 | ✓ | ✗ | ❌ 缺失 |
| Frontmatter 解析 | ✓ | ✗ | ❌ 缺失 |
| Skills prompt | ✓ | ✗ | ❌ 缺失 |
| Skill commands | ✓ | ✗ | ❌ 缺失 |
| Skill 合并策略 | ✓ | ✗ | ❌ 缺失 |
| **Plugin 系统** | ✓ | ⚠️ | ⚠️ 部分实现 |
| Plugin registry | ✓ | ✗ | ❌ 缺失 |
| Tool factory | ✓ | ✗ | ❌ 缺失 |
| Hook 系统 | ✓ | ✗ | ❌ 缺失 |
| HTTP handlers | ✓ | ✗ | ❌ 缺失 |

## 🎯 关键差异

### 1. 架构设计

**TypeScript**:
- 插件化架构
- 工厂模式创建工具
- 统一的注册表
- 动态加载和卸载

**Python**:
- 静态工具注册
- 直接实例化工具
- 缺少插件框架
- 缺少动态能力

### 2. Skills 理念

**TypeScript**:
- Skills 是可重用的指令集
- 存储为 SKILL.md 文件
- 可以从多个源加载
- 与工具系统解耦

**Python**:
- 完全缺失 skills 概念
- 所有逻辑硬编码在工具中

### 3. 扩展性

**TypeScript**:
- 插件可以注册工具、钩子、频道等
- 工厂模式支持动态创建
- 配置驱动

**Python**:
- 扩展需要修改核心代码
- 缺少插件 API

## 💡 实现建议总结

### 优先级 1 (必须实现)

1. **Skills 核心系统**
   - SKILL.md 加载
   - Frontmatter 解析
   - Workspace 管理
   - Prompt 生成

2. **System Prompt 集成**
   - Skills section 生成
   - 与现有 prompt 系统集成

### 优先级 2 (重要)

3. **Plugin Registry**
   - 工具工厂模式
   - ToolContext 传递
   - 动态工具创建

4. **Skill Commands**
   - Command dispatch
   - 与聊天命令集成

### 优先级 3 (可选)

5. **高级 Skills 特性**
   - Skill installation
   - Bundled skills
   - Remote skills

6. **完整 Plugin 系统**
   - Hook 系统
   - HTTP handlers
   - CLI registrars

---

**总结**: Python 版本具有完整的工具系统和安全策略，但**完全缺失 Skills 系统和完整的 Plugin 架构**。建议优先实现 Skills 核心系统，以实现与 TypeScript 版本的功能对齐。
