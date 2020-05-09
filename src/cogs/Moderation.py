#  Copyright (c) 2020 defracted
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

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
