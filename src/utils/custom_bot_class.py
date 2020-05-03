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

        self.cfg = cfg
        self.cache = Cache
        self.db = Database
