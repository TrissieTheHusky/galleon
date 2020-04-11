from discord.ext.commands import Cog, command, Context, is_owner
from src.typings import BotType
from discord.ext import menus


class MySource(menus.ListPageSource):
    def format_page(self, menu: menus.MenuPages, page):
        if isinstance(page, str):
            return page
        else:
            return '\n'.join(page) + f"\n\n**Page {menu.current_page + 1}/{self.get_max_pages()}**"


class TestCog(Cog, command_attrs={"hidden": True}):
    def __init__(self, bot):
        self.bot: BotType = bot

    @command()
    @is_owner()
    async def test(self, ctx: Context):
        entries = ['The random text here', 'Bottom Text', 'MS Comic Sans is the best', "Hi page 2",
                   "is this a good page?", "nah looks like 3rd"]

        source = MySource(entries, per_page=2)
        menu = menus.MenuPages(source, clear_reactions_after=True)

        await menu.start(ctx)


def setup(bot):
    bot.add_cog(TestCog(bot))