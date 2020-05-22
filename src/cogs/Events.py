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

from aiohttp import ClientSession
from discord import RawReactionActionEvent, TextChannel, Message, utils, Guild, Color
from discord.ext import commands

from src.database import Database
from src.utils.base import current_time_with_tz
from src.utils.custom_bot_class import DefraBot
from src.utils.premade_embeds import DefraEmbed


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot: DefraBot = bot
        self.karma_phrases = bot.cfg.get("KARMA_PHRASES", [])

        if self.bot.aiohttp_session is None:
            self.bot.aiohttp_session = ClientSession()

    async def cog_unload(self):
        self.bot.aiohttp_session.close()

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
        await self.bot.cache.prefixes.refresh(guild.id)


def setup(bot):
    bot.add_cog(Events(bot))
