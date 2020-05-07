from discord.ext import commands

from src.utils.custom_bot_class import DefraBot
from src.utils.menus import MyPagesMenu, MyPagesSource
from src.utils.premade_embeds import warn_embed, DefraEmbed
from src.utils.translator import Translator


class TodosSource(MyPagesSource):
    def __init__(self, entries, *, title):
        super().__init__(entries, per_page=4, title=title)


class ToDo(commands.Cog):
    def __init__(self, bot):
        self.bot: DefraBot = bot

    @commands.group()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def todo(self, ctx):
        """TODO_HELP"""
        if ctx.invoked_subcommand is None:
            await ctx.send(embed=warn_embed(title=Translator.translate("EMBED_NO_SUBCOMMAND_TITLE", ctx),
                                            text=Translator.translate("EMBED_NO_SUBCOMMAND_DESCRIPTION", ctx,
                                                                      help=f"{ctx.prefix}help {ctx.command.qualified_name}")))

    @todo.command(aliases=("ls",))
    async def list(self, ctx):
        """TODO_LIST_HELP"""
        await ctx.trigger_typing()

        current_todos = await self.bot.db.get_todos(ctx.author.id)
        if len(current_todos) <= 0:
            await ctx.send(Translator.translate("TODOS_EMPTY", ctx))
        else:
            entries = []
            for index, todo in enumerate(current_todos):
                entries.append(f"`{index + 1}` {todo['content']}")

            source = TodosSource(entries, title=Translator.translate("TODOS_LIST_TITLE", ctx, user=ctx.author))
            menu = MyPagesMenu(source, delete_message_after=True)
            await menu.start(ctx)

    @todo.command()
    async def add(self, ctx, *, task: str = None):
        """TODO_ADD_HELP"""
        await ctx.trigger_typing()

        if task is None:
            return await ctx.send(embed=warn_embed(title=Translator.translate("TODO_MISSING_ARG", ctx), text=""))

        resp = await self.bot.db.add_todo(ctx.author.id, task)
        if resp is True:
            await ctx.send(Translator.translate("TODO_ADDED", ctx))

    @todo.command(aliases=("rmv", "del", "delete"))
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def remove(self, ctx, todo_id):
        """TODO_REMOVE_HELP"""
        await ctx.trigger_typing()

        if not todo_id.isdigit():
            return await ctx.send(Translator.translate("TODO_MUST_BE_INT", ctx))

        todo_id = int(todo_id)
        target_todo = None
        todos = await self.bot.db.get_todos(ctx.author.id)

        for index, todo in enumerate(todos):
            if index + 1 == todo_id:
                target_todo = todo

        if target_todo is None:
            await ctx.send(warn_embed(title=Translator.translate('TODO_NOT_EXISTING', ctx)))
        else:
            is_deleted = await self.bot.db.remove_todo(target_todo.get('timestamp'), target_todo.get('user_id'))
            if is_deleted:
                await ctx.send(embed=DefraEmbed(description=Translator.translate('TODO_REMOVED', ctx, todo=target_todo.get('content'))))

    @todo.command()
    async def purge(self, ctx):
        """TODO_PURGE_HELP"""
        await ctx.trigger_typing()

        resp = await self.bot.db.purge_todos(ctx.author.id)

        if resp is True:
            await ctx.send(Translator.translate("TODO_PURGE_DONE", ctx))
        else:
            await ctx.send(Translator.translate("TODO_PURGE_EMPTY_LIST", ctx))


def setup(bot):
    bot.add_cog(ToDo(bot))
