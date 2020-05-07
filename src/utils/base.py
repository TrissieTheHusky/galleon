#  The MIT License (MIT)
#
#  Copyright (c) 2020 defracted
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

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
