#  Copyright (c) 2020 defracted
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

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
