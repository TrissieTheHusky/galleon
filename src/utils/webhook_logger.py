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

from typing import NoReturn

import aiohttp
from discord import Webhook, AsyncWebhookAdapter, Embed

from src.utils.configuration import cfg


class WebhookLogger:
    url = cfg['WEBHOOK']['LOGGING_URL']
    name = cfg['WEBHOOK']['NAME']
    avatar_url = cfg['WEBHOOK']['AVATAR_URL']

    @classmethod
    async def log(cls, text: str = None, embed: Embed = None) -> NoReturn:
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(cls.url, adapter=AsyncWebhookAdapter(session))
            await webhook.send(text, embed=embed, username=cls.name, avatar_url=cls.avatar_url)
