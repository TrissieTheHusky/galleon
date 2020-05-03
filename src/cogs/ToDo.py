from discord import Embed
from discord.ext import commands
from discord.ext.menus import MenuPages, ListPageSource, button, First, Last

from src.utils.custom_bot_class import DefraBot
from src.utils.premade_embeds import warn_embed
from src.utils.translator import Translator


class TodosMenu(MenuPages, inherit_buttons=False):
    def __init__(self, source, **kwargs):
        super().__init__(source, **kwargs)

    @button('<:previous_page:706576101844975716>', position=First(1))
    async def go_to_previous_page(self, payload):
        """go to the previous page"""
        await self.show_checked_page(self.current_page - 1)

    @button('<:next_page:706576101719277629>', position=Last(2))
    async def go_to_next_page(self, payload):
        """go to the next page"""
        await self.show_checked_page(self.current_page + 1)

    @button('<:stop:706576101681528853>', position=Last(0))
    async def stop_pages(self, payload):
        """stops the pagination session."""
        self.stop()


class TodosSource(ListPageSource):
    def __init__(self, entries, *, per_page, user):
        super().__init__(entries, per_page=per_page)
        self.embed = Embed(color=0x008081)
        self.user = user

    def format_page(self, menu, page):
        if isinstance(page, str):
            return page
        else:
            self.embed.set_author(name=Translator.translate("TODOS_LIST_TITLE", menu.ctx, user=str(self.user)),
                                  icon_url=self.user.avatar_url)
            self.embed.set_footer(text=Translator.translate("PAGE", menu.ctx) +
                                       f" {menu.current_page + 1}/{self.get_max_pages()}")
            self.embed.description = '\n'.join(page)
            return self.embed


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

            source = TodosSource(entries, per_page=4, user=ctx.author)
            menu = TodosMenu(source, delete_message_after=True)
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
