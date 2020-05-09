#  Copyright (c) 2020 defracted
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

import textwrap
from functools import partial
from io import BytesIO
from os.path import join, dirname

import aiohttp
import discord
from PIL import Image, ImageDraw, ImageFont
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType

from src.utils.custom_bot_class import DefraBot
from src.utils.translator import Translator


class Memes(commands.Cog):
    def __init__(self, bot):
        self.session = aiohttp.ClientSession(loop=bot.loop)
        self.bot: DefraBot = bot
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

    @commands.command()
    @commands.cooldown(1, 10, BucketType.user)
    @commands.max_concurrency(2, BucketType.default)
    async def shpaklevka(self, ctx, *, body: str):
        msg = await ctx.send("Your meme is being generated")

        if len(body) > 90:
            return await msg.edit(content=Translator.translate("CONTENT_LENGTH_90_MAX", ctx))

        fn = partial(self.generate_meme, "shpaklevka", body)
        meme = await self.bot.loop.run_in_executor(None, fn)
        file = discord.File(fp=meme, filename="shpaklevka.jpg")

        await ctx.send(file=file, content=f"{ctx.author.mention}")
        return await msg.delete()

    @commands.command()
    @commands.cooldown(1, 10, BucketType.user)
    @commands.max_concurrency(2, BucketType.default)
    async def pika(self, ctx, *, body: str):
        msg = await ctx.send("Generating your HQ meme...")

        fn = partial(self.generate_meme, "pika", body)
        meme = await self.bot.loop.run_in_executor(None, fn)
        file = discord.File(fp=meme, filename="pika.jpg")

        await ctx.send(file=file, content=f"{ctx.author.mention} pika-pika!")
        return await msg.delete()


def setup(bot):
    bot.add_cog(Memes(bot))
