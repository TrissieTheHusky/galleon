from discord.ext import commands
from src.utils.custom_bot_class import DefraBot
from src.utils.premade_embeds import warn_embed


class ToDo(commands.Cog):
    def __init__(self, bot):
        self.bot: DefraBot = bot

    async def cog_check(self, ctx):
        return await ctx.bot.is_owner(ctx.author)

    @commands.group()
    async def todo(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(embed=warn_embed(title=":warning: You didn't specify any subcommand!",
                                            text=f"See `{ctx.prefix}help {ctx.command.qualified_name}`"))

    @todo.command()
    async def add(self, ctx, *, task: str = None):
        if task is None:
            return await ctx.send(embed=warn_embed(title=":warning: You didn't specify what you want to do!", text=""))

        await ctx.send("haha")


def setup(bot):
    bot.add_cog(ToDo(bot))
