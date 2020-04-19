from asyncpg.pool import Pool, create_pool
from typing import Optional
from socket import gaierror


class DatabaseException(Exception):
    pass


class Database:
    pool: Optional[Pool] = None

    @classmethod
    async def connect(cls, credentials) -> None:
        try:
            cls.pool = await create_pool(**credentials)
            print("[DB] Connection pool created.")
        except gaierror:
            raise DatabaseException("Unable to connect to the database")

    @classmethod
    async def get_prefix(cls, guild_id: int) -> str:
        async with cls.pool.acquire() as db:
            row = await db.fetchrow("SELECT prefix FROM bot.guilds WHERE guild_id = $1;", guild_id)
            return row['prefix']

    @classmethod
    async def set_prefix(cls, guild_id: int, new_prefix: str):
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
