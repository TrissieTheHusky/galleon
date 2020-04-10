from discord.ext.commands import AutoShardedBot
from discord import User, TextChannel
from typing import Dict, Union


class DefraBot(AutoShardedBot):
    def __init__(self, command_prefix, **options):
        super().__init__(command_prefix, **options)
        self.prefixes: Dict[str, str] = {}
        self.owner: Union[User, None] = None
        self.dev_log_channel: Union[TextChannel, None] = None
