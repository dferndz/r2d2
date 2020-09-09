from discord.ext.commands.cog import Cog


class BaseCog(Cog):
    admin = False

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
