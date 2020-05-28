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

from typing import MutableSet, Dict, List, Optional, NamedTuple

from src.database import Database
from src.utils.logger import logger


class LoggingStruct(NamedTuple):
    misc: List[int]
    messages: List[int]
    join_leave: List[int]
    mod_actions: List[int]
    config_logs: List[int]
    server_changes: List[int]
    ignored_users: List[int]


class CacheStruct(NamedTuple):
    prefix: Optional[str]
    language: Optional[str]
    timezone: str
    mod_roles: List[int]
    admin_roles: List[int]
    mute_role: Optional[int]
    log_messages: bool
    logging: LoggingStruct


class CacheManager:
    guilds: Dict[int, CacheStruct] = {}
    blacklisted_users: MutableSet[int] = set()

    @classmethod
    async def refresh(cls, guild_id: int):
        settings = await Database.fetchrow("SELECT * FROM bot.guilds WHERE guild_id = $1", guild_id)
        logging = await Database.fetchrow("SELECT * FROM bot.logging_channels WHERE guild_id = $1", guild_id)

        def l_s_l(x: list):
            return list(set(x))

        cls.guilds.update({
            guild_id: CacheStruct(settings['prefix'], settings['language'], settings['_timezone'], settings['mod_roles'],
                                  settings['admin_roles'], settings['mute_role'], settings['log_messages'],

                                  LoggingStruct(l_s_l(logging['misc']), l_s_l(logging['messages']), l_s_l(logging['join_leave']),
                                                l_s_l(logging['mod_actions']), l_s_l(logging['config_logs']), l_s_l(logging['server_changes']),
                                                l_s_l(logging['ignored_users'])))
        })
        print("[CACHE] Refreshed settings data for Guild {0}".format(guild_id))

    @classmethod
    async def refresh_blacklist(cls):
        db_blacklist = await Database.blacklist.get()
        for row in db_blacklist:
            cls.blacklisted_users.add(row['user_id'])
        logger.info(f"Blacklist cache has been refreshed")
