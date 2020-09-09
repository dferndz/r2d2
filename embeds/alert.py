from embeds.embed import Embed
from discord.ext.commands.context import Context
from discord.colour import Colour


def alert(msg: str):
    embed = Embed(msg, colour=Colour.red())
    return embed
