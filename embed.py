from typing import List

from discord.colour import Colour
from discord.member import User
from discord.embeds import Embed as D_Embed


class Embed:
    def __init__(
        self,
        title: str,
        description: str,
        author: User,
        content: List[tuple],
        colour: Colour = Colour.green(),
    ):
        self.author = author
        self.content = content
        self.colour = colour
        self.title = title
        self.description = description

    def get_embed(self):
        embed = D_Embed(title=self.title, colour=self.colour, description=self.description)
        embed.set_author(name=self.author.display_name, icon_url=self.author.avatar_url)

        for name, value in self.content:
            embed.add_field(name=name, value=value, inline=False)

        return embed
