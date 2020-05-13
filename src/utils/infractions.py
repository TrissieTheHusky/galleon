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

from .database import Database as db
from .translator import Translator


class Infractions:
    @staticmethod
    async def add(inf_type: str, guild_id: int, moderator_id: int, target_id: int, reason: str = None, expires_at: datetime = None):
        added_at = datetime.utcnow()

        if expires_at is None:
            expires_at = added_at

        if reason is None:
            reason = Translator.translate('INF_NO_REASON', guild_id)

        query_params = (guild_id, moderator_id, target_id, reason, inf_type, added_at, expires_at)

        async with db.pool.acquire() as conn:
            async with conn.transaction():
                await conn.execute(
                    "INSERT INTO bot.infractions (guild_id, moderator_id, target_id, reason, inf_type, added_at, expires_at) VALUES ($1, $2, $3, $4, $5, $6, $7)",
                    *query_params
                )

    @staticmethod
    async def get(target_id: int = None, **kwargs):
        if target_id is None:
            return None

        if kwargs.get('latest', False):
            return await db.fetch_row("SELECT * FROM bot.infractions WHERE target_id = $1 ORDER BY inf_id DESC LIMIT 500", target_id,
                                      transaction=True)
        else:
            return await db.fetch("SELECT * FROM bot.infractions WHERE target_id = $1 ORDER BY inf_id DESC LIMIT 500", target_id, transaction=True)

    @staticmethod
    async def remove(inf_id: int):
        async with db.pool.acquire() as conn:
            async with conn.transaction():
                await conn.execute("DELETE FROM bot.infractions WHERE inf_id = $1", inf_id)
