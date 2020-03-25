from discord.ext import commands
import random


class Fun(commands.Cog, name="Fun"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def joke(self, ctx: commands.Context):
        """Sends some stupid joke lmao"""

    @commands.command()
    async def reverse_text(self, ctx: commands.Context, *, body: commands.clean_content):
        """Flips your input"""
        return await ctx.send(body[::-1])

    @commands.command(name="rate")
    async def _rate(self, ctx: commands.Context, *, body: commands.clean_content):
        """Rates something"""
        rating = random.randint(0, 10)
        return await ctx.send(f"I'd give `{body}` **{rating} / 10**.")

    @commands.command(name="compare", usage="thing | another thing | one more thing")
    async def _compare(self, ctx: commands.Context, things: commands.clean_content):
        """Compares things"""
        things = " ".join(str(things)).split("|")
        things = [thing.strip(' ') for thing in things]
        return await ctx.send(f"**{random.choice(things)}** sounds better.")

    @commands.command()
    async def yesno(self, ctx: commands.Context, *, body: commands.clean_content):
        """Answers with yes or no to your question"""
        ans = random.choice(["yes", "no"])
        return await ctx.send(f"**{ctx.author.name}:** {body}\n**{self.bot.user.name}:** {ans}")


def setup(bot):
    bot.add_cog(Fun(bot))
