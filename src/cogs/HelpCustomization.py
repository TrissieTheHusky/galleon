from discord.ext import commands
from src.utils.translator import Translator
from src.utils.base import DefraEmbed
from src.utils.custom_bot_class import DefraBot
import discord


class HelpCustomization(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot: DefraBot = bot

    @commands.command()
    async def help(self, ctx: commands.Context, *cog):
        embed = DefraEmbed(title=Translator.translate("HELP_TITLE_GENERAL", ctx))

        if not cog:
            for cog in self.bot.cogs:
                actual_cog: commands.Cog = self.bot.cogs[cog]
                cog_description = ""

                for command in actual_cog.get_commands():
                    if not command.hidden:
                        cog_description += "**{0}** {1}\n".format(
                            f"{ctx.prefix}{command}", f"- {Translator.translate(f'{command.short_doc}', ctx)}" \
                                if len(command.short_doc) > 0 else '')

                if len(cog_description) > 0:
                    embed.add_field(name=actual_cog.qualified_name, value=cog_description, inline=False)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(HelpCustomization(bot))
