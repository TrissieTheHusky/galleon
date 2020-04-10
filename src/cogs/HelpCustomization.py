from discord.ext import commands
from src.typings import BotType


class MyHelpCommand(commands.DefaultHelpCommand):
    def get_ending_note(self):
        return f'Используйте {self.clean_prefix}help <команда>, чтобы узнать больше.'


class HelpCustomization(commands.Cog, name='Помощь'):
    def __init__(self, client: BotType):
        self._original_help_command = client.help_command
        client.help_command = MyHelpCommand(
            indent=3,
            no_category='Без категории',
            command_attrs=dict(hidden=True)
        )
        client.help_command.cog = self


def setup(client):
    client.add_cog(HelpCustomization(client))
