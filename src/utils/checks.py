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
