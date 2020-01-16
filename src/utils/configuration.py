from discord.ext.commands import when_mentioned_or
from os.path import join, dirname
import json
import os

with open(join(dirname(__file__), "../../config/master.json"), encoding="utf-8") as master_config:
    cfg = json.load(master_config)


class Config:
    @staticmethod
    async def update_prefixes():
        with open(join(dirname(__file__), "../../config/prefixes.json"), encoding="utf-8") as guild_prefix:
            return json.load(guild_prefix)

    @staticmethod
    async def get_prefix(client, message):
        if not message.guild:
            return when_mentioned_or(cfg['DEFAULT_PREFIX'])(client, message)

        prefix = client.prefixes.get(str(message.guild.id), cfg['DEFAULT_PREFIX'])
        return when_mentioned_or(prefix)(client, message)
