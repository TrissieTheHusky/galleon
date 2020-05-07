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

import json
from os.path import join, dirname

from discord import Message
from discord.ext.commands import when_mentioned_or

from src.typings import ConfigType

with open(join(dirname(__file__), "../../config/master.json"), encoding="utf-8") as master_config:
    cfg: ConfigType = json.load(master_config)


class Config:
    @staticmethod
    async def reload_master():
        """
        Reloads master configuration
        """
        global cfg

        with open(join(dirname(__file__), "../../config/master.json"), encoding="utf-8") as master_config:
            cfg = json.load(master_config)

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
