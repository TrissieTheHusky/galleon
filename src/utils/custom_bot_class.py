from discord.ext.commands import AutoShardedBot
from discord import User, TextChannel
from typing import Dict, Optional

from src.utils.database import Database


class DefraBot(AutoShardedBot):
    def __init__(self, command_prefix, **options):
        super().__init__(command_prefix, **options)
        self.prefixes: Dict[int, str] = {}
        self.timezones: Dict[int, str] = {}

        self.owner: Optional[User] = None
        self.dev_channel: Optional[TextChannel] = None

    async def update_timezone(self, guild_id: int):
        """
        Updates Guild's timezone in bot's cache

        :param guild_id: Discord Guild ID
        """
        tz = await Database.get_timezone(guild_id)
        self.timezones.update({guild_id: tz})
        print(f"[CACHE] Timezone has been updated for Guild ID {guild_id}")

    async def update_prefix(self, guild_id: int):
        """
        Updates Guild's prefix in bot's cache

        :param guild_id: Discord Guild ID
        """
        prefix = await Database.get_prefix(guild_id)
        self.prefixes.update({guild_id: prefix})
        print(f"[CACHE] Prefix has been updated for Guild ID {guild_id}")
