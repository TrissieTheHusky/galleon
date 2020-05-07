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

from discord import Embed
from discord.ext.menus import MenuPages, ListPageSource, button, First, Last

from src.utils.translator import Translator


class MyPagesMenu(MenuPages, inherit_buttons=False):
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
            self.embed.set_footer(text=Translator.translate("PAGE", menu.ctx) +
                                       f" {menu.current_page + 1}/{self.get_max_pages()}")
            self.embed.description = '\n'.join(page)
            return self.embed
