from src.utils.configuration import cfg
from discord import Embed
from datetime import datetime
from pytz import timezone


def current_time_with_tz(tz_name=cfg['DEFAULT_TZ']) -> datetime:
    """
    :param str tz_name: Timezone name, e.g. "Europe/Moscow"
    :return: Datetime object with timezone from tz_name argument
    """
    return datetime.now().astimezone(tz=timezone(tz_name))


def is_num_in_str(arg: str):
    """
    Checks if the string can be converted into the integer

    :param arg: a string to check
    :return: True if can be converted, False if not
    """
    try:
        int(arg)
        return True
    except ValueError:
        return False


class DefraEmbed(Embed):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        try:
            colour = kwargs["colour"]
        except KeyError:
            colour = kwargs.get("color", 0x3498db)

        footer_text = kwargs.get("footer_text", None)
        footer_icon_url = kwargs.get("footer_icon_url", "")

        if footer_text is not None:
            self.set_footer(text=footer_text, icon_url=footer_icon_url)

        self.color = colour
        self.colour = colour
        self.timestamp = datetime.utcnow()
