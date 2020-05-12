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
from ..utils.menus import MyPagesMenu, MyPagesSource


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot: DefraBot = bot

    async def cog_check(self, ctx):
        return ctx.author.id == self.bot.owner.id

    # TODO: Make custom checks for admin or mod role in DB
    # TODO: Add i18n

    @commands.group(aliases=('i', 'inf', 'infraction'))
    @commands.guild_only()
    async def infractions(self, ctx):
        if ctx.invoked_subcommand is None:
            return await ctx.send("what subcommand???!!! SEE HELP YOU GOOD PERSON!!!!")

    @infractions.command()
    @commands.guild_only()
    async def search(self, ctx, *, query: str):
        if query.lower().startswith("[mod]"):
            pass
        elif query.lower().startswith("[user]"):
            pass
        else:
            infractions = await self.bot.infraction.get(target_id=int(query))

            entries = []
            for inf in infractions:
                entries.append(
                    f'{inf["inf_type"].upper()}\n**Moderator:** {inf["moderator_id"]}\n**User:** {inf["target_id"]}\n**Reason:** {inf["reason"]}\n\n')

            src = MyPagesSource(per_page=4, title=f"Infraction history for {query}", entries=entries)
            menu = MyPagesMenu(src)
            await menu.start(ctx)

    @commands.command()
    @commands.guild_only()
    @commands.bot_has_guild_permissions(ban_members=True)
    async def ban(self, ctx, target: discord.Member = None, *, reason=None):
        if target is None:
            return await ctx.send("You need to specify someone you want to ban")

        if reason is None:
            reason = Translator.translate('INF_NO_REASON', ctx.guild.id)

        try:
            await ctx.guild.ban(user=target, reason=reason)
            await self.bot.infraction.add(inf_type='permaban', guild_id=ctx.guild.id, target_id=target.id, moderator_id=ctx.author.id, reason=reason)
            await ctx.send(f":ok_hand: {target} (`{target.id}`) banned for: `{reason}`.")
        except:
            return

    @commands.command()
    @commands.guild_only()
    async def warn(self, ctx, target: discord.Member = None, *, reason=None):
        if target is None:
            return await ctx.send("You need to specify someone you want to warn")

        if reason is None:
            reason = Translator.translate('INF_NO_REASON', ctx.guild.id)

        await self.bot.infraction.add(inf_type='warn', guild_id=ctx.guild.id, target_id=target.id, moderator_id=ctx.author.id, reason=reason)
        await ctx.send(f":ok_hand: Warning for {target} (`{target.id}`) added, reason: `{reason}`")


def setup(bot):
    bot.add_cog(Moderation(bot))
