from discord.ext import commands
import random


class Fun(commands.Cog, name="Смешнявки"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def reverse_text(self, ctx, *, body: str):
        return await ctx.send(body[::-1])

    @commands.command(name="rate")
    async def _rate(self, ctx, *, body: commands.clean_content):
        rating = random.randint(0, 10)
        return await ctx.send(f"Я бы оценил `{body}` на **{rating} / 10**.")

    @commands.command(name="compare")
    async def _compare(self, ctx, *things: commands.clean_content):
        things = " ".join(list(things)).split("|")
        things = [thing.strip(' ') for thing in things]
        return await ctx.send(f"Я думаю, что **{random.choice(things)}** лучше.")

    @commands.command()
    async def yesno(self, ctx, *, body: commands.clean_content):
        ans = random.choice(["да", "нет"])
        return await ctx.send(f"**{ctx.author.name}:** {body}\n**{self.bot.user.name}:** {ans}")


def setup(bot):
    bot.add_cog(Fun(bot))
