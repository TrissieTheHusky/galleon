"""
The MIT License (MIT)

Copyright (c) 2020 defracted

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from datetime import datetime
from typing import TypedDict, Optional, List


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


class ConfigApiKeys(TypedDict):
    CATS: str
    YANDEX: str


class ConfigType(TypedDict):
    DEFAULT_TZ: str
    DEFAULT_PRESENCE: str
    DEFAULT_PREFIX: str
    DEV_LOG_CHANNEL_ID: int
    SHARD_COUNT: int
    SHARD_IDS: List[int]
    COGS: List[str]
    WEBHOOK: WebhookConfig
    DATABASE: Optional[DatabaseCredentials]
    KARMA_PHRASES: List[str]
    API_KEYS: ConfigApiKeys


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
    _timezone: str  # UTC by default
