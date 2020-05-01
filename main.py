import logging
import os
from os.path import join, dirname

from discord import ActivityType, Activity
from dotenv import load_dotenv

from src.utils.base import current_time_with_tz
from src.utils.cache import Cache
from src.utils.configuration import Config
from src.utils.custom_bot_class import DefraBot
from src.utils.database import Database
from src.utils.translator import Translator

bot = DefraBot(command_prefix=Config.get_prefix)
bot.remove_command("help")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    load_dotenv(join(dirname(__file__), ".env"))
    # Pass bot to Translator
    Translator.set_bot(bot)


@bot.event
async def on_connect():
    # Connecting to Redis
    await Cache.connect()
    # Purging all the data in Redis
    await Cache.purge()
    # Loading jsk
    bot.load_extension('jishaku')

    # Connecting to database
    await Database.connect({
        "user": bot.cfg["DATABASE"]["USER"], "password": bot.cfg["DATABASE"]["PASSWORD"],
        "database": bot.cfg["DATABASE"]["DATABASE"], "host": bot.cfg["DATABASE"]["HOST"],
        "port": bot.cfg["DATABASE"]["PORT"]
    })

    # Loading languages
    for file in os.listdir(join(dirname(__file__), "./src/translations")):
        await Translator.load_translation_file(file[:-5])

    # Updating data in memory cache and redis
    for guild in bot.guilds:
        bot.loop.create_task(bot.update_prefix(guild.id))
        bot.loop.create_task(bot.update_language(guild.id))
        bot.loop.create_task(Cache.update_timezone(guild.id))

    # Loading cogs
    for file in os.listdir(join(dirname(__file__), "./src/cogs")):
        if file.endswith(".py") and not file.endswith(".disabled.py"):
            bot.load_extension(f"src.cogs.{file[:-3]}")
            print(f"[COG] {file[:-3]} loaded")


@bot.event
async def on_ready():
    bot.owner = await bot.fetch_user(576322791129743361)
    bot.dev_channel = bot.get_channel(bot.cfg["DEV_LOG_CHANNEL_ID"])

    await bot.change_presence(activity=Activity(name=bot.cfg['DEFAULT_PRESENCE'], type=ActivityType.playing))
    await bot.dev_channel.send(
        f"\U0001f527 **`[{current_time_with_tz(bot.cfg.get('DEFAULT_TZ')).strftime('%d.%M.%Y %H:%M')}]`** I am ready!")

    print(f"[{bot.user.name.upper()}] Ready.")


bot.run(os.environ.get("TOKEN"))
