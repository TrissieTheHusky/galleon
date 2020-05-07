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

from datetime import datetime

import pytz
from discord import Guild, Color
from discord import RawReactionActionEvent, TextChannel, Message, utils
from discord.ext import commands

from src.utils.base import current_time_with_tz
from src.utils.custom_bot_class import DefraBot
from src.utils.database import Database
from src.utils.premade_embeds import DefraEmbed


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot: DefraBot = bot
        self.karma_phrases = bot.cfg.get("KARMA_PHRASES", [])

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: RawReactionActionEvent):
        if payload.emoji.name == '🗑️' and payload.user_id == self.bot.owner.id:
            c: TextChannel = self.bot.get_channel(payload.channel_id)
            m: Message = await c.fetch_message(payload.message_id)

            if m.author == self.bot.user:
                await self.bot.dev_channel.send(
                    f":warning: **`[{current_time_with_tz().strftime('%d.%m.%Y %H:%M:%S')}]`** "
                    f"Received a request to delete this message, sent by **{m.author}**: \n{utils.escape_markdown(m.content)}\n")
                await m.delete()

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: Guild):
        await self.bot.dev_channel.send(
            content=f"\U00002139 **`[{current_time_with_tz().strftime('%d.%m.%Y %H:%M:%S')}]`**",
            embed=DefraEmbed(
                title="Removed from Guild",
                color=Color.red(),
                description=f":inbox_tray: {guild.name} (`{guild.id}`)"
            ).add_field(name="Owner", value=f"{guild.owner} (`{guild.owner_id}`)").add_field(
                name="Members count", value=f"{guild.member_count}").add_field(
                name="Channels count", value=f"{len(guild.channels)}"
            ))

    @commands.Cog.listener()
    async def on_guild_join(self, guild: Guild):
        await self.bot.dev_channel.send(
            content=f"\U00002139 **`[{current_time_with_tz().strftime('%d.%m.%Y %H:%M:%S')}]`**",
            embed=DefraEmbed(
                title="New Guild",
                color=Color.green(),
                description=f":inbox_tray: {guild.name} (`{guild.id}`)"
            ).add_field(name="Owner", value=f"{guild.owner} (`{guild.owner_id}`)").add_field(
                name="Members count", value=f"{guild.member_count}").add_field(
                name="Channels count", value=f"{len(guild.channels)}"
            ))

        # Adding the guild to database of settings
        await Database.safe_add_guild(guild.id)
        # Refreshing bot's cache for the guild
        await self.bot.update_prefix(guild.id)

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        # Adding karma points when people being nice to each other
        if any(element in message.clean_content.lower() for element in self.karma_phrases):
            karma, modified_at = await Database.get_karma(message.author.id)

            if karma is None or modified_at is None:
                await Database.add_karma(message.author.id)

            if karma is not None and modified_at is not None:
                # Add more points if an hour passed from last modification time
                if datetime.utcnow().timestamp() - modified_at.astimezone(pytz.utc).timestamp() < 3600:
                    return

                await Database.add_karma(message.author.id)


def setup(bot):
    bot.add_cog(Events(bot))
