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

import aiohttp

from src.utils.configuration import cfg


class APIs:
    yandex_translate_url = 'https://translate.yandex.net/api/v1.5/tr.json'
    yandex_key = cfg['API_KEYS']['YANDEX']

    @staticmethod
    async def get_cat(token):
        """Returns image URL with cats"""
        async with aiohttp.ClientSession(headers={"x-api-key": token}) as cs:
            async with cs.get('https://api.thecatapi.com/v1/images/search') as r:
                data = await r.json()
                return data[0].get("url", None)

    @staticmethod
    async def get_fox():
        """Returns image URL with some foxes"""
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://randomfox.ca/floof/') as r:
                data = await r.json()
                return data.get('image', None)

    @classmethod
    async def yandex_translate(cls, tr_from=None, tr_to="en", text="hello"):
        """Translates input to desired language"""
        async with aiohttp.ClientSession() as cs:
            if tr_from is None:
                async with cs.get(f'{cls.yandex_translate_url}/translate?lang={tr_to}&key={cls.yandex_key}&text={text}') as res:
                    data = await res.json()
                    return data

            elif tr_from is not None:
                async with cs.get(f'{cls.yandex_translate_url}/translate?lang={tr_from}-{tr_to}&key={cls.yandex_key}&text={text}') as res:
                    data = await res.json()
                    return data
