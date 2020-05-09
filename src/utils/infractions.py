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
    async def add_infraction(inf_type: str, guild_id: int, moderator_id: int, target_id: int, reason: str = None, expires_at: datetime = None):
        if expires_at is None:
            expires_at = datetime.utcnow()

        if reason is None:
            reason = Translator.translate('INF_NO_REASON', guild_id)

        query_params = (guild_id, moderator_id, target_id, reason, inf_type, expires_at)

        async with Database.pool.acquire() as conn:
            async with conn.transaction():
                await conn.execute(
                    "INSERT INTO bot.infractions (guild_id, moderator_id, target_id, reason, inf_type, expires_at) VALUES ($1, $2, $3, $4, $5, $6)",
                    query_params
                )
