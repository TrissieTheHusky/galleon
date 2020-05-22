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

from src.utils.logger import logger
from .blacklist import DBBlacklist
from .language import DBLanguage
from .mod_roles import DBModRoles
from .modlogs import DBModlogs
from .prefix import DBPrefix
from .timezone import DBTimezone


class DatabaseException(Exception):
    pass


class Database:
    pool: Optional[Pool] = None

    prefixes: Optional[DBPrefix] = None
    timezones: Optional[DBTimezone] = None
    languages: Optional[DBLanguage] = None
    blacklist: Optional[DBBlacklist] = None
    mod_roles: Optional[DBModRoles] = None
    modlogs: Optional[DBModlogs] = None

    @classmethod
    async def connect(cls, credentials) -> None:
        try:
            # Creating the pool connection
            cls.pool = await create_pool(**credentials)

            # Passing the pool to the subclasses
            cls.prefixes = DBPrefix(cls.pool)
            cls.timezones = DBTimezone(cls.pool)
            cls.languages = DBLanguage(cls.pool)
            cls.blacklist = DBBlacklist(cls.pool)
            cls.mod_roles = DBModRoles(cls.pool)
            cls.modlogs = DBModlogs(cls.pool)

            logger.info("[DB] Connection pool created.")
        except gaierror:
            raise DatabaseException("Unable to connect to the database")

    @classmethod
    async def execute(cls, execute_string, *args, **kwargs):
        async with cls.pool.acquire() as db:
            if kwargs.get('transaction', False):
                async with db.transaction():
                    await db.execute(execute_string, *args)
            else:
                await db.execute(execute_string, *args)

    @classmethod
    async def fetch_row(cls, query_string, *args, **kwargs):
        async with cls.pool.acquire() as db:
            if kwargs.get('transaction', False):
                async with db.transaction():
                    return await db.fetchrow(query_string, *args)
            else:
                return await db.fetchrow(query_string, *args)

    @classmethod
    async def fetch(cls, query_string, *args, **kwargs):
        async with cls.pool.acquire() as db:
            if kwargs.get('transaction', False):
                async with db.transaction():
                    return await db.fetch(query_string, *args)
            else:
                return await db.fetch(query_string, *args)

    @classmethod
    async def safe_add_guild(cls, guild_id: int):
        """Adds a guild to settings table if it's not there"""
        async with cls.pool.acquire() as db:
            async with db.transaction():
                settings = await db.fetchval("INSERT INTO bot.guilds (guild_id) VALUES ($1) ON CONFLICT DO NOTHING RETURNING True", guild_id)
                logging = await db.fetchval("INSERT INTO bot.logging_channels (guild_id) VALUES ($1) ON CONFLICT DO NOTHING RETURNING True", guild_id)
                return settings, logging

    @classmethod
    async def get_admin_roles(cls, guild_id: int):
        async with cls.pool.acquire() as db:
            async with db.transaction():
                return await db.fetchval("SELECT admin_roles FROM bot.guilds WHERE guild_id = $1", guild_id)

    @classmethod
    async def get_trusted_roles(cls, guild_id: int):
        async with cls.pool.acquire() as db:
            async with db.transaction():
                return await db.fetchval("SELECT trusted_roles FROM bot.guilds WHERE guild_id = $1", guild_id)
