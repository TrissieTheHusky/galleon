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

from datetime import datetime

from src.database import Database as db
from .translator import Translator


class Infractions:
    @staticmethod
    async def add(inf_type: str, guild_id: int, moderator_id: int, target_id: int, reason: str = None, expires_at: datetime = None):
        added_at = datetime.now()

        if expires_at is None:
            expires_at = added_at

        if reason is None:
            reason = Translator.translate('INF_NO_REASON', guild_id)

        query_params = (guild_id, moderator_id, target_id, reason, inf_type, added_at, expires_at)

        async with (await db.get_pool()).acquire() as conn:
            async with conn.transaction():
                return await conn.fetchval(
                    "INSERT INTO bot.infractions (guild_id, moderator_id, target_id, reason, inf_type, added_at, expires_at) VALUES ($1, $2, $3, $4, $5, $6, $7) RETURNING inf_id",
                    *query_params
                )

    @staticmethod
    async def get(guild_id: int, target_id: int = None, moderator_id: int = None, latest: bool = False, inf_id: int = None):
        if inf_id:
            return await db.fetchrow("SELECT * FROM bot.infractions WHERE inf_id = $1 LIMIT 1;", inf_id)

        elif latest:
            if moderator_id is not None:
                return await db.fetchrow("SELECT * FROM bot.infractions WHERE (moderator_id = $1 AND guild_id = $2) ORDER BY inf_id DESC LIMIT 500",
                                         moderator_id, guild_id, transaction=True)
            elif target_id is not None:
                return await db.fetchrow("SELECT * FROM bot.infractions WHERE (target_id = $1 AND guild_id = $2) ORDER BY inf_id DESC LIMIT 500",
                                         target_id, guild_id, transaction=True)
            else:
                return await db.fetchrow("SELECT * FROM bot.infractions WHERE (guild_id = $1) ORDER BY inf_id DESC LIMIT 500",
                                         guild_id, transaction=True)

        else:
            if moderator_id is not None:
                return await db.fetch("SELECT * FROM bot.infractions WHERE (moderator_id = $1 AND guild_id = $2) ORDER BY inf_id DESC LIMIT 500",
                                      moderator_id, guild_id, transaction=True)
            elif target_id is not None:
                return await db.fetch("SELECT * FROM bot.infractions WHERE (target_id = $1 AND guild_id = $2) ORDER BY inf_id DESC LIMIT 500",
                                      target_id, guild_id, transaction=True)
            else:
                return await db.fetch("SELECT * FROM bot.infractions WHERE (guild_id = $1) ORDER BY inf_id DESC LIMIT 500",
                                      guild_id, transaction=True)

    @staticmethod
    async def deactivate(inf_id: int):
        async with (await db.get_pool()).acquire() as conn:
            async with conn.transaction():
                return await conn.execute("UPDATE bot.infractions SET is_active = FALSE WHERE inf_id = $1", inf_id)

    @staticmethod
    async def remove(inf_id: int):
        async with (await db.get_pool()).acquire() as conn:
            async with conn.transaction():
                await conn.execute("DELETE FROM bot.infractions WHERE inf_id = $1", inf_id)
