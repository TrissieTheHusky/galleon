from discord.ext import commands
from datetime import datetime
from pytz import timezone

from src.utils.configuration import cfg
from src.utils.converters import DiscordUser
from src.utils.base import DefraEmbed
from src.typings import BotType
from src.utils.database import Database
from src.utils.cache import Cache

import discord
import sys


class Other(commands.Cog):
    def __init__(self, bot):
        self.bot: BotType = bot

    @commands.command(name="whatprefix", aliases=["prefix", "currentprefix"])
    async def what_prefix(self, ctx):
        if ctx.guild is None:
            return await ctx.send(f"Current prefix is `{cfg['DEFAULT_PREFIX']}`")

        prefix = self.bot.prefixes.get(ctx.guild.id, cfg['DEFAULT_PREFIX'])
        await ctx.send(f"Current prefix is `{prefix if prefix is not None else cfg['DEFAULT_PREFIX']}`")

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
        e.add_field(name='Avatar',
                    value=f"[Go to URL]({user.avatar_url_as(format='png') if not user.is_avatar_animated() else user.avatar_url_as(format='gif')})",
                    inline=False)

        e.description = '\N{HEAVY BLACK HEART} This is my creator!' if user == self.bot.owner else None

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
