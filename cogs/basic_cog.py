import os
from typing import List

from discord.ext.commands import Cog, command, CommandNotFound
from discord.ext.commands.context import Context
from discord.member import Member
from discord.guild import Guild
from discord.channel import TextChannel
from discord.invite import Invite
from discord.utils import oauth_url
from discord.permissions import Permissions

from exceptions import (
    BaseUserError,
    OutOfServer,
    PermissionDenied,
    COMMAND_NOT_FOUND_RESPONSE,
    INTERNAL_ERROR_RESPONSE,
)
from tools import send_help, mention_admin
from logger import log, log_msg
from cogs.base_cog import BaseCog


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
