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

from typing import Optional

from .base import DBBase


class DBBlacklist(DBBase):
    async def get(self):
        """Returns List[`int`] of blacklisted user ids"""
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                return await conn.fetch("SELECT user_id FROM bot.blacklist")

    async def check(self, user_id: int) -> Optional[bool]:
        async with self.pool.acquire() as db:
            async with db.transaction():
                val = await db.fetchval("SELECT user_id FROM bot.blacklist WHERE user_id = $1", user_id)
                if val is not None:
                    return True
                else:
                    return False

    async def add(self, user_id: int) -> Optional[bool]:
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                is_added = await conn.fetchval("INSERT INTO bot.blacklist (user_id) VALUES ($1) ON CONFLICT DO NOTHING RETURNING True", user_id)
                if is_added:
                    return True
                else:
                    return False

    async def remove(self, user_id: int) -> Optional[bool]:
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                is_removed = await conn.fetchval("DELETE FROM bot.blacklist WHERE user_id = $1 RETURNING True", user_id)
                if is_removed:
                    return True
                else:
                    return False
