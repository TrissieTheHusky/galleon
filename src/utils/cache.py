#  Copyright (c) 2020 defracted
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

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
