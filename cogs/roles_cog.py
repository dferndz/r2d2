from discord.ext.commands import command
from discord.ext.commands.context import Context

from exceptions import OutOfServer
from tools import filter_public_roles, list_roles, find_role
from cogs.base_cog import BaseCog
from embeds.alert import alert


class Roles(BaseCog):
    @command(brief="list, add or remove roles", aliases=["role"])
    async def roles(self, ctx: Context, role_name: str = None):
        server = ctx.guild

        if not server:
            raise OutOfServer()

        roles = filter_public_roles(server.roles)

        if role_name:
            role = find_role(role_name, roles, raise_exception=True)
            if role in ctx.author.roles:
                await ctx.author.remove_roles(role)
                await ctx.author.send(
                    embed=alert(
                        f"Removed the role {role.name} at {ctx.guild}"
                    ).get_embed()
                )
            else:
                await ctx.author.add_roles(role)
                await ctx.author.send(
                    embed=alert(
                        f"Added the role {role.name} at {ctx.guild}"
                    ).get_embed()
                )
        else:
            await ctx.send(embed=list_roles(roles))
