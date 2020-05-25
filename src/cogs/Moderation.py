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
from datetime import datetime
from typing import Union

import discord
from discord.ext import commands, tasks
from discord.ext.menus import ListPageSource
from pytz import timezone

from src.utils.converters import Duration
from src.utils.custom_bot_class import DefraBot
from src.utils.enums import InfractionType
from src.utils.menus import MyPagesMenu
from src.utils.messages import Messages
from src.utils.premade_embeds import warn_embed
from src.utils.temp_actions import TempActions
from src.utils.translator import Translator


class InfractionsPagesSource(ListPageSource):
    def format_page(self, menu, page):
        if isinstance(page, str):
            return page
        else:
            if len(page) <= 0:
                return Translator.translate('EMPTY_INF_SEARCH', menu.ctx)
            return "```{0}``` {1}".format("\n".join(page), f"{Translator.translate('PAGE', menu.ctx)} {menu.current_page + 1}/{self.get_max_pages()}")


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot: DefraBot = bot
        self.infractions_checker.start()

    def cog_unload(self):
        self.infractions_checker.cancel()

    async def cog_check(self, ctx):
        if ctx.guild is None:
            raise commands.NoPrivateMessage() from None
        if ctx.author.id != self.bot.owner.id:
            raise commands.CheckFailure() from None
        return True

    async def add_ban(self, context, reason: str, target: Union[discord.Member, int]):
        if isinstance(target, discord.Member):
            await context.guild.ban(user=target, reason=reason)
        elif isinstance(target, int):
            target = await self.bot.fetch_user(target)
            await context.guild.ban(discord.Object(id=target.id), reason=reason)

    @tasks.loop(seconds=1.0)
    async def infractions_checker(self):
        # If there's no active infractions, do nothing
        if len(self.bot.active_infractions) <= 0:
            return

        for infraction in self.bot.active_infractions:
            # If the infraction still active (expiration date is not in the past or not this moment) - do nothing
            if infraction['expires_at'].timestamp() >= datetime.utcnow().timestamp():
                return

            # Obtain the guild object
            guild = self.bot.get_guild(infraction['guild_id'])

            # Do nothing if guild is None, perform actions if otherwise
            if guild is not None:
                if infraction['inf_type'] == InfractionType.tempban:
                    try:
                        member = discord.Object(id=infraction['target_id'])
                        await guild.unban(member, reason=Translator.translate('TEMP_BAN_EXPIRED', guild.id, inf_id=infraction['inf_id']))
                        await self.bot.infraction.deactivate(infraction['inf_id'])
                        self.bot.active_infractions.remove(infraction)
                    except discord.Forbidden:
                        pass  # TODO: Must inform the server owner through logging that bot lacks required permissions to un-ban
                    except discord.HTTPException:
                        pass  # Well, there's nothing we can do about it :P

    @commands.Cog.listener()
    async def on_check_actions(self):
        await self.bot.wait_until_ready()

        active_actions = await TempActions.get_active_actions(self.bot.db.pool)

        for action in active_actions:
            self.bot.active_infractions.append(action)

    @commands.group()
    async def archive(self, ctx):
        """ARCHIVE_HELP"""
        if ctx.invoked_subcommand is None:
            await ctx.send(embed=warn_embed(
                text=Translator.translate('NO_SUBCOMMAND_TEXT', ctx, help=f"{ctx.prefix}help {ctx.command.qualified_name}"),
                title=Translator.translate('NO_SUBCOMMAND_TITLE', ctx)))

    @archive.command(name="channel")
    async def archive_channel(self, ctx, amount: int = 100, channel: discord.TextChannel = None):
        """ARCHIVE_CHANNEL_HELP"""
        channel = channel or ctx.channel

        if amount > 2000:
            return await ctx.send(":x: You can archive up to 2000 messages!")

        messages = await channel.history(limit=amount).flatten()
        await Messages.send_archive(self.bot, ctx, messages, channel)

    @archive.command(name="user")
    async def archive_user(self, ctx, amount: int = 100, user: discord.Member = None, channel: discord.TextChannel = None):
        """ARCHIVE_USER_HELP"""
        if user is None:
            return await ctx.send(":x: You must specify some server member!")

        channel = channel or ctx.channel

        if amount > 3000:
            return await ctx.send(":x: You can archive up to 3000 messages for users!")

        messages = []
        async for message in channel.history(limit=amount):
            if message.author == user:
                messages.append(message)

        await Messages.send_archive(self.bot, ctx, messages, channel)

    @commands.group(aliases=('i', 'inf', 'infraction'))
    async def infractions(self, ctx):
        """INFRACTIONS_HELP"""
        if ctx.invoked_subcommand is None:
            return await ctx.send("what subcommand???!!! SEE HELP YOU GOOD PERSON!!!!")

    @infractions.command()
    async def search(self, ctx, *, query: str = None):
        """INFRACTIONS_SEARCH_HELP"""
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
            inf_type_format = Translator.translate(inf["inf_type"].upper(), ctx.guild.id)
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

            entry = (f'{inf_type_format} #{inf["inf_id"]}\n'
                     '-----------------------\n'
                     f'Timestamp: {date_format}\n'
                     f'Is active: {inf["is_active"]}\n'
                     f'User: {target_format}\n'
                     f'Moderator: {mod_format}\n'
                     f'Reason: {reason_format}\n'
                     '\n')

            entries.append(entry)

        src = InfractionsPagesSource(per_page=4, entries=entries)
        menu = MyPagesMenu(src, delete_message_after=True)
        await menu.start(ctx)

    @commands.command()
    @commands.bot_has_guild_permissions(kick_members=True)
    async def kick(self, ctx):
        """KICK_HELP"""
        pass

    @commands.command()
    @commands.bot_has_guild_permissions(ban_members=True)
    async def tempban(self, ctx, target: Union[discord.Member, int], duration: Duration, *, reason=None):
        """TEMPBAN_HELP"""
        if target is None:
            return await ctx.send("You need to specify someone you want to ban")

        if reason is None:
            reason = Translator.translate('INF_NO_REASON', ctx.guild.id)

        # Adding time to the current moment to create expiration datetime object
        duration += datetime.utcnow()

        # Formatting the string
        reason_format = f"Moderator {ctx.author.id}: {reason}"

        # Normal ban if Member, hack ban if integer
        await self.add_ban(ctx, reason_format, target)

        # Adding to infraction table
        inf_id = await self.bot.infraction.add(inf_type=InfractionType.tempban, guild_id=ctx.guild.id, target_id=target.id,
                                               moderator_id=ctx.author.id, expires_at=duration, reason=reason)

        # Getting the infraction row object from the table
        infraction_object = await self.bot.infraction.get(ctx.guild.id, inf_id=inf_id)
        # Adding it to the tasks checker
        self.bot.active_infractions.append(infraction_object)

        banned_until = infraction_object['expires_at'].astimezone(timezone(self.bot.cache.timezones.get(ctx.guild.id))).strftime("%d-%m-%Y %H:%M:%S")

        # Inform the context author
        await ctx.send(f":ok_hand: **{target}** (`{target.id}`) temporary banned until `{banned_until}` for: `{reason}`.")

    @commands.command(aliases=('permaban',))
    @commands.bot_has_guild_permissions(ban_members=True)
    async def ban(self, ctx, target: Union[discord.Member, int] = None, *, reason=None):
        """BAN_HELP"""
        if target is None:
            return await ctx.send("You need to specify someone you want to ban")

        if reason is None:
            reason = Translator.translate('INF_NO_REASON', ctx.guild.id)

        reason_format = f"Moderator {ctx.author.id}: {reason}"

        # Normal ban if Member, hack ban if integer
        await self.add_ban(ctx, reason_format, target)

        # Add the infraction to the table
        await self.bot.infraction.add(inf_type=InfractionType.permaban, guild_id=ctx.guild.id, target_id=target.id, moderator_id=ctx.author.id,
                                      reason=reason)

        # Inform the context author
        await ctx.send(f":ok_hand: {target} (`{target.id}`) banned for: `{reason}`.")

    @commands.command()
    async def warn(self, ctx, target: discord.Member = None, *, reason=None):
        """WARN_HELP"""
        if target is None:
            return await ctx.send("You need to specify someone you want to warn")

        if reason is None:
            reason = Translator.translate('INF_NO_REASON', ctx.guild.id)

        await self.bot.infraction.add(inf_type='warn', guild_id=ctx.guild.id, target_id=target.id, moderator_id=ctx.author.id, reason=reason)
        await ctx.send(f":ok_hand: Warning for {target} (`{target.id}`) added, reason: `{reason}`")


def setup(bot):
    bot.add_cog(Moderation(bot))
