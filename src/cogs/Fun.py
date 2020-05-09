#  Galleon — A multipurpose Discord bot.
#  Copyright (C) 2020  defracted.
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

import asyncio
import random
from typing import Optional

from discord import Status
from discord.ext import commands

from src.utils.base import is_num_in_str, text_from_bits, text_to_bits
from src.utils.custom_bot_class import DefraBot
from src.utils.jokes import Jokes
from src.utils.premade_embeds import DefraEmbed
from src.utils.translator import Translator


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot: DefraBot = bot

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
                return await ctx.send(":warning: {0}".format(Translator.translate("FLIPS_NUM_MUST_BE_INT", ctx)))

            if int(times) > 1000:
                return await ctx.send(":warning: {0}".format(Translator.translate("FLIPS_MAX_NUM", ctx)))

            flips = [bool(random.getrandbits(1)) for _ in range(int(times))]
            success = sum(res is True for res in flips)
            fails = sum(res is False for res in flips)

            return await ctx.send("{0}\n{1}".format(Translator.translate('HEADS', ctx, heads=success),
                                                    Translator.translate('TAILS', ctx, tails=fails)))

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
