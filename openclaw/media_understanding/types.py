"""Media Understanding types."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Literal
from enum import Enum


class MediaScope(str, Enum):
    """Scope for media understanding."""
    
    AUTO = "auto"  # Automatic based on config
    ALL = "all"  # Process all media
    IMAGES = "images"  # Only images
    AUDIO = "audio"  # Only audio
    VIDEO = "video"  # Only video
    NONE = "none"  # No media understanding


@dataclass
class MediaUnderstandingResult:
    """Result of media understanding."""
    
    media_type: Literal["image", "audio", "video"]
    url: str
    description: Optional[str] = None
    transcript: Optional[str] = None
    error: Optional[str] = None
    provider: Optional[str] = None
    model: Optional[str] = None
