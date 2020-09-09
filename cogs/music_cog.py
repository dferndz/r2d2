from youtube_search import YoutubeSearch

from discord.ext.commands import Cog, command, CommandNotFound, Bot
from discord.ext.commands.context import Context
from discord.guild import Guild
from discord.voice_client import VoiceClient
from ytdl import YTDLSource

from cogs.base_cog import BaseCog
from exceptions import (
    OutOfServer,
    InvalidArgs,
    OutOfVoiceChannel,
)


class Music(BaseCog):
    clients = {}

    @command(brief="look up and play music")
    async def play(self, ctx: Context, *, query: str = None):
        if not ctx.guild:
            raise OutOfServer()
        if not ctx.author.voice:
            raise OutOfVoiceChannel()

        guild: Guild = ctx.guild
        clients = self.clients

        if guild.id not in clients:
            client: VoiceClient = await ctx.author.voice.channel.connect()
            clients[guild.id] = client
        else:
            client = clients[guild.id]

        if not query:
            if client.is_paused():
                client.resume()
                return
            raise InvalidArgs("Tell me what to play!")

        results = YoutubeSearch(query).to_dict()
        url = f"https://youtube.com{results[0]['url_suffix']}"

        player = await YTDLSource.from_url(url, loop=self.bot.loop)

        if client.is_playing():
            client.stop()

        client.play(
            player, after=lambda e: print("Player error: %s" % e) if e else None
        )

    @command(brief="pause music")
    async def pause(self, ctx: Context):
        if not ctx.guild:
            raise OutOfServer()

        guild: Guild = ctx.guild
        clients = self.clients

        if guild.id in clients:
            client: VoiceClient = clients[guild.id]
            if client.is_playing():
                client.pause()

    @command(brief="stop music")
    async def stop(self, ctx: Context):
        if not ctx.guild:
            raise OutOfServer()

        guild: Guild = ctx.guild
        clients = self.clients

        if guild.id in clients:
            client: VoiceClient = clients[guild.id]
            if client.is_paused() or client.is_playing():
                client.stop()

    @command(brief="disconnect from voice channel")
    async def disconnect(self, ctx: Context):
        if not ctx.guild:
            raise OutOfServer()

        guild: Guild = ctx.guild
        clients = self.clients

        if guild.id in clients:
            client: VoiceClient = guild.voice_client
            del clients[guild.id]
            await client.disconnect()
