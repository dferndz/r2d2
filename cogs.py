import random
import os
from typing import List
from youtube_search import YoutubeSearch


from discord.ext.commands import Cog, command, CommandNotFound, Bot
from discord.ext.commands.context import Context
from discord.member import Member
from discord.guild import Guild
from discord.channel import TextChannel
from discord.invite import Invite
from discord.utils import oauth_url
from discord.permissions import Permissions
from discord.voice_client import VoiceClient
from ytdl import YTDLSource

from exceptions import (
    BaseUserError,
    OutOfServer,
    InvalidArgs,
    PermissionDenied,
    OutOfVoiceChannel,
    COMMAND_NOT_FOUND_RESPONSE,
    INTERNAL_ERROR_RESPONSE,
)
from tools import send_help, filter_public_roles, list_roles, find_role, mention_admin
from logger import log, log_msg
from constants import QUESTION_RESPONSES


class BaseCog(Cog):
    admin = False

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None


class Basic(BaseCog):
    def __init__(self, bot):
        super().__init__(bot)
        self.bot.remove_command("help")

    @Cog.listener()
    async def on_ready(self):
        log("Bot is ready")

    @Cog.listener()
    async def on_message(self, message):
        if self.bot.user in message.mentions:
            await message.channel.send("Hey there!")
        if message.author == self.bot.user:
            log("Bot sent response")
        else:
            log_msg(message)

    @command(aliases=["h"], brief="display this help message")
    async def help(self, ctx: Context):
        await send_help(ctx, self)

    @command(brief="share r2d2 to a server")
    async def r2d2(self, ctx: Context):
        if "CLIENT_ID" in os.environ:
            client_id = os.environ["CLIENT_ID"]
            permission = Permissions(administrator=True)
            link = oauth_url(client_id, permissions=permission)
            await ctx.send(f"Share me! {link}")

    @command(aliases=["invites"], brief="invite url for this server")
    async def invite(self, ctx: Context):
        if not ctx.guild:
            raise OutOfServer()
        guild: Guild = ctx.guild
        author: Member = ctx.author
        if not author.guild_permissions.create_instant_invite:
            raise PermissionDenied()

        server_invites: List[Invite] = await guild.invites()

        for invite in server_invites:
            if invite.inviter == self.bot.user and invite.max_age == 0:
                await ctx.send(invite.url)
                return

        channel: TextChannel = ctx.channel
        invite: Invite = await channel.create_invite()
        await ctx.send(invite.url)

    @command(brief="mention @everyone")
    async def all(self, ctx: Context):
        if not ctx.guild:
            raise OutOfServer()
        if not ctx.author.guild_permissions.mention_everyone:
            raise PermissionDenied()
        await ctx.send(ctx.guild.default_role)

    @Cog.listener()
    async def on_command_error(self, ctx: Context, error):
        if isinstance(error, CommandNotFound):
            await ctx.send(COMMAND_NOT_FOUND_RESPONSE)
        elif isinstance(error, BaseUserError):
            if error.private:
                await ctx.author.send(error.message)
            else:
                await ctx.send(error.message)
        else:
            log(error)
            await ctx.send(mention_admin(ctx, INTERNAL_ERROR_RESPONSE))


class Greetings(BaseCog):
    @Cog.listener()
    async def on_member_join(self, member: Member):
        guild: Guild = member.guild
        log(f"{str(member)} joined {guild.name}")
        guild.system_channel.send(f"Say hi to {member.display_name}")

    @Cog.listener()
    async def on_member_remove(self, member: Member):
        guild: Guild = member.guild
        log(f"{str(member)} left {guild.name}")


class Misc(BaseCog):
    @command(name="8ball", brief="ask a question, get a prediction")
    async def _8ball(self, ctx: Context, *args):
        if args:
            await ctx.send(random.choice(QUESTION_RESPONSES))
        else:
            raise InvalidArgs("I need a question!")

    @command(brief="get the bot latency")
    async def ping(self, ctx: Context):
        await ctx.send(f"Pong! Latency: {round(self.bot.latency * 1000)} ms")

    @command(name="rand", aliases=["random"], brief="mention a random member")
    async def random_member(self, ctx: Context):
        if not ctx.guild:
            raise OutOfServer()
        guild: Guild = ctx.guild
        members: List[Member] = guild.members
        await ctx.send(random.choice(members).mention)


class Roles(BaseCog):
    @command(brief="list, add or remove roles", aliases=["role"])
    async def roles(self, ctx: Context, role_name: str = None):
        server = ctx.guild

        if not server:
            raise OutOfServer()

        roles = filter_public_roles(server.roles)

        if role_name:
            role = find_role(role_name, roles, raise_exception=True)
            if role in ctx.author.roles:
                await ctx.author.remove_roles(role)
                await ctx.author.send(f"Removed the role {role.name} at {ctx.guild}")
            else:
                await ctx.author.add_roles(role)
                await ctx.author.send(f"Added the role {role.name} at {ctx.guild}")
        else:
            await ctx.send(list_roles(roles))


clients = {}


class Music(BaseCog):
    @command(brief="look up and play music")
    async def play(self, ctx: Context, *, query: str = None):
        if not ctx.guild:
            raise OutOfServer()
        if not ctx.author.voice:
            raise OutOfVoiceChannel()

        guild: Guild = ctx.guild

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

        client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

    @command(brief="pause music")
    async def pause(self, ctx: Context):
        if not ctx.guild:
            raise OutOfServer()

        guild: Guild = ctx.guild

        if guild.id in clients:
            client: VoiceClient = clients[guild.id]
            if client.is_playing():
                client.pause()

    @command(brief="stop music")
    async def stop(self, ctx: Context):
        if not ctx.guild:
            raise OutOfServer()

        guild: Guild = ctx.guild

        if guild.id in clients:
            client: VoiceClient = clients[guild.id]
            if client.is_paused() or client.is_playing():
                client.stop()

    @command(brief="disconnect from voice channel")
    async def disconnect(self, ctx: Context):
        if not ctx.guild:
            raise OutOfServer()

        guild: Guild = ctx.guild

        if guild.id in clients:
            client: VoiceClient = guild.voice_client
            del clients[guild.id]
            await client.disconnect()


