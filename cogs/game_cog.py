from discord.ext.commands import command
from discord.ext.commands.context import Context
from discord import Message, User, Reaction
from discord.ext.commands import Cog, Bot

from embeds.alert import alert
from cogs.base_cog import BaseCog
from game_engine import Game as GameEngine


UP = '⬆️'
DOWN = '⬇️'
LEFT = '⬅️'
RIGHT = '➡️'
TIMEOUT = 120


class Game(BaseCog):
    games = {}

    @staticmethod
    def init_game():
        game = GameEngine()
        game.put_player(1, 0)
        game.put_box(4, 6)
        game.put_box(4, 7)
        game.add_goal(1, 3)
        game.add_goal(9, 9)
        game.build_wall(2, 2, 1, 3)
        game.build_wall(0, 4, 3, 1)
        game.build_wall(5, 3, 2, 1)
        game.build_wall(4, 2, 1, 2)
        game.build_wall(4, 0, 1, 1)
        return game

    @command()
    async def game(self, ctx: Context):
        message: Message = ctx.message
        if message.id in self.games:
            await ctx.send("Game already started")
        else:
            game = self.init_game()
            g_message: Message = await ctx.send(str(game.board), delete_after=TIMEOUT)
            self.games[g_message.id] = game
            moves = [LEFT, RIGHT, UP, DOWN]
            for m in moves:
                await g_message.add_reaction(m)

    @Cog.listener()
    async def on_reaction_add(self, reaction: Reaction, user: User):
        message: Message = reaction.message
        if user == self.bot.user:
            return
        if message.id in self.games:
            g = self.games[message.id]
            e = reaction.emoji
            if e == UP:
                g.up()
            if e == DOWN:
                g.down()
            if e == RIGHT:
                g.right()
            if e == LEFT:
                g.left()
            if g.win():
                await message.edit(content=str(g.board), embed=alert("VICTORY!").get_embed())
                await message.clear_reactions()
                del self.games[message.id]
            else:
                await message.edit(content=str(g.board), delete_after=TIMEOUT)

    @Cog.listener()
    async def on_message_delete(self, message: Message):
        if message.id in self.games:
            del self.games[message.id]

    @Cog.listener()
    async def on_reaction_remove(self, reaction: Reaction, user: User):
        await self.on_reaction_add(reaction, user)
