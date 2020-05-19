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

import toml
from os.path import join, dirname

from discord import Message
from discord.ext.commands import when_mentioned_or

with open(join(dirname(__file__), "../../config/master.toml"), encoding="utf-8") as master_config:
    cfg = toml.load(master_config)


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
