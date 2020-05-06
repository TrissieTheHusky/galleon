import re
from datetime import datetime

from pytz import timezone, exceptions

from src.utils.configuration import cfg


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


def is_timezone(arg: str):
    """
    Checks if the timezone in argument is correct timezone

    :param arg: timezone but in string
    :return: True if it, False if not
    """
    try:
        timezone(arg)
        return True
    except exceptions.UnknownTimeZoneError:
        return False


def escape_hyperlinks(text):
    hyperlinks_pattern = r"(\[(.*)]\((?P<url><[^: >]+:\/[^ >]+>|(?:https?|steam):\/\/[^\s<]+[^<.,:;\"\'\]\s])\))"
    return re.sub(hyperlinks_pattern, r'[REDACTED]', text)
