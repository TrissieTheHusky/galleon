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
