#  The MIT License (MIT)
#
#  Copyright (c) 2020 defracted
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

import os
from os.path import join, dirname

from discord import ActivityType, Activity
from dotenv import load_dotenv

from src.utils.base import current_time_with_tz
from src.utils.configuration import Config, cfg
from src.utils.custom_bot_class import DefraBot
from src.utils.database import Database
from src.utils.translator import Translator

FIRST_CONNECTION = True
SHARD_IDS = cfg['SHARD_IDS']
SHARD_COUNT = cfg['SHARD_COUNT']

bot = DefraBot(command_prefix=Config.get_prefix, shard_count=SHARD_COUNT, shard_ids=SHARD_IDS)

if __name__ == "__main__":
    load_dotenv(join(dirname(__file__), ".env"))
    # Loading jsk
    bot.load_extension('jishaku')


@bot.event
async def on_ready():
    global FIRST_CONNECTION
    if FIRST_CONNECTION:
        # Changing the indicator value
        FIRST_CONNECTION = False

        # Connecting to database
        await Database.connect({
            "user": bot.cfg["DATABASE"]["USER"], "password": bot.cfg["DATABASE"]["PASSWORD"],
            "database": bot.cfg["DATABASE"]["DATABASE"], "host": bot.cfg["DATABASE"]["HOST"],
            "port": bot.cfg["DATABASE"]["PORT"]
        })

        # Loading languages
        for file in os.listdir(join(dirname(__file__), "./src/translations")):
            await Translator.load_translation_file(file[:-5])

        # Loading cogs
        for cog_name in bot.cfg.get("COGS"):
            bot.load_extension(cog_name)
            bot.logger.info(f"{cog_name} loaded")

        # Fetching bot owner and logging channel
        bot.owner = await bot.fetch_user(576322791129743361)
        bot.dev_channel = await bot.fetch_channel(bot.cfg["DEV_LOG_CHANNEL_ID"])

        # Informing bot dev
        await bot.dev_channel.send(
            f"\U0001f527 **`[{current_time_with_tz(bot.cfg['DEFAULT_TZ']).strftime('%H:%M:%S')}]`**"
            f" Connection to Discord API has been established."
        )

    # Safe adding every existing guild to the database
    for guild in bot.guilds:
        await Database.safe_add_guild(guild.id)

    # Updating data in cache
    await bot.refresh_cache()


@bot.event
async def on_shard_ready(shard_id=SHARD_IDS[len(SHARD_IDS) - 1]):
    bot.logger.info(f"Shard #{shard_id} is ready.")
    # Resetting presence
    await bot.change_presence(activity=Activity(name=bot.cfg['DEFAULT_PRESENCE'], type=ActivityType.playing))


bot.run(os.environ.get("TOKEN"))
