from discord.ext.commands import Cog, command

from exceptions import PermissionDenied, InvalidArgs, OutOfServer
from tools import find_member
from cogs import BaseCog


class Members(BaseCog):
    admin = True

    @command()
    async def ban(self, ctx, member_name=None):
        if not ctx.guild:
            raise OutOfServer()

        if not ctx.author.guild_permissions.ban_members:
            raise PermissionDenied()

        if not member_name:
            raise InvalidArgs("I need a name!")

        member = find_member(member_name, ctx.guild.members, raise_exception=True)

        await member.ban()
        await ctx.send(f"{member.mention} has been banned.")

    @command()
    async def unban(self, ctx, member_name=None):
        if not ctx.guild:
            raise OutOfServer()

        if not ctx.author.guild_permissions.ban_members:
            raise PermissionDenied()

        if not member_name:
            raise InvalidArgs("I need a name!")

        bans = await ctx.guild.bans()
        banned_members = [b.user for b in bans]

        member = find_member(member_name, banned_members, raise_exception=True)

        await ctx.guild.unban(member)
        await ctx.send(f"{member.mention} has been banned.")
