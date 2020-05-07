import discord
from discord.ext import commands
import itertools

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
    def __init__(self, **options):
        super().__init__(**options, command_attrs=dict(hidden=True))
        self.embed = discord.Embed(color=0x008081)

    def command_not_found(self, string):
        return Translator.translate("HELP_COMMAND_NOT_FOUND", self.context, command=string)

    def subcommand_not_found(self, command, string):
        if isinstance(command, commands.Group) and len(command.all_commands) > 0:
            return Translator.translate("HELP_COMMAND_SUBCOMMAND_NOT_FOUND", self.context, command=command.qualified_name, element=string)
        return Translator.translate("HELP_COMMAND_NO_SUBCOMMANDS", self.context, command=command.qualified_name)

    async def send_error_message(self, error):
        destination = self.get_destination()
        self.embed.title = error
        await destination.send(embed=self.embed)

    def prepare_embed(self):
        self.embed.description = None
        self.embed.title = None

    async def prepare_help_command(self, ctx, command):
        await ctx.trigger_typing()
        # i18n
        self.aliases_heading = Translator.translate("ALIASES", self.context)
        self.commands_heading = Translator.translate("COMMANDS", self.context)
        # Original class methods
        self.paginator.clear()
        self.prepare_embed()
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
        self.paginator.add_line('**%s** %s' % (self.aliases_heading, ', '.join((f"`{alias}`" for alias in aliases))),
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

    async def send_bot_help(self, mapping):
        ctx = self.context
        bot = ctx.bot

        if bot.description:
            self.paginator.add_line(bot.description, empty=True)

        no_category = '\u200b{0.no_category}'.format(self)

        def get_category(command, *, no_category=no_category):
            cog = command.cog
            return cog.qualified_name if cog is not None else no_category

        filtered = await self.filter_commands(bot.commands, sort=True, key=get_category)
        to_iterate = itertools.groupby(filtered, key=get_category)

        for category, commands in to_iterate:
            commands = sorted(commands, key=lambda c: c.name) if self.sort_commands else list(commands)
            self.add_bot_commands_formatting(commands, category)

        note = self.get_ending_note()
        if note:
            self.embed.set_footer(text=note)

        await self.send_pages()

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
                self.embed.set_footer(text=note)

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
                self.embed.set_footer(text=note)

        await self.send_pages()

    async def send_command_help(self, command):
        self.add_command_formatting(command)
        self.paginator.close_page()
        await self.send_pages()


def setup(bot):
    bot.add_cog(Help(bot))
