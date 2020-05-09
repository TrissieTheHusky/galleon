#  Galleon — A multipurpose Discord bot.
#  Copyright (C) 2020  defracted.
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

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
