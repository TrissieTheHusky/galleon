from discord import HTTPException, NotFound
from discord.ext.commands import BadArgument, Converter


class NotCachedUser(Converter):
    async def convert(self, ctx, argument):
        try:
            int(argument)
        except ValueError:
            raise BadArgument('{0} is invalid User ID'.format(argument)) from None

        try:
            return await ctx.bot.fetch_user(argument)
        except NotFound:
            raise BadArgument('{0} not found'.format(argument)) from None
        except HTTPException:
            raise BadArgument('Fetching USER {0} failed'.format(argument)) from None
