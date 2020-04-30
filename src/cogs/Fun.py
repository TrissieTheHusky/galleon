import random
from typing import Optional
from discord.ext import commands
from src.utils.base import DefraEmbed
from src.utils.base import is_num_in_str
from src.utils.custom_bot_class import DefraBot
from src.utils.jokes import Jokes
from src.utils.apis import APIs


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot: DefraBot = bot

    @commands.command()
    async def fox(self, ctx):
        """Sends a fox in the chat"""
        some_cat = await APIs.get_fox()

        embed = DefraEmbed(title=":fox: This is a fox!")
        embed.set_image(url=some_cat)

        await ctx.send(embed=embed)

    @commands.command()
    async def cat(self, ctx):
        """Sends a cat in the chat"""
        some_cat = await APIs.get_cat(self.bot.cfg['API_KEYS']['CATS'])

        embed = DefraEmbed(title=":cat: This is a cat!")
        embed.set_image(url=some_cat)

        await ctx.send(embed=embed)

    @commands.command()
    async def coinflip(self, ctx, times: Optional[str] = None):
        """Heads or Tails"""
        if times is None:
            if bool(random.getrandbits(1)) is True:
                return await ctx.send("Heads!")
            else:
                return await ctx.send("Tails!")

        if times is not None:
            if not is_num_in_str(times):
                return await ctx.send(":warning: The number of flips must be an integer number type!")

            if int(times) > 1000:
                return await ctx.send(":warning: The number of flips can't be higher than `1000`!")

            flips = [bool(random.getrandbits(1)) for _ in range(int(times))]
            success = sum(res is True for res in flips)
            fails = sum(res is False for res in flips)

            return await ctx.send(f"**Heads:** {success}\n**Tails:** {fails}")

    @commands.command()
    async def joke(self, ctx):
        """Very funny jokes in Russian"""
        await ctx.send(embed=DefraEmbed(description=Jokes.get(), title="Анекдоты)"))

    @commands.command(aliases=["reverse"])
    async def reverse_text(self, ctx, *, body: commands.clean_content):
        """Reverses your text input"""
        await ctx.send(embed=DefraEmbed(description=body[::-1], title="Reversed text"))

    @commands.command(name="rate")
    async def _rate(self, ctx, *, body: commands.clean_content):
        """Rates something"""
        rating = random.randint(0, 10)
        await ctx.send(embed=DefraEmbed(description=f"I would rate `{body}` by **{rating} / 10**.",
                                        title="The Best Opinion of the Universe"))

    @commands.command(name="compare", usage="thing | another thing | and another thing")
    async def _compare(self, ctx, things: commands.clean_content):
        """Compares something"""
        things = "".join(str(things)).split("|")
        things = [thing.strip(' ') for thing in things]

        await ctx.send(embed=DefraEmbed(description=f"**{random.choice(things)}** sounds better.",
                                        title="The Best Opinion of the Universe"))

    @commands.command()
    async def yesno(self, ctx, *, body: commands.clean_content):
        """Answers with yes or no"""
        ans = random.choice((":white_check_mark:", ":x:"))
        await ctx.send(embed=DefraEmbed(
            description=f"**{ctx.author.name}:** {body}\n**{self.bot.user.name}:** {ans}",
            title="Yes or No"))


def setup(bot):
    bot.add_cog(Fun(bot))
