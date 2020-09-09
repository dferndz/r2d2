import random
from typing import List

from discord.ext.commands import command
from discord.ext.commands.context import Context
from discord.member import Member
from discord.guild import Guild

from exceptions import OutOfServer, InvalidArgs
from constants import QUESTION_RESPONSES
from cogs.base_cog import BaseCog


class Misc(BaseCog):
    @command(name="8ball", brief="ask a question, get a prediction")
    async def _8ball(self, ctx: Context, *args):
        if args:
            await ctx.send(random.choice(QUESTION_RESPONSES))
        else:
            raise InvalidArgs("I need a question!")

    @command(brief="get the bot latency")
    async def ping(self, ctx: Context):
        await ctx.send(f"Pong! Latency: {round(self.bot.latency * 1000)} ms")

    @command(name="rand", aliases=["random"], brief="mention a random member")
    async def random_member(self, ctx: Context):
        if not ctx.guild:
            raise OutOfServer()
        guild: Guild = ctx.guild
        members: List[Member] = guild.members
        await ctx.send(random.choice(members).mention)
