from datetime import datetime
from random import randint
from socket import gaierror
from typing import Optional, Tuple
from src.utils.logger import logger
from asyncpg.pool import Pool, create_pool


class DatabaseException(Exception):
    pass


class Database:
    pool: Optional[Pool] = None

    @classmethod
    async def connect(cls, credentials) -> None:
        try:
            cls.pool = await create_pool(**credentials)
            logger.info("[DB] Connection pool created.")
        except gaierror:
            raise DatabaseException("Unable to connect to the database")

    @classmethod
    async def get_language(cls, guild_id: int) -> Optional[str]:
        """
        Gets guild's language

        :param guild_id: Discord Guild ID
        :return: 'en_US' if None
        """
        async with cls.pool.acquire() as db:
            guild_lang = await db.fetchval("SELECT language FROM bot.guilds WHERE guild_id = $1 LIMIT 1;", guild_id)
            return guild_lang or 'en_US'

    @classmethod
    async def set_language(cls, guild_id: int, new_lang: str):
        """
        Sets guild's language

        :param guild_id: Discord Guild ID
        :param new_lang: new lang code
        """
        async with cls.pool.acquire() as db:
            await db.execute("UPDATE bot.guilds SET language = $2 WHERE guild_id = $1;", guild_id, new_lang)

    @classmethod
    async def get_karma(cls, user_id: int) -> Tuple[Optional[int], Optional[datetime]]:
        """
        Gets users karma points and datetime when they received some

        :param user_id: Discord User ID
        :return: A tuple with amount of karma and last modification time
        """
        async with cls.pool.acquire() as db:
            row = await db.fetchrow("SELECT karma, modified_at FROM bot.karma WHERE user_id = $1 LIMIT 1;", user_id)

            if row is not None:
                return row.get('karma'), row.get('modified_at')
            else:
                return None, None

    @classmethod
    async def add_karma(cls, user_id: int, new_karma: int = None):
        """
        Adds karma points to users in database

        :param user_id: Discord User ID
        :param new_karma: New amount of karma, by default will be random integer number between 1 and 10
        """

        async with cls.pool.acquire() as db:
            query = "INSERT INTO bot.karma (user_id, karma) VALUES ($1, $2)" \
                    "ON CONFLICT (user_id) DO UPDATE SET karma = karma.karma + $2, modified_at = default;"

            if new_karma is not None:
                await db.execute(query, user_id, new_karma)
            else:
                await db.execute(query, user_id, randint(1, 10))

    @classmethod
    async def get_timezone(cls, guild_id: int) -> Optional[str]:
        """
        Gets timezone for specified Discord Guild

        :param guild_id: Discord Guild ID
        :return: Timezone string
        """
        async with cls.pool.acquire() as db:
            guild_tz = await db.fetchval("SELECT _timezone FROM bot.guilds WHERE guild_id = $1 LIMIT 1;", guild_id)
            return guild_tz

    @classmethod
    async def set_timezone(cls, guild_id: int, new_timezone: str):
        """
        Sets timezone for specified Discord Guild

        :param guild_id: Discord Guild ID
        :param new_timezone: Timezone string
        """
        async with cls.pool.acquire() as db:
            await db.execute("UPDATE bot.guilds SET _timezone = $2 WHERE guild_id = $1;",
                             guild_id,
                             new_timezone)

    @classmethod
    async def get_prefix(cls, guild_id: int) -> str:
        """
        :param guild_id: Discord Guild ID
        :return: Guild prefix from settings table
        """
        async with cls.pool.acquire() as db:
            row = await db.fetchrow("SELECT prefix FROM bot.guilds WHERE guild_id = $1 LIMIT 1;", guild_id)
            return row['prefix']

    @classmethod
    async def set_prefix(cls, guild_id: int, new_prefix: str):
        """
        Changes prefix for a guild in the settings table

        :param guild_id: Discord Guild ID
        :param new_prefix: prefix that user wants to set
        """
        async with cls.pool.acquire() as db:
            await db.execute("UPDATE bot.guilds SET prefix = $2 WHERE guild_id = $1;", guild_id, new_prefix)

    @classmethod
    async def execute(cls, execute_string, *args):
        async with cls.pool.acquire() as db:
            return await db.execute(execute_string, *args)

    @classmethod
    async def fetch_row(cls, query_string, *args):
        async with cls.pool.acquire() as db:
            return await db.fetchrow(query_string, *args)

    @classmethod
    async def fetch(cls, query_string, *args):
        async with cls.pool.acquire() as db:
            return await db.fetch(query_string, *args)
