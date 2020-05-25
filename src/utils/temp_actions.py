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

from datetime import timedelta

from asyncpg.pool import Pool


class TempActions:
    @staticmethod
    async def get_active_actions(pool: Pool, limit: int = None):
        query = "SELECT * FROM bot.infractions WHERE inf_type IN('tempban', 'tempmute') AND is_active = true AND expires_at < (CURRENT_DATE + $1::interval) ORDER BY inf_id"

        if limit is not None:
            query += "LIMIT $2"

        async with pool.acquire() as conn:
            if limit is not None:
                active_actions = await conn.fetch(query, timedelta(days=365), limit)
            else:
                active_actions = await conn.fetch(query, timedelta(days=365))

        return active_actions
