from discord import Embed


def error_debug():
    return


def error_embed(title=":x: Something went wrong",
                text="It looks like something broke, bot developer should now about it by now!"):
    return Embed(title=title, description=text, color=0xFF0000)


def warn_embed(text, title=":warning: Notice!", ):
    return Embed(title=title, description=text, color=0xF1C40F)
