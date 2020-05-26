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

from socket import gaierror
from typing import Optional

from asyncpg.pool import Pool, create_pool

from .blacklist import SQLBlacklist
from .language import SQLLanguage
from .prefix import SQLPrefix
from .roles import SQLRoles
from .temp_actions import SQLTempActions
from .timezone import SQLTimezone
from ..utils.exceptions import DatabaseException
from ..utils.logger import logger


class Database:
    _pool: Optional[Pool] = None
    prefixes: Optional[SQLPrefix] = None
    timezones: Optional[SQLTimezone] = None
    languages: Optional[SQLLanguage] = None
    blacklist: Optional[SQLBlacklist] = None
    roles: Optional[SQLRoles] = None
    temp_actions: Optional[SQLTempActions] = None

    @classmethod
    async def connect(cls, credentials) -> None:
        try:
            # Creating the pool connection
            cls._pool = await create_pool(**credentials)

            # Passing the pool to the subclasses
            cls.prefixes = SQLPrefix(cls._pool)
            cls.timezones = SQLTimezone(cls._pool)
            cls.languages = SQLLanguage(cls._pool)
            cls.blacklist = SQLBlacklist(cls._pool)
            cls.roles = SQLRoles(cls._pool)
            cls.temp_actions = SQLTempActions(cls._pool)

            logger.info("[DB] Connection pool created.")
        except gaierror:
            raise DatabaseException("Unable to connect to the database")

    @classmethod
    async def execute(cls, execute_string, *args, **kwargs):
        async with cls._pool.acquire() as db:
            if kwargs.get('transaction', False):
                async with db.transaction():
                    await db.execute(execute_string, *args)
            else:
                await db.execute(execute_string, *args)

    @classmethod
    async def fetchrow(cls, query_string, *args, **kwargs):
        async with cls._pool.acquire() as db:
            if kwargs.get('transaction', False):
                async with db.transaction():
                    return await db.fetchrow(query_string, *args)
            else:
                return await db.fetchrow(query_string, *args)

    @classmethod
    async def fetch(cls, query_string, *args, **kwargs):
        async with cls._pool.acquire() as db:
            if kwargs.get('transaction', False):
                async with db.transaction():
                    return await db.fetch(query_string, *args)
            else:
                return await db.fetch(query_string, *args)

    @classmethod
    async def fetchval(cls, query_string, *args):
        async with cls._pool.acquire() as conn:
            return await conn.fetchval(query_string, *args)

    @classmethod
    async def get_pool(cls) -> Pool:
        return cls._pool

    @classmethod
    async def safe_add_guild(cls, guild_id: int):
        """Adds a guild to settings table if it's not there"""
        async with cls._pool.acquire() as db:
            async with db.transaction():
                settings = await db.fetchval("INSERT INTO bot.guilds (guild_id) VALUES ($1) ON CONFLICT DO NOTHING RETURNING True", guild_id)
                logging = await db.fetchval("INSERT INTO bot.logging_channels (guild_id) VALUES ($1) ON CONFLICT DO NOTHING RETURNING True", guild_id)
                return settings, logging
