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

import json
from os.path import join, dirname

import pyseeyou

from .cache import CacheManager
from .logger import logger


class Translator:
    translations = {}

    @classmethod
    async def load_translation_file(cls, language_code):
        with open(join(dirname(__file__), f"../translations/{language_code}.json"), encoding="utf-8") as lang_file:
            cls.translations.update({language_code: json.load(lang_file)})
            logger.info(f"Language file for {language_code} was loaded.")

    @classmethod
    def translate(cls, query_string, context=None, **kwargs) -> str:
        current_lang = 'en_US'

        if context is not None:
            if hasattr(context, 'guild'):
                if context.guild is not None:
                    if (settings_cache := CacheManager.guilds.get(context.guild.id, None)) is not None:
                        current_lang = settings_cache.language

            elif isinstance(context, int):
                if (settings_cache := CacheManager.guilds.get(context, None)) is not None:
                    current_lang = settings_cache.language

        try:
            translation = pyseeyou.format(cls.translations[current_lang][query_string], kwargs, current_lang)
        except KeyError:
            try:
                translation = pyseeyou.format(cls.translations['en_US'][query_string], kwargs, current_lang)
            except KeyError:
                translation = "..."

        return translation
