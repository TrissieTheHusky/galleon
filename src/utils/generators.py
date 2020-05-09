#  Copyright (c) 2020 defracted
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

def walk_role_mentions(roles, guild_id):
    """Role mention iterator"""
    for r in roles:
        if r.id != guild_id:
            yield r.mention


def walk_emojis(emojis):
    """Custom emojis iterator"""
    for emoji in emojis:
        yield str(emoji)
