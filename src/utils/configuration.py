#  Copyright (c) 2020 defracted
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

import json
from os.path import join, dirname

from discord import Message
from discord.ext.commands import when_mentioned_or

with open(join(dirname(__file__), "../../config/master.json"), encoding="utf-8") as master_config:
    cfg = json.load(master_config)


class Config:
    @staticmethod
    async def get_prefix(client, message: Message):
        """
        :param client: Bot instance
        :param message: Received message
        :return: Data for command_prefix
        """
        if not message.guild:
            return when_mentioned_or(cfg['DEFAULT_PREFIX'])(client, message)

        prefix = client.cache.prefixes.get(message.guild.id, cfg['DEFAULT_PREFIX'])
        return when_mentioned_or(prefix if prefix is not None else cfg['DEFAULT_PREFIX'])(client, message)
