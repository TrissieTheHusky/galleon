from src.utils.custom_bot_class import DefraBot
from src.utils.configuration import Config, cfg
from src.utils.webhook_logger import Logger
from os.path import join, dirname
from datetime import datetime as dt
from dotenv import load_dotenv
from uuid import uuid4
import discord
import asyncio
import os

bot = DefraBot(command_prefix=Config.get_prefix)

if __name__ == "__main__":
    # Loading .env
    load_dotenv(join(dirname(__file__), ".env"))

    # Iterating though all the existing cogs
    for file in os.listdir(join(dirname(__file__), "./src/cogs")):
        # If cog is disable or not python file - do nothing
        if file.endswith(".py") and not file.endswith(".disabled.py"):
            # If above is true - load it as extension/cog
            bot.load_extension(f"src.cogs.{file[:-3]}")
            print(f"* {file[:-3]} loaded")

    print("--------------")


@bot.event
async def on_ready():
    # Refreshing prefixes
    bot.prefixes = await Config.update_prefixes()

    # Getting the bot creator user
    bot.owner = await bot.fetch_user(576322791129743361)

    # Updating presence
    await bot.change_presence(activity=discord.Activity(name=cfg["DEFAULT_PRESENCE"], type=discord.ActivityType.playing))

    # Logging
    await Logger.log(embed=discord.Embed(color=0x3498db,
                                         description=f":white_check_mark: Sucessfully loaded!\n\n" +
                                                     f":hash: `{str(uuid4())[-6:]}`",
                                         timestamp=dt.utcnow()))
    print(f"[{bot.user.name.upper()}] Ready.")


bot.run(os.environ.get("TOKEN"))
