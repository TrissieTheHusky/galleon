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


class DBModlogs(DBBase):
    async def get(self, logging_type: str, guild_id: int):
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                return await conn.fetchval("SELECT $1 FROM bot.logging_channels WHERE guild_id = $2;", logging_type.lower(), guild_id)

    async def add(self, logging_type: str, guild_id: int, channel_id: int):
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                return await conn.execute("UPDATE bot.logging_channels SET $1 = array_append($1, $3) WHERE guild_id = $2;",
                                          logging_type, guild_id, channel_id)

    async def set(self, logging_type: str, guild_id: int, channel_ids: List[int]):
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                return await conn.execute("UPDATE bot.logging_channels SET $1 = $2 WHERE guild_id = $3", logging_type, channel_ids, guild_id)
