"""Media Understanding - Automatic audio/video/image analysis.

Aligned with TypeScript src/media-understanding/
"""

from __future__ import annotations

from .types import MediaUnderstandingResult, MediaScope
from .runner import run_media_understanding
from .apply import apply_media_understanding

__all__ = [
    "MediaUnderstandingResult",
    "MediaScope",
    "run_media_understanding",
    "apply_media_understanding",
]
