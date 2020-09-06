import os

from cogs import Misc, Greetings, Basic, Roles
from admin_cogs import Members
from discord.ext import commands


client = commands.Bot(command_prefix=".")
client.add_cog(Basic(client))
client.add_cog(Misc(client))
client.add_cog(Greetings(client))
client.add_cog(Roles(client))

client.add_cog(Members(client))


client.run(os.environ["BOT_TOKEN"])
