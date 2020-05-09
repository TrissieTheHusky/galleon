#  Copyright (c) 2020 defracted
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import Optional

from discord import User, TextChannel
from discord.ext.commands import AutoShardedBot

from .cache import Cache
from .configuration import cfg
from .database import Database
from .logger import logger
from .infractions import Infractions


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
        self.infraction = Infractions

    async def refresh_cache(self):
        # General data cache
        await self.cache.refresh_blacklist()

        # Guild related cache
        for guild in self.guilds:
            await self.cache.refresh_language(guild.id)
            await self.cache.refresh_prefix(guild.id)
            await self.cache.refresh_timezone(guild.id)
