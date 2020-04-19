from discord.ext.commands import AutoShardedBot
from discord import User, TextChannel
from typing import Dict, Optional
from src.utils.database import Database


class DefraBot(AutoShardedBot):
    def __init__(self, command_prefix, **options):
        super().__init__(command_prefix, **options)
        self.prefixes: Dict[int, str] = {}
        self.owner: Optional[User] = None
        self.dev_log_channel: Optional[TextChannel] = None

    async def update_prefix(self, guild_id: int):
        prefix = await Database.get_prefix(guild_id)
        self.prefixes.update({guild_id: prefix})
