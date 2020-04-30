import aiohttp


class APIs:
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
