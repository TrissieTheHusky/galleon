from discord.ext import commands
from src.utils.custom_bot_class import DefraBot


class MyHelpCommand(commands.DefaultHelpCommand):
    def get_ending_note(self):
        return f'Use {self.clean_prefix}help <command>, to learn more.'


class HelpCustomization(commands.Cog, name='Помощь'):
    def __init__(self, client: DefraBot):
        self._original_help_command = client.help_command
        client.help_command = MyHelpCommand(
            indent=3,
            no_category='No category',
            command_attrs=dict(hidden=True)
        )
        client.help_command.cog = self


def setup(client):
    client.add_cog(HelpCustomization(client))
