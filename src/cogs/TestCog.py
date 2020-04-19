from discord.ext.commands import Cog, command, Context, is_owner
from src.typings import BotType
from discord.ext import menus
from typing import List, Optional


class MySource(menus.ListPageSource):
    def format_page(self, menu: menus.MenuPages, page):
        if isinstance(page, str):
            return page
        else:
            return '\n'.join(page) + f"\n\n**Page {menu.current_page + 1}/{self.get_max_pages()}**"


class TestCog(Cog, command_attrs={"hidden": True}):
    def __init__(self, bot):
        self.bot: BotType = bot

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
