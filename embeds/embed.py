from typing import List

from discord.colour import Colour
from discord.member import User
from discord.embeds import Embed as D_Embed


class Embed:
    def __init__(
        self,
        title: str,
        description: str = None,
        author: User = None,
        content: List[tuple] = [],
        footer: str = None,
        image: str = None,
        colour: Colour = Colour.green(),
    ):
        self.author = author
        self.content = content
        self.colour = colour
        self.title = title
        self.description = description
        self.footer = footer
        self.image = image

    def get_embed(self):
        embed = D_Embed(title=self.title, colour=self.colour, description=self.description)

        if self.author:
            embed.set_author(name=self.author.display_name, icon_url=self.author.avatar_url)

        if self.image:
            embed.set_image(url=self.image)

        for name, value in self.content:
            embed.add_field(name=name, value=value, inline=False)

        if self.footer:
            embed.set_footer(text=self.footer)

        return embed
