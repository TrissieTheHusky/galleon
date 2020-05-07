from datetime import datetime

from discord import Embed


def error_debug():
    return


def error_embed(title=":x: Something went wrong",
                text="It looks like something broke, bot developer should now about it by now!"):
    return Embed(title=title, description=text, color=0xFF0000)


def warn_embed(text=None, title=":warning: Notice!"):
    e = Embed(title=title, color=0xF1C40F)
    if text is not None:
        e.description = text
    return e


class DefraEmbed(Embed):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        try:
            colour = kwargs["colour"]
        except KeyError:
            colour = kwargs.get("color", 0x008081)

        footer_text = kwargs.get("footer_text", None)
        footer_icon_url = kwargs.get("footer_icon_url", "")

        if footer_text is not None:
            self.set_footer(text=footer_text, icon_url=footer_icon_url)

        self.color = colour
        self.colour = colour

        if kwargs.get('now_time', True):
            self.timestamp = datetime.utcnow()
