"""tlon channel plugin"""

from clawdbot.channels.tlon import TlonChannel
from clawdbot.channels.registry import get_channel_registry


def register(api):
    """Register tlon channel"""
    channel = TlonChannel()
    registry = get_channel_registry()
    registry.register(channel)
