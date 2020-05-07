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

from discord import Member
from discord.ext import commands

from src.utils.apis import APIs
from src.utils.custom_bot_class import DefraBot
from src.utils.premade_embeds import DefraEmbed
from src.utils.translator import Translator


class CuteStuff(commands.Cog):
    def __init__(self, bot):
        self.bot: DefraBot = bot

    @commands.command()
    async def fox(self, ctx):
        """FOX_HELP"""
        await ctx.trigger_typing()
        some_cat = await APIs.get_fox()

        embed = DefraEmbed(title=":fox: " + Translator.translate("THIS_FOX", ctx))
        embed.set_image(url=some_cat)

        await ctx.send(embed=embed)

    @commands.command()
    async def cat(self, ctx):
        """CAT_HELP"""
        await ctx.trigger_typing()
        some_cat = await APIs.get_cat(self.bot.cfg['API_KEYS']['CATS'])

        embed = DefraEmbed(title=":cat: " + Translator.translate("THIS_CAT", ctx))
        embed.set_image(url=some_cat)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 1, commands.BucketType.guild)
    @commands.guild_only()
    async def hug(self, ctx, target: Member):
        """HUG_HELP"""
        await ctx.send(Translator.translate("HUG_MESSAGE_1", ctx, target=target.mention, author=str(ctx.author)))


def setup(bot):
    bot.add_cog(CuteStuff(bot))
