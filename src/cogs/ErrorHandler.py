from datetime import datetime
from discord.ext import commands

from src.utils.custom_bot_class import DefraBot

import discord
import traceback
import sys


class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot: DefraBot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        """
        ctx   : Context
        error : Exception
        """
        if hasattr(ctx.command, 'on_error'):
            return

        error = getattr(error, 'original', error)
        is_ignore_enabled = False
        ignored = commands.UserInputError

        if is_ignore_enabled:
            if isinstance(error, ignored):
                return

        async def send_here(message: str):
            await ctx.send(message)

        async def send_here_no_perms():
            await ctx.send(f":lock: You don't have enough power to run `{ctx.command}`")

        # """"
        # Reference: isinstance(error, event)
        # """

        if isinstance(error, commands.CommandNotFound):
            return

        elif isinstance(error, commands.DisabledCommand):
            return await ctx.send(f'`{ctx.command}` is disabled.')

        elif isinstance(error, commands.MissingPermissions):
            return await send_here_no_perms()

        elif isinstance(error, commands.MissingRequiredArgument):
            return await send_here(
                ":warning: You've missed some important argument!.\n"
                f"\N{SPIRAL NOTE PAD} Command syntax: "
                f"`{ctx.prefix}{ctx.command.qualified_name} {ctx.command.signature}`"
            )

        elif isinstance(error, commands.errors.NotOwner):
            return await send_here_no_perms()

        elif isinstance(error, commands.BotMissingPermissions):
            return await ctx.send(f":x: I don't have enough permissions to perform this.")

        elif isinstance(error, commands.CheckFailure):
            return await send_here_no_perms()

        elif isinstance(error, commands.NoPrivateMessage):
            return await ctx.author.send(f":x: {ctx.command} can only be used on a server.")

        elif isinstance(error, discord.Forbidden):
            return await ctx.send(f":x: I don't have enough permissions to perform this.")

        # ==== COOLDOWN CHECKS ====

        elif isinstance(error, commands.CommandOnCooldown):
            if await ctx.bot.is_owner(ctx.message.author):
                return await ctx.reinvoke()

            return await ctx.send(
                f'Please, wait **{round(error.retry_after, 2)}** seconds before running this command.')

        e = discord.Embed(
            color=0xFF0000,
            title=f"Uncaught Exception in command {ctx.command}",
            description=f"{error}",
            timestamp=datetime.utcnow()
        )
        e.add_field(name="Author", value=f"{ctx.author} (`{ctx.author.id}`)")
        e.add_field(name="Command", value=f"{ctx.message.content}", inline=False)

        if ctx.guild is not None:
            e.add_field(name="Guild", value=f"{ctx.guild} (`{ctx.guild.id}`)")

        await self.bot.dev_channel.send(f"{self.bot.owner.mention}", embed=e)
        await ctx.send(':x: Unexpected error, developer was informed about it.')
        e.clear_fields()
        print('---------\nIgnoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
