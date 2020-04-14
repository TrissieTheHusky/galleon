from discord.ext.commands import Cog, Context, group
from src.typings import BotType, InfractionRow
from typing import List
from src.utils.database import Database
from src.utils.base import DefraEmbed, is_num_in_str
from datetime import timezone

# TODO: Создать систему прав

class Moderation(Cog):
    def __init__(self, bot):
        self.bot: BotType = bot

    async def cog_check(self, ctx: Context):
        return await ctx.bot.is_owner(ctx.author)

    @group(aliases=["inf"])
    async def infraction(self, ctx: Context):
        if ctx.invoked_subcommand is None:
            await ctx.send("Вы не указали субкоманду")

    @infraction.command()
    async def info(self, ctx: Context, infraction_id=None):
        if infraction_id is None:
            return await ctx.send(":warning: Вы должны указать ID инфракции, чтобы просмотреть информацию о ней.")

        if is_num_in_str(infraction_id) is False:
            return await ctx.send(":warning: ID инфракции должен являться целочисленным значением.")

        row: List[InfractionRow] = await Database.fetch(
            "SELECT * FROM bot.infractions WHERE inf_id = $1 AND guild_id = $2 LIMIT 1;",
            int(infraction_id), ctx.guild.id)

        if len(row) <= 0:
            return await ctx.send(f":x: Инфракция `#{infraction_id}` не найдена.")

        DB_INF_ID = row[0]['inf_id']
        DB_MODERATOR_ID = row[0]['moderator_id']
        DB_TARGET_ID = row[0]['target_id']
        DB_REASON = row[0]['reason']
        DB_INF_TYPE = row[0]['inf_type']
        DB_ADDED_AT = row[0]['added_at']
        DB_EXPIRES_AT = row[0]['expires_at']

        TARGET_USER = self.bot.get_user(DB_TARGET_ID)
        MODERATOR_USER = self.bot.get_user(DB_MODERATOR_ID)

        embed = DefraEmbed(title=f"Инфракция #{DB_INF_ID}", footer_text=f"Запрос отправил {ctx.author}")
        embed.add_field(
            name="Модератор",
            value=f"{MODERATOR_USER} (`{DB_MODERATOR_ID}`)" if MODERATOR_USER is not None else f"`{DB_MODERATOR_ID}`"
        )
        embed.add_field(
            name="Наказанный",
            value=f"{TARGET_USER} (`{DB_TARGET_ID}`)" if TARGET_USER is not None else f"`{DB_TARGET_ID}`"
        )
        embed.add_field(name="Тип инфракции", value=f"{DB_INF_TYPE}")
        embed.add_field(name="Причина", value=f"{DB_REASON}", inline=False)
        embed.add_field(
            name="Дата получения инфракции (UTC)",
            value=f"{DB_ADDED_AT.astimezone(tz=timezone.utc).strftime('%d.%m.%Y at %H:%M:%S')}"
        )
        embed.add_field(
            name="Дата истечения срока инфракции (UTC)",
            value=f"{DB_EXPIRES_AT.astimezone(tz=timezone.utc).strftime('%d.%m.%Y at %H:%M:%S')}"
        )

        await ctx.send(embed=embed, content=f"{(DB_EXPIRES_AT - DB_ADDED_AT)}\n{(DB_EXPIRES_AT > DB_ADDED_AT)}")


def setup(bot):
    bot.add_cog(Moderation(bot))
