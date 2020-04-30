from typing import Optional

import aioredis

from src.utils.database import Database


class Cache:
    redis: Optional[aioredis.Redis]

    @classmethod
    async def connect(cls):
        cls.redis = await aioredis.create_redis_pool('redis://localhost')
        print("[REDIS 0] Connection to Redis established.")

    @classmethod
    async def purge(cls):
        with await cls.redis as conn:
            await conn.execute("FLUSHALL")
            print("[REDIS 0] Database has been purged.")

    @classmethod
    async def get(cls, key):
        with await cls.redis as conn:
            val: bytes = await conn.execute("GET", str(key))
            return val.decode(encoding="utf-8")

    @classmethod
    async def set(cls, key, value):
        with await cls.redis as conn:
            await conn.set(str(key), str(value))

    @classmethod
    async def get_timezone(cls, guild_id):
        with await cls.redis as conn:
            val: bytes = await conn.execute("GET", f"timezone_{str(guild_id)}")
            return val.decode(encoding="utf-8")

    @classmethod
    async def set_timezone(cls, guild_id, timezone: str):
        with await cls.redis as conn:
            await conn.set(f"timezone_{str(guild_id)}", str(timezone))
            print(f"[REDIS 0] Updated timezone value for GUILD ID {str(guild_id)}")

    @classmethod
    async def update_timezone(cls, guild_id):
        timezone = await Database.get_timezone(int(guild_id))
        await cls.set_timezone(guild_id, str(timezone))
