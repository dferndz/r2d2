import random
from discord.ext.commands import Cog, command, CommandNotFound

from exceptions import (
    BaseUserError,
    OutOfServer,
    InvalidArgs,
    COMMAND_NOT_FOUND_RESPONSE,
    INTERNAL_ERROR_RESPONSE,
)
from tools import send_help, filter_public_roles, list_roles, find_role
from logger import log, log_msg
from constants import QUESTION_RESPONSES


class Basic(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command("help")
        self._last_member = None

    @Cog.listener()
    async def on_ready(self):
        log("Bot is ready")

    @Cog.listener()
    async def on_message(self, message):
        if self.bot.user in message.mentions:
            await message.channel.send("Hey there!")
        if message.author == self.bot.user:
            log("Bot sent response")
        else:
            log_msg(message)

    @command(aliases=["h"])
    async def help(self, ctx):
        await send_help(ctx, self)

    @Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, CommandNotFound):
            await ctx.send(COMMAND_NOT_FOUND_RESPONSE)
        elif isinstance(error, BaseUserError):
            if error.private:
                await ctx.author.send(error.message)
            else:
                await ctx.send(error.message)
        else:
            await ctx.send(INTERNAL_ERROR_RESPONSE)


class Greetings(Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @Cog.listener()
    async def on_member_join(self, member):
        print(f"{member} has joined the server.")

    @Cog.listener()
    async def on_member_remove(self, member):
        print(f"{member} has left the server.")


class Misc(Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @command(name="8ball")
    async def _8ball(self, ctx, *args):
        if args:
            await ctx.send(random.choice(QUESTION_RESPONSES))
        else:
            raise InvalidArgs("I need a question!")

    @command(brief="get the bot latency")
    async def ping(self, ctx):
        await ctx.send(f"Pong! Latency: {round(self.bot.latency * 1000)} ms")


class Roles(Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @command(brief="list, add or remove roles", aliases=["role"])
    async def roles(self, ctx, role_name=None):
        server = ctx.guild

        if not server:
            raise OutOfServer()

        roles = filter_public_roles(server.roles)

        if role_name:
            role = find_role(role_name, roles, raise_exception=True)
            if role in ctx.author.roles:
                await ctx.author.remove_roles(role)
                await ctx.author.send(f"Removed the role {role.name} at {ctx.guild}")
            else:
                await ctx.author.add_roles(role)
                await ctx.author.send(f"Added the role {role.name} at {ctx.guild}")
        else:
            await ctx.send(list_roles(roles))
