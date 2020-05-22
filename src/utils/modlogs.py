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

from datetime import datetime
from typing import Union

from discord import TextChannel, User, Member, Message, utils
from pytz import timezone

from .translator import Translator
from .exceptions import ModlogsNotFound


class Modlogs:
    @staticmethod
    async def send(context, logging_type: str, guild_id: int, **kwargs):
        guild_tz = context.bot.cache.timezones.get(guild_id)
        now = datetime.utcnow().astimezone(timezone(guild_tz))

        try:
            channel_ids = context.bot.cache.modlogs[guild_id][logging_type]

            if len(channel_ids) <= 0:
                raise ModlogsNotFound("There are no channels for logging {0} in {1}".format(logging_type.upper(), guild_id))

        except KeyError:
            raise ModlogsNotFound("Couldn't find logging channel for {0} in {1}".format(logging_type.upper(), guild_id))

        for channel_id in channel_ids:
            channel: TextChannel = context.bot.get_channel(channel_id)

            if channel is not None:
                if 'messages' == logging_type.lower():
                    message_type = kwargs.get('message_type').lower()

                    if message_type == 'archive':
                        archived_channel = kwargs.get('archived_channel')
                        requester: Union[Member, User] = kwargs.get('requester')

                        await channel.send(
                            file=kwargs.get('file'),
                            content=":envelope: [**`{0}`**] {1}".format(
                                now.strftime("%d-%m-%Y %H:%M:%S"),
                                Translator.translate('MOD_LOG_ARCHIVE_CHANNEL', context, channel=archived_channel, requester=str(requester),
                                                     requester_id=str(requester.id))
                            ))

                    elif message_type == 'deleted':
                        message: Message = kwargs.get('message')
                        content = utils.escape_markdown(utils.escape_mentions(message.content))

                        await channel.send(
                            ":envelope: [**`{0}`**] {1}".format(
                                now.strftime("%d-%m-%Y %H:%M:%S"),
                                Translator.translate('MOD_LOG_DELETED_MESSAGE', context, channel=message.channel.mention, user=str(message.author),
                                                     user_id=str(message.author.id), content=content)
                            )
                        )
