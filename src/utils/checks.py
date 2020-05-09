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


class BlacklistedUser(commands.CheckFailure):
    pass


def is_server_manager_or_bot_owner():
    """
    Checks if context author is a bot owner or has manage_guild permission
    """

    def predicate(ctx):
        return ctx.author.id == ctx.bot.owner.id or ctx.channel.permissions_for(ctx.author).manage_guild

    return commands.check(predicate)
