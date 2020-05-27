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

from discord.ext import commands

from src.utils.base import is_timezone
from src.utils.checks import is_server_manager_or_bot_owner
from src.utils.custom_bot_class import DefraBot
from src.utils.enums import TableRolesTypes
from src.utils.premade_embeds import DefraEmbed, error_embed
from src.utils.translator import Translator


class ServerAdmin(commands.Cog):
    def __init__(self, bot):
        self.bot: DefraBot = bot

    @commands.command(name="whatprefix", aliases=("prefix", "currentprefix"))
    async def what_prefix(self, ctx):
        """WHATPREFIX_HELP"""
        if ctx.guild is None:
            return await ctx.send(Translator.translate('WHATPREFIX', ctx, prefix=self.bot.cfg['DEFAULT_PREFIX']))

        prefix = self.bot.cache.guilds.get(ctx.guild.id).prefix or self.bot.cfg['DEFAULT_PREFIX']
        await ctx.send(Translator.translate('WHATPREFIX', ctx, prefix=prefix))

    @commands.guild_only()
    @is_server_manager_or_bot_owner()
    @commands.group(aliases=("cfg",))
    async def config(self, ctx: commands.Context):
        """CONFIG_HELP"""
        if ctx.invoked_subcommand is None:
            await ctx.send(Translator.translate("NO_SUBCOMMAND", ctx, help=f"{ctx.prefix}help {ctx.command} {ctx.command.signature}"))

    @config.command()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def prefix(self, ctx: commands.Context, new_prefix=None):
        """CONFIG_PREFIX_HELP"""
        if new_prefix is None:
            return await ctx.send(Translator.translate("CONFIG_PREFIX_NO_NEW"))

        await self.bot.db.prefixes.set(ctx.guild.id, new_prefix)
        await self.bot.cache.refresh(ctx.guild.id)

        if self.bot.cache.guilds.get(ctx.guild.id).prefix == new_prefix:
            await ctx.send(Translator.translate("CONFIG_PREFIX_UPDATED", ctx, prefix=new_prefix))
        else:
            await ctx.send(Translator.translate("CONFIG_UPDATE_ERROR", ctx))

    @config.command()
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def timezone(self, ctx, new_timezone=None):
        """CONFIG_TIMEZONE_HELP"""
        if new_timezone is None:
            current_tz = self.bot.cache.guilds.get(ctx.guild.id).timezone
            return await ctx.send(Translator.translate("CONFIG_TIMEZONE_CURRENT", ctx, current=current_tz))

        if is_timezone(new_timezone) is False:
            return await ctx.send(Translator.translate("CONFIG_TIMEZONE_BAD_TIMEZONE", ctx))

        await self.bot.db.timezones.set(ctx.guild.id, new_timezone)
        await self.bot.cache.refresh(ctx.guild.id)

        if self.bot.cache.guilds.get(ctx.guild.id).timezone == new_timezone:
            await ctx.send(Translator.translate("CONFIG_TIMEZONE_UPDATED", ctx, timezone=new_timezone))
        else:
            await ctx.send(Translator.translate("CONFIG_UPDATE_ERROR", ctx))

    @config.command(aliases=("lang",))
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def language(self, ctx, new_language=None):
        """CONFIG_LANGUAGE_HELP"""
        if new_language is None:
            settings = self.bot.cache.guilds.get(ctx.guild.id, None)
            current_language = (settings.language if settings is not None else 'en_US') or 'en_US'

            return await ctx.send(Translator.translate("CONFIG_LANGUAGE_CURRENT", ctx, language=current_language))

        if new_language not in Translator.translations.keys():
            return await ctx.send(
                Translator.translate("CONFIG_LANGUAGE_BAD_LANGUAGE", ctx, languages=", ".join(list(Translator.translations.keys()))))

        await self.bot.db.languages.set(ctx.guild.id, new_language)
        await self.bot.cache.refresh(ctx.guild.id)

        await ctx.send(Translator.translate("CONFIG_LANGUAGE_UPDATED", ctx, language=new_language))

    @config.group()
    @commands.cooldown(1, 1, commands.BucketType.guild)
    async def mod_roles(self, ctx):
        """MOD_ROLES_HELP"""
        if ctx.invoked_subcommand is None:
            e = DefraEmbed(
                title=Translator.translate('CONFIG_MOD_ROLES_CURRENT', ctx.guild.id),
                description='\n'.join([f'{role.mention} (`{role.id}`)'
                                       if (role := ctx.guild.get_role(role_id)) is not None
                                       else f"`{role_id}`" for role_id in self.bot.cache.guilds.get(ctx.guild.id).mod_roles])
            )

            await ctx.send(embed=e)

    @mod_roles.command(name="add")
    @commands.cooldown(1, 1, commands.BucketType.guild)
    async def mod_roles_add(self, ctx, roles: commands.Greedy[int] = None):
        """MOD_ROLES_ADD_HELP"""
        if roles is None:
            return await ctx.send(embed=error_embed(text=None, title=Translator.translate('CONFIG_MOD_ROLES_EMPTY_ARGUMENT', ctx.guild.id)))

        # Filtering out non-existing roles and deleting duplicates
        roles = [ctx.guild.get_role(role) for role in set(filter(lambda _id: True if ctx.guild.get_role(_id) is not None else False, roles))]

        if len(roles) <= 0:
            return await ctx.send(embed=error_embed(text=None, title=Translator.translate('CONFIG_MOD_ROLES_NONE_ADDED', ctx.guild.id)))

        # Adding each role id into the database
        for role in roles:
            if role.id not in self.bot.cache.guilds.get(ctx.guild.id).mod_roles:
                await self.bot.db.roles.add(TableRolesTypes.mod_roles, ctx.guild.id, role.id)
            else:
                return await ctx.send(embed=error_embed(title=Translator.translate('NOTHING_CHANGED', ctx.guild.id), text=None))

        await self.bot.cache.refresh(ctx.guild.id)
        await ctx.send(embed=DefraEmbed(
            title=Translator.translate('CONFIG_MOD_ROLES_ADDED', ctx.guild.id),
            description='\n'.join([f"{role.mention} (`{role.id}`)" for role in roles])
        ))

    @mod_roles.command(name="remove", aliases=("delete", "del", "rmv"))
    @commands.cooldown(1, 1, commands.BucketType.guild)
    async def mod_roles_remove(self, ctx, roles: commands.Greedy[int] = None):
        """MOD_ROLES_REMOVE_HELP"""
        if roles is None:
            return await ctx.send(embed=error_embed(text=None, title=Translator.translate('CONFIG_MOD_ROLES_EMPTY_ARGUMENT', ctx.guild.id)))

        # Iterate through provided list of roles
        for role_id in roles:
            # Check if role_id is already a mod role
            if role_id not in self.bot.cache.guilds.get(ctx.guild.id).mod_roles:
                return await ctx.send(embed=error_embed(text=None,
                                                        title=Translator.translate('CONFIG_MOD_ROLES_REMOVE_BAD_ROLE', ctx, role_id=role_id)))

            # Delete the role
            await self.bot.db.roles.remove(TableRolesTypes.mod_roles, ctx.guild.id, role_id)

        await self.bot.cache.refresh(ctx.guild.id)
        await ctx.send(embed=DefraEmbed(
            title=Translator.translate('CONFIG_MOD_ROLES_REMOVED', ctx.guild.id),
            description='\n'.join(
                [str(ctx.guild.get_role(role_id).mention if ctx.guild.get_role(role_id) is not None else role_id) for role_id in roles])))


def setup(bot):
    bot.add_cog(ServerAdmin(bot))
