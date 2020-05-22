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

from aiohttp import ClientSession
from discord import User, TextChannel, AllowedMentions
from discord.ext.commands import AutoShardedBot

from .apis import APIs
from src.cache import Cache
from .configuration import cfg
from src.database import Database
from .infractions import Infractions
from .logger import logger


class DefraBot(AutoShardedBot):
    def __init__(self, command_prefix, **options):
        super().__init__(command_prefix, allowed_mentions=AllowedMentions(everyone=False, roles=False), **options)
        self.cfg = cfg
        self.owner: Optional[User] = None
        self.dev_channel: Optional[TextChannel] = None
        self.logger = logger
        self.primary_color = 0x008081

        # We need this for data fetching
        self.aiohttp_session = ClientSession()
        self.apis = APIs(self.aiohttp_session)

        # Option for cooldown bypass
        self.owner_cd_bypass = False

        # Databases related attrs
        self.db = Database
        self.cache = Cache
        self.infraction = Infractions

    async def refresh_cache(self):
        # General data cache
        await self.cache.refresh_blacklist()

        # Guild related cache
        for guild in self.guilds:
            await self.cache.languages.refresh(guild.id)
            await self.cache.prefixes.refresh(guild.id)
            await self.cache.timezones.refresh(guild.id)
            await self.cache.mod_roles.refresh(guild.id)
            await self.cache.modlogs.refresh(guild.id)
