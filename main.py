#  Galleon — A multipurpose Discord bot.
#  Copyright (C) 2020  defracted.
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
from os.path import join, dirname

from discord import ActivityType, Activity
from dotenv import load_dotenv

from src.database import Database
from src.utils.base import current_time_with_tz
from src.utils.checks import BlacklistedUser
from src.utils.configuration import Config, cfg
from src.utils.custom_bot_class import DefraBot
from src.utils.translator import Translator

FIRST_CONNECTION = True
SHARD_IDS = cfg['SHARD_IDS']
SHARD_COUNT = cfg['SHARD_COUNT']

bot = DefraBot(command_prefix=Config.get_prefix, shard_count=SHARD_COUNT, shard_ids=SHARD_IDS)

if __name__ == "__main__":
    load_dotenv(join(dirname(__file__), ".env"))
    # Loading jsk
    bot.load_extension('jishaku')


@bot.check
async def check_blacklist(ctx):
    if ctx.author.id in ctx.bot.cache.blacklisted_users:
        raise BlacklistedUser(f"{ctx.author.id} is blacklisted!") from None

    return True


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
        bot.owner = await bot.fetch_user(bot.cfg.get("OWNER_ID", 576322791129743361))
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
