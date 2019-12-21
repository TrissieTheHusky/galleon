from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
import discord
from os.path import join, dirname
from PIL import Image, ImageDraw, ImageFont
from functools import partial
from io import BytesIO
import textwrap


class MemeGenerator(commands.Cog, name="Генератор мемов"):
    def __init__(self, bot):
        self.bot = bot
        self.meme_font = ImageFont.truetype(font=join(dirname(__file__), "../meme_templates/FiraMono-Bold.ttf"), size=75, encoding="utf-8")

    def generate_meme(self, meme: str, text: str) -> BytesIO:
        buffer = BytesIO()

        with Image.open(join(dirname(__file__), f"../meme_templates/{meme}.jpg")) as img:
            draw = ImageDraw.Draw(img)

            img_width, img_height = img.size

            char_width, char_height = self.meme_font.getsize('A')
            chars_per_line = img_width // char_width

            text_line = textwrap.wrap(text.upper(), width=chars_per_line)

            y = 0

            if meme == "shpaklevka":
                y = 900
            elif meme == "pika":
                y = 30

            for line in text_line:
                line_width, line_height = self.meme_font.getsize(line)

                x = (img_width - line_width) / 2

                # Обводка
                draw.text((x - 5, y), line, font=self.meme_font, fill='black')
                draw.text((x + 5, y), line, font=self.meme_font, fill='black')
                draw.text((x, y - 5), line, font=self.meme_font, fill='black')
                draw.text((x, y + 5), line, font=self.meme_font, fill='black')

                # Сам текст
                draw.text((x, y), line, fill='white', font=self.meme_font)

                y += line_height

            img.save(buffer, format="jpeg", optimize=True, quality=90)

        buffer.seek(0)

        return buffer

    @commands.command(name="shpaklevka")
    @commands.cooldown(1, 30, BucketType.user)
    async def shpaklevka_meme(self, ctx, *, body: str):
        """шапклёвка )))"""
        msg = await ctx.send("Generating your HQ meme...")

        if len(body) > 90:
            return await msg.edit(content=":x: Длина текста не может превышать 90 символов!")

        fn = partial(self.generate_meme, "shpaklevka", body)
        meme = await self.bot.loop.run_in_executor(None, fn)
        file = discord.File(fp=meme, filename="shpaklevka.jpg")

        await ctx.send(file=file, content=f"{ctx.author.mention}, ваше чудо-творение готово!")
        return await msg.delete()

    @commands.command(name="pika")
    @commands.cooldown(1, 30, BucketType.user)
    async def surprised_pika(self, ctx, *, body: str):
        """Генерирует мем с шокированным Пикачу :о"""
        msg = await ctx.send("Generating your HQ meme...")

        fn = partial(self.generate_meme, "pika", body)
        meme = await self.bot.loop.run_in_executor(None, fn)
        file = discord.File(fp=meme, filename="pika.jpg")

        await ctx.send(file=file, content=f"{ctx.author.mention}, ваше чудо-творение готово!")
        return await msg.delete()


def setup(bot):
    bot.add_cog(MemeGenerator(bot))
