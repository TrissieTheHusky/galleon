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


class DBModRoles(DBBase):
    async def get(self, guild_id: int):
        """Returns `List[int]` of moderator role IDs"""
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                data = await conn.fetchval("SELECT (mod_roles) FROM bot.guilds WHERE guild_id = $1;", guild_id)
                return data

    async def set(self, guild_id: int, roles: List[int]):
        """Sets a mod roles list in guild settings"""
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                execution = await conn.execute("UPDATE bot.guilds SET mod_roles = $1 WHERE guild_id = $2", roles, guild_id)
                return execution

    async def add(self, guild_id: int, role_id: int):
        """Adds a mod role id into guild settings"""
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                execution = await conn.execute("UPDATE bot.guilds SET mod_roles = array_append(mod_roles, $1) WHERE guild_id = $2", role_id, guild_id)
                return execution

    async def remove(self, guild_id: int, role_id: int):
        """Removes a mod role id into guild settings"""
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                execution = await conn.execute("UPDATE bot.guilds SET mod_roles = array_remove(mod_roles, $1) WHERE guild_id = $2", role_id, guild_id)
                return execution
