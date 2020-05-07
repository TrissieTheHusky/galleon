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
