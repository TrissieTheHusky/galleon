from discord.ext import commands
from discord import Embed
from src.utils.configuration import cfg


class Other(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="whatprefix", aliases=("prefix", "currentprefix"))
    async def what_prefix(self, ctx):
        await ctx.send(f"Current prefix is: `{self.bot.prefixes.get(str(ctx.guild.id), cfg['DEFAULT_PREFIX'])}`")

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def about(self, ctx: commands.Context):
        e = Embed(color=0x3498db)
        e.set_author(name=f"{self.bot.user}", icon_url=self.bot.user.avatar_url)
        e.add_field(name="Author", value=f"{self.bot.owner}")
        e.add_field(name="Source Code", value="[Click to open](https://github.com/runic-tears/def-bot)")
        e.set_footer(text=f"Invoked by {ctx.author}")

        await ctx.send(embed=e)


def setup(bot):
    bot.add_cog(Other(bot))
