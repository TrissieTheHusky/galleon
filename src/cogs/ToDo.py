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

from io import BytesIO
import sys

from discord import File, Forbidden
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

        async with self.bot.db.pool.acquire() as db:
            current_todos = await db.fetch("SELECT * FROM bot.todos WHERE user_id = $1 ORDER BY timestamp DESC LIMIT 200;", ctx.author.id)

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
    async def export(self, ctx):
        """TODO_EXPORT_HELP"""
        await ctx.trigger_typing()

        async with self.bot.db.pool.acquire() as db:
            current_todos = await db.fetch("SELECT * FROM bot.todos WHERE user_id = $1 ORDER BY timestamp DESC LIMIT 200;", ctx.author.id)

        if len(current_todos) <= 0:
            await ctx.send(Translator.translate("TODOS_EMPTY", ctx))
        else:
            output = "Todo:\n"
            for index, todo in enumerate(current_todos):
                output += f"{index + 1}) {todo['content']}\n"

            bdata = BytesIO()
            bdata.write(output.encode(encoding='utf-8'))
            bdata.seek(0)

            try:
                await ctx.author.send(file=File(bdata, filename="Todo List.txt"))
                await ctx.send(Translator.translate('TODO_EXPORTED', ctx))
            except Forbidden:
                await ctx.send(Translator.translate('TODO_EXPORT_CLOSED_DM', ctx, author=ctx.author.mention))

    @todo.command()
    async def add(self, ctx, *, task: str = None):
        """TODO_ADD_HELP"""
        await ctx.trigger_typing()

        if task is None:
            return await ctx.send(embed=warn_embed(title=Translator.translate("TODO_MISSING_ARG", ctx), text=""))

        async with self.bot.db.pool.acquire() as conn:
            async with conn.transaction():
                resp = await conn.fetchval("INSERT INTO bot.todos (user_id, content) VALUES($1, $2) RETURNING True", ctx.author.id, task)

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

        async with self.bot.db.pool.acquire() as conn:
            todos = await conn.fetch("SELECT * FROM bot.todos WHERE user_id = $1 ORDER BY timestamp DESC LIMIT 200;", ctx.author.id)

        for index, todo in enumerate(todos):
            if index + 1 == todo_id:
                target_todo = todo

        if target_todo is None:
            await ctx.send(embed=warn_embed(title=Translator.translate('TODO_NOT_EXISTING', ctx)))
        else:
            async with self.bot.db.pool.acquire() as db:
                async with db.transaction():
                    params = (target_todo.get('timestamp'), target_todo.get('user_id'))
                    is_deleted = await db.fetchval("DELETE FROM bot.todos WHERE timestamp = $1 AND user_id = $2 RETURNING True", *params)

            if is_deleted:
                await ctx.send(embed=DefraEmbed(description=Translator.translate('TODO_REMOVED', ctx, todo=target_todo.get('content'))))

    @todo.command()
    async def purge(self, ctx):
        """TODO_PURGE_HELP"""
        await ctx.trigger_typing()

        async with self.bot.db.pool.acquire() as conn:
            async with conn.transaction():
                resp = await conn.fetchval("DELETE FROM bot.todos WHERE user_id = $1 RETURNING True", ctx.author.id)

        if resp is True:
            await ctx.send(Translator.translate("TODO_PURGE_DONE", ctx))
        else:
            await ctx.send(Translator.translate("TODO_PURGE_EMPTY_LIST", ctx))


def setup(bot):
    bot.add_cog(ToDo(bot))
