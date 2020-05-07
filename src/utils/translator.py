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

import json
from os.path import join, dirname

import pyseeyou

from src.utils.cache import Cache
from src.utils.logger import logger


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
                translation = pyseeyou.format(cls.translations['en_US'][query_string], kwargs, current_lang)
            except KeyError:
                translation = ""

        return translation
