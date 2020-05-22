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


class DBTimezone(DBBase):
    async def get(self, guild_id: int) -> Optional[str]:
        """
        Gets timezone for specified Discord Guild

        :param guild_id: Discord Guild ID
        :return: Timezone string
        """
        async with self.pool.acquire() as conn:
            guild_tz = await conn.fetchval("SELECT _timezone FROM bot.guilds WHERE guild_id = $1 LIMIT 1;", guild_id)
            return guild_tz

    async def set(self, guild_id: int, new_timezone: str):
        """
        Sets timezone for specified Discord Guild

        :param guild_id: Discord Guild ID
        :param new_timezone: Timezone string
        """
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                await conn.execute("UPDATE bot.guilds SET _timezone = $2 WHERE guild_id = $1;", guild_id, new_timezone)
