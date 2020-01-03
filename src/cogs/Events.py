from discord.ext import commands
import discord
from src.utils.configuration import cfg


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg):
        if cfg["CLOWNS"]["ENABLED"]:
            if msg.author.id in cfg["CLOWNS"]["LIST"]:
                await msg.add_reaction("🤡")


def setup(bot):
    bot.add_cog(Events(bot))
