from src.utils.custom_bot_class import DefraBot
import src.utils.converters as converters
from src.utils.configuration import Config, cfg
from os.path import join, dirname
from datetime import datetime
from dotenv import load_dotenv
from discord import Activity, ActivityType
from discord.ext import commands
import os

bot = DefraBot(command_prefix=Config.get_prefix)
converters.init(bot)

if __name__ == "__main__":
    load_dotenv(join(dirname(__file__), ".env"))


@bot.event
async def on_ready():
    bot.prefixes = await Config.update_prefixes()
    bot.owner = await bot.fetch_user(576322791129743361)
    bot.dev_log_channel = bot.get_channel(cfg["DEV_LOG_CHANNEL_ID"])

    for file in os.listdir(join(dirname(__file__), "./src/cogs")):
        if file.endswith(".py") and not file.endswith(".disabled.py"):
            bot.load_extension(f"src.cogs.{file[:-3]}")
            print(f"* {file[:-3]} loaded")

    print("--------------")

    await bot.change_presence(activity=Activity(name=cfg['DEFAULT_PRESENCE'], type=ActivityType.playing))
    await bot.dev_log_channel.send(f"`[{datetime.utcnow()}]` I am ready!")

    print(f"[{bot.user.name.upper()}] Ready.")


@bot.group(name="cogs", aliases=("cog",))
@commands.is_owner()
async def cog(ctx: commands.Context):
    if ctx.invoked_subcommand is None:
        await ctx.send("You didn't specify the subcommand")


@cog.command(name="load")
@commands.is_owner()
async def load(ctx: commands.Context, cog: str):
    bot.load_extension(f"src.cogs.{cog}")
    await ctx.send(f":white_check_mark: Loaded `{cog}`")


@cog.command(name="unload")
@commands.is_owner()
async def unload(ctx: commands.Context, cog: str):
    bot.unload_extension(f"src.cogs.{cog}")
    await ctx.send(f":white_check_mark: Unloaded `{cog}`")


@load.error
@unload.error
async def cog_err_handler(ctx: commands.Context, error):
    # For some reason isinstance(error, error_event) is not working here...
    # TODO: Fix it
    return await ctx.send(f"{error=}")


bot.run(os.environ.get("TOKEN"))
