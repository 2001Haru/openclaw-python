"""Link Understanding - Automatic URL detection and content extraction."""

from __future__ import annotations

from .detect import detect_urls
from .fetch import fetch_url_content
from .format import format_url_content
from .apply import apply_link_understanding

__all__ = [
    "detect_urls",
    "fetch_url_content",
    "format_url_content",
    "apply_link_understanding",
]
