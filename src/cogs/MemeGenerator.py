from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
import discord
from os.path import join, dirname
from PIL import Image, ImageDraw, ImageFont
from functools import partial
from io import BytesIO
import aiohttp
import textwrap


class MemeGenerator(commands.Cog, name="Memes generator"):
    def __init__(self, bot):
        self.session = aiohttp.ClientSession(loop=bot.loop)
        self.bot = bot
        self.meme_font = ImageFont.truetype(font=join(dirname(__file__), "../meme_templates/FiraMono-Bold.ttf"),
                                            size=75, encoding="utf-8")

    def become_mandalorian(self, minecraft_skin: bytes) -> BytesIO:
        buffer = BytesIO()

        with Image.open(BytesIO(minecraft_skin)) as img:
            img = img.convert("RGBA")

            with Image.new("RGBA", img.size) as bg:
                with Image.open(join(dirname(__file__), f"../meme_templates/mando_helm.png")) as mando:
                    mando = mando.convert("RGBA")
                    mando = mando.crop((0, 0, 64, 16))

                    bg.paste(img)
                    bg.paste(mando)

                bg.save(buffer, format="PNG")

        buffer.seek(0)

        return buffer

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

    @commands.command(name="mandalorianize")
    @commands.cooldown(1, 30, BucketType.user)
    async def mandalorianize(self, ctx):
        """Become The Mandalorian"""
        msg = await ctx.send("Generating...")
        attachments = ctx.message.attachments

        if len(attachments) <= 0:
            return await msg.edit(content="You have to attach your minecraft skin to the message!")

        if attachments[0].width != 64 and (attachments[0].height != 64 or attachments[0].height != 32):
            return await msg.edit(content="Picture size must be 64x64 or 64x32!")

        skin_url = attachments[0].url

        async with self.session.get(skin_url) as res:
            skin_bytes = await res.read()

        fn = partial(self.become_mandalorian, skin_bytes)
        mandalorized = await self.bot.loop.run_in_executor(None, fn)
        file = discord.File(fp=mandalorized, filename=f"mando_{ctx.author.name}.png")

        await ctx.send(file=file, content=f"{ctx.author.mention}, this is the way.")
        return await msg.delete()

    @commands.command(name="shpaklevka")
    @commands.cooldown(1, 30, BucketType.user)
    async def shpaklevka_meme(self, ctx, *, body: str):
        """some steve from minecref"""
        msg = await ctx.send("Generating your HQ meme...")

        if len(body) > 90:
            return await msg.edit(content=":x: Text length must be less than 90 characters")

        fn = partial(self.generate_meme, "shpaklevka", body)
        meme = await self.bot.loop.run_in_executor(None, fn)
        file = discord.File(fp=meme, filename="shpaklevka.jpg")

        await ctx.send(file=file, content=f"{ctx.author.mention}, your art is here!")
        return await msg.delete()

    @commands.command(name="pika")
    @commands.cooldown(1, 30, BucketType.user)
    async def surprised_pika(self, ctx, *, body: str):
        """Shocked pika meme with your text"""
        msg = await ctx.send("Generating your HQ meme...")

        fn = partial(self.generate_meme, "pika", body)
        meme = await self.bot.loop.run_in_executor(None, fn)
        file = discord.File(fp=meme, filename="pika.jpg")

        await ctx.send(file=file, content=f"{ctx.author.mention} pika-pika!")
        return await msg.delete()


def setup(bot):
    bot.add_cog(MemeGenerator(bot))
