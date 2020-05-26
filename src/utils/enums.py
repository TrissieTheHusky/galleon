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

from enum import Enum


class InfractionType(Enum):
    tempban = 'tempban'
    tempmute = 'tempmute'
    permaban = 'permaban'
    ban = 'permaban'
    warning = 'warn'
    warn = 'warn'


class TableRolesTypes(Enum):
    mute_role = 'mute_role'
    mod_roles = 'mod_roles'
    admin_roles = 'admin_roles'
