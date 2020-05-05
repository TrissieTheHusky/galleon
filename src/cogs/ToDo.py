from discord.ext import commands

from src.utils.custom_bot_class import DefraBot
from src.utils.menus import MyPagesMenu, MyPagesSource
from src.utils.premade_embeds import warn_embed
from src.utils.translator import Translator


class TodosSource(MyPagesSource):
    def __init__(self, entries, *, title):
        super().__init__(entries, per_page=4, title=title)


class ToDo(commands.Cog):
    def __init__(self, bot):
        self.bot: DefraBot = bot

    @commands.group()
    async def todo(self, ctx):
        """TODO_HELP"""
        if ctx.invoked_subcommand is None:
            await ctx.send(embed=warn_embed(
                title=Translator.translate("EMBED_NO_SUBCOMMAND_TITLE", ctx),
                text=Translator.translate("EMBED_NO_SUBCOMMAND_DESCRIPTION", ctx,
                                          help=f"{ctx.prefix}help {ctx.command.qualified_name}")
            ))

    @todo.command()
    async def list(self, ctx):
        """TODO_LIST_HELP"""
        current_todos = await self.bot.db.get_todos(ctx.author.id)

        if len(current_todos) <= 0:
            await ctx.send(Translator.translate("TODOS_EMPTY", ctx))
        else:
            entries = [
                (f"**`[{todo.get('id')}]`**: {todo.get('content')[0:299]}" +
                 ("..." if len(todo.get('content')) > 300 else "")) for todo in current_todos
            ]

            source = TodosSource(entries, title=Translator.translate("TODOS_LIST_TITLE", ctx, user=ctx.author))
            menu = MyPagesMenu(source, delete_message_after=True)
            await menu.start(ctx)

    @todo.command()
    async def add(self, ctx, *, task: str = None):
        """TODO_ADD_HELP"""
        if task is None:
            return await ctx.send(embed=warn_embed(title=Translator.translate("TODO_MISSING_ARG", ctx), text=""))

        resp = await self.bot.db.add_todo(ctx.author.id, task)
        if resp is True:
            await ctx.send(Translator.translate("TODO_ADDED", ctx))

    @todo.command()
    async def remove(self, ctx, todo_id):
        """TODO_REMOVE_HELP"""
        if not todo_id.isdigit():
            return await ctx.send(Translator.translate("TODO_MUST_BE_INT", ctx))

        resp = await self.bot.db.remove_todo(int(todo_id), ctx.author.id)

        if resp is None:
            await ctx.send(Translator.translate("TODO_NO_PERMISSION", ctx))
        elif resp is True:
            await ctx.send(Translator.translate("TODO_REMOVED", ctx, todo_id=todo_id))

    @todo.command()
    async def purge(self, ctx):
        """TODO_PURGE_HELP"""

        # TODO: Implement confirmation message

        resp = await self.bot.db.purge_todos(ctx.author.id)

        if resp is True:
            await ctx.send(Translator.translate("TODO_PURGE_DONE", ctx))
        else:
            await ctx.send(Translator.translate("TODO_PURGE_EMPTY_LIST", ctx))


def setup(bot):
    bot.add_cog(ToDo(bot))
