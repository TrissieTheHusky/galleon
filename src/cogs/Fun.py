from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
import discord
from os.path import join, dirname
from PIL import Image, ImageDraw, ImageFont
from functools import partial
from io import BytesIO
import textwrap
import random
import os


class Fun(commands.Cog, name="Смешнявки"):
    def __init__(self, bot):
        self.bot = bot
        self.meme_font = ImageFont.truetype(font=join(dirname(__file__), "../meme_templates/FiraMono-Bold.ttf"), size=72, encoding="utf-8")

    def surprise_pika(self, text: str) -> BytesIO:
        buffer = BytesIO()

        with Image.open(join(dirname(__file__), "../meme_templates/pika_surprised.png")) as pika:
            draw = ImageDraw.Draw(pika)

            pika_width, pika_height = pika.size

            char_width, char_height = self.meme_font.getsize('A')
            chars_per_line = pika_width // char_width

            text_line = textwrap.wrap(text.upper(), width=chars_per_line)

            y = 20

            for line in text_line:
                line_width, line_height = self.meme_font.getsize(line)

                x = (pika_width - line_width) / 2

                # Обводка
                draw.text((x-2, y), line, font=self.meme_font, fill='black')
                draw.text((x+2, y), line, font=self.meme_font, fill='black')
                draw.text((x, y-2), line, font=self.meme_font, fill='black')
                draw.text((x, y+2), line, font=self.meme_font, fill='black')

                # Сам текст
                draw.text((x, y), line, fill='white', font=self.meme_font)

                y += line_height

            pika.save(buffer, format="png")

        buffer.seek(0)

        return buffer

    @commands.command(name="pika")
    @commands.cooldown(1, 30, BucketType.user)
    async def surprised_pika(self, ctx, *, body: str):
        """Генерирует мем с шкоированным Пикачу :о"""
        msg = await ctx.send("Generating your HQ meme...")

        fn = partial(self.surprise_pika, body)
        meme = await self.bot.loop.run_in_executor(None, fn)
        file = discord.File(fp=meme, filename="pika.png")

        await ctx.send(file=file, content=f"{ctx.author.mention}, ваше чудо-творение готово!")
        return await msg.delete()

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
