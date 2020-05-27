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
from typing import Union, Optional, List

from pytz import timezone
from discord import utils, TextChannel, RawMessageDeleteEvent, RawMessageUpdateEvent, Member
from discord.ext import commands

from src.utils.custom_bot_class import DefraBot
from src.utils.enums import ModLoggingType, MessageLogType, InfractionType
from src.utils.types import InfractionStruct
from src.utils.translator import Translator


class ModLogging(commands.Cog):
    def __init__(self, bot):
        self.bot: DefraBot = bot

    async def get_destinations(self, guild_id: int, logging_type: ModLoggingType) -> Optional[List[Optional[TextChannel]]]:
        if logging_type is ModLoggingType.misc:
            channel_ids = await self.bot.db.fetchval("SELECT misc FROM bot.logging_channels WHERE guild_id = $1", guild_id)
            return [self.bot.get_channel(channel_id) for channel_id in channel_ids] if channel_ids is not None else None

        elif logging_type is ModLoggingType.messages:
            channel_ids = await self.bot.db.fetchval("SELECT messages FROM bot.logging_channels WHERE guild_id = $1", guild_id)
            return [self.bot.get_channel(channel_id) for channel_id in channel_ids] if channel_ids is not None else None

        elif logging_type is ModLoggingType.join_leave:
            channel_ids = await self.bot.db.fetchval("SELECT join_leave FROM bot.logging_channels WHERE guild_id = $1", guild_id)
            return [self.bot.get_channel(channel_id) for channel_id in channel_ids] if channel_ids is not None else None

        elif logging_type is ModLoggingType.mod_actions:
            channel_ids = await self.bot.db.fetchval("SELECT mod_actions FROM bot.logging_channels WHERE guild_id = $1", guild_id)
            return [self.bot.get_channel(channel_id) for channel_id in channel_ids] if channel_ids is not None else None

        elif logging_type is ModLoggingType.config_logs:
            channel_ids = await self.bot.db.fetchval("SELECT config_logs FROM bot.logging_channels WHERE guild_id = $1", guild_id)
            return [self.bot.get_channel(channel_id) for channel_id in channel_ids] if channel_ids is not None else None

        elif logging_type is ModLoggingType.server_changes:
            channel_ids = await self.bot.db.fetchval("SELECT server_changes FROM bot.logging_channels WHERE guild_id = $1", guild_id)
            return [self.bot.get_channel(channel_id) for channel_id in channel_ids] if channel_ids is not None else None

    @commands.Cog.listener()
    async def on_mod_log_join_leave(self, is_join: bool, member: Member):
        destinations = await self.get_destinations(member.guild.id, ModLoggingType.join_leave)
        guild_tz = self.bot.cache.guilds.get(member.guild.id).timezone

        if is_join:
            time_fmt = datetime.now().astimezone(timezone(guild_tz)).strftime("%H:%M:%S")

            for channel in destinations:
                await channel.send(Translator.translate('MOD_LOGS_JOIN', member.guild.id, time=time_fmt, target=str(member),
                                                        target_id=str(member.id)))
        else:
            time_fmt = datetime.now().astimezone(timezone(guild_tz)).strftime("%H:%M:%S")

            for channel in destinations:
                await channel.send(Translator.translate('MOD_LOGS_LEAVE', member.guild.id, time=time_fmt, target=str(member),
                                                        target_id=str(member.id)))

    @commands.Cog.listener()
    async def on_mod_logging_messages(self, payload: Union[RawMessageUpdateEvent, RawMessageDeleteEvent], message_log_type: MessageLogType):
        if message_log_type is MessageLogType.deleted_message:
            destinations = await self.get_destinations(payload.guild_id, ModLoggingType.messages)
            guild_tz = self.bot.cache.guilds.get(payload.guild_id).timezone

            time_fmt = datetime.now().astimezone(timezone(guild_tz)).strftime("%H:%M:%S")

            if (cached_message := payload.cached_message) is None:
                message = await self.bot.db.fetchrow("SELECT * FROM bot.messages WHERE guild_id = $1 AND message_id = $2",
                                                     payload.guild_id, payload.message_id)

                if message is not None:
                    content = self.bot.cryptor.decrypt(message['content'])
                    content_fmt = utils.escape_mentions(utils.escape_markdown(content.decode(encoding='utf-8')))
                    author = self.bot.get_user(message['author_id'])
                    c = self.bot.get_channel(message['channel_id'])

                    for channel in destinations:
                        await channel.send(Translator.translate('MOD_LOGS_MESSAGE_DELETED', payload.guild_id, user=str(author), time=time_fmt,
                                                                user_id=str(message['author_id']), content=content_fmt, channel=c.mention))

            elif cached_message is not None:
                content_fmt = utils.escape_mentions(utils.escape_markdown(cached_message.content))

                for channel in destinations:
                    await channel.send(Translator.translate('MOD_LOGS_MESSAGE_DELETED', cached_message.guild.id, user=str(cached_message.author),
                                                            time=time_fmt, user_id=str(cached_message.author.id), content=content_fmt,
                                                            channel=cached_message.channel.mention))

    @commands.Cog.listener()
    async def on_mod_logging_inf_add(self, infraction: InfractionStruct):
        guild_tz = self.bot.cache.guilds.get(infraction.guild.id).timezone
        destinations = await self.get_destinations(infraction.guild.id, ModLoggingType.mod_actions)

        if infraction.inf_type is InfractionType.tempban:
            added_at_fmt = infraction.added_at.astimezone(timezone(guild_tz)).strftime("%H:%M:%S")
            until_fmt = infraction.expires_at.astimezone(timezone(guild_tz)).strftime("%d-%m-%Y %H:%M:%S")

            for channel in destinations:
                await channel.send(Translator.translate('MOD_LOGS_TEMP_BAN', infraction.guild.id, time=added_at_fmt, target=str(infraction.target),
                                                        target_id=str(infraction.target.id), moderator=str(infraction.moderator),
                                                        moderator_id=str(infraction.moderator.id), until=until_fmt, reason=infraction.reason))

        elif infraction.inf_type is InfractionType.permaban:
            added_at_fmt = infraction.added_at.astimezone(timezone(guild_tz)).strftime("%H:%M:%S")

            for channel in destinations:
                await channel.send(Translator.translate('MOD_LOGS_PERMA_BAN', infraction.guild.id, time=added_at_fmt, target=str(infraction.target),
                                                        target_id=str(infraction.target.id), moderator=str(infraction.moderator),
                                                        moderator_id=str(infraction.moderator.id), reason=infraction.reason))

        elif infraction.inf_type is InfractionType.kick:
            added_at_fmt = infraction.added_at.astimezone(timezone(guild_tz)).strftime("%H:%M:%S")

            for channel in destinations:
                await channel.send(Translator.translate('MOD_LOGS_KICK', infraction.guild.id, time=added_at_fmt, target=str(infraction.target),
                                                        target_id=str(infraction.target.id), moderator=str(infraction.moderator),
                                                        moderator_id=str(infraction.moderator.id), reason=infraction.reason))

        elif infraction.inf_type is InfractionType.warn:
            added_at_fmt = infraction.added_at.astimezone(timezone(guild_tz)).strftime("%H:%M:%S")

            for channel in destinations:
                await channel.send(Translator.translate('MOD_LOGS_WARN', infraction.guild.id, time=added_at_fmt, target=str(infraction.target),
                                                        target_id=str(infraction.target.id), moderator=str(infraction.moderator),
                                                        moderator_id=str(infraction.moderator.id), reason=infraction.reason))


def setup(bot):
    bot.add_cog(ModLogging(bot))
