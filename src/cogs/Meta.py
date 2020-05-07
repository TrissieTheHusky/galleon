#  The MIT License (MIT)
#
#  Copyright (c) 2020 defracted
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

from datetime import datetime
from typing import Union

import discord
from discord.ext import commands
from pytz import timezone

from src.utils.apis import APIs
from src.utils.base import escape_hyperlinks
from src.utils.converters import NotCachedUser
from src.utils.custom_bot_class import DefraBot
from src.utils.generators import walk_emojis, walk_role_mentions
from src.utils.premade_embeds import DefraEmbed, error_embed
from src.utils.translator import Translator


class Meta(commands.Cog):
    def __init__(self, bot):
        self.bot: DefraBot = bot
        self.info_emojis = dict(
            staff="<:staff_badge:704986283008851975>", partner="<:partner_badge:704986283189075968>",
            hse="<:hypesquad_events_badge:704989654033629205>", bravery="<:bravery_badge:704986283231019079>",
            brilliance="<:brilliance_badge:704986283386208289>", balance="<:balance_badge:704986283243601970>",
            bh="<:bug_hunter_badge:704986283273093200>", bh_t2="<:bug_hunter_badge_t2:704989653903736925>",
            early="<:early_supporter_badge:704986283398660106>",
            verified_bot_dev="<:verified_developer_badge:704986283369562112>",
            verified_bot="<:verified_bot1:707676558332002455><:verified_bot2:707676277787590686>"
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

    @commands.command(aliases=('tr',))
    async def translate(self, ctx, translate_from, translate_to, *, text: str):
        """TRANSLATE_HELP"""
        await ctx.trigger_typing()

        data = await APIs.yandex_translate(text=text, tr_to=translate_to, tr_from=translate_from)
        if data['code'] != 200:
            await ctx.send(embed=error_embed(title=Translator.translate('YANDEX_TRANSLATE_FAILED', ctx), text=data['message']))
        elif data['code'] == 200:
            e = DefraEmbed()
            e.description = data['text'][0]
            e.set_footer(text=Translator.translate('YANDEX_TRANSLATE_NOTICE', ctx), icon_url="https://translate.yandex.ru/icons/favicon.png")

            await ctx.send(embed=e)

    @commands.command()
    async def invite(self, ctx):
        """INVITE_HELP"""
        embed = DefraEmbed(title=Translator.translate("INVITE_BOT", ctx))
        embed.description = Translator.translate("INVITE_BOT_URL", ctx, url=discord.utils.oauth_url(self.bot.user.id))
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def avatar(self, ctx, user: Union[discord.Member, NotCachedUser] = None):
        """AVATAR_HELP"""
        user = user or ctx.author

        avatar_url = user.avatar_url_as(static_format="png")

        embed = DefraEmbed(
            title=Translator.translate("AVATAR_TITLE", ctx, user=user),
            description=Translator.translate("AVATAR_DESCRIPTION", ctx, url=avatar_url)
        )
        embed.set_image(url=avatar_url)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def about(self, ctx):
        """ABOUT_TITLE"""
        e = DefraEmbed(
            title=Translator.translate("ABOUT_TITLE", ctx),
            footer_text=Translator.translate("ABOUT_FOOTER", ctx, user=ctx.author),
            footer_icon_url=ctx.author.avatar_url,
            description=Translator.translate('ABOUT_DESCRIPTION', ctx, owner=self.bot.owner, lib_version=f"discord.py {discord.__version__}")
        )
        e.set_thumbnail(url=self.bot.user.avatar_url_as(format="png"))
        await ctx.send(embed=e)

    @commands.command(aliases=("server", "guildinfo", "si", "gi"))
    @commands.guild_only()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def serverinfo(self, ctx, server_id: Union[discord.Guild, int] = None):
        """SERVERINFO_HELP"""
        if server_id is None:
            guild = ctx.guild
        else:
            guild = self.bot.get_guild(server_id)

        if guild is None:
            return await ctx.send(Translator.translate('SERVERINFO_NOT_FOUND', ctx, id=str(server_id)))

        guild_features = "\n".join(guild.features) if len(guild.features) > 0 else None
        guild_emojis = " ".join(walk_emojis(guild.emojis))

        embed = DefraEmbed(title=f"{guild.name}")
        embed.set_thumbnail(url=guild.icon_url)
        embed.add_field(name="**ID**", value=str(guild.id), inline=False)
        embed.add_field(name=Translator.translate("SERVERINFO_OWNER", ctx), value=str(guild.owner), inline=False)
        embed.add_field(name=Translator.translate("SERVERINFO_MEMBERS", ctx), value=str(guild.member_count), inline=False)

        if guild_features is not None:
            embed.add_field(name=Translator.translate("SERVERINFO_FEATURES", ctx), value=guild_features, inline=False)

        embed.add_field(name=Translator.translate("SERVERINFO_EMOJILIST", ctx), value=guild_emojis[0:1000], inline=False)

        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.command(aliases=("info", "ui"))
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.max_concurrency(5, commands.BucketType.default, wait=True)
    async def userinfo(self, ctx, user: Union[discord.Member, NotCachedUser] = None):
        """USERINFO_HELP"""
        if user is None:
            user = member = ctx.author

        else:
            member: discord.Member = None if ctx.guild is None else ctx.guild.get_member(user.id)

        e = discord.Embed(colour=0x3498db)
        e.set_thumbnail(url=f"{user.avatar_url_as(format='png') if not user.is_avatar_animated() else user.avatar_url_as(format='gif')}")
        e.add_field(name=Translator.translate("USERINFO_NAME", ctx),
                    value=f'{escape_hyperlinks(discord.utils.escape_markdown(str(user)))}',
                    inline=False)
        e.add_field(name='**ID**', value=str(user.id), inline=False)

        if len(user.public_flags.all) > 0:
            badges_field_val = ""

            if user.public_flags.verified_bot:
                badges_field_val += self.info_emojis['verified_bot'] + ' **Verified Bot**\n'

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
                e.add_field(name=Translator.translate('USERINFO_BADGES', ctx), value=badges_field_val)

        if not user.is_avatar_animated():
            avatar_url = user.avatar_url_as(format='png')
        else:
            avatar_url = user.avatar_url_as(format='gif')

        e.add_field(name=Translator.translate('USERINFO_AVATAR', ctx),
                    value=Translator.translate("CLICK_TO_OPEN", ctx, url=avatar_url), inline=False)

        if user == self.bot.owner:
            e.description = Translator.translate("OWNER_NOTICE", ctx)

        guild_timezone = self.bot.cache.timezones.get(ctx.guild.id) if ctx.guild is not None else "UTC"

        if member is not None:
            e.colour = member.top_role.color
            e.set_field_at(0, name=Translator.translate('USERINFO_NAME', ctx),
                           value=f'{self.user_status_icon(user.status)} {user}', inline=False)

            if member.bot is not True:
                if member.activity is not None:
                    for activity in member.activities:
                        if issubclass(type(activity), discord.activity.CustomActivity):
                            if activity.name is not None:
                                e.add_field(name=Translator.translate('USERINFO_ACTIVITY_CUSTOM', ctx),
                                            value=discord.utils.escape_markdown(escape_hyperlinks(member.activity.name)))

                        if int(activity.type) == 0:
                            e.add_field(name=Translator.translate('USERINFO_ACTIVITY_PLAYING', ctx),
                                        value=escape_hyperlinks(discord.utils.escape_markdown(activity.name)), inline=False)

                        if issubclass(type(activity), discord.activity.Spotify):
                            track_url = f"https://open.spotify.com/track/{activity.track_id}"
                            e.add_field(name=Translator.translate('USERINFO_ACTIVITY_LISTENING', ctx),
                                        value=f'[\N{MUSICAL NOTE} {", ".join(activity.artists)} \N{EM DASH} {activity.title}]({track_url})',
                                        inline=False)

            e.add_field(name=Translator.translate('USERINFO_ROLES', ctx),
                        value=", ".join(walk_role_mentions(reversed(member.roles), member.guild.id)),
                        inline=False)

            member_joined_days_ago = (datetime.utcnow() - member.joined_at).days
            e.add_field(name=f'**{Translator.translate("JOINED_AT", ctx)} ({guild_timezone.upper()})**',
                        value=Translator.translate("DAYS_AGO", ctx, days=member_joined_days_ago) +
                              f' (`{member.joined_at.astimezone(timezone(guild_timezone)).strftime("%d.%m.%Y %H:%M:%S")}`)', inline=False)

        user_created_days_ago = (datetime.utcnow() - user.created_at).days
        e.add_field(name=f'**{Translator.translate("ACCOUNT_CREATED_AT", ctx)} ({guild_timezone.upper()})**',
                    value=Translator.translate("DAYS_AGO", ctx, days=user_created_days_ago) +
                          f' (`{user.created_at.astimezone(timezone(guild_timezone)).strftime("%d.%m.%Y %H:%M:%S")}`)', inline=False)

        await ctx.send(embed=e)
        del e


def setup(bot):
    bot.add_cog(Meta(bot))
