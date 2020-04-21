from src.utils.custom_bot_class import DefraBot
import src.utils.converters as converters
from src.utils.configuration import Config, cfg
from os.path import join, dirname
from dotenv import load_dotenv
from discord.ext import commands
from discord import ActivityType, Activity
from src.utils.database import Database
from src.utils.base import current_time_with_tz
import os
import logging

bot = DefraBot(command_prefix=Config.get_prefix)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    load_dotenv(join(dirname(__file__), ".env"))

    converters.init(bot)


@bot.event
async def on_connect():
    await Database.connect({
        "user": cfg["DATABASE"]["USER"], "password": cfg["DATABASE"]["PASSWORD"],
        "database": cfg["DATABASE"]["DATABASE"], "host": cfg["DATABASE"]["HOST"],
        "port": cfg["DATABASE"]["PORT"]
    })

    for guild in bot.guilds:
        bot.loop.create_task(bot.update_prefix(guild.id))
        bot.loop.create_task(bot.update_timezone(guild.id))

    for file in os.listdir(join(dirname(__file__), "./src/cogs")):
        if file.endswith(".py") and not file.endswith(".disabled.py"):
            bot.load_extension(f"src.cogs.{file[:-3]}")
            print(f"* {file[:-3]} loaded")

    print("--------------")


@bot.event
async def on_ready():
    bot.owner = await bot.fetch_user(576322791129743361)
    bot.dev_channel = bot.get_channel(cfg["DEV_LOG_CHANNEL_ID"])

    await bot.change_presence(activity=Activity(name=cfg['DEFAULT_PRESENCE'], type=ActivityType.playing))
    await bot.dev_channel.send(
        f"\U0001f527 **`[{current_time_with_tz(cfg.get('DEFAULT_TZ')).strftime('%d.%M.%Y %H:%M')}]`** I am ready!")

    print(f"[{bot.user.name.upper()}] Ready.")


@bot.group(name="cogs", aliases=["cog"])
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


bot.run(os.environ.get("TOKEN"))
