from discord.ext import commands

from src.utils.base import is_timezone
from src.utils.cache import Cache
from src.utils.checks import is_server_manager_or_bot_owner
from src.utils.custom_bot_class import DefraBot
from src.utils.database import Database
from src.utils.translator import Translator


class ServerAdmin(commands.Cog):
    def __init__(self, bot):
        self.bot: DefraBot = bot

    @commands.command(name="whatprefix", aliases=["prefix", "currentprefix"])
    async def what_prefix(self, ctx):
        """WHATPREFIX_HELP"""
        if ctx.guild is None:
            return await ctx.send(Translator.translate('WHATPREFIX', ctx, prefix=self.bot.cfg['DEFAULT_PREFIX']))

        prefix = self.bot.prefixes.get(ctx.guild.id, self.bot.cfg['DEFAULT_PREFIX'])
        await ctx.send(Translator.translate('WHATPREFIX', ctx, prefix=prefix))

    @commands.guild_only()
    @is_server_manager_or_bot_owner()
    @commands.group(aliases=["cfg"])
    async def config(self, ctx: commands.Context):
        """CONFIG_HELP"""
        if ctx.invoked_subcommand is None:
            await ctx.send(Translator.translate("NO_SUBCOMMAND", ctx, help=f"{ctx.prefix}{ctx.command} {ctx.command.signature}"))

    @config.command()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def prefix(self, ctx: commands.Context, new_prefix=None):
        """CONFIG_PREFIX_HELP"""
        if new_prefix is None:
            return await ctx.send(Translator.translate("CONFIG_PREFIX_NO_NEW"))

        await Database.set_prefix(ctx.guild.id, new_prefix)
        await self.bot.update_prefix(ctx.guild.id)

        if self.bot.prefixes.get(ctx.guild.id) == new_prefix:
            await ctx.send(Translator.translate("CONFIG_PREFIX_UPDATED", ctx, prefix=new_prefix))
        else:
            await ctx.send(Translator.translate("CONFIG_UPDATE_ERROR", ctx))

    @config.command()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def timezone(self, ctx, new_timezone=None):
        """CONFIG_TIMEZONE_HELP"""
        if new_timezone is None:
            current_tz = await Cache.get_timezone(str(ctx.guild.id))
            return await ctx.send(Translator.translate("CONFIG_TIMEZONE_CURRENT", ctx, current=current_tz))

        if is_timezone(new_timezone) is False:
            return await ctx.send(Translator.translate("CONFIG_TIMEZONE_BAD_TIMEZONE", ctx))

        await Database.set_timezone(ctx.guild.id, new_timezone)
        await Cache.update_timezone(str(ctx.guild.id))

        if await Cache.get_timezone(str(ctx.guild.id)) == new_timezone:
            await ctx.send(Translator.translate("CONFIG_TIMEZONE_UPDATED", ctx, timezone=new_timezone))
        else:
            await ctx.send(Translator.translate("CONFIG_UPDATE_ERROR", ctx))

    @config.command(aliases=["lang"])
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def language(self, ctx, new_language=None):
        """CONFIG_LANGUAGE_HELP"""
        if new_language is None:
            return await ctx.send(Translator.translate("CONFIG_LANGUAGE_CURRENT", ctx,
                                                       language=self.bot.languages.get(ctx.guild.id, "en_US")))

        if new_language not in Translator.languages.keys():
            return await ctx.send(Translator.translate("CONFIG_LANGUAGE_BAD_LANGUAGE", ctx,
                                                       languages=", ".join(list(Translator.languages.keys()))))

        await Database.set_language(ctx.guild.id, new_language)
        await self.bot.update_language(ctx.guild.id)

        await ctx.send(Translator.translate("CONFIG_LANGUAGE_UPDATED", ctx, language=new_language))


def setup(bot):
    bot.add_cog(ServerAdmin(bot))
