#  The MIT License (MIT)
#
#  Copyright (c) 2020 defracted
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

from typing import List, Optional

from discord.ext import menus
from discord.ext.commands import Cog, command, Context

from src.utils.custom_bot_class import DefraBot


class MySource(menus.ListPageSource):
    def format_page(self, menu: menus.MenuPages, page):
        if isinstance(page, str):
            return page
        else:
            return '\n'.join(page) + f"\n\n**Page {menu.current_page + 1}/{self.get_max_pages()}**"


class TestCog(Cog, command_attrs={"hidden": True}):
    def __init__(self, bot):
        self.bot: DefraBot = bot

    async def cog_check(self, ctx: Context):
        return await ctx.bot.is_owner(ctx.author)

    @command()
    async def test(self, ctx: Context, *name: Optional[str]):
        # source = MySource(entries, per_page=2)
        # menu = menus.MenuPages(source, clear_reactions_after=True)
        #
        # await menu.start(ctx)
        cogs: List[str] = []

        for cog in self.bot.cogs:
            cogs.append(cog)

        await ctx.send(f"")


def setup(bot):
    bot.add_cog(TestCog(bot))
