from discord.ext import commands

from src.typings import BotType
from src.utils.database import Database
from src.utils.base import is_timezone
from src.utils.checks import is_server_manager_or_bot_owner


class ServerAdmin(commands.Cog):
    def __init__(self, bot):
        self.bot: BotType = bot

    @commands.guild_only()
    @is_server_manager_or_bot_owner()
    @commands.group(aliases=["cfg"])
    async def config(self, ctx: commands.Context):
        """
        Updates guild configuration
        """
        if ctx.invoked_subcommand is None:
            await ctx.send(":warning: You didn't specify any subcommand.\n"
                           f":information_source: Learn more: `{ctx.prefix}help {ctx.invoked_with}`")

    @config.command()
    async def prefix(self, ctx: commands.Context, new_prefix=None):
        """
        Changes prefix
        """
        if new_prefix is None:
            return await ctx.send(":warning: You didn't specify new prefix!")

        await Database.set_prefix(ctx.guild.id, new_prefix)
        await self.bot.update_prefix(ctx.guild.id)

        await ctx.send(f":ok_hand: Prefix was changed to `{self.bot.prefixes.get(ctx.guild.id)}`")

    @config.command()
    async def timezone(self, ctx: commands.Context, new_timezone=None):
        """
        Changes timezone for logs and other bot functionality that involves time
        """
        if new_timezone is None:
            current_tz = self.bot.timezones.get(ctx.guild.id)
            return await ctx.send(f":information_source: Current timezone: **`{current_tz}`**")

        if is_timezone(new_timezone) is False:
            return await ctx.send(":warning: Got invalid timezone argument!")

        await ctx.send(f"{is_timezone(new_timezone)=}")


def setup(bot):
    bot.add_cog(ServerAdmin(bot))
