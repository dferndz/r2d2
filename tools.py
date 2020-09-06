from exceptions import InvalidArgs


async def send_help(ctx, cog):
    message = "```"
    for name in cog.bot.cogs:
        if cog.bot.cogs[name].get_commands():
            message += f"{name}: \n"
            for c in cog.bot.cogs[name].get_commands():
                brief = ""
                if c.brief:
                    brief = c.brief
                message += f"{c.name:>12}   {brief}\n"
    message += "```"
    await ctx.send(message)


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
