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


class CacheBase(dict):
    def __init__(self, database, name: str):
        super().__init__()
        self.name = name
        self.database = database

    async def refresh(self, guild_id: int):
        current = await getattr(self.database, self.name.lower()).get(guild_id)
        super().update({guild_id: current})
        print("[CACHE] {0} for {1} was refreshed.".format(self.name.capitalize(), guild_id))
