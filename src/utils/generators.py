def walk_role_mentions(roles):
    """Role mention iterator"""
    for r in roles:
        yield r.mention


def walk_emojis(emojis):
    """Custom emojis iterator"""
    for emoji in emojis:
        yield f"<:{emoji.name}:{emoji.id}>"
