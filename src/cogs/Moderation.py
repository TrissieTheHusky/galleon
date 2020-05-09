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

import discord
from discord.ext import commands
from ..utils.translator import Translator
from ..utils.custom_bot_class import DefraBot


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot: DefraBot = bot

    async def cog_check(self, ctx):
        return ctx.author.id == self.bot.owner.id

    @commands.command()
    @commands.guild_only()
    @commands.bot_has_guild_permissions(ban_members=True)
    async def ban(self, ctx, target: discord.Member = None, reason=None):
        if target is None:
            return await ctx.send("You need to specify someone you want to ban")

        if reason is None:
            reason = Translator.translate('INF_NO_REASON', ctx.guild.id)

        try:
            await ctx.guild.ban(user=target, reason=reason)
            await self.bot.infraction.add(inf_type='permaban', guild_id=ctx.guild.id, target_id=target.id, moderator_id=ctx.author.id, reason=reason)
        except:
            return


def setup(bot):
    bot.add_cog(Moderation(bot))
