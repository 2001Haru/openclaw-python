"""Hook type definitions.

Aligned with TypeScript src/hooks/types.ts
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Literal, Callable, Any, Awaitable
from pathlib import Path


@dataclass
class HookInstallSpec:
    """Installation specification for a hook."""
    
    id: Optional[str] = None
    kind: Literal["bundled", "npm", "git"] = "bundled"
    label: Optional[str] = None
    package: Optional[str] = None
    repository: Optional[str] = None
    bins: Optional[list[str]] = None


@dataclass
class OpenClawHookMetadata:
    """OpenClaw-specific hook metadata from HOOK.md frontmatter."""
    
    events: list[str] = field(default_factory=list)  # Events this hook handles
    always: bool = False  # Always load this hook
    hook_key: Optional[str] = None
    emoji: Optional[str] = None
    homepage: Optional[str] = None
    export: str = "default"  # Export name (default: "default")
    os: Optional[list[str]] = None  # Supported OS
    requires: Optional[dict[str, Any]] = None  # Requirements
    install: Optional[list[HookInstallSpec]] = None


@dataclass
class HookInvocationPolicy:
    """Hook invocation policy."""
    
    enabled: bool = True


HookSource = Literal[
    "openclaw-bundled",
    "openclaw-managed",
    "openclaw-workspace",
    "openclaw-plugin"
]


@dataclass
class Hook:
    """A hook definition."""
    
    name: str
    description: str
    source: HookSource
    plugin_id: Optional[str] = None
    file_path: str = ""  # Path to HOOK.md
    base_dir: str = ""  # Directory containing hook
    handler_path: str = ""  # Path to handler module


@dataclass
class HookEntry:
    """Hook entry with metadata."""
    
    hook: Hook
    frontmatter: dict[str, str] = field(default_factory=dict)
    metadata: Optional[OpenClawHookMetadata] = None
    invocation: Optional[HookInvocationPolicy] = None


@dataclass
class HookEligibilityContext:
    """Context for determining hook eligibility."""
    
    remote: Optional[dict[str, Any]] = None


@dataclass
class HookSnapshot:
    """Snapshot of current hooks state."""
    
    hooks: list[dict[str, Any]] = field(default_factory=list)
    resolved_hooks: Optional[list[Hook]] = None
    version: int = 1


# Hook handler type
HookHandler = Callable[[dict[str, Any]], Awaitable[None]]
