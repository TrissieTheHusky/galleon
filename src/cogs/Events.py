from discord.ext import commands
from src.typings import BotType
from discord import Guild, Color
from src.utils.base import DefraEmbed


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot: BotType = bot

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: Guild):
        await self.bot.dev_log_channel.send(embed=DefraEmbed(
            title="Удаление с сервера",
            color=Color.red(),
            description=f":inbox_tray: Меня удалили с сервера {guild.name} (`{guild.id}`)"
        ).add_field(name="Владелец", value=f"{guild.owner} (`{guild.owner_id}`)").add_field(
            name="Количетсво участников", value=f"{guild.member_count}").add_field(
            name="Количество каналов", value=f"{len(guild.channels)}"
        ))

    @commands.Cog.listener()
    async def on_guild_join(self, guild: Guild):
        await self.bot.dev_log_channel.send(embed=DefraEmbed(
            title="Обнаружен новый сервер",
            color=Color.green(),
            description=f":inbox_tray: Меня добавили на сервер {guild.name} (`{guild.id}`)"
        ).add_field(name="Владелец", value=f"{guild.owner} (`{guild.owner_id}`)").add_field(
            name="Количетсво участников", value=f"{guild.member_count}").add_field(
            name="Количество каналов", value=f"{len(guild.channels)}"
        ))

        # TODO: Генерировать конфиг гильдии, основываясь на темплейте


def setup(bot):
    bot.add_cog(Events(bot))
