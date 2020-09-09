from exceptions import InvalidArgs
from embed import Embed
from discord.ext.commands.context import Context


async def send_help(ctx: Context, cog):
    fields = []
    for name in cog.bot.cogs:
        if cog.bot.cogs[name].get_commands():
            for c in cog.bot.cogs[name].get_commands():
                brief = ""
                if c.brief:
                    brief = c.brief
                fields.append((c.name, brief))
    await ctx.send(embed=Embed("Commands", "Commands are prefixed by a dot '.'", cog.bot.user, fields).get_embed())


def filter_public_roles(roles):
    return filter(
        lambda x: not x.is_default() and not x.permissions.administrator, roles,
    )


def list_roles(roles):
    msg_roles = "```Roles:\n"
    for r in roles:
        msg_roles += f"- {r.name}\n"
    msg_roles += "\n Add or remove a role with the command 'roles role_name'```"
    return msg_roles


def find_role(role, roles, raise_exception=False):
    for r in roles:
        if r.name == role:
            return r
    if raise_exception:
        raise InvalidArgs(f"I couldn't find the role {role}", private=True)
    return None


def find_member(name, members, raise_exception=False):
    for m in members:
        if str(m) == name:
            return m
    if raise_exception:
        raise InvalidArgs(f"I couldn't find the member {name}")
    return None


def mention_admin(ctx, message):
    server = ctx.guild
    if not server:
        return message

    roles = server.roles

    return f"{message} {roles[len(roles)-1].mention}"
