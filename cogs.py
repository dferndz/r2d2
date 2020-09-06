import random
from discord.ext.commands import Cog, command, CommandNotFound

from tools import send_help
from logger import log, log_msg


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
        if message.author == self.bot.user:
            log("Bot sent response")
        else:
            log_msg(message)

    @command()
    async def help(self, ctx):
        await send_help(ctx, self)

    @Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, CommandNotFound):
            log(f"{ctx.author} -> Command not found")
            await ctx.send(
                "Hmm, I don't know what that means. Type '.help' to get a list of commands."
            )
        else:
            raise error


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
        responses = [
            "It is certain.",
            "It is decidedly so.",
            "Without a doubt.",
            "Yes - definitely.",
            "You may rely on it.",
            "As I see it, yes.",
            "Most likely.",
            "Outlook good.",
            "Yes.",
            "Signs point to yes.",
            "Reply hazy, try again.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again.",
            "Don't count on it.",
            "My reply is no.",
            "My sources say no.",
            "Outlook not so good.",
            "Very doubtful.",
        ]
        if args:
            await ctx.send(random.choice(responses))
        else:
            await ctx.send("I need a question!")

    @command(brief="get the bot latency")
    async def ping(self, ctx):
        await ctx.send(f"Pong! Latency: {round(self.bot.latency * 1000)} ms")


class Roles(Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @command(brief="list, add or remove roles")
    async def roles(self, ctx, role=None):
        server = ctx.guild

        if not server:
            await ctx.send("You must call this command from a server.")
            return

        roles = filter(lambda x: not x.is_default() and not x.permissions.administrator, server.roles)

        if role:
            for r in roles:
                if r.name == role:
                    if r in ctx.author.roles:
                        await ctx.author.remove_roles(r)
                        await ctx.author.send(f"Removed the role {r.name} at {ctx.guild}")
                    else:
                        await ctx.author.add_roles(r)
                        await ctx.author.send(f"Added the role {r.name} at {ctx.guild}")
                    return
            await ctx.author.send(f"Didn't find the role {role}")

        else:
            await ctx.send("Roles:")
            msg_roles = ""
            for r in roles:
                msg_roles += f"- {r.name}\n"
            msg_roles += "\n Add or remove a role with the command 'roles role_name'"
            await ctx.send(msg_roles)
