import sys
from datetime import datetime
from typing import Union

import discord
from discord.ext import commands
from pytz import timezone

from src.utils.base import DefraEmbed
from src.utils.cache import Cache
from src.utils.converters import NotCachedUser
from src.utils.custom_bot_class import DefraBot


class Meta(commands.Cog):
    def __init__(self, bot):
        self.bot: DefraBot = bot
        self.info_emojis = dict(
            staff="<:staff_badge:704986283008851975>", partner="<:partner_badge:704986283189075968>",
            hse="<:hypesquad_events_badge:704989654033629205>", bravery="<:bravery_badge:704986283231019079>",
            brilliance="<:brilliance_badge:704986283386208289>", balance="<:balance_badge:704986283243601970>",
            bh="<:bug_hunter_badge:704986283273093200>", bh_t2="<:bug_hunter_badge_t2:704989653903736925>",
            early="<:early_supporter_badge:704986283398660106>",
            verified_bot_dev="<:verified_developer_badge:704986283369562112>"
        )

    def user_status_icon(self, status: discord.Status):
        if status == discord.Status.online:
            return "<:online:705378474503831552>"
        elif status == discord.Status.idle:
            return "<:inactive:705378474470408193>"
        elif status == discord.Status.dnd:
            return "<:dnd:705378474608558112>"
        elif status == discord.Status.offline:
            return "<:offline:705378474373677107>"

    @commands.command()
    async def invite(self, ctx):
        """Send an invitation URL of the bot"""
        embed = DefraEmbed(title="Invite the bot")
        embed.description = f"[Click to invite]({discord.utils.oauth_url(self.bot.user.id)})"
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def avatar(self, ctx, user: Union[discord.Member, NotCachedUser] = None):
        """Shows user's avatar"""
        user = user or ctx.author

        avatar_url = user.avatar_url_as(static_format="png")

        embed = DefraEmbed(title=f"{user} avatar", description=f"[See full size]({avatar_url})")
        embed.set_image(url=avatar_url)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def about(self, ctx):
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
    async def userinfo(self, ctx, user: Union[discord.Member, NotCachedUser] = None):
        """Shows information summary about discord users"""
        if user is None:
            user = member = ctx.author

        else:
            member: discord.Member = None if ctx.guild is None else ctx.guild.get_member(user.id)

        e = discord.Embed(colour=0x3498db)
        e.set_thumbnail(
            url=f"{user.avatar_url_as(format='png') if not user.is_avatar_animated() else user.avatar_url_as(format='gif')}")
        e.add_field(name='**Name**', value=f'{user}', inline=False)
        e.add_field(name='**ID**', value=str(user.id), inline=False)

        if len(user.public_flags.all) > 0:
            badges_field_val = ""

            if user.public_flags.staff:
                badges_field_val += self.info_emojis['staff'] + ' **Discord Staff**\n'

            if user.public_flags.partner:
                badges_field_val += self.info_emojis['partner'] + ' **Discord Partner**\n'

            if user.public_flags.hypesquad:
                badges_field_val += self.info_emojis['hse'] + ' **HypeSquad Events**\n'

            if user.public_flags.hypesquad_bravery:
                badges_field_val += self.info_emojis['bravery'] + ' **HypeSquad Bravery**\n'

            if user.public_flags.hypesquad_brilliance:
                badges_field_val += self.info_emojis['brilliance'] + ' **HypeSquad Brilliance**\n'

            if user.public_flags.hypesquad_balance:
                badges_field_val += self.info_emojis['balance'] + ' **HypeSquad Balance**\n'

            if user.public_flags.verified_bot_developer:
                badges_field_val += self.info_emojis['verified_bot_dev'] + ' **Verified Bot Developer**\n'

            if user.public_flags.bug_hunter:
                badges_field_val += self.info_emojis['bh'] + ' **Discord Bug Hunter**\n'

            if user.public_flags.bug_hunter_level_2:
                badges_field_val += self.info_emojis['bh_t2'] + ' **Discord Bug Hunter**\n'

            if user.public_flags.early_supporter:
                badges_field_val += self.info_emojis['early'] + ' **Early Supporter**\n'

            if len(badges_field_val) > 0:
                e.add_field(name="**Badges**", value=badges_field_val)

        e.add_field(name='**Avatar**',
                    value=f"[Go to URL]({user.avatar_url_as(format='png') if not user.is_avatar_animated() else user.avatar_url_as(format='gif')})",
                    inline=False)

        if user == self.bot.owner:
            e.description = '\n\N{HEAVY BLACK HEART} This is my creator!'

        guild_timezone = await Cache.get_timezone(ctx.guild.id) if ctx.guild is not None else "UTC"

        if member is not None:
            e.colour = member.top_role.colour
            e.set_field_at(0, name='**Name**', value=f'{self.user_status_icon(user.status)} {user}', inline=False)

            if member.bot is not True:
                if member.activity is not None:
                    for activity in member.activities:
                        if int(activity.type) == 0:
                            e.add_field(name="**Playing**", value=f'{activity.name}', inline=False)

                        if issubclass(type(activity), discord.activity.Spotify):
                            track_url = f"https://open.spotify.com/track/{member.activity.track_id}"
                            e.add_field(name="**Listening**",
                                        value=f'[\N{MUSICAL NOTE} {", ".join(member.activity.artists)} \N{EM DASH} {member.activity.title}]({track_url})',
                                        inline=False)

            e.add_field(name=f'**Joined at ({guild_timezone})**',
                        value=f'{(datetime.utcnow() - member.joined_at).days} days ago (`{member.joined_at.astimezone(timezone(guild_timezone)).strftime("%d.%m.%Y %H:%M:%S")}`)',
                        inline=False)

        e.add_field(name=f'**Account created at ({guild_timezone})**',
                    value=f'{(datetime.utcnow() - user.created_at).days} days ago (`{user.created_at.astimezone(timezone(guild_timezone)).strftime("%d.%m.%Y %H:%M:%S")}`)',
                    inline=False)

        await ctx.send(embed=e)
        del e


def setup(bot):
    bot.add_cog(Meta(bot))
