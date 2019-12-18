import discord
from discord.ext import commands
import traceback
import sys
from src.utils.webhook_logger import Logger


class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """
        ctx   : Context
        error : Exception
        """

        # Это предотвращает обработку ошибок для команд, с локальным обработчиками
        if hasattr(ctx.command, 'on_error'):
            return

        error = getattr(error, 'original', error)

        # Все типы ошибок, внутри ignored - будут игнорироваться обработчиком
        is_ignore_enabled = False
        ignored = commands.UserInputError

        if is_ignore_enabled:
            if isinstance(error, ignored):
                return

        async def send_here(message):
            await ctx.send(message)

        async def send_here_no_perms():
            await ctx.send(f':lock: У вас нет доступа к команде `{ctx.command}`')

        # """"
        # Обработка ошибок происходит тут
        # Reference: isinstance(error, event)
        # """

        if isinstance(error, commands.CommandNotFound):
            return

        elif isinstance(error, commands.DisabledCommand):
            return await ctx.send(f'Команда `{ctx.command}` отключена.')

        elif isinstance(error, commands.MissingPermissions):
            return await send_here_no_perms()

        elif isinstance(error, commands.MissingRequiredArgument):
            return await send_here(
                ":warning: Вы пропустили какой-то важный аргумент.\n"
                f"\N{SPIRAL NOTE PAD} Синтаксис команды: "
                f"`{ctx.prefix}{ctx.command.qualified_name} {ctx.command.signature}`"
            )

        elif isinstance(error, commands.errors.NotOwner):
            return await send_here_no_perms()

        elif isinstance(error, commands.BotMissingPermissions):
            return await ctx.send(f":x: Мне недостатчно прав, чтобы это сделать.")

        elif isinstance(error, commands.CheckFailure):
            return await send_here_no_perms()

        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.author.send(f":x: Команду {ctx.command} можно использовать только на серверах.")

        elif isinstance(error, discord.Forbidden):
            return await ctx.send(":x: Мне недостаточно прав, чтобы выполнить это действие.")

        # ==== COOLDOWN CHECKS ====

        elif isinstance(error, commands.CommandOnCooldown):
            if await ctx.bot.is_owner(ctx.message.author):
                return await ctx.reinvoke()

            return await ctx.send(f'Подождите ещё **{round(error.retry_after, 2)}** секунд.')

        await Logger.log(
            embed=discord.Embed(
                color=0xFF0000, title=f"Uncaught Exception in command {ctx.command}", description=f"{error}"
            ).add_field(
                name="Guild", value=f"{ctx.guild} (`{ctx.guild.id}`)"
            ).add_field(
                name="Author", value=f"{ctx.author} (`{ctx.author.id}`)"
            )
        )
        await ctx.send(':x: Произошла непредвиденная ошибка, разработчик уже знает о ней.')
        print('---------\nIgnoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
