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
