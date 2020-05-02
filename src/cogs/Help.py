from discord.ext import commands
from src.utils.translator import Translator


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._original_help_command = bot.help_command
        bot.help_command = MyHelpCommand()
        bot.help_command.cog = self

    def cog_unload(self):
        self.bot.help_command = self._original_help_command


class MyHelpCommand(commands.MinimalHelpCommand):
    def get_opening_note(self):
        return Translator.translate("HELP_ENDING_NOTE", self.context, prefix=self.context.prefix)

    def add_subcommand_formatting(self, command):
        fmt = '{0}{1} \N{EN DASH} {2}' if command.short_doc else '{0}{1}'
        self.paginator.add_line(fmt.format(self.clean_prefix, command.qualified_name,
                                           Translator.translate(command.short_doc, self.context)))


def setup(bot):
    bot.add_cog(Help(bot))
