from typing import Optional

from discord import User, TextChannel
from discord.ext.commands import AutoShardedBot

from src.utils.cache import Cache
from src.utils.configuration import cfg
from src.utils.database import Database
from src.utils.logger import logger


class DefraBot(AutoShardedBot):
    def __init__(self, command_prefix, **options):
        super().__init__(command_prefix, **options)
        self.owner: Optional[User] = None
        self.dev_channel: Optional[TextChannel] = None
        self.logger = logger
        self.primary_color = 0x008081

        self.cfg = cfg
        self.cache = Cache
        self.db = Database

    async def refresh_cache(self):
        for guild in self.guilds:
            await self.cache.refresh_language(guild.id)
            await self.cache.refresh_prefix(guild.id)
            await self.cache.refresh_timezone(guild.id)
