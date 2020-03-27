from discord.ext import commands
from discord import Embed
from src.utils.configuration import cfg
from src.utils.converters import DiscordUser
import discord
from datetime import datetime


class Other(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="whatprefix", aliases=("prefix", "currentprefix"))
    async def what_prefix(self, ctx):
        await ctx.send(f"Current prefix is: `{self.bot.prefixes.get(str(ctx.guild.id), cfg['DEFAULT_PREFIX'])}`")

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def about(self, ctx: commands.Context):
        e = Embed(color=0x3498db)
        e.set_author(name=f"{self.bot.user}", icon_url=self.bot.user.avatar_url)
        e.add_field(name="Author", value=f"{self.bot.owner}")
        e.add_field(name="Source Code", value="[Click to open](https://github.com/runic-tears/def-bot)")
        await ctx.send(embed=e)

    @commands.command(aliases=("info",))
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def userinfo(self, ctx: commands.Context, user: DiscordUser = None):
        """Get user information"""
        if user is None:
            user = member = ctx.author
            user = await self.bot.fetch_user(user.id)

        else:
            member: discord.Member = None if ctx.guild is None else ctx.guild.get_member(user.id)

        e = discord.Embed(colour=0x3498db)
        e.set_thumbnail(url=user.avatar_url)
        e.add_field(name='Name', value=f'{user}', inline=False)
        e.add_field(name='ID', value=str(user.id), inline=False)
        e.add_field(name='Avatar', value=f'[Go to URL]({user.avatar_url})', inline=False)

        e.description = '\N{HEAVY BLACK HEART} This human is very-very dumb person, this is my creator!' if user == self.bot.owner else None

        if member is not None:
            e.colour = member.top_role.colour
            member_status = str(member.status)

            if member_status == 'online':
                member_status = 'Online'

            elif member_status == 'dnd':
                member_status = 'Do not disturb'

            elif member_status == 'idle':
                member_status = 'Idle'

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

            e.add_field(name='Joined at (UTC)',
                        value=f'{(datetime.utcnow() - member.joined_at).days} days ago (`{member.joined_at.strftime("%Y-%m-%d %H:%M:%S.%f")}`)',
                        inline=False)

        e.add_field(name='Account created at (UTC)',
                    value=f'{(datetime.utcnow() - user.created_at).days} days ago (`{user.created_at.strftime("%Y-%m-%d %H:%M:%S.%f")}`)',
                    inline=False)

        await ctx.send(embed=e)
        del e


def setup(bot):
    bot.add_cog(Other(bot))
