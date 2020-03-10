import subprocess
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
        start = subprocess.Popen(
            ['systemctl', 'start', 'minecraft.service'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )

        stdout, stderr = start.communicate()

        if stderr is None:
            return await ctx.send('**SUCCESS**')
        else:
            return await ctx.send(':x: **ERROR**:\n```yaml\n' + f'{stderr.decode("utf-8")}' + '\n```')

    @server.command()
    @commands.has_any_role("Team Member", "Team Lead")
    async def update_datapack(self, ctx: Context, mapname, datapack):
        proc = subprocess.Popen(
            ['git', '-C', f"/home/minecraft/{mapname}/datapacks/{datapack}", "pull", "origin", "master"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )

        stdout, stderr = proc.communicate()

        if stderr is None:
            return await ctx.send('**SUCCESS**')
        else:
            return await ctx.send(':x: **ERROR**:\n```yaml\n' + f'{stderr.decode("utf-8")}' + '\n```')


def setup(bot):
    bot.add_cog(MapMaker(bot))
