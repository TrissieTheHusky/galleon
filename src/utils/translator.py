import json
from os.path import join, dirname
from src.utils.logger import logger

import pyseeyou

from src.utils.cache import Cache


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
            if context.guild is not None:
                current_lang = Cache.languages.get(context.guild.id, 'en_US')

        try:
            translation = pyseeyou.format(cls.translations[current_lang][query_string], kwargs, current_lang)
        except KeyError:
            try:
                translation = cls.translations['en_US'][query_string]
            except KeyError:
                translation = ""

        return translation
