#  The MIT License (MIT)
#
#  Copyright (c) 2020 defracted
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

import random
from typing import Optional

from discord.ext import commands

from src.utils.base import is_num_in_str
from src.utils.custom_bot_class import DefraBot
from src.utils.jokes import Jokes
from src.utils.premade_embeds import DefraEmbed
from src.utils.translator import Translator


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot: DefraBot = bot

    def text_to_bits(self, text: str, encoding='utf-8', errors='surrogatepass'):
        bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
        return '0b' + bits.zfill(8 * ((len(bits) + 7) // 8))

    def text_from_bits(self, bits, encoding='utf-8', errors='surrogatepass'):
        n = int(bits, 2)
        return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'

    @commands.command(aliases=('bin',))
    async def binary(self, ctx, *, text: str):
        """BINARY_HELP"""
        if text.startswith("0b"):
            await ctx.send(embed=DefraEmbed(description=self.text_from_bits(text)))
        else:
            await ctx.send(embed=DefraEmbed(description=self.text_to_bits(text)))

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
