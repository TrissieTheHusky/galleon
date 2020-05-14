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

from src.utils.configuration import cfg


class APIs:
    def __init__(self, session):
        self.session = session
        self.yandex_translate_url = 'https://translate.yandex.net/api/v1.5/tr.json'
        self.yandex_key = cfg['API_KEYS']['YANDEX']

    async def get_cat(self, token):
        """Returns image URL with cats"""
        async with self.session.get('https://api.thecatapi.com/v1/images/search', headers={"x-api-key": token}) as r:
            data = await r.json()
            return data[0].get("url", None)

    async def get_fox(self):
        """Returns image URL with some foxes"""
        async with self.session.get('https://randomfox.ca/floof/') as r:
            data = await r.json()
            return data.get('image', None)

    async def yandex_translate(self, tr_from=None, tr_to="en", text="hello"):
        """Translates input to desired language"""
        if tr_from is None:
            async with self.session.get(f'{self.yandex_translate_url}/translate?lang={tr_to}&key={self.yandex_key}&text={text}') as res:
                data = await res.json()
                return data

        elif tr_from is not None:
            async with self.session.get(f'{self.yandex_translate_url}/translate?lang={tr_from}-{tr_to}&key={self.yandex_key}&text={text}') as res:
                data = await res.json()
                return data
