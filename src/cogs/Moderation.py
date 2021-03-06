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
from src.utils.translator import Translator
from src.utils.types import InfractionStruct


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

    @tasks.loop(seconds=1.0)
    async def infractions_checker(self):
        # If there's no active infractions, do nothing
        if len(self.bot.active_infractions) <= 0:
            return

        for infraction in self.bot.active_infractions:
            # If the infraction still active (expiration date is not in the past or not this moment) - do nothing
            if infraction['expires_at'].timestamp() < datetime.now().timestamp():
                # Do nothing if guild is None, perform actions if otherwise
                if (guild := self.bot.get_guild(infraction['guild_id'])) is not None:
                    if infraction['inf_type'] == InfractionType.tempban.value:
                        try:
                            member = discord.Object(id=infraction['target_id'])
                            await guild.unban(member, reason=Translator.translate('TEMP_BAN_EXPIRED', guild.id, inf_id=infraction['inf_id']))
                            await self.bot.infraction.deactivate(infraction['inf_id'])
                            self.bot.active_infractions.remove(infraction)
                            # Inform that someone got unbanned, use bot.dispatch and handle in mod logging cog
                        except discord.Forbidden:
                            pass  # TODO: Must inform the server owner through logging that bot lacks required permissions to un-ban
                        except discord.HTTPException:
                            pass  # Well, there's nothing we can do about it :P
            else:
                # print(f'{infraction["inf_id"]} still not expired')
                pass

    @commands.Cog.listener()
    async def on_check_actions(self):
        await self.bot.wait_until_ready()
        active_actions = await self.bot.db.temp_actions.get()

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
            return await ctx.send(Translator.translate('ARCHIVE_UP_TO', ctx, number=str(2000)))

        messages = await channel.history(limit=amount).flatten()
        await Messages.send_archive(self.bot, ctx, messages, channel)

    @archive.command(name="user")
    async def archive_user(self, ctx, amount: int = 100, user: discord.Member = None, channel: discord.TextChannel = None):
        """ARCHIVE_USER_HELP"""
        if user is None:
            return await ctx.send(Translator.translate('MEMBER_ARG_REQUIRED', ctx))

        channel = channel or ctx.channel

        if amount > 3000:
            return await ctx.send(Translator.translate('ARCHIVE_UP_TO', ctx, number=str(3000)))

        messages = []
        async for message in channel.history(limit=amount):
            if message.author == user:
                messages.append(message)

        await Messages.send_archive(self.bot, ctx, messages, channel)

    @commands.group(aliases=('i', 'inf', 'infraction'))
    async def infractions(self, ctx):
        """INFRACTIONS_HELP"""
        if ctx.invoked_subcommand is None:
            return await ctx.send(Translator.translate('NO_SUBCOMMAND', ctx, help=f"{ctx.prefix} help {ctx.command.qualified_name}"))

    @infractions.command()
    async def search(self, ctx, *, query: Union[discord.Member, str] = None):
        """INFRACTIONS_SEARCH_HELP"""
        infractions = []
        if query is None:
            infractions = await self.bot.infraction.get(guild_id=ctx.guild.id)
        elif query is not None:
            if isinstance(query, str):
                if query.lower().startswith("[mod]"):
                    infractions = await self.bot.infraction.get(guild_id=ctx.guild.id, moderator_id=int(re.findall(r'\d+', query)[0]))
                elif query.lower().startswith("[user]"):
                    infractions = await self.bot.infraction.get(guild_id=ctx.guild.id, target_id=int(re.findall(r'\d+', query)[0]))
                else:
                    infractions = await self.bot.infraction.get(guild_id=ctx.guild.id, target_id=int(query))
            elif isinstance(query, discord.Member):
                infractions = await self.bot.infraction.get(guild_id=ctx.guild.id, target_id=query.id)

        entries = []
        for inf in infractions:
            inf_type_format = Translator.translate(inf["inf_type"].upper(), ctx.guild.id)
            reason_format = discord.utils.escape_markdown(discord.utils.escape_mentions(inf["reason"]))

            settings = self.bot.cache.guilds.get(ctx.guild.id, None)
            guild_timezone = settings.timezone if settings is not None else 'UTC'
            date_format = inf['added_at'].astimezone(timezone(guild_timezone)).strftime("%d-%m-%Y %H:%M:%S")

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
    async def kick(self, ctx, target: Union[discord.Member, int] = None, *, reason=None):
        """KICK_HELP"""
        if target is None:
            return await ctx.send(Translator.translate('MEMBER_ARG_REQUIRED', ctx))

        member = target

        if reason is None:
            reason = Translator.translate('INF_NO_REASON', ctx.guild.id)

        reason_format = f"Moderator {ctx.author.id}: {reason}"

        # Normal kick if Member, hack kick if integer
        if isinstance(target, discord.Member):
            await target.kick(reason=reason_format)
        elif isinstance(target, int):
            member = ctx.guild.get_member(target)
            if member is None:
                return await ctx.send(Translator.translate('MEMBER_NOT_FOUND', ctx, id=str(target)))

            await member.kick(reason=reason_format)

        # Add the infraction to the table
        inf_id = await self.bot.infraction.add(inf_type=InfractionType.kick.value, guild_id=ctx.guild.id, target_id=member.id,
                                               moderator_id=ctx.author.id, reason=reason)

        # Inform the context author
        await ctx.send(Translator.translate('KICKED_MESSAGE', ctx, target=str(member), target_id=str(member.id), reason=reason))
        # Prepare mod log
        infraction = InfractionStruct(inf_id, InfractionType.kick, ctx.guild, member, ctx.author, reason, datetime.now(), None)
        self.bot.dispatch('mod_logging_inf_add', infraction=infraction)

    @commands.command()
    @commands.bot_has_guild_permissions(ban_members=True)
    async def tempban(self, ctx, target: Union[discord.Member, int], duration: Duration, *, reason=None):
        """TEMPBAN_HELP"""
        if target is None:
            return await ctx.send(Translator.translate('MEMBER_ARG_REQUIRED', ctx))

        msg = await ctx.send(Translator.translate('PROCESSING', ctx))

        if reason is None:
            reason = Translator.translate('INF_NO_REASON', ctx.guild.id)

        # Adding time to the current moment to create expiration datetime object
        duration = datetime.now() + duration

        # Formatting the string
        reason_format = f"Moderator {ctx.author.id}: {reason}"

        # Normal ban if Member, hack ban if integer
        if isinstance(target, discord.Member):
            await ctx.guild.ban(user=target, reason=reason_format)
        elif isinstance(target, int):
            target = await self.bot.fetch_user(target)
            await ctx.guild.ban(discord.Object(id=target.id), reason=reason_format)

        # Adding to infraction table
        inf_id = await self.bot.infraction.add(inf_type=InfractionType.tempban.value, guild_id=ctx.guild.id, target_id=target.id,
                                               moderator_id=ctx.author.id, expires_at=duration, reason=reason)

        # Getting the infraction row object from the table
        infraction_object = await self.bot.infraction.get(ctx.guild.id, inf_id=inf_id)
        # Adding it to the tasks checker
        self.bot.active_infractions.append(infraction_object)

        # Formatting info message
        if (settings := self.bot.cache.guilds.get(ctx.guild.id, None)) is None:
            guild_timezone = 'UTC'
        else:
            guild_timezone = settings.timezone

        banned_until = infraction_object['expires_at'].astimezone(timezone(guild_timezone)).strftime("%d-%m-%Y %H:%M:%S")

        # Inform the context author
        await msg.edit(content=Translator.translate('TEMP_BANNED_MESSAGE', ctx, target=str(target), target_id=str(target.id), until=banned_until,
                                                    reason=reason))
        # Prepare mod log
        infraction = InfractionStruct(inf_id, InfractionType.tempban, ctx.guild, target, ctx.author, reason, infraction_object['added_at'], duration)
        self.bot.dispatch('mod_logging_inf_add', infraction=infraction)

    @commands.command(aliases=('permaban',))
    @commands.bot_has_guild_permissions(ban_members=True)
    async def ban(self, ctx, target: Union[discord.Member, int] = None, *, reason=None):
        """BAN_HELP"""
        if target is None:
            return await ctx.send(Translator.translate('MEMBER_ARG_REQUIRED', ctx))

        msg = await ctx.send(Translator.translate('PROCESSING', ctx))

        if reason is None:
            reason = Translator.translate('INF_NO_REASON', ctx.guild.id)

        reason_format = f"Moderator {ctx.author.id}: {reason}"

        # Normal ban if Member, hack ban if integer
        if isinstance(target, discord.Member):
            await ctx.guild.ban(user=target, reason=reason_format)
        elif isinstance(target, int):
            target = await self.bot.fetch_user(target)
            await ctx.guild.ban(discord.Object(id=target.id), reason=reason_format)

        # Add the infraction to the table
        inf_id = await self.bot.infraction.add(inf_type=InfractionType.permaban.value, guild_id=ctx.guild.id, target_id=target.id,
                                               moderator_id=ctx.author.id, reason=reason)

        # Inform the context author
        await msg.edit(content=Translator.translate('BANNED_MESSAGE', ctx, target=str(target), target_id=str(target.id), reason=reason))
        # Prepare mod log
        infraction = InfractionStruct(inf_id, InfractionType.permaban, ctx.guild, target, ctx.author, reason, datetime.now(), None)
        self.bot.dispatch('mod_logging_inf_add', infraction=infraction)

    @commands.command()
    async def warn(self, ctx, target: discord.Member = None, *, reason=None):
        """WARN_HELP"""
        if target is None:
            return await ctx.send("You need to specify someone you want to warn")

        if reason is None:
            reason = Translator.translate('INF_NO_REASON', ctx.guild.id)

        inf_id = await self.bot.infraction.add(inf_type=InfractionType.warn.value, guild_id=ctx.guild.id, target_id=target.id,
                                               moderator_id=ctx.author.id, reason=reason)

        await ctx.send(Translator.translate('WARNING_MESSAGE', ctx, target=str(target), target_id=str(target.id), reason=reason))
        # Prepare mod log
        infraction = InfractionStruct(inf_id, InfractionType.warn, ctx.guild, target, ctx.author, reason, datetime.now(), None)
        self.bot.dispatch('mod_logging_inf_add', infraction=infraction)


def setup(bot):
    bot.add_cog(Moderation(bot))
