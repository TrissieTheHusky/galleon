from discord.ext import commands
from src.utils.base import DefraEmbed
from src.utils.jokes import Jokes
import random
from typing import Optional
from src.utils.base import is_num_in_str


class Fun(commands.Cog, name="Забавы"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def coinflip(self, ctx: commands.Context, times: Optional[str] = None):
        """Подбрасывает монетку"""
        if times is None:
            if bool(random.getrandbits(1)) is True:
                return await ctx.send("Орёл!")
            else:
                return await ctx.send("Решка!")

        if times is not None:
            if not is_num_in_str(times):
                return await ctx.send(":warning: Количество подбрасываний должно являться целочисленным значением!")

            if int(times) > 1000:
                return await ctx.send(":warning: Количество подбрасываний не должно превышать `1000`!")

            flips = [bool(random.getrandbits(1)) for _ in range(int(times))]
            success = sum(res is True for res in flips)
            fails = sum(res is False for res in flips)

            return await ctx.send(f"**Выпало орлов:** {success}\n**Выпало решек:** {fails}")

    @commands.command()
    async def joke(self, ctx: commands.Context):
        """Отправляет самые смешные (нет) шутки"""
        await ctx.send(embed=DefraEmbed(description=Jokes.get(), title="Анекдоты)"))

    @commands.command()
    async def reverse_text(self, ctx: commands.Context, *, body: commands.clean_content):
        """тскет шав тёнревереп"""
        await ctx.send(embed=DefraEmbed(description=body[::-1], title="Текст-первёртыш"))

    @commands.command(name="rate")
    async def _rate(self, ctx: commands.Context, *, body: commands.clean_content):
        """Оценю что-нибудь по десятибальной шкале"""
        rating = random.randint(0, 10)
        await ctx.send(embed=DefraEmbed(description=f"Я бы оценил `{body}` на **{rating} / 10**.",
                                        title="Экспертная оценка от бота"))

    @commands.command(name="compare", usage="что-то | ещё что-то | потом ещё что-то")
    async def _compare(self, ctx: commands.Context, things: commands.clean_content):
        """Могу что-нибудь сравнить"""
        things = "".join(str(things)).split("|")
        things = [thing.strip(' ') for thing in things]

        await ctx.send(embed=DefraEmbed(description=f"**{random.choice(things)}** звучит круче.",
                                        title="Самое независимое мнение в интернете"))

    @commands.command()
    async def yesno(self, ctx: commands.Context, *, body: commands.clean_content):
        """Ответит да или нет на ваш вопрос"""
        ans = random.choice((":white_check_mark:", ":x:"))
        await ctx.send(embed=DefraEmbed(
            description=f"**{ctx.author.name}:** {body}\n**{self.bot.user.name}:** {ans}",
            title="Да или нет? Вот в чём вопрос..."))


def setup(bot):
    bot.add_cog(Fun(bot))
