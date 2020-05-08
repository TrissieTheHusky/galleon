import asyncio
import random
import textwrap
from functools import partial
from io import BytesIO
from os.path import join, dirname
from typing import Optional, Union

from PIL import Image, ImageDraw, ImageFont
from colorthief import ColorThief
from discord import Status, Member, File
from discord.ext import commands

from src.utils.base import is_num_in_str, text_from_bits, text_to_bits
from src.utils.converters import NotCachedUser
from src.utils.custom_bot_class import DefraBot
from src.utils.jokes import Jokes
from src.utils.premade_embeds import DefraEmbed
from src.utils.translator import Translator


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot: DefraBot = bot
        self.pil_font = ImageFont.truetype(font=join(dirname(__file__), "../meme_templates/FiraSans-SemiBold.ttf"), size=30, encoding="utf-8")

    @commands.command(aliases=("ac", "avatarcolor"))
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def avatarcolors(self, ctx, user: Optional[Union[Member, NotCachedUser]] = None):
        """AVATARCOLORS_HELP"""
        await ctx.trigger_typing()

        user = user or ctx.author

        user_avatar_bytes = BytesIO(await user.avatar_url_as(format="png").read())
        colors = ColorThief(user_avatar_bytes)
        palette = colors.get_palette(quality=1, color_count=5)

        def make_the_image():
            buffer = BytesIO()

            with Image.new('RGBA', (900, 600), (0, 0, 0, 0)) as im:

                avatar = Image.open(user_avatar_bytes).resize((500, 500), Image.ANTIALIAS)
                avatar.convert("RGBA")
                im.paste(avatar, (300, 10))

                img_width, img_height = avatar.size

                char_width, char_height = self.pil_font.getsize('A')
                chars_per_line = img_width // char_width

                text_line = textwrap.wrap(f"{user.name}#{user.discriminator}", width=chars_per_line)

                draw = ImageDraw.Draw(im)
                for index, color in enumerate(palette):
                    y = (index * 100) + 10
                    draw.ellipse([(0, 0 + y), (100, 100 + y)], fill=color, outline=(0, 0, 0))

                    r, g, b = color
                    hex_color = "{:02x}{:02x}{:02x}".format(r, g, b)
                    draw.text((110, 0 + (y + 31)), f"#{hex_color}", (255, 255, 255), font=self.pil_font)

                for line in text_line:
                    line_width, line_height = self.pil_font.getsize(line)
                    x = 300 + (img_width - line_width) / 2
                    y = 530

                    draw.text((x, y), line, (255, 255, 255), font=self.pil_font)
                    y += line_height

                im.save(buffer, "png")

            buffer.seek(0)
            return buffer

        fn = partial(make_the_image)
        final_buffer = await self.bot.loop.run_in_executor(None, fn)
        file = File(filename=f"avatar_colors_for_{user.display_name}.png", fp=final_buffer)

        await ctx.send(file=file)

    @commands.command()
    @commands.cooldown(2, 5, commands.BucketType.guild)
    async def who(self, ctx):
        """WHO_HELP"""
        picked_member = random.choice(tuple(filter(lambda m: True if m.status is not Status.offline else False, ctx.guild.members)))

        e = DefraEmbed()
        e.title = Translator.translate('WHO_TITLE', ctx)
        e.set_image(url=picked_member.avatar_url)

        def check(m):
            return picked_member.name.lower() in m.content.lower() or picked_member.display_name.lower() in m.content.lower()

        try:
            await ctx.send(embed=e)
            msg = await self.bot.wait_for('message', check=check, timeout=10.0)
        except asyncio.TimeoutError:
            await ctx.send(Translator.translate('WHO_CORRECT_ANSWER_WAS', ctx, user=picked_member.display_name))
        else:
            await ctx.send(embed=DefraEmbed(
                now_time=False, description=Translator.translate('WHO_ANSWER_IS_CORRECT', ctx, author=msg.author.mention, message_url=msg.jump_url)))

    @commands.command(aliases=('bin',))
    async def binary(self, ctx, *, text: str):
        """BINARY_HELP"""
        if text.startswith("0b"):
            await ctx.send(embed=DefraEmbed(description=text_from_bits(text)))
        else:
            await ctx.send(embed=DefraEmbed(description=text_to_bits(text)))

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

            return await ctx.send(Translator.translate('HEADS', ctx, heads=success) + "\n" + Translator.translate('TAILS', ctx, tails=fails))

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

    @commands.command(aliases=("choose",))
    async def compare(self, ctx, *things: commands.clean_content):
        """COMPARE_HELP"""
        await ctx.send(embed=DefraEmbed(
            description=Translator.translate("COMPARE_DESCRIPTION", ctx, thing=random.choice(things)),
            title=Translator.translate("RATE_TITLE", ctx)))

    @commands.command()
    async def yesno(self, ctx, *, text: commands.clean_content):
        """YESNO_HELP"""
        ans = random.choice((Translator.translate("YES", ctx), Translator.translate("NO", ctx)))
        await ctx.send(embed=DefraEmbed(
            description=Translator.translate("YES_OR_NO_ANSWER", ctx, author=ctx.author.name, text=text, bot=self.bot.user.name, answer=ans),
            title=Translator.translate("YES_OR_NO", ctx)))


def setup(bot):
    bot.add_cog(Fun(bot))
