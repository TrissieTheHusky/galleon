from discord import Webhook, AsyncWebhookAdapter
import aiohttp
from src.utils.configuration import cfg


class Logger:
    @staticmethod
    async def log(text=None, embed=None):
        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(cfg['WEBHOOK']['LOGGING_URL'], adapter=AsyncWebhookAdapter(session))

            await webhook.send(
                text,
                embed=embed,
                username=cfg['WEBHOOK']['NAME'],
                avatar_url=cfg['WEBHOOK']['AVATAR_URL']
            )
