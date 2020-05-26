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

from typing import MutableSet, Dict
from collections import namedtuple

from src.database import Database
from src.utils.logger import logger

CacheStruct = namedtuple('CacheStruct', 'prefix language timezone mod_roles admin_roles mute_role')


class Cache:
    guilds: Dict[int, CacheStruct] = {}
    blacklisted_users: MutableSet[int] = set()

    @classmethod
    async def refresh(cls, guild_id: int):
        row = await Database.fetchrow("SELECT * FROM bot.guilds WHERE guild_id = $1", guild_id)
        cls.guilds.update({
            guild_id: CacheStruct(row['prefix'], row['language'], row['_timezone'], row['mod_roles'], row['admin_roles'], row['mute_role'])
        })
        print("[CACHE] Refreshed settings data for Guild {0}".format(guild_id))

    @classmethod
    async def refresh_blacklist(cls):
        db_blacklist = await Database.blacklist.get()
        for row in db_blacklist:
            cls.blacklisted_users.add(row['user_id'])
        logger.info(f"Blacklist cache has been refreshed")
