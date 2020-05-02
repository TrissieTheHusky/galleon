import discord
from discord.ext import commands

from src.utils.translator import Translator


class Help(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot
        self._original_help_command = bot.help_command
        bot.help_command = MyHelpCommand()
        bot.help_command.cog = self

    def cog_unload(self):
        self.bot.help_command = self._original_help_command


class MyHelpCommand(commands.MinimalHelpCommand):
    def __init__(self, **options):
        super().__init__(**options)

        self.embed = discord.Embed(color=0x4285F4)

    async def prepare_help_command(self, ctx, command):
        # i18n
        self.aliases_heading = Translator.translate("ALIASES", self.context)
        self.commands_heading = Translator.translate("COMMANDS", self.context)
        # Original class methods
        self.paginator.clear()
        self.embed.description = ""
        self.embed.title = None
        await super().prepare_help_command(ctx, command)

    # Formatter for the embed
    def format_pages(self, **kwargs):
        if kwargs.get("title", None) is not None:
            self.embed.title = kwargs.get("title", None)

    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            self.embed.description = page
            await destination.send(embed=self.embed)

    def get_opening_note(self):
        return None

    def get_ending_note(self):
        return Translator.translate("HELP_ENDING_NOTE", self.context, prefix=self.context.prefix)

    def add_bot_commands_formatting(self, commands, heading):
        if commands:
            joined = ', '.join(f"`{c.name}`" for c in commands)
            self.paginator.add_line('\n**%s**' % Translator.translate(heading, self.context))
            self.paginator.add_line(joined)

    def add_subcommand_formatting(self, command):
        fmt = '`{0}{1}` — {2}' if command.short_doc else '`{0}{1}`'
        self.paginator.add_line(fmt.format(self.clean_prefix, command.qualified_name,
                                           Translator.translate(command.short_doc, self.context)))

    def add_aliases_formatting(self, aliases):
        self.paginator.add_line('**%s** %s' % (self.aliases_heading, ', '.join([f"`{alias}`" for alias in aliases])),
                                empty=True)

    def add_command_formatting(self, command):
        if command.description:
            self.paginator.add_line(Translator.translate(command.description, self.context), empty=True)

        signature = self.get_command_signature(command)
        if command.aliases:
            self.format_pages(title=signature)
            self.add_aliases_formatting(command.aliases)
        else:
            self.format_pages(title=signature)

        if command.help:
            try:
                self.paginator.add_line(Translator.translate(command.help, self.context), empty=True)
            except RuntimeError:
                for line in command.help.splitlines():
                    self.paginator.add_line(line)
                self.paginator.add_line()

    async def send_cog_help(self, cog):
        bot = self.context.bot
        if bot.description:
            self.paginator.add_line(bot.description, empty=True)

        if cog.description:
            self.paginator.add_line(cog.description, empty=True)

        filtered = await self.filter_commands(cog.get_commands(), sort=self.sort_commands)
        if filtered:
            self.paginator.add_line('**%s %s**' % (cog.qualified_name, self.commands_heading))
            for command in filtered:
                self.add_subcommand_formatting(command)

            note = self.get_ending_note()
            if note:
                self.paginator.add_line()
                self.paginator.add_line(note)

        await self.send_pages()

    async def send_group_help(self, group):
        self.add_command_formatting(group)

        filtered = await self.filter_commands(group.commands, sort=self.sort_commands)
        if filtered:
            self.paginator.add_line('**%s**' % self.commands_heading)
            for command in filtered:
                self.add_subcommand_formatting(command)

            note = self.get_ending_note()
            if note:
                self.paginator.add_line()
                self.paginator.add_line(note)

        await self.send_pages()

    async def send_command_help(self, command):
        self.add_command_formatting(command)
        self.paginator.close_page()
        await self.send_pages()


def setup(bot):
    bot.add_cog(Help(bot))