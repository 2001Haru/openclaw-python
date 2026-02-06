"""Hooks system for event-driven extensibility.

Aligned with TypeScript src/hooks/types.ts
"""

from __future__ import annotations

from .types import (
    Hook,
    HookEntry,
    HookSource,
    HookSnapshot,
    OpenClawHookMetadata,
    HookInstallSpec,
    HookInvocationPolicy,
)
from .loader import load_hooks_from_dir
from .workspace import load_workspace_hook_entries, build_workspace_hook_snapshot
from .registry import HookRegistry, get_hook_registry

__all__ = [
    "Hook",
    "HookEntry",
    "HookSource",
    "HookSnapshot",
    "OpenClawHookMetadata",
    "HookInstallSpec",
    "HookInvocationPolicy",
    "load_hooks_from_dir",
    "load_workspace_hook_entries",
    "build_workspace_hook_snapshot",
    "HookRegistry",
    "get_hook_registry",
]
