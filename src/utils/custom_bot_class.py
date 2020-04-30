from typing import Dict, Optional

from discord import User, TextChannel
from discord.ext.commands import AutoShardedBot

from src.utils.configuration import cfg
from src.utils.database import Database


class DefraBot(AutoShardedBot):
    def __init__(self, command_prefix, **options):
        super().__init__(command_prefix, **options)
        self.cfg = cfg
        self.prefixes: Dict[int, str] = {}
        self.owner: Optional[User] = None
        self.dev_channel: Optional[TextChannel] = None

    async def update_prefix(self, guild_id: int):
        """
        Updates Guild's prefix in bot's cache

        :param guild_id: Discord Guild ID
        """
        prefix = await Database.get_prefix(guild_id)
        self.prefixes.update({guild_id: prefix})
        print(f"[CACHE] Prefix has been updated for Guild ID {guild_id}")
