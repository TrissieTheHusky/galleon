#  Copyright (c) 2020 defracted
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

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
