from typing import TypedDict, Optional, Union
from src.utils.custom_bot_class import DefraBot
from discord import AutoShardedClient, Client


class WebhookConfig(TypedDict):
    NAME: Optional[str]
    AVATAR_URL: Optional[str]
    LOGGING_URL: str


class ConfigType(TypedDict):
    DEFAULT_PRESENCE: str
    DEFAULT_PREFIX: str
    DEV_LOG_CHANNEL_ID: int
    WEBHOOK: WebhookConfig


BotType = Union[DefraBot, AutoShardedClient, Client]
