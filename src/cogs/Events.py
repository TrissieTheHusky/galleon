from discord.ext import commands
from src.typings import BotType
from discord import Guild, Color
from src.utils.base import DefraEmbed, current_time_with_tz
from discord import RawReactionActionEvent, TextChannel, Message, utils
from src.utils.database import Database


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot: BotType = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: RawReactionActionEvent):
        if payload.emoji.name == '🗑️' and payload.user_id == self.bot.owner.id:
            c: TextChannel = self.bot.get_channel(payload.channel_id)
            m: Message = await c.fetch_message(payload.message_id)

            if m.author == self.bot.user:
                await self.bot.dev_log_channel.send(
                    f":warning: **`[{current_time_with_tz().strftime('%d.%m.%Y %H:%M:%S')}]`** "
                    f"Received a request to delete this message, sent by **{m.author}**: \n{utils.escape_markdown(m.content)}\n")
                await m.edit(content=":warning: This message was requested to get deleted by my owner."
                                     "\n:hammer: Deletion in 5 seconds...", embed=None)
                await m.delete(delay=5)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: Guild):
        await self.bot.dev_log_channel.send(
            content=f"\U00002139 **`[{current_time_with_tz().strftime('%d.%m.%Y %H:%M:%S')}]`**",
            embed=DefraEmbed(
                title="Удаление с сервера",
                color=Color.red(),
                description=f":inbox_tray: Меня удалили с сервера {guild.name} (`{guild.id}`)"
            ).add_field(name="Владелец", value=f"{guild.owner} (`{guild.owner_id}`)").add_field(
                name="Количество участников", value=f"{guild.member_count}").add_field(
                name="Количество каналов", value=f"{len(guild.channels)}"
            ))

    @commands.Cog.listener()
    async def on_guild_join(self, guild: Guild):
        await self.bot.dev_log_channel.send(
            content=f"\U00002139 **`[{current_time_with_tz().strftime('%d.%m.%Y %H:%M:%S')}]`**",
            embed=DefraEmbed(
                title="Обнаружен новый сервер",
                color=Color.green(),
                description=f":inbox_tray: Меня добавили на сервер {guild.name} (`{guild.id}`)"
            ).add_field(name="Владелец", value=f"{guild.owner} (`{guild.owner_id}`)").add_field(
                name="Количество участников", value=f"{guild.member_count}").add_field(
                name="Количество каналов", value=f"{len(guild.channels)}"
            ))

        await Database.execute("INSERT INTO bot.guilds (guild_id) VALUES ($1) ON CONFLICT DO NOTHING;", guild.id)


def setup(bot):
    bot.add_cog(Events(bot))
