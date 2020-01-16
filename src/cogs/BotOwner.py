from discord.ext import commands
import discord
from discord import Forbidden
import traceback
import textwrap
from contextlib import redirect_stdout
import io
import asyncio
from src.utils.configuration import cfg, Config
from mcstatus import MinecraftServer
from socket import gaierror


class BotOwner(commands.Cog, name='Bot Owner'):
    def __init__(self, bot):
        self.bot = bot
        self._last_result = None
        self.sessions = set()

    async def cog_check(self, ctx):
        return await ctx.bot.is_owner(ctx.author)

    def cleanup_code(self, content):
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])
        return content.strip('` \n')

    @commands.command(name="refresh_prefixes")
    async def refresh_prefixes(self, ctx):
        m = await ctx.send("Refreshing prefixes...")
        self.bot.prefixes = await Config.update_prefixes()
        await m.edit(content=":ok_hand: Guild prefixes data refreshed")

    @commands.command()
    async def clown(self, ctx, user: discord.User):
        await ctx.send(f":clown: {user} has been clowned")

        try:
            message = await self.bot.wait_for("message", timeout=60 * 5,
                                              check=lambda m: m.author == user and m.channel.guild == ctx.guild and m.channel.permissions_for(
                                                  m.guild.me).add_reactions)
        except asyncio.TimeoutError:
            pass
        else:
            try:
                await message.add_reaction("🤡")
            except Forbidden:
                await message.channel.send("🤡")

    @commands.command()
    async def mcstatus(self, ctx, *, ip: str):
        try:
            srv = MinecraftServer.lookup(ip)
            status = srv.status()
        except gaierror:
            return await ctx.send(f"Connection error")
        else:
            return await ctx.send(f"{status.players.online} players, {round(status.latency / 2, 2)} мs")

    @commands.command(name="logout", aliases=("shutdown", "turnoff"))
    async def shutdown_the_bot(self, ctx):
        await ctx.send("The bot will turn off in 10 seconds...")
        await asyncio.sleep(10)
        return await self.bot.logout()

    @commands.group(name="message", aliases=("msg", "✉"))
    @commands.guild_only()
    async def msg(self, ctx):
        if ctx.invoked_subcommand is None:
            return await ctx.send('You didn\'t specify any subcommand.')

    @msg.command(name="repeat", aliases=('mimic', 'copy'))
    async def msg_repeat(self, ctx, *, _input: str):
        await ctx.send(_input)

    @msg.command(name="edit")
    async def msg_edit(self, ctx, channel_id: int, message_id: int, *, _input: str = None):
        c = self.bot.get_channel(channel_id)

        if c is None:
            return await ctx.send(":x: Unknown channel.")

        m = await c.fetch_message(message_id)

        await m.edit(content=_input)

        e = discord.Embed(
            colour=0x3498db,
            description="\N{OK HAND SIGN} Message edited."
        ).add_field(
            name=f"See updated content",
            value=f"[Jump to message](https://discordapp.com/{ctx.guild.id}/{channel_id}/{message_id}/)"
        )

        await ctx.send(embed=e)
        del e

    @commands.group(name="status")
    async def _status(self, ctx):
        """Manipulations with bot's presence"""
        if ctx.invoked_subcommand is None:
            return await ctx.send('No subcommand.')

    @_status.command(name="reset")
    async def _status_reset(self, ctx):
        """Makes bot's status back to default"""
        stat = discord.Activity(name="Status being reset...", type=discord.ActivityType.playing)
        await self.bot.change_presence(activity=stat)
        await asyncio.sleep(0.5)
        await self.bot.change_presence(activity=discord.Activity(name=cfg['DEFAULT_PRESENCE'], type=discord.ActivityType.playing))

        del stat
        return await ctx.send(":ok_hand: Статус успешно сброшен.")

    @_status.command(name="set")
    async def _status_set(self, ctx, stype, *, text):
        """Changes bot's status"""
        if (stype == 'playing') or (stype == '1'):
            playing_now = discord.Activity(name=str(text), type=discord.ActivityType.playing)
        elif (stype == 'watching') or (stype == '2'):
            playing_now = discord.Activity(name=str(text), type=discord.ActivityType.watching)
        elif (stype == 'listening') or (stype == '3'):
            playing_now = discord.Activity(name=str(text), type=discord.ActivityType.listening)
        # Something broken here.
        elif (stype == 'streaming') or (stype == '4'):
            if " | " not in text:
                return await ctx.send("URL is needed `<name> | <url>`")
            text = text.split(" | ")
            playing_now = discord.Activity(name=str(text[0]), url=str(text[1]), type=discord.ActivityType.streaming)
        else:
            playing_now = discord.Activity(name=str(text), type=discord.ActivityType.playing)

        await self.bot.change_presence(activity=playing_now)

        del playing_now, text, stype
        return await ctx.send(":ok_hand: Status changed.")

    # ==== GUILD COMMANDS ==== #

    @commands.group(name='guild')
    async def _guild(self, ctx):
        """Manipulations with guilds"""
        if ctx.invoked_subcommand is None:
            return await ctx.send('Pls, use some subcommand')

    @_guild.command(name='list')
    async def _guild_list(self, ctx):
        guilds_ls = self.bot.guilds
        resulting_txt = "```xl\n"
        for i in range(len(guilds_ls)):
            resulting_txt = resulting_txt + "\n" + str(guilds_ls[i]) + " (" + str(guilds_ls[i].id) + ")"

        resulting_txt += "```"
        del guilds_ls
        return await ctx.send(resulting_txt)

    @_guild.command(name='leave')
    async def _guild_leave(self, ctx, guild_id):
        guild = self.bot.get_guild(int(guild_id))
        await guild.leave()
        await ctx.send(f"I left **{guild.name}** (`{guild.id}`)")

    @commands.command(pass_context=True, name='eval')
    async def _eval(self, ctx, *, body: str):
        """
        Evaluates the code

        ❤ Also huge thanks to the https://github.com/Rapptz/RoboDanny ❤
        """

        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            '_': self._last_result
        }

        env.update(globals())

        body = self.cleanup_code(body)
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction('\u2705')
            except:
                pass

            if ret is None:
                if value:
                    await ctx.send(f'```py\n{value}\n```')
            else:
                self._last_result = ret
                await ctx.send(f'```py\n{value}{ret}\n```')


def setup(bot):
    bot.add_cog(BotOwner(bot))
