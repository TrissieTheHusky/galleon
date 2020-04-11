from discord.ext.commands import AutoShardedBot
from discord import User, TextChannel
from typing import Dict, Optional


class DefraBot(AutoShardedBot):
    def __init__(self, command_prefix, **options):
        super().__init__(command_prefix, **options)
        self.prefixes: Dict[str, str] = {}
        self.owner: Optional[User] = None
        self.dev_log_channel: Optional[TextChannel] = None
