from typing import Dict, Optional
from src.utils.logger import logger
from discord import User, TextChannel
from discord.ext.commands import AutoShardedBot

from src.utils.configuration import cfg
from src.utils.database import Database


class DefraBot(AutoShardedBot):
    def __init__(self, command_prefix, **options):
        super().__init__(command_prefix, **options)
        self.owner: Optional[User] = None
        self.dev_channel: Optional[TextChannel] = None

        self.cfg = cfg
        self.prefixes: Dict[int, str] = {}
        self.languages: Dict[int, str] = {}
        self.logger = logger

    async def update_language(self, guild_id: int):
        """
        Updates Guild's language data in cache

        :param guild_id: Discord Guild ID
        """
        lang = await Database.get_language(guild_id)
        self.languages.update({guild_id: lang})
        self.logger.info(f"Language cache has been updated for Guild ID {guild_id}")

    async def update_prefix(self, guild_id: int):
        """
        Updates Guild's prefix in bot's cache

        :param guild_id: Discord Guild ID
        """
        prefix = await Database.get_prefix(guild_id)
        self.prefixes.update({guild_id: prefix})
        self.logger.info(f"Prefix cache has been updated for Guild ID {guild_id}")
