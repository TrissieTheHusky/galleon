from discord.ext import commands


def is_server_manager_or_bot_owner():
    """
    Checks if context author is a bot owner or has manage_guild permission
    """

    def predicate(ctx: commands.Context):
        return (ctx.message.author.id == ctx.bot.owner.id) or \
               ((ctx.guild.get_member(ctx.message.author.id).guild_permissions.value & 0x20) == 0x20)

    return commands.check(predicate)
