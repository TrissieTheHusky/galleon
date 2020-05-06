from discord import Member
from discord.ext import commands

from src.utils.apis import APIs
from src.utils.custom_bot_class import DefraBot
from src.utils.premade_embeds import DefraEmbed
from src.utils.translator import Translator


class CuteStuff(commands.Cog):
    def __init__(self, bot):
        self.bot: DefraBot = bot

    @commands.command()
    async def fox(self, ctx):
        """FOX_HELP"""
        await ctx.trigger_typing()
        some_cat = await APIs.get_fox()

        embed = DefraEmbed(title=":fox: " + Translator.translate("THIS_FOX", ctx))
        embed.set_image(url=some_cat)

        await ctx.send(embed=embed)

    @commands.command()
    async def cat(self, ctx):
        """CAT_HELP"""
        await ctx.trigger_typing()
        some_cat = await APIs.get_cat(self.bot.cfg['API_KEYS']['CATS'])

        embed = DefraEmbed(title=":cat: " + Translator.translate("THIS_CAT", ctx))
        embed.set_image(url=some_cat)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 1, commands.BucketType.guild)
    @commands.guild_only()
    async def hug(self, ctx, target: Member):
        """HUG_HELP"""
        await ctx.send(Translator.translate("HUG_MESSAGE_1", ctx, target=target.mention, author=str(ctx.author)))


def setup(bot):
    bot.add_cog(CuteStuff(bot))
