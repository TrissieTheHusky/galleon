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


class ModlogsCache(dict):
    def __init__(self, database):
        super().__init__()
        self.db = database

    async def refresh(self, guild_id: int):
        async with self.db.pool.acquire() as conn:
            async with conn.transaction():
                misc, messages, join_leave, mod_actions, config_logs, server_changes = await conn.fetchval(
                    "SELECT (misc, messages, join_leave, mod_actions, config_logs, server_changes) FROM bot.logging_channels WHERE guild_id = $1",
                    guild_id)

                super().update({
                    guild_id: {
                        "misc": misc,
                        "messages": messages,
                        "join_leave": join_leave,
                        "mod_actions": mod_actions,
                        "config_logs": config_logs,
                        "server_changes": server_changes
                    }})

                print("[CACHE] Modlogs for {0} was refreshed.".format(guild_id))
