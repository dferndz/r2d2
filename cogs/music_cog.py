from youtube_search import YoutubeSearch

from discord.ext.commands import command
from discord.ext.commands.context import Context
from discord.guild import Guild
from discord.voice_client import VoiceClient
from discord.colour import Colour
from ytdl import YTDLSource

from embeds.embed import Embed
from embeds.alert import alert
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
                await ctx.send(embed=alert("▶️ Resumed").get_embed())
                return
            raise InvalidArgs("Tell me what to play!")

        await ctx.send(embed=alert(f"🔎 Searching for '{query}'").get_embed())
        results = YoutubeSearch(query).to_dict()
        url = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"]

        player = await YTDLSource.from_url(url, loop=self.bot.loop)

        if results[0]["thumbnails"]:
            image = results[0]["thumbnails"][0]
        else:
            image = None

        await ctx.send(
            embed=Embed(
                f"Now playing {title}",
                description=url,
                colour=Colour.red(),
                image=image,
            ).get_embed()
        )

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
                await ctx.send(embed=alert("⏸ Paused").get_embed())

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
                await ctx.send(embed=alert("⏹ Stoped").get_embed())

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
            await ctx.send(embed=alert("❌ Disconnected").get_embed())
