from discord.ext import commands
from discord import Guild, Color
from discord import RawReactionActionEvent, TextChannel, Message, utils
from datetime import datetime

from src.utils.base import DefraEmbed, current_time_with_tz
from src.utils.database import Database
from src.typings import BotType

import pytz


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot: BotType = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: RawReactionActionEvent):
        if payload.emoji.name == '🗑️' and payload.user_id == self.bot.owner.id:
            c: TextChannel = self.bot.get_channel(payload.channel_id)
            m: Message = await c.fetch_message(payload.message_id)

            if m.author == self.bot.user:
                await self.bot.dev_channel.send(
                    f":warning: **`[{current_time_with_tz().strftime('%d.%m.%Y %H:%M:%S')}]`** "
                    f"Received a request to delete this message, sent by **{m.author}**: \n{utils.escape_markdown(m.content)}\n")
                await m.edit(content=":warning: This message was requested to get deleted by my owner."
                                     "\n:hammer: Deletion in 5 seconds...", embed=None)
                await m.delete(delay=5)

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

        # Adding the guild to database of settinga
        await Database.execute("INSERT INTO bot.guilds (guild_id) VALUES ($1) ON CONFLICT DO NOTHING;", guild.id)
        # Refreshing bot's cache for the guild
        await self.bot.update_prefix(guild.id)

    @commands.Cog.listener()
    async def on_message(self, message: Message):

        # Adding karma points when people being nice to each other
        if any(element in message.clean_content.lower() for element in ["have a nice day", "хорошего дня"]):
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
