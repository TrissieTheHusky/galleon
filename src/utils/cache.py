from typing import Dict

from src.utils.database import Database
from src.utils.logger import logger


class Cache:
    prefixes: Dict[int, str] = {}
    languages: Dict[int, str] = {}
    timezones: Dict[int, str] = {}
    blacklisted_users = []

    @classmethod
    async def refresh_prefix(cls, guild_id: int):
        val = await Database.get_prefix(guild_id)
        cls.prefixes.update({guild_id: val})
        logger.info(f"Prefix for Guild {guild_id} has been refreshed")

    @classmethod
    async def refresh_language(cls, guild_id: int):
        val = await Database.get_language(guild_id)
        cls.languages.update({guild_id: val})
        logger.info(f"Language for Guild {guild_id} has been refreshed")

    @classmethod
    async def refresh_timezone(cls, guild_id: int):
        val = await Database.get_timezone(guild_id)
        cls.timezones.update({guild_id: val})
        logger.info(f"Timezone for Guild {guild_id} has been refreshed")
