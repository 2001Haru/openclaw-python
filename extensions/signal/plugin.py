"""Signal channel plugin"""

from clawdbot.channels.signal import SignalChannel
from clawdbot.channels.registry import get_channel_registry


def register(api):
    """Register Signal channel"""
    channel = SignalChannel()
    registry = get_channel_registry()
    registry.register(channel)
