from discord.ext import commands


class MyHelpCommand(commands.DefaultHelpCommand):
    def get_ending_note(self):
        return 'Используйте {0.clean_prefix}help <команда>, '.format(self) + \
               'чтобы узнать подробнее об этой команде.'


class HelpCustomization(commands.Cog, name='Помощь'):
    def __init__(self, client):
        self._original_help_command = client.help_command
        client.help_command = MyHelpCommand(
            indent=3,
            no_category='Без Категории',
            command_attrs=dict(hidden=True)
        )
        client.help_command.cog = self


def setup(client):
    client.add_cog(HelpCustomization(client))
