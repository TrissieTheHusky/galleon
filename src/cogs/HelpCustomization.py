from discord.ext import commands


class MyHelpCommand(commands.DefaultHelpCommand):
    def get_ending_note(self):
        return f'Use {self.clean_prefix}help [command | cog], to learn more.'


class HelpCustomization(commands.Cog):
    def __init__(self, client):
        self._original_help_command = client.help_command
        client.help_command = MyHelpCommand(
            indent=3,
            no_category='No Category',
            command_attrs=dict(hidden=True)
        )
        client.help_command.cog = self


def setup(client):
    client.add_cog(HelpCustomization(client))
