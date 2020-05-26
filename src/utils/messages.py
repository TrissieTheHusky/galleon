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

import asyncio
import io
from typing import List

from discord import Message, utils, TextChannel, File, Forbidden
from discord.ext.commands import Context
from pytz import timezone

from src.utils.translator import Translator


class Messages:
    @staticmethod
    async def archive_messages(bot, messages: List[Message]):
        # Preparing text file heading
        guild_timezone = bot.cache.guilds.get(messages[0].guild.id).timezone
        server_format = f"{messages[0].guild.name} ({messages[0].guild.id})"
        channel_format = f"{messages[0].channel.name} ({messages[0].channel.id})"
        timezone_format = f"{guild_timezone.title()}"

        output = f"Server: {server_format}\nChannel: {channel_format}\nLogs timezone: {timezone_format}\n\n\n"
        for msg in messages:
            # Preparing format
            created_at_format = msg.created_at.astimezone(timezone(guild_timezone)).strftime("%d-%m-%Y %H:%M:%S")
            content_format = utils.escape_markdown(utils.escape_mentions(msg.content))
            prefix = f"{created_at_format} | {msg.author} ({msg.author.id})"

            # Adding the message content to output string
            output += f"{prefix}: {content_format}\n"

            # Check if the message has any attachments
            if len(msg.attachments) > 0:
                # Add all the links from message attachments
                for attachment in msg.attachments:
                    output += f"{prefix}: {attachment.proxy_url}\n"

        # Return BytesIO object so it can be used in discord.File
        bdata = io.BytesIO()
        bdata.write(output.encode(encoding='utf-8'))
        bdata.seek(0)
        return bdata

    @staticmethod
    async def send_archive(bot, ctx: Context, messages: List[Message], archived_channel: TextChannel):
        file_bytes = await Messages.archive_messages(bot, messages)
        filename = f"Archive for {archived_channel.name}.txt"

        try:
            file_bytes.seek(0)
            await ctx.author.send(file=File(file_bytes, filename=filename))
            await ctx.send(Translator.translate('ARCHIVE_SENT', ctx))
        except Forbidden:
            file_bytes.seek(0)
            await ctx.send(Translator.translate('ARCHIVE_WARNING_CLOSED_DMS', ctx, author=ctx.author.mention))

            try:
                def check(m):
                    return m.author == ctx.author and any(ext.lower() in m.content.lower() for ext in ['yes', 'no'])

                msg = await bot.wait_for('message', check=check, timeout=60.0)
            except asyncio.TimeoutError:
                await ctx.send(Translator.translate('ARCHIVE_TOO_SLOW', ctx))
            else:
                if 'yes' in msg.content.lower():
                    await ctx.send(file=File(file_bytes, filename=filename))
                else:
                    await ctx.send(Translator.translate('ARCHIVE_CANCELLED', ctx))
