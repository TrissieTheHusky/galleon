from asyncio import subprocess
from discord.ext import commands
from discord.ext.commands import Cog, Context


class MapMaker(Cog, name="MapMakers"):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx: Context):
        return ctx.guild.id == 686098043816509471

    @commands.group()
    @commands.has_any_role("Team Member", "Team Lead")
    async def server(self, ctx: Context):
        if ctx.invoked_subcommand is None:
            return await ctx.send("No subcommand was specified!")

    @server.command()
    @commands.has_any_role("Team Member", "Team Lead")
    async def start(self, ctx: Context):
        pull = subprocess.Popen(['systemd', 'start', 'minecraft'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout, stderr = pull.communicate()

        if stderr is None:
            return await ctx.send('**SUCCESS**\n```yaml\n' + f'{stdout.decode("utf-8")}' + '\n```')
        else:
            return await ctx.send(':x: **ERROR**:\n```yaml\n' + f'{stderr.decode("utf-8")}' + '\n```')

    @server.command()
    @commands.has_any_role("Team Member", "Team Lead")
    async def update_datapack(self, ctx: Context):
        return await ctx.send("Time to get newer version og datapack, isn't it? huh?")


def setup(bot):
    bot.add_cog(MapMaker(bot))
