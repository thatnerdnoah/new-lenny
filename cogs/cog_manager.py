import discord
from discord.ext import commands
from discord import app_commands, Interaction

class CogManager(commands.Cog, name="CogManager"):
    pass



async def setup(client):
    await client.add_cog(CogManager(client))