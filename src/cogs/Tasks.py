from discord.ext import commands, tasks
from discord import VoiceChannel, Guild
from src.utils.custom_bot_class import DefraBot


class Tasks(commands.Cog):
    def __init__(self, bot):
        self.bot: DefraBot = bot
        self.counter_channel: VoiceChannel = self.bot.get_channel(693748230445465641)
        self.defrabot_guild: Guild = self.bot.get_guild(692405029755158549)
        self.defracted_server_members_counter.start()

    def cog_unload(self):
        self.defracted_server_members_counter.cancel()

    @tasks.loop(hours=6)
    async def defracted_server_members_counter(self):
        await self.counter_channel.edit(name=f"Участников: {self.defrabot_guild.member_count}", reason="Tasks")


def setup(bot):
    bot.add_cog(Tasks(bot))
