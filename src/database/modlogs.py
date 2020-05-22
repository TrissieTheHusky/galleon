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

from typing import List

from .base import DBBase
from ..utils.exceptions import DatabaseBadLoggingType


class DBModlogs(DBBase):
    async def available_types(self):
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                data = await conn.fetch(
                    "SELECT (column_name) FROM information_schema.columns WHERE table_schema = 'bot' AND table_name = 'logging_channels'")
                return list(filter(lambda col: col != 'guild_id', [col['column_name'] for col in data]))

    async def get(self, logging_type: str, guild_id: int):
        logging_type = logging_type.lower()
        if logging_type not in await self.available_types():
            raise DatabaseBadLoggingType("Bad logging type")

        async with self.pool.acquire() as conn:
            async with conn.transaction():
                return await conn.fetchval("SELECT $1 FROM bot.logging_channels WHERE guild_id = $2;", logging_type.lower(), guild_id)

    async def add(self, logging_type: str, guild_id: int, channel_id: int):
        logging_type = logging_type.lower()
        if logging_type not in await self.available_types():
            raise DatabaseBadLoggingType("Bad logging type")

        async with self.pool.acquire() as conn:
            async with conn.transaction():
                return await conn.execute(f"UPDATE bot.logging_channels SET {logging_type} = array_append({logging_type}, $2) WHERE guild_id = $1;",
                                          guild_id, channel_id)

    async def remove(self, logging_type: str, guild_id: int, channel_id: int):
        logging_type = logging_type.lower()
        if logging_type not in await self.available_types():
            raise DatabaseBadLoggingType("Bad logging type")

        async with self.pool.acquire() as conn:
            async with conn.transaction():
                return await conn.execute(f"UPDATE bot.logging_channels SET {logging_type} = array_remove({logging_type}, $2) WHERE guild_id = $1",
                                          guild_id, channel_id)

    async def set(self, logging_type: str, guild_id: int, channel_ids: List[int]):
        logging_type = logging_type.lower()
        if logging_type not in await self.available_types():
            raise DatabaseBadLoggingType("Bad logging type")

        async with self.pool.acquire() as conn:
            async with conn.transaction():
                return await conn.execute(f"UPDATE bot.logging_channels SET {logging_type} = $2 WHERE guild_id = $3", channel_ids, guild_id)
