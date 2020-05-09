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

        embed = DefraEmbed(title=":fox: {0}".format(Translator.translate("THIS_FOX", ctx)))
        embed.set_image(url=some_cat)

        await ctx.send(embed=embed)

    @commands.command()
    async def cat(self, ctx):
        """CAT_HELP"""
        await ctx.trigger_typing()
        some_cat = await APIs.get_cat(self.bot.cfg['API_KEYS']['CATS'])

        embed = DefraEmbed(title=":cat: {0}".format(Translator.translate("THIS_CAT", ctx)))
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
