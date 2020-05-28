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
from .base import SQLBase
from src.utils.enums import ModLoggingType


class IgnoredUsers(SQLBase):
    async def add(self, guild_id: int, user_id: int):
        """Adds a User ID to ignored users list of the mod logging"""
        async with self._pool.acquire() as conn:
            async with conn.transaction():
                return await conn.execute("UPDATE bot.logging_channels SET ignored_users = array_append(ignored_users, $1) WHERE guild_id = $2",
                                          user_id, guild_id)

    async def remove(self, guild_id: int, user_id: int):
        """Removed a User ID from ignored users list of the mod logging"""
        async with self._pool.acquire() as conn:
            async with conn.transaction():
                return await conn.execute("UPDATE bot.logging_channels SET ignored_users = array_remove(ignored_users, $1) WHERE guild_id = $2",
                                          user_id, guild_id)


class SQLLogging(SQLBase):
    def __init__(self, pool):
        super().__init__(pool)
        self.ignored_users = IgnoredUsers(pool)

    async def set(self, logging_type: ModLoggingType, guild_id: int, channel_ids: List[int]):
        """Sets a channels list for logging type"""
        params = (channel_ids, guild_id)

        async with self._pool.acquire() as conn:
            async with conn.transaction():
                if logging_type is ModLoggingType.misc:
                    return await conn.execute("UPDATE bot.logging_channels SET misc = $1 WHERE guild_id = $2", *params)

                elif logging_type is ModLoggingType.messages:
                    return await conn.execute("UPDATE bot.logging_channels SET messages = $1 WHERE guild_id = $2", *params)

                elif logging_type is ModLoggingType.join_leave:
                    return await conn.execute("UPDATE bot.logging_channels SET join_leave = $1 WHERE guild_id = $2", *params)

                elif logging_type is ModLoggingType.mod_actions:
                    return await conn.execute("UPDATE bot.logging_channels SET mod_actions = $1 WHERE guild_id = $2", *params)

                elif logging_type is ModLoggingType.config_logs:
                    return await conn.execute("UPDATE bot.logging_channels SET config_logs = $1 WHERE guild_id = $2", *params)

                elif logging_type is ModLoggingType.server_changes:
                    return await conn.execute("UPDATE bot.logging_channels SET server_changes = $1 WHERE guild_id = $2", *params)

    async def add(self, logging_type: ModLoggingType, guild_id: int, channel_id: int):
        """Adds a logging type to a channel"""
        params = (channel_id, guild_id)

        async with self._pool.acquire() as conn:
            async with conn.transaction():
                if logging_type is ModLoggingType.misc:
                    return await conn.execute("UPDATE bot.logging_channels SET misc = array_append(misc, $1) WHERE guild_id = $2", *params)

                elif logging_type is ModLoggingType.messages:
                    return await conn.execute("UPDATE bot.logging_channels SET messages = array_append(messages, $1) WHERE guild_id = $2", *params)

                elif logging_type is ModLoggingType.join_leave:
                    return await conn.execute("UPDATE bot.logging_channels SET join_leave = array_append(join_leave, $1) WHERE guild_id = $2",
                                              *params)

                elif logging_type is ModLoggingType.mod_actions:
                    return await conn.execute("UPDATE bot.logging_channels SET mod_actions = array_append(mod_actions, $1) WHERE guild_id = $2",
                                              *params)

                elif logging_type is ModLoggingType.config_logs:
                    return await conn.execute("UPDATE bot.logging_channels SET config_logs = array_append(config_logs, $1) WHERE guild_id = $2",
                                              *params)

                elif logging_type is ModLoggingType.server_changes:
                    return await conn.execute("UPDATE bot.logging_channels SET server_changes = array_append(server_changes, $1) WHERE guild_id = $2",
                                              *params)

    async def remove(self, logging_type: ModLoggingType, guild_id: int, channel_id: int):
        """Removes a logging type from a channel"""
        params = (channel_id, guild_id)

        async with self._pool.acquire() as conn:
            async with conn.transaction():
                if logging_type is ModLoggingType.misc:
                    return await conn.execute("UPDATE bot.logging_channels SET misc = array_remove(misc, $1) WHERE guild_id = $2", *params)

                elif logging_type is ModLoggingType.messages:
                    return await conn.execute("UPDATE bot.logging_channels SET messages = array_remove(messages, $1) WHERE guild_id = $2",
                                              *params)

                elif logging_type is ModLoggingType.join_leave:
                    return await conn.execute("UPDATE bot.logging_channels SET join_leave = array_remove(join_leave, $1) WHERE guild_id = $2",
                                              *params)

                elif logging_type is ModLoggingType.mod_actions:
                    return await conn.execute("UPDATE bot.logging_channels SET mod_actions = array_remove(mod_actions, $1) WHERE guild_id = $2",
                                              *params)

                elif logging_type is ModLoggingType.config_logs:
                    return await conn.execute("UPDATE bot.logging_channels SET config_logs = array_remove(config_logs, $1) WHERE guild_id = $2",
                                              *params)

                elif logging_type is ModLoggingType.server_changes:
                    return await conn.execute("UPDATE bot.logging_channels SET server_changes = array_remove(server_changes, $1) WHERE guild_id = $2",
                                              *params)
