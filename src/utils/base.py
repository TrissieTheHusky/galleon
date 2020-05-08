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


def text_to_bits(text: str, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    return '0b{0}'.format(bits.zfill(8 * ((len(bits) + 7) // 8)))


def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'


def escape_hyperlinks(text):
    hyperlinks_pattern = r"(\[(.*)]\((?P<url><[^: >]+:\/[^ >]+>|(?:https?|steam):\/\/[^\s<]+[^<.,:;\"\'\]\s])\))"
    return re.sub(hyperlinks_pattern, r'[REDACTED]', text)
