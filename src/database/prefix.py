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

from .base import DBBase


class DBPrefix(DBBase):
    async def get(self, guild_id: int):
        """
        Returns the non-cached value of the current guild's prefix

        :param guild_id: Discord Guild ID
        :return: Guild prefix from settings table
        """
        async with self.pool.acquire() as conn:
            data = await conn.fetchval("SELECT prefix FROM bot.guilds WHERE guild_id = $1 LIMIT 1;", guild_id)
            return data

    async def set(self, guild_id: int, new_prefix: str):
        """
        Changes prefix for a guild in the settings table

        :param guild_id: Discord Guild ID
        :param new_prefix: prefix that user wants to set
        """
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                await conn.execute("UPDATE bot.guilds SET prefix = $2 WHERE guild_id = $1;", guild_id, new_prefix)
