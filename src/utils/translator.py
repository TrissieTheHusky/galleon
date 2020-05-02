import json
from os.path import join, dirname
from typing import Optional

import pyseeyou

from src.utils.custom_bot_class import DefraBot


class Translator:
    bot: Optional[DefraBot] = None
    languages = {}

    @classmethod
    def set_bot(cls, bot: DefraBot):
        cls.bot = bot

    @classmethod
    async def load_translation_file(cls, language_code):
        with open(join(dirname(__file__), f"../translations/{language_code}.json"), encoding="utf-8") as lang_file:
            cls.languages.update({language_code: json.load(lang_file)})
            print(f"[TRANSLATOR] Language file for {language_code} was loaded.")

    @classmethod
    def translate(cls, query_string, ctx=None, **kwargs) -> str:
        if ctx is not None:
            current_lang = cls.bot.languages.get(ctx.guild.id, 'en_US') if ctx.guild is not None else 'en_US'
        else:
            current_lang = 'en_US'

        try:
            translation = pyseeyou.format(cls.languages[current_lang][query_string], kwargs, current_lang)
        except KeyError:
            try:
                translation = cls.languages['en_US'][query_string]
            except KeyError:
                translation = ""

        return translation
