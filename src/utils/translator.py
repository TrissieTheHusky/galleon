#  Copyright (c) 2020 defracted
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

import json
from os.path import join, dirname

import pyseeyou

from .cache import Cache
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
                    current_lang = Cache.languages.get(context.guild.id, 'en_US')

            elif isinstance(context, int):
                current_lang = Cache.languages.get(context, 'en_US')

        try:
            translation = pyseeyou.format(cls.translations[current_lang][query_string], kwargs, current_lang)
        except KeyError:
            try:
                translation = pyseeyou.format(cls.translations['en_US'][query_string], kwargs, current_lang)
            except KeyError:
                translation = ""

        return translation
