#  Copyright (c) 2020 defracted
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from datetime import datetime

from .translator import Translator
from .database import Database


class Infractions:
    @staticmethod
    async def add(inf_type: str, guild_id: int, moderator_id: int, target_id: int, reason: str = None, expires_at: datetime = None):
        added_at = datetime.utcnow()

        if expires_at is None:
            expires_at = added_at

        if reason is None:
            reason = Translator.translate('INF_NO_REASON', guild_id)

        query_params = (guild_id, moderator_id, target_id, reason, inf_type, added_at, expires_at)

        async with Database.pool.acquire() as conn:
            async with conn.transaction():
                await conn.execute(
                    "INSERT INTO bot.infractions (guild_id, moderator_id, target_id, reason, inf_type, added_at, expires_at) VALUES ($1, $2, $3, $4, $5, $6, $7)",
                    *query_params
                )

    @staticmethod
    async def remove(inf_id: int):
        async with Database.pool.acquire() as conn:
            async with conn.transaction():
                await conn.execute("DELETE FROM bot.infractions WHERE inf_id = $1", inf_id)
