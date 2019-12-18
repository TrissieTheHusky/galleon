from discord.ext.commands import when_mentioned_or
from os.path import join, dirname
import json
import os

with open(join(dirname(__file__), "../../config/master.json")) as master_config:
    cfg = json.load(master_config)


class Config:
    @staticmethod
    async def get_prefix(client, message):
        return when_mentioned_or(cfg['DEFAULT_PREFIX'])(client, message)
