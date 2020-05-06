def walk_role_mentions(roles, guild_id):
    """Role mention iterator"""
    for r in roles:
        if r.id != guild_id:
            yield r.mention


def walk_emojis(emojis):
    """Custom emojis iterator"""
    for emoji in emojis:
        yield f"<:{emoji.name}:{emoji.id}>"
