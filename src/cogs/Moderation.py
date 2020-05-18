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

import re
from typing import Union

import discord
from discord.ext import commands
from discord.ext.menus import ListPageSource
from pytz import timezone

from ..utils.custom_bot_class import DefraBot
from ..utils.menus import MyPagesMenu
from ..utils.translator import Translator


class InfractionsPagesSource(ListPageSource):
    def format_page(self, menu, page):
        if isinstance(page, str):
            return page
        else:
            # self.embed.set_footer(text=)
            # self.embed.description = '\n'.join(page)
            return "```{0}``` {1}".format("\n".join(page), f"{Translator.translate('PAGE', menu.ctx)} {menu.current_page + 1}/{self.get_max_pages()}")


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
    async def search(self, ctx, *, query: str = None):
        infractions = []
        if query is None:
            infractions = await self.bot.infraction.get(guild_id=ctx.guild.id)
        elif query is not None:
            if query.lower().startswith("[mod]"):
                infractions = await self.bot.infraction.get(guild_id=ctx.guild.id, moderator_id=int(re.findall(r'\d+', query)[0]))
            elif query.lower().startswith("[user]"):
                infractions = await self.bot.infraction.get(guild_id=ctx.guild.id, target_id=int(re.findall(r'\d+', query)[0]))
            else:
                infractions = await self.bot.infraction.get(guild_id=ctx.guild.id, target_id=int(query))

        entries = []
        for inf in infractions:
            inf_type_format = Translator.translate(inf["inf_type"].upper(), ctx.guild.id)  # TODO: use translator on that
            reason_format = discord.utils.escape_markdown(discord.utils.escape_mentions(inf["reason"]))

            if (guild_timezone := self.bot.cache.timezones.get(ctx.guild.id, None)) is not None:
                date_format = inf['added_at'].astimezone(timezone(guild_timezone)).strftime("%d-%m-%Y %H:%M:%S")
            else:
                date_format = inf['added_at'].astimezone(timezone('UTC')).strftime("%d-%m-%Y %H:%M:%S")

            if (moderator := self.bot.get_user(inf["moderator_id"])) is None:
                mod_format = f'{inf["moderator_id"]}'
            else:
                mod_format = f'{moderator} ({moderator.id})'

            if (target := self.bot.get_user(inf["target_id"])) is None:
                target_format = f'{inf["target_id"]}'
            else:
                target_format = f'{target} ({target.id})'

            entries.append(
                f'{inf_type_format} #{inf["inf_id"]}\n----------------\nTimestamp: {date_format}\nUser: {target_format}\nModerator: {mod_format}\nReason: {reason_format}\n')

        src = InfractionsPagesSource(per_page=4, entries=entries)
        menu = MyPagesMenu(src, delete_message_after=True)
        await menu.start(ctx)

    @commands.command()
    @commands.guild_only()
    @commands.bot_has_guild_permissions(ban_members=True)
    async def ban(self, ctx, target: Union[discord.Member, int] = None, *, reason=None):
        if target is None:
            return await ctx.send("You need to specify someone you want to ban")

        if reason is None:
            reason = Translator.translate('INF_NO_REASON', ctx.guild.id)

        try:
            if isinstance(target, discord.Member):
                await ctx.guild.ban(user=target, reason=reason)
            elif isinstance(target, int):
                await ctx.guild.ban(discord.Object(id=target))

            await self.bot.infraction.add(inf_type='permaban', guild_id=ctx.guild.id, target_id=target.id, moderator_id=ctx.author.id, reason=reason)
            await ctx.send(f":ok_hand: {target} (`{target.id}`) banned for: `{reason}`.")
        except Exception as e:
            raise e

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
