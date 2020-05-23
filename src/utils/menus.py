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

from discord import Embed
from discord.ext.menus import MenuPages, ListPageSource, button, First, Last

from src.utils.configuration import cfg
from src.utils.translator import Translator


class MyPagesMenu(MenuPages, inherit_buttons=False):
    def __init__(self, source, **kwargs):
        super().__init__(source, clear_reactions_after=True, timeout=120.0, **kwargs)

    def _skip_double_triangle_buttons(self):
        max_pages = self._source.get_max_pages()
        if max_pages is None:
            return True
        return max_pages <= 2

    @button(cfg['EMOJIS'].get('FIRST_PAGE', '\N{BLACK LEFT-POINTING DOUBLE TRIANGLE WITH VERTICAL BAR}\ufe0f'), position=First(0),
            skip_if=_skip_double_triangle_buttons)
    async def go_to_first_page(self, payload):
        """go to the first page"""
        await self.show_page(0)

    @button(cfg['EMOJIS'].get('PREVIOUS_PAGE', '\N{BLACK LEFT-POINTING TRIANGLE}\ufe0f'), position=First(1))
    async def go_to_previous_page(self, payload):
        """go to the previous page"""
        await self.show_checked_page(self.current_page - 1)

    @button(cfg['EMOJIS'].get('NEXT_PAGE', '\N{BLACK RIGHT-POINTING TRIANGLE}\ufe0f'), position=Last(1))
    async def go_to_next_page(self, payload):
        """go to the next page"""
        await self.show_checked_page(self.current_page + 1)

    @button(cfg['EMOJIS'].get('LAST_PAGE', '\N{BLACK RIGHT-POINTING DOUBLE TRIANGLE WITH VERTICAL BAR}\ufe0f'), position=Last(2), skip_if=_skip_double_triangle_buttons)
    async def go_to_last_page(self, payload):
        """go to the last page"""
        # The call here is safe because it's guarded by skip_if
        await self.show_page(self._source.get_max_pages() - 1)

    @button(cfg['EMOJIS'].get('STOP_PAGES', '\N{BLACK SQUARE FOR STOP}\ufe0f'), position=Last(0))
    async def stop_pages(self, payload):
        """stops the pagination session."""
        self.stop()


class MyPagesSource(ListPageSource):
    def __init__(self, entries, *, per_page, title=None, **kwargs):
        super().__init__(entries, per_page=per_page)
        self.embed = Embed(color=0x008081)

        if title is not None:
            self.embed.title = title

    def format_page(self, menu, page):
        if isinstance(page, str):
            return page
        else:
            self.embed.set_footer(text=f"{Translator.translate('PAGE', menu.ctx)} {menu.current_page + 1}/{self.get_max_pages()}")
            self.embed.description = '\n'.join(page)
            return self.embed
