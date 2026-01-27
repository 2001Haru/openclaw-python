"""teams channel plugin"""

from clawdbot.channels.teams import TeamsChannel
from clawdbot.channels.registry import get_channel_registry


def register(api):
    """Register teams channel"""
    channel = TeamsChannel()
    registry = get_channel_registry()
    registry.register(channel)
