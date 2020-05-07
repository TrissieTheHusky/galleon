#  The MIT License (MIT)
#
#  Copyright (c) 2020 defracted
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

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
