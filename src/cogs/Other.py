from discord.ext import commands
from datetime import datetime
from pytz import timezone

from src.utils.converters import DiscordUser
from src.utils.base import DefraEmbed
from src.utils.custom_bot_class import DefraBot
from src.utils.database import Database
from src.utils.cache import Cache

import discord
import sys


class Other(commands.Cog):
    def __init__(self, bot):
        self.bot: DefraBot = bot
        self.info_emojis = dict(
            staff="<:staff_badge:704986283008851975>",
            partner="<:partner_badge:704986283189075968>",
            hse="<:hypesquad_events_badge:704989654033629205>",
            bravery="<:bravery_badge:704986283231019079>",
            brilliance="<:brilliance_badge:704986283386208289>",
            balance="<:balance_badge:704986283243601970>",
            bh="<:bug_hunter_badge:704986283273093200>",
            bh_t2="<:bug_hunter_badge_t2:704989653903736925>",
            early="<:early_supporter_badge:704986283398660106>",
            verified_bot_dev="<:verified_developer_badge:704986283369562112>"
        )

    @commands.command(name="whatprefix", aliases=["prefix", "currentprefix"])
    async def what_prefix(self, ctx):
        if ctx.guild is None:
            return await ctx.send(f"Current prefix is `{self.bot.cfg['DEFAULT_PREFIX']}`")

        prefix = self.bot.prefixes.get(ctx.guild.id, self.bot.cfg['DEFAULT_PREFIX'])
        await ctx.send(f"Current prefix is `{prefix if prefix is not None else self.bot.cfg['DEFAULT_PREFIX']}`")

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def about(self, ctx: commands.Context):
        e = DefraEmbed(
            title="Bot Info",
            footer_text=f"Requested by {ctx.author}",
            footer_icon_url=ctx.author.avatar_url,
            description=f"**Bot Author:** {self.bot.owner} ({self.bot.owner.mention})\n"
                        f"**discord.py version:** {discord.__version__}\n"
                        f"**Python version:** {'.'.join(map(str, sys.version_info[:3]))}\n\n"
                        "**Source Code:** [Click to open](https://github.com/defracted/def-bot)"
        )
        await ctx.send(embed=e)

    @commands.guild_only()
    @commands.command(aliases=["info"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.max_concurrency(10, commands.BucketType.default, wait=True)
    async def userinfo(self, ctx: commands.Context, user: DiscordUser = None):
        """Shows information summary about discord users"""
        if user is None:
            user = member = ctx.author

        else:
            member: discord.Member = None if ctx.guild is None else ctx.guild.get_member(user.id)

        e = discord.Embed(colour=0x3498db)
        e.set_thumbnail(
            url=f"{user.avatar_url_as(format='png') if not user.is_avatar_animated() else user.avatar_url_as(format='gif')}")
        e.add_field(name='Name', value=f'{user}', inline=False)
        e.add_field(name='ID', value=str(user.id), inline=False)

        if user.public_flags > 0:
            badges_field_val = f"{(self.info_emojis['staff'] + ' ') if user.is_discord_employee else ''}" \
                               f"{(self.info_emojis['partner'] + ' ') if user.is_discord_partner else ''}" \
                               f"{(self.info_emojis['hse'] + ' ') if user.is_hypesquad_events_member else ''}" \
                               f"{(self.info_emojis['bravery'] + ' ') if user.is_house_bravery else ''}" \
                               f"{(self.info_emojis['brilliance'] + ' ') if user.is_house_brilliance else ''}" \
                               f"{(self.info_emojis['balance'] + ' ') if user.is_house_balance else ''}" \
                               f"{(self.info_emojis['bh'] + ' ') if user.is_bug_hunter else ''}" \
                               f"{(self.info_emojis['bh_t2'] + ' ') if user.is_golden_bug_hunter else ''}" \
                               f"{(self.info_emojis['verified_bot_dev'] + ' ') if user.is_verified_bot_developer else ''}" \
                               f"{(self.info_emojis['early'] + ' ') if user.is_early_supporter else ''}"

            e.add_field(name="Badges", value=badges_field_val)

        e.add_field(name='Avatar',
                    value=f"[Go to URL]({user.avatar_url_as(format='png') if not user.is_avatar_animated() else user.avatar_url_as(format='gif')})",
                    inline=False)

        if user == self.bot.owner:
            e.description = '\n\N{HEAVY BLACK HEART} This is my creator!'

        karma_points, _ = await Database.get_karma(user.id)
        e.add_field(name="Karma Points", value=f"{karma_points if karma_points is not None else 0}")

        guild_timezone = await Cache.get_timezone(ctx.guild.id) if ctx.guild is not None else "UTC"

        if member is not None:
            e.colour = member.top_role.colour
            member_status = str(member.status)

            if member_status == 'online':
                member_status = 'Online'

            elif member_status == 'dnd':
                member_status = 'Do Not Disturb'

            elif member_status == 'idle':
                member_status = 'Inactive'

            elif member_status == 'offline':
                member_status = 'Offline'

            e.add_field(name='Status', value=member_status, inline=False)

            if member.bot is not True:
                if member.activity is not None:
                    if member.activity.type == discord.ActivityType.playing:
                        e.add_field(name='\N{VIDEO GAME} Playing', value=f'{member.activity.name}', inline=False)

                    elif member.activity.type == discord.ActivityType.streaming:
                        e.add_field(name='Streaming', value=f'{member.activity.name}', inline=False)

                    elif member.activity.type == discord.ActivityType.watching:
                        e.add_field(name='\N{EYES} Watching', value=f'{member.activity.name}', inline=False)

                    elif member.activity.type == discord.ActivityType.listening:
                        track_url = f"https://open.spotify.com/track/{member.activity.track_id}"
                        e.add_field(name='Listening',
                                    value=f'[\N{MUSICAL NOTE} {", ".join(member.activity.artists)} \N{EM DASH} {member.activity.title}]({track_url})',
                                    inline=False)

                    elif member.activity.type == discord.ActivityType.custom:
                        e.add_field(name="Status", value=f"{member.activity.name}", inline=False)

                    else:
                        e.add_field(name='Unknown activity', value='\U00002753 Unknown', inline=False)

            e.add_field(name=f'Joined at ({guild_timezone})',
                        value=f'{(datetime.utcnow() - member.joined_at).days} days ago (`{member.joined_at.astimezone(timezone(guild_timezone)).strftime("%d.%m.%Y %H:%M:%S")}`)',
                        inline=False)

        e.add_field(name=f'Account created at ({guild_timezone})',
                    value=f'{(datetime.utcnow() - user.created_at).days} days ago (`{user.created_at.astimezone(timezone(guild_timezone)).strftime("%d.%m.%Y %H:%M:%S")}`)',
                    inline=False)

        await ctx.send(embed=e)
        del e


def setup(bot):
    bot.add_cog(Other(bot))
