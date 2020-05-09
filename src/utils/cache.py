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

from typing import Dict, MutableSet

from src.utils.database import Database
from src.utils.logger import logger


class Cache:
    prefixes: Dict[int, str] = dict()
    languages: Dict[int, str] = dict()
    timezones: Dict[int, str] = dict()
    blacklisted_users: MutableSet[int] = set()

    @classmethod
    async def refresh_blacklist(cls):
        db_blacklist = await Database.get_blacklist()
        for row in db_blacklist:
            cls.blacklisted_users.add(row['user_id'])
        logger.info(f"Blacklist cache has been refreshed")

    @classmethod
    async def refresh_prefix(cls, guild_id: int):
        val = await Database.get_prefix(guild_id)
        cls.prefixes.update({guild_id: val})
        logger.info(f"Prefix for Guild {guild_id} has been refreshed")

    @classmethod
    async def refresh_language(cls, guild_id: int):
        val = await Database.get_language(guild_id)
        cls.languages.update({guild_id: val})
        logger.info(f"Language for Guild {guild_id} has been refreshed")

    @classmethod
    async def refresh_timezone(cls, guild_id: int):
        val = await Database.get_timezone(guild_id)
        cls.timezones.update({guild_id: val})
        logger.info(f"Timezone for Guild {guild_id} has been refreshed")
