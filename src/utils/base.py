from discord import Embed
from datetime import datetime


class DefraEmbed(Embed):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        try:
            colour = kwargs["colour"]
        except KeyError:
            colour = kwargs.get("color", 0x3498db)

        self.color = colour
        self.colour = colour
        self.timestamp = datetime.utcnow()
