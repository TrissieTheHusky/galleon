import random
from typing import Optional

from discord.ext import commands

from src.utils.apis import APIs
from src.utils.base import DefraEmbed, is_num_in_str
from src.utils.custom_bot_class import DefraBot
from src.utils.jokes import Jokes
from src.utils.translator import Translator


class Fun(commands.Cog):
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

    @commands.command(aliases=("cf",))
    async def coinflip(self, ctx, times: Optional[str] = None):
        """COINFLIP_HELP"""
        if times is None:
            if bool(random.getrandbits(1)) is True:
                return await ctx.send(Translator.translate("HEADS", ctx, heads=1))
            else:
                return await ctx.send(Translator.translate("TAILS", ctx, tails=1))

        if times is not None:
            if not is_num_in_str(times):
                return await ctx.send(":warning: " + Translator.translate("FLIPS_NUM_MUST_BE_INT", ctx))

            if int(times) > 1000:
                return await ctx.send(":warning: " + Translator.translate("FLIPS_MAX_NUM", ctx))

            flips = [bool(random.getrandbits(1)) for _ in range(int(times))]
            success = sum(res is True for res in flips)
            fails = sum(res is False for res in flips)

            return await ctx.send(Translator.translate('HEADS', ctx, heads=success) + "\n" +
                                  Translator.translate('TAILS', ctx, tails=fails))

    @commands.command()
    async def joke(self, ctx):
        """JOKE_HELP"""
        await ctx.send(embed=DefraEmbed(description=Jokes.get(), title="Анекдоты)"))

    @commands.command(aliases=("reverse",))
    async def reverse_text(self, ctx, *, body: commands.clean_content):
        """REVERSE_HELP"""
        await ctx.send(embed=DefraEmbed(description=body[::-1], title=Translator.translate("REVERSED_TEXT", ctx)))

    @commands.command()
    async def rate(self, ctx, *, thing: commands.clean_content):
        """RATE_HELP"""
        rating = random.randint(0, 10)
        await ctx.send(embed=DefraEmbed(
            description=Translator.translate("RATE_DESCRIPTION", ctx, thing=thing, rating=rating),
            title=Translator.translate("RATE_TITLE", ctx)))

    @commands.command()
    async def compare(self, ctx, things: commands.clean_content):
        """COMPARE_HELP"""
        things = "".join(str(things)).split("|")
        things = [thing.strip(' ') for thing in things]

        await ctx.send(embed=DefraEmbed(
            description=Translator.translate("COMPARE_DESCRIPTION", ctx, thing=random.choice(things)),
            title=Translator.translate("RATE_TITLE", ctx)))

    @commands.command()
    async def yesno(self, ctx, *, text: commands.clean_content):
        """YESNO_HELP"""
        ans = random.choice((Translator.translate("YES", ctx), Translator.translate("NO", ctx)))
        await ctx.send(embed=DefraEmbed(
            description=Translator.translate("YES_OR_NO_ANSWER", ctx,
                                             author=ctx.author.name, text=text, bot=self.bot.user.name, answer=ans),
            title=Translator.translate("YES_OR_NO", ctx)))


def setup(bot):
    bot.add_cog(Fun(bot))
