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

from .base import SQLBase
from src.utils.enums import TableRolesTypes


class SQLRoles(SQLBase):
    async def remove(self, role_type: str, guild_id: int, role_id: int = 0):
        """Removes a mod role id into guild settings"""
        async with self._pool.acquire() as conn:
            async with conn.transaction():
                if TableRolesTypes(role_type) is TableRolesTypes.mod_roles:
                    return await conn.execute("UPDATE bot.guilds SET mod_roles = array_remove(mod_roles, $1) WHERE guild_id = $2", role_id, guild_id)

                elif TableRolesTypes(role_type) is TableRolesTypes.admin_roles:
                    return await conn.execute(
                        "UPDATE bot.guilds SET admin_roles = array_remove(admin_roles, $1) WHERE guild_id = $2", role_id, guild_id)

                elif TableRolesTypes(role_type) is TableRolesTypes.mute_role:
                    return await conn.execute("UPDATE bot.guilds SET mod_roles = $1 WHERE guild_id = $2", role_id, guild_id)

    async def add(self, role_type: str, guild_id: int, role_id: int):
        async with self._pool.acquire() as conn:
            async with conn.transaction():
                if TableRolesTypes(role_type) is TableRolesTypes.mod_roles:
                    return await conn.execute("UPDATE bot.guilds SET mod_roles = array_append(mod_roles, $1) WHERE guild_id = $2", role_id, guild_id)

                elif TableRolesTypes(role_type) is TableRolesTypes.admin_roles:
                    return await conn.execute(
                        "UPDATE bot.guilds SET admin_roles = array_append(admin_roles, $1) WHERE guild_id = $2", role_id, guild_id)

                elif TableRolesTypes(role_type) is TableRolesTypes.mute_role:
                    return await conn.execute("UPDATE bot.guilds SET mod_roles = $1 WHERE guild_id = $2", role_id, guild_id)

    async def get(self, role_type: str, guild_id: int):
        async with self._pool.acquire() as conn:
            async with conn.transaction():
                query = "SELECT (mute_role, mod_roles, admin_roles) FROM bot.guilds WHERE guild_id = $1"
                mute_role, mod_roles, admin_roles = conn.fetchval(query, guild_id)

                if TableRolesTypes(role_type) is TableRolesTypes.mod_roles:
                    data = mod_roles
                elif TableRolesTypes(role_type) is TableRolesTypes.admin_roles:
                    data = admin_roles
                elif TableRolesTypes(role_type) is TableRolesTypes.mute_role:
                    data = mute_role

        return data
