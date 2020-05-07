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

from random import choice


class Jokes:
    memes = (
        "Выводы, сделанные из выводов — это квинтэссенция результата.",
        "Москвичи умеют определять точное время по длине пробок.",
        "— Дочь, ты пила?\n— Нет, мама, я топор!",
        "— Ты шутишь хуже чем Елена воробей\n— КАПИТАН Елена Воробей!",
        "Свежо пердение, но дышится с трудом!",
        "— Скажи триста.\n— Триста.\n— Абстрагируйся от суеты, достигнув с космосом единства.",
        "— Помогите мне избавиться от комплексов!\n— От каких именно?\n— От зенитно—ракетных.",
        "— Вы сообразительный?\n— В смысле?"
    )

    @classmethod
    def get(cls):
        """Возвращает очень смешную шутку из набора настолько же смешных шуток"""
        return choice(cls.memes)
