from discord.ext.commands import command
from discord.ext.commands.context import Context

from exceptions import PermissionDenied, InvalidArgs, OutOfServer
from tools import find_member
from cogs import BaseCog


class Members(BaseCog):
    admin = True

    @command(brief="ban member")
    async def ban(self, ctx: Context, member_name: str = None):
        if not ctx.guild:
            raise OutOfServer()

        if not ctx.author.guild_permissions.ban_members:
            raise PermissionDenied()

        if not member_name:
            raise InvalidArgs("I need a name!")

        member = find_member(member_name, ctx.guild.members, raise_exception=True)

        await member.ban()
        await ctx.send(f"{member.mention} has been banned.")

    @command(brief="unban user")
    async def unban(self, ctx: Context, member_name: str = None):
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

    @command(brief="create a role")
    async def create_role(self, ctx: Context, role: str = None):
        if not ctx.guild:
            raise OutOfServer()
        if not ctx.author.guild_permissions.manage_roles:
            raise PermissionDenied()
        if not role:
            raise InvalidArgs("I need a role name!")

        await ctx.guild.create_role(name=role)
        await ctx.send(f"Created role {role}")
