"""TUI type definitions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class TUIOptions:
    """Options for TUI."""
    
    agent_id: str = "default"
    session_key: Optional[str] = None
    workspace_dir: Optional[str] = None
    config_path: Optional[str] = None
