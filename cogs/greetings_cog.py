from discord.ext.commands import Cog, command, CommandNotFound, Bot
from discord.member import Member
from discord.guild import Guild

from logger import log
from cogs.base_cog import BaseCog


class Greetings(BaseCog):
    @Cog.listener()
    async def on_member_join(self, member: Member):
        guild: Guild = member.guild
        log(f"{str(member)} joined {guild.name}")
        guild.system_channel.send(f"Say hi to {member.display_name}")

    @Cog.listener()
    async def on_member_remove(self, member: Member):
        guild: Guild = member.guild
        log(f"{str(member)} left {guild.name}")
