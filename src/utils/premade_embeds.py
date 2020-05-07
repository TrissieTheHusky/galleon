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
        self.timestamp = datetime.utcnow()
