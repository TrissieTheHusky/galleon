from discord.ext import commands
from src.typings import BotType
from src.utils.database import Database


def is_server_manager_or_bot_owner():
    """
    Checks if context author is a bot owner or has manage_guild permission
    """

    def predicate(ctx: commands.Context):
        return (ctx.message.author.id == ctx.bot.owner.id) or \
               ((ctx.guild.get_member(ctx.message.author.id).guild_permissions.value & 0x20) == 0x20)

    return commands.check(predicate)


class ServerAdmin(commands.Cog, name="Администрирование"):
    def __init__(self, bot):
        self.bot: BotType = bot

    @commands.group()
    @is_server_manager_or_bot_owner()
    async def config(self, ctx: commands.Context):
        """
        Обновление параметров конфигурации
        """
        if ctx.invoked_subcommand is None:
            await ctx.send(":warning: Вы не указали субкоманду.\n"
                           f":information_source: Подробнее: `{ctx.prefix}help {ctx.invoked_with}`")

    @config.command()
    async def prefix(self, ctx: commands.Context, new_prefix=None):
        """
        Смена префикса бота
        """
        if new_prefix is None:
            return await ctx.send(":warning: Вы не указали новый префикс!")

        await Database.set_prefix(ctx.guild.id, new_prefix)
        await self.bot.update_prefix(ctx.guild.id)

        await ctx.send(f":ok_hand: Вы успешно сменили префикс на `{self.bot.prefixes.get(ctx.guild.id)}`")


def setup(bot):
    bot.add_cog(ServerAdmin(bot))
