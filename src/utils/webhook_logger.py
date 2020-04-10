from discord import Webhook, AsyncWebhookAdapter, Embed
import aiohttp
from src.utils.configuration import cfg
from typing import NoReturn


class WebhookLogger:
    url = cfg['WEBHOOK']['LOGGING_URL']
    name = cfg['WEBHOOK']['NAME']
    avatar_url = cfg['WEBHOOK']['AVATAR_URL']

    @classmethod
    async def log(cls, text: str = None, embed: Embed = None) -> NoReturn:
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(cls.url, adapter=AsyncWebhookAdapter(session))
            await webhook.send(text, embed=embed, username=cls.name, avatar_url=cls.avatar_url)
