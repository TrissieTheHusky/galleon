from discord.ext import commands


def is_server_manager_or_bot_owner():
    """
    Checks if context author is a bot owner or has manage_guild permission
    """

    def predicate(ctx: commands.Context):
        return (ctx.author.id == ctx.bot.owner.id) or ((ctx.author.guild_permissions.value & 0x20) == 0x20)

    return commands.check(predicate)
