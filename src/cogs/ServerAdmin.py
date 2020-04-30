from discord.ext import commands

from src.utils.custom_bot_class import DefraBot
from src.utils.database import Database
from src.utils.base import is_timezone
from src.utils.checks import is_server_manager_or_bot_owner
from src.utils.cache import Cache


class ServerAdmin(commands.Cog):
    def __init__(self, bot):
        self.bot: DefraBot = bot

    @commands.command(name="whatprefix", aliases=["prefix", "currentprefix"])
    async def what_prefix(self, ctx):
        if ctx.guild is None:
            return await ctx.send(f"Current prefix is `{self.bot.cfg['DEFAULT_PREFIX']}`")

        prefix = self.bot.prefixes.get(ctx.guild.id, self.bot.cfg['DEFAULT_PREFIX'])
        await ctx.send(f"Current prefix is `{prefix if prefix is not None else self.bot.cfg['DEFAULT_PREFIX']}`")

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
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def prefix(self, ctx: commands.Context, new_prefix=None):
        """
        Changes prefix
        """
        if new_prefix is None:
            return await ctx.send(":warning: You didn't specify new prefix!")

        await Database.set_prefix(ctx.guild.id, new_prefix)
        await self.bot.update_prefix(ctx.guild.id)

        if self.bot.prefixes.get(ctx.guild.id) == new_prefix:
            await ctx.send(f":ok_hand: Server's prefix has been updated to `{new_prefix}`")
        else:
            await ctx.send(f":x: It looks like something went wrong and server's timezone didn't update. "
                           "Please, contact bot developer to fix this issue.")

    @config.command()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def timezone(self, ctx: commands.Context, new_timezone=None):
        """
        Changes timezone for logs and other bot functionality that involves time
        """
        if new_timezone is None:
            current_tz = await Cache.get_timezone(str(ctx.guild.id))
            return await ctx.send(f":ok_hand: Current timezone: **`{current_tz}`**")

        if is_timezone(new_timezone) is False:
            return await ctx.send(":warning: Got invalid timezone argument!")

        await Database.set_timezone(ctx.guild.id, new_timezone)
        await Cache.update_timezone(str(ctx.guild.id))

        if await Cache.get_timezone(str(ctx.guild.id)) == new_timezone:
            await ctx.send(f":ok_hand: Server's timezone has been updated to `{new_timezone}`")
        else:
            await ctx.send(f":x: It looks like something went wrong and server's timezone didn't update. "
                           "Please, contact bot developer to fix this issue.")


def setup(bot):
    bot.add_cog(ServerAdmin(bot))
