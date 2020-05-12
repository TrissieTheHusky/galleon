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

import re
import sys
import traceback
from datetime import datetime

import discord
from discord.ext import commands

from src.utils.checks import BlacklistedUser
from src.utils.custom_bot_class import DefraBot
from src.utils.premade_embeds import error_embed, warn_embed
from src.utils.translator import Translator


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
        ignored = (BlacklistedUser, commands.CommandNotFound)

        if isinstance(error, ignored):
            return

        elif isinstance(error, commands.CommandOnCooldown):
            if ctx.author.id == self.bot.owner.id:
                return await ctx.reinvoke()

            return await ctx.send(
                delete_after=10,
                embed=warn_embed(title=Translator.translate("ERROR_HANDLER_ON_COOLDOWN", ctx),
                                 text=Translator.translate("ERROR_HANDLER_ON_COOLDOWN_WAIT", ctx, wait_more=str(round(error.retry_after, 2)))))

        elif isinstance(error, commands.DisabledCommand):
            return await ctx.send(f'`{ctx.command}` is disabled.')

        elif isinstance(error, commands.MissingPermissions):
            return await ctx.send(embed=warn_embed(title=Translator.translate("ERROR_HANDLER_NO_PERMS", ctx)))

        elif isinstance(error, commands.errors.NotOwner):
            return await ctx.send(embed=warn_embed(title=Translator.translate("ERROR_HANDLER_NO_PERMS", ctx)))

        elif isinstance(error, commands.CheckFailure):
            return await ctx.send(embed=warn_embed(title=Translator.translate("ERROR_HANDLER_NO_PERMS", ctx)))

        elif isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send(embed=warn_embed(
                title=Translator.translate("ERROR_HANDLER_SYNTAX_ERR", ctx),
                text=Translator.translate("ERROR_HANDLER_MISSING_ARG", ctx,
                                          syntax=f"{ctx.prefix}{ctx.command.qualified_name} {ctx.command.signature}")))

        elif isinstance(error, commands.BadUnionArgument):
            if ctx.command.qualified_name == "userinfo" or ctx.command.qualified_name == "avatar":
                return await ctx.send(embed=warn_embed(
                    title=Translator.translate("ERROR_HANDLER_BAD_ARGUMENT", ctx),
                    text=Translator.translate("ERROR_HANDLER_USERINFO_INVALID_ARG", ctx)))

            elif ctx.command.qualified_name == "serverinfo":
                return await ctx.send(embed=warn_embed(
                    title=Translator.translate("ERROR_HANDLER_BAD_ARGUMENT", ctx),
                    text=Translator.translate('ERROR_HANDLER_SERVERINFO_INVALID_ARG', ctx)))

        elif isinstance(error, commands.BadArgument):
            if ctx.command.qualified_name == "hug":
                return await ctx.send(embed=warn_embed(
                    title=Translator.translate("ERROR_HANDLER_BAD_ARGUMENT", ctx),
                    text=Translator.translate("ERROR_HANDLER_HUG_NOT_FOUND", ctx, target=re.findall(r'"([^"]*)"', error.args[0])[0])
                ))

        elif isinstance(error, commands.NoPrivateMessage):
            return await ctx.author.send(Translator.translate("ERROR_HANDLER_SERVER_ONLY", ctx, command=str(ctx.command)))

        elif isinstance(error, commands.BotMissingPermissions):
            return await ctx.send(embed=error_embed(text=Translator.translate("ERROR_HANDLER_BOT_MISSING_PERMS", ctx)))

        elif isinstance(error, discord.Forbidden):
            return await ctx.send(embed=error_embed(text=Translator.translate("ERROR_HANDLER_BOT_MISSING_PERMS", ctx)))

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
            e.add_field(name="Message URL", value=f"[Jump to error](https://discord.com/channels/{ctx.guild.id}/{ctx.channel.id}/{ctx.message.id})")

        await self.bot.dev_channel.send(f"{self.bot.owner.mention}", embed=e)
        await ctx.send(
            embed=discord.Embed(
                title=Translator.translate("ERROR_HANDLER_UNEXPECTED", ctx),
                color=discord.Color.red(),
                description=f"```py\n{error}\n```"
            )
        )
        e.clear_fields()
        print('---------\nIgnoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
