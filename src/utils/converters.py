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

from discord import HTTPException, NotFound
from discord.ext.commands import BadArgument, Converter


class SmartUser(Converter):
    async def convert(self, ctx, argument):
        try:
            int(argument)
        except ValueError:
            raise BadArgument('{0} is invalid User ID'.format(argument)) from None

        if user := ctx.bot.get_user(argument) is not None:
            return user
        else:
            try:
                return await ctx.bot.fetch_user(argument)
            except NotFound:
                raise BadArgument('{0} not found'.format(argument)) from None
            except HTTPException:
                raise BadArgument('Fetching USER {0} failed'.format(argument)) from None
