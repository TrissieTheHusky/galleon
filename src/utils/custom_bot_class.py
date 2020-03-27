from discord.ext.commands import AutoShardedBot


class DefraBot(AutoShardedBot):
    def __init__(self, command_prefix, **options):
        super().__init__(command_prefix, **options)
        self.prefixes = {}
        self.owner = None
