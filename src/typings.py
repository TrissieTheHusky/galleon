from typing import TypedDict, Optional, Union, List
from src.utils.custom_bot_class import DefraBot
from discord import AutoShardedClient, Client
from datetime import datetime

BotType = Union[DefraBot, AutoShardedClient, Client]


class WebhookConfig(TypedDict):
    NAME: Optional[str]
    AVATAR_URL: Optional[str]
    LOGGING_URL: str


class DatabaseCredentials(TypedDict):
    USER: str
    PASSWORD: str
    DATABASE: str
    HOST: str
    PORT: Optional[str]


class ConfigType(TypedDict):
    DEFAULT_TZ: str
    DEFAULT_PRESENCE: str
    DEFAULT_PREFIX: str
    DEV_LOG_CHANNEL_ID: int
    WEBHOOK: WebhookConfig
    DATABASE: Optional[DatabaseCredentials]


class InfractionRow(TypedDict):
    inf_id: int
    guild_id: int
    moderator_id: int
    target_id: int
    reason: str
    inf_type: str
    added_at: datetime
    expires_at: datetime


class GuildConfig(TypedDict):
    prefix: Optional[str]
    admin_roles: List[int]
    mod_roles: List[int]
    trusted_roles: List[int]
    mod_logs: List[int]
