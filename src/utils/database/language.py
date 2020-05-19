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


class DBLanguage(DBBase):
    async def get(self, guild_id: int) -> Optional[str]:
        """
        Gets guild's language

        :param guild_id: Discord Guild ID
        :return: 'en_US' if None
        """
        async with self.pool.acquire() as conn:
            guild_lang = await conn.fetchval("SELECT language FROM bot.guilds WHERE guild_id = $1 LIMIT 1;", guild_id)
            return guild_lang or 'en_US'

    async def set(self, guild_id: int, new_lang: str):
        """
        Sets guild's language

        :param guild_id: Discord Guild ID
        :param new_lang: new lang code
        """
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                await conn.execute("UPDATE bot.guilds SET language = $2 WHERE guild_id = $1;", guild_id, new_lang)
