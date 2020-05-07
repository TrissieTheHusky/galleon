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

from typing import Dict

from src.utils.database import Database
from src.utils.logger import logger


class Cache:
    prefixes: Dict[int, str] = {}
    languages: Dict[int, str] = {}
    timezones: Dict[int, str] = {}

    @classmethod
    async def refresh_prefix(cls, guild_id: int):
        val = await Database.get_prefix(guild_id)
        cls.prefixes.update({guild_id: val})
        logger.info(f"Prefix for Guild {guild_id} has been refreshed")

    @classmethod
    async def refresh_language(cls, guild_id: int):
        val = await Database.get_language(guild_id)
        cls.languages.update({guild_id: val})
        logger.info(f"Language for Guild {guild_id} has been refreshed")

    @classmethod
    async def refresh_timezone(cls, guild_id: int):
        val = await Database.get_timezone(guild_id)
        cls.timezones.update({guild_id: val})
        logger.info(f"Timezone for Guild {guild_id} has been refreshed")
